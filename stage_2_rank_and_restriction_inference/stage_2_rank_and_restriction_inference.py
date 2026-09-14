# CORRECTED 2026-09-06: exact constrained system-ML LR tests.
import os, json, math, warnings, re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2, norm
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, zivot_andrews
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.stats.sandwich_covariance import cov_hac
from statsmodels.stats.diagnostic import het_white, acorr_breusch_godfrey
from scipy.stats import combine_pvalues
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Local-run configuration
# Put this script in the same folder as data.xlsx, or change INPUT below.
BASE_DIR = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
INPUT = BASE_DIR / 'data.xlsx'
OUT = BASE_DIR / 'jalali_q1_python_secondstage_final_outputs'
OUT.mkdir(exist_ok=True)
FIG = OUT / 'figures'
FIG.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Load Jalali monthly data
# ------------------------------------------------------------
_xls = pd.ExcelFile(INPUT)
if 'Sheet1' in _xls.sheet_names:
    _main_sheet = 'Sheet1'
elif 'assets' in _xls.sheet_names:
    _main_sheet = 'assets'
else:
    _main_sheet = _xls.sheet_names[0]
df_raw = pd.read_excel(INPUT, sheet_name=_main_sheet)

# Flexible column mapper. The script accepts either the standardized names used in
# the EViews workfile or the original Jalali-data names used in the source workbook.
def first_existing(cols):
    for c in cols:
        if c in df_raw.columns:
            return c
    return None

colmap = {
    'date': first_existing(['date','month_jalali','jalali_month','month']),
    'tedpix': first_existing(['tedpix','tedpix_monthly_average','TEDPIX']),
    'usd': first_existing(['usd','dollarprice','usd_monthly_average','dollar_price']),
    'goldcoin': first_existing(['goldcoin','sekeh_monthly_average','goldcoinprice','sekeh','gcoin']),
    'housing': first_existing(['housing','housing_price','housingprice']),
    'vehicle': first_existing(['vehicle','vehicle_cpi_1400_100','carpi','vehicle_cpi'])
}
missing = [k for k,v in colmap.items() if v is None]
if missing:
    raise ValueError(f'Missing required input columns for: {missing}. Available columns: {list(df_raw.columns)}')

df = pd.DataFrame({k: df_raw[v] for k,v in colmap.items()})
# Optional obs column if present; otherwise create sequential index.
df.insert(0, 'obs', np.arange(1, len(df)+1))
for c in ['tedpix','usd','goldcoin','housing','vehicle']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df = df.dropna().reset_index(drop=True)
# Normalise Jalali labels to 1395m01 style.
def normalize_jalali_month(value):
    s = str(value).strip().replace('/', 'm').replace('-', 'm')
    match = re.fullmatch(r'(\d{4})m(\d{1,2})', s)
    if match:
        return f'{match.group(1)}m{int(match.group(2)):02d}'
    return s

months = [normalize_jalali_month(v) for v in df['date']]
Traw = len(df)

# ------------------------------------------------------------
# Load auxiliary CPI and world-gold series for the unit-root audit
# ------------------------------------------------------------
def load_auxiliary_series(sheet_candidates, value_candidates, label):
    """Read an auxiliary monthly series and align it exactly to the asset sample."""
    candidate_sheets = [s for s in sheet_candidates if s in _xls.sheet_names]
    candidate_sheets += [s for s in _xls.sheet_names if s not in candidate_sheets]

    frames = [(_main_sheet, df_raw)]
    frames += [(s, pd.read_excel(INPUT, sheet_name=s)) for s in candidate_sheets if s != _main_sheet]

    for sheet_name, frame in frames:
        value_col = next((c for c in value_candidates if c in frame.columns), None)
        date_col = next((c for c in ['date','month_jalali','jalali_month','month'] if c in frame.columns), None)
        if value_col is None or date_col is None:
            continue

        temp = pd.DataFrame({
            'month': [normalize_jalali_month(v) for v in frame[date_col]],
            'value': pd.to_numeric(frame[value_col], errors='coerce')
        }).dropna()
        temp = temp.groupby('month', as_index=True)['value'].mean()
        aligned = np.array([temp.get(m, np.nan) for m in months], dtype=float)

        if np.isnan(aligned).any():
            missing_months = [months[i] for i in np.where(np.isnan(aligned))[0]]
            raise ValueError(
                f'{label} is missing for {len(missing_months)} asset-sample months: '
                f'{missing_months[:10]}'
            )
        if np.any(aligned <= 0):
            raise ValueError(f'{label} must be strictly positive before logarithms are taken.')
        return aligned

    raise ValueError(
        f'Could not locate {label}. Expected one of columns {value_candidates} '
        f'in workbook sheets {_xls.sheet_names}.'
    )

CPI_AUX = load_auxiliary_series(
    sheet_candidates=['cpi','CPI'],
    value_candidates=['cpi','CPI','consumer_price_index'],
    label='CPI'
)
XAU_AUX = load_auxiliary_series(
    sheet_candidates=['globalgoldprice','xau','XAU','global_gold'],
    value_candidates=['globalgoldprice','xau','XAU','global_gold_price','goldprice'],
    label='world gold price (XAU)'
)

log_cols = {'LUSD':'usd','LGCOIN':'goldcoin','LSTOCK':'tedpix','LVEHICLE':'vehicle','LHOUSING':'housing'}
Y5 = np.column_stack([np.log(df[v].astype(float).to_numpy()) for v in log_cols.values()])
names5 = list(log_cols.keys())
idx4 = [0,1,3,4]
Y4 = Y5[:, idx4]
names4 = ['LUSD','LGCOIN','LVEHICLE','LHOUSING']

# Auxiliary levels used only for the additional unit-root audit.
LCPI_AUX = np.log(CPI_AUX)
LXAU_AUX = np.log(XAU_AUX)
LCPREM_AUX = Y5[:,1] - Y5[:,0] - LXAU_AUX
auxiliary_levels = {
    'LCPI': LCPI_AUX,
    'LXAU': LXAU_AUX,
    'LCPREM': LCPREM_AUX
}

# returns in log points
R5 = 100*np.diff(Y5, axis=0)
ret_names5 = ['D'+n[1:] if n.startswith('L') else 'D'+n for n in names5]

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def round_float(x, d=4):
    if isinstance(x, (float, np.floating)):
        if np.isnan(x) or np.isinf(x): return None
        return round(float(x), d)
    return x

def rtab(rows, d=4):
    return [[round_float(v,d) for v in row] for row in rows]

def lag_selection(Y, maxlags=4):
    mod = VAR(Y)
    sel = mod.select_order(maxlags=maxlags)
    out = {}
    for key in ['aic','bic','hqic','fpe']:
        try: out[key] = int(getattr(sel, key))
        except Exception: out[key] = None
    return out

def vecm_fit(Y, kdiff=1, rank=1, det='co'):
    fit = VECM(Y, k_ar_diff=kdiff, coint_rank=rank, deterministic=det).fit()
    b = fit.beta[:,0] / fit.beta[0,0]
    a = fit.alpha[:,0] * fit.beta[0,0]
    tb = fit.tvalues_beta[:,0]
    ta = fit.tvalues_alpha[:,0]
    return fit, b, a, tb, ta

def mats(Y):
    # For VECM with one lagged difference and a constant in short-run regression.
    d = np.diff(Y, axis=0)
    X = d[1:]
    Z = Y[1:-1]
    W = np.column_stack([np.ones(len(X)), d[:-1]])
    return X, Z, W

def ld_beta(Y, beta, alpha_zero=()):
    """Gaussian system profile likelihood, allowing zero alpha rows.

    After projecting out the common short-run regressors W, concentrate the
    unrestricted covariance through its Schur complement. With restricted
    equations B, regress both the ECT and unrestricted equations on B before
    estimating the free alpha entries. Separate equation OLS is not system ML.
    """
    X, Z, W = mats(Y)
    X = X - W @ np.linalg.lstsq(W, X, rcond=None)[0]
    Z = Z - W @ np.linalg.lstsq(W, Z, rcond=None)[0]
    ect = Z @ np.asarray(beta)
    az = sorted(set(alpha_zero))
    free = [j for j in range(X.shape[1]) if j not in az]
    A, z = X[:, free], ect
    if az:
        B = X[:, az]
        A = A - B @ np.linalg.lstsq(B, A, rcond=None)[0]
        z = z - B @ np.linalg.lstsq(B, z, rcond=None)[0]
    alpha = np.zeros(X.shape[1])
    alpha[free] = (z @ A) / (z @ z)
    E = X - ect[:, None] * alpha[None, :]
    sign, logdet = np.linalg.slogdet(E.T @ E / len(X))
    if sign <= 0:
        raise np.linalg.LinAlgError('Nonpositive residual covariance determinant')
    return float(logdet)


def lr_restriction(Y, beta_u, fixed=None, alpha_zero=(), norm_idx=0, homog=False, df=1, seed=33):
    """Exact rank-one constrained Gaussian ML by generalized eigenvalues.

    Applies to this study's zero beta rows, zero alpha rows, and sum(beta)=0.
    H spans admissible beta vectors. Zero alpha equations are projected out
    from both dependent and level residuals (Schur complement likelihood).
    No numerical multistart optimizer or equation-by-equation likelihood.
    API arguments seed and beta_u are retained for existing callers.
    Reference: Johansen alpha/beta restriction likelihood; urca::alrtest.
    """
    from scipy.linalg import eigh, null_space
    fixed = fixed or {}
    if any(value != 0 for value in fixed.values()):
        raise ValueError('This exact solver supports homogeneous beta constraints only')
    k = Y.shape[1]
    constraints = [np.eye(k)[j] for j in fixed]
    if homog:
        constraints.append(np.ones(k))
    H = null_space(np.array(constraints)) if constraints else np.eye(k)
    if H.shape[1] == 0:
        raise ValueError('Restrictions eliminate the entire cointegration vector')
    X, Z, W = mats(Y)
    X = X - W @ np.linalg.lstsq(W, X, rcond=None)[0]
    Z = Z - W @ np.linalg.lstsq(W, Z, rcond=None)[0]
    az = sorted(set(alpha_zero))
    if az:
        B = X[:, az]
        A = np.delete(X, az, axis=1)
        X = A - B @ np.linalg.lstsq(B, A, rcond=None)[0]
        Z = Z - B @ np.linalg.lstsq(B, Z, rcond=None)[0]
    ZH = Z @ H
    cross = ZH.T @ X
    M = cross @ np.linalg.solve(X.T @ X, cross.T)
    V = ZH.T @ ZH
    eig, vectors = eigh((M + M.T) / 2, (V + V.T) / 2)
    beta_r = H @ vectors[:, -1]
    if abs(beta_r[norm_idx]) < 1e-12:
        raise ValueError('Requested beta normalization is unavailable under restriction')
    beta_r /= beta_r[norm_idx]
    lr = (len(Y) - 2) * (ld_beta(Y, beta_r, az) - ld_beta(Y, beta_u))
    if lr < -1e-7:
        raise ArithmeticError('Restricted likelihood exceeds unrestricted likelihood')
    lr = max(0.0, float(lr))
    return lr, df, float(chi2.sf(lr, df)), beta_r.tolist(), True

def wild_bootstrap_rank(Y, reps=999, seed=2026):
    # Bootstrap under no cointegration: VAR in first differences with one lagged difference and constant.
    X, Z, W = mats(Y)
    coef = np.linalg.lstsq(W, X, rcond=None)[0]
    E = X - W @ coef
    rng = np.random.default_rng(seed)
    obs = coint_johansen(Y, 0, 1)
    trace_count = 0
    max_count = 0
    failed = 0
    for _ in range(reps):
        signs = rng.choice([-1,1], size=E.shape[0])[:,None]
        Eb = E * signs
        Yb = np.zeros_like(Y)
        Yb[0] = Y[0]
        Yb[1] = Y[1]
        dprev = Yb[1] - Yb[0]
        for t in range(E.shape[0]):
            dnew = np.r_[1.0, dprev] @ coef + Eb[t]
            Yb[t+2] = Yb[t+1] + dnew
            dprev = dnew
        try:
            jb = coint_johansen(Yb, 0, 1)
            trace_count += jb.lr1[0] >= obs.lr1[0]
            max_count += jb.lr2[0] >= obs.lr2[0]
        except Exception:
            failed += 1
    denom = reps - failed
    return trace_count/denom, max_count/denom, denom, failed

def ols_hac(y, x, bw=5):
    X = sm.add_constant(np.asarray(x, float))
    m = sm.OLS(np.asarray(y, float), X, missing='drop').fit()
    # Python bandwidth here means maximum included lag (Bartlett denominator bw+1).
    # EViews covbw=h uses maximum lag h-1; these are different conventions.
    cov = cov_hac(m, nlags=bw)
    se = np.sqrt(np.diag(cov))
    t = m.params / se
    p = 2*(1-norm.cdf(np.abs(t)))
    return m, se, t, p


def vecm_regressor_matrix(Y, beta):
    # Aligns with VECM residuals for k_ar_diff=1: ΔY_t on ECT_{t-1}, constant, ΔY_{t-1}.
    d = np.diff(Y, axis=0)
    Z = Y[1:-1]
    ect = (Z @ np.asarray(beta).reshape(-1,1))
    W = np.column_stack([np.ones(len(ect)), d[:-1]])
    return np.column_stack([ect, W])

def companion_roots_from_vecm(fit):
    # Compute roots of the level VAR companion matrix implied by the VECM.
    A = np.asarray(fit.var_rep)  # shape: p x k x k
    p, k, _ = A.shape
    comp = np.zeros((k*p, k*p))
    comp[:k, :k*p] = np.hstack(A)
    if p > 1:
        comp[k:, :-k] = np.eye(k*(p-1))
    eig = np.linalg.eigvals(comp)
    return eig

def system_serial_lm_style(resid, exog, maxlag=12):
    # Multivariate LM/LR-style residual serial-correlation tests.
    # For lag h, regress residuals on model exog and residual lag h. For cumulative H,
    # include all residual lags 1..H. Report chi-square approximation.
    resid = np.asarray(resid, float)
    exog = np.asarray(exog, float)
    n, k = resid.shape
    rows_single = []
    rows_cum = []
    for h in range(1, maxlag+1):
        y = resid[h:]
        Xr = exog[h:]
        Xu = np.column_stack([Xr, resid[:-h]])
        Er = y - Xr @ np.linalg.lstsq(Xr, y, rcond=None)[0]
        Eu = y - Xu @ np.linalg.lstsq(Xu, y, rcond=None)[0]
        Sr = (Er.T @ Er) / len(y)
        Su = (Eu.T @ Eu) / len(y)
        sr_s, sr_ld = np.linalg.slogdet(Sr)
        su_s, su_ld = np.linalg.slogdet(Su)
        stat = len(y)*(sr_ld - su_ld) if sr_s > 0 and su_s > 0 else np.nan
        df_lm = k*k
        pval = chi2.sf(max(stat,0), df_lm) if np.isfinite(stat) else np.nan
        rows_single.append([h, stat, df_lm, pval])
        # cumulative 1..h
        y2 = resid[h:]
        Xlag = [exog[h:]]
        for L in range(1,h+1):
            Xlag.append(resid[h-L:n-L])
        Xuc = np.column_stack(Xlag)
        Erc = y2 - exog[h:] @ np.linalg.lstsq(exog[h:], y2, rcond=None)[0]
        Euc = y2 - Xuc @ np.linalg.lstsq(Xuc, y2, rcond=None)[0]
        Src = (Erc.T @ Erc) / len(y2)
        Suc = (Euc.T @ Euc) / len(y2)
        sr_s, sr_ld = np.linalg.slogdet(Src)
        su_s, su_ld = np.linalg.slogdet(Suc)
        statc = len(y2)*(sr_ld - su_ld) if sr_s > 0 and su_s > 0 else np.nan
        dfc = k*k*h
        pc = chi2.sf(max(statc,0), dfc) if np.isfinite(statc) else np.nan
        rows_cum.append([h, statc, dfc, pc])
    return rows_single, rows_cum

def white_by_equation(resid, exog, names):
    # Equation-by-equation White test. This is not identical to EViews' multivariate system
    # White test, but it is transparent and reproducible in Python.
    rows=[]; pvals=[]
    for j,nm in enumerate(names):
        try:
            lm, lm_p, fval, f_p = het_white(resid[:,j], exog)
            rows.append([nm, lm, lm_p, fval, f_p])
            if np.isfinite(lm_p): pvals.append(lm_p)
        except Exception:
            rows.append([nm, np.nan, np.nan, np.nan, np.nan])
    if len(pvals)>0:
        fish_stat, fish_p = combine_pvalues(pvals, method='fisher')
        rows.append(['Fisher combined p-values', fish_stat, fish_p, '', ''])
    return rows

def equation_bg_tests(Y, beta, names, maxlag=12):
    # Equation-by-equation Breusch-Godfrey tests on the conditional VECM regressions.
    d = np.diff(Y, axis=0)
    Xdep = d[1:]
    X = vecm_regressor_matrix(Y, beta)
    rows=[]
    for j,nm in enumerate(names):
        mod = sm.OLS(Xdep[:,j], X).fit()
        for L in [1,2,3,12]:
            try:
                lm, lm_p, fval, f_p = acorr_breusch_godfrey(mod, nlags=L)
                rows.append([nm, L, lm, lm_p, fval, f_p])
            except Exception:
                rows.append([nm, L, np.nan, np.nan, np.nan, np.nan])
    return rows

def vecm_diagnostics(fit, Y, beta, names, label):
    exog = vecm_regressor_matrix(Y, beta)
    resid = np.asarray(fit.resid)
    # Statsmodels multivariate Portmanteau whiteness and normality.
    try:
        white = fit.test_whiteness(nlags=12, adjusted=False)
        white_row = [label, 'Portmanteau whiteness up to lag 12', white.test_statistic, white.df, white.pvalue, white.conclusion]
    except Exception:
        white_row = [label, 'Portmanteau whiteness up to lag 12', np.nan, np.nan, np.nan, 'failed']
    try:
        normres = fit.test_normality()
        norm_row = [label, 'Multivariate Jarque-Bera normality', normres.test_statistic, normres.df, normres.pvalue, normres.conclusion]
    except Exception:
        norm_row = [label, 'Multivariate Jarque-Bera normality', np.nan, np.nan, np.nan, 'failed']
    lm_single, lm_cum = system_serial_lm_style(resid, exog, maxlag=12)
    white_eq = white_by_equation(resid, exog, names)
    bg_eq = equation_bg_tests(Y, beta, names, maxlag=12)
    roots = companion_roots_from_vecm(fit)
    root_rows = []
    for i,z in enumerate(sorted(roots, key=lambda x: -abs(x)), start=1):
        root_rows.append([label, i, float(np.real(z)), float(np.imag(z)), float(abs(z))])
    root_summary = [[label, len([r for r in roots if abs(abs(r)-1)<1e-5]), max([abs(r) for r in roots if abs(abs(r)-1)>=1e-5] or [np.nan])]]
    return {
        'summary_rows':[white_row, norm_row],
        'lm_single': [[label]+r for r in lm_single],
        'lm_cum': [[label]+r for r in lm_cum],
        'white_eq': [[label]+r for r in white_eq],
        'bg_eq': [[label]+r for r in bg_eq],
        'roots': root_rows,
        'root_summary': root_summary
    }

# ------------------------------------------------------------
# Descriptive statistics, correlations, unit roots
# ------------------------------------------------------------
desc = []
for j, nm in enumerate(names5):
    r = R5[:,j]
    desc.append([ret_names5[j], np.mean(r), np.std(r, ddof=1), np.min(r), np.max(r)])
corr = pd.DataFrame(R5, columns=ret_names5).corr().values
corr_rows = []
for i,nm in enumerate(ret_names5):
    corr_rows.append([nm] + [corr[i,j] if j <= i else '' for j in range(len(ret_names5))])

adf_rows = []
za_rows = []
for j,nm in enumerate(names5):
    x = Y5[:,j]
    ac = adfuller(x, regression='c', autolag='AIC')
    act = adfuller(x, regression='ct', autolag='AIC')
    dc = adfuller(np.diff(x), regression='c', autolag='AIC')
    adf_rows.append([nm, ac[0], ac[1], act[0], act[1], dc[0], dc[1]])
    try:
        zac = zivot_andrews(x, trim=.15, maxlag=6, regression='c')
        zact = zivot_andrews(x, trim=.15, maxlag=6, regression='ct')
        # statsmodels tuple: stat, pvalue, crit, baselag, bpidx
        bp_c = int(zac[4]); bp_ct = int(zact[4])
        za_rows.append([nm, zac[0], zac[1], months[bp_c], zact[0], zact[1], months[bp_ct]])
    except Exception as e:
        za_rows.append([nm, None, None, None, None, None, None])


# Additional audit for the auxiliary variables used in the CPI-real and XAU/premium specifications.
# ADF settings are explicit here: AIC lag selection with a maximum of 12 lags.
# Zivot-Andrews tests use trim=0.15, maxlag=6 and AIC lag selection.
aux_adf_rows = []
aux_za_rows = []
aux_summary_rows = []
for nm, x in auxiliary_levels.items():
    ac = adfuller(x, maxlag=12, regression='c', autolag='AIC')
    act = adfuller(x, maxlag=12, regression='ct', autolag='AIC')
    dc = adfuller(np.diff(x), maxlag=12, regression='c', autolag='AIC')
    aux_adf_rows.append([
        nm,
        ac[0], ac[1], ac[2],
        act[0], act[1], act[2],
        dc[0], dc[1], dc[2]
    ])

    try:
        zac = zivot_andrews(x, trim=.15, maxlag=6, regression='c', autolag='AIC')
        zact = zivot_andrews(x, trim=.15, maxlag=6, regression='ct', autolag='AIC')
        dzac = zivot_andrews(np.diff(x), trim=.15, maxlag=6, regression='c', autolag='AIC')
        dzact = zivot_andrews(np.diff(x), trim=.15, maxlag=6, regression='ct', autolag='AIC')
        aux_za_rows.append([
            nm,
            zac[0], zac[1], months[int(zac[4])], int(zac[3]),
            zact[0], zact[1], months[int(zact[4])], int(zact[3]),
            dzac[0], dzac[1], months[1:][int(dzac[4])], int(dzac[3]),
            dzact[0], dzact[1], months[1:][int(dzact[4])], int(dzact[3])
        ])
        za_diff_reject = (dzac[1] <= .05) or (dzact[1] <= .05)
    except Exception:
        aux_za_rows.append([nm] + [None]*16)
        za_diff_reject = False

    level_nonstationary = (ac[1] > .05) and (act[1] > .05)
    if level_nonstationary and dc[1] <= .05:
        classification = 'I(1)'
    elif level_nonstationary and za_diff_reject:
        classification = 'I(1), subject to structural-break qualification'
    else:
        classification = 'Inconclusive; inspect full test output'
    aux_summary_rows.append([nm, classification])

lags5 = lag_selection(Y5, maxlags=4)
lags4 = lag_selection(Y4, maxlags=4)
lag_rows = [['Five-variable', lags5.get('aic'), lags5.get('fpe'), lags5.get('hqic'), lags5.get('bic'), 'VAR(2) if AIC/FPE/HQ select 2; otherwise shorter baseline noted'],
            ['Four-variable', lags4.get('aic'), lags4.get('fpe'), lags4.get('hqic'), lags4.get('bic'), 'VAR(2) if AIC/FPE/HQ select 2; otherwise shorter baseline noted']]

# ------------------------------------------------------------
# Johansen rank and VECMs
# ------------------------------------------------------------
jo5 = coint_johansen(Y5, 0, 1)
jo4 = coint_johansen(Y4, 0, 1)
Tj5 = Y5.shape[0]-2
Tj4 = Y4.shape[0]-2
ra5 = (Tj5 - 5*2)/Tj5
ra4 = (Tj4 - 4*2)/Tj4
boot5 = wild_bootstrap_rank(Y5, reps=999, seed=1001)
boot4 = wild_bootstrap_rank(Y4, reps=999, seed=1002)

rank_rows = [
    ['Five-variable','Trace r=0',jo5.lr1[0],jo5.cvt[0,1],jo5.lr1[0]*ra5,boot5[0]],
    ['Five-variable','Max-Eigen r=0',jo5.lr2[0],jo5.cvm[0,1],jo5.lr2[0]*ra5,boot5[1]],
    ['Five-variable','Trace r<=1',jo5.lr1[1],jo5.cvt[1,1],jo5.lr1[1]*ra5,''],
    ['Four-variable','Trace r=0',jo4.lr1[0],jo4.cvt[0,1],jo4.lr1[0]*ra4,boot4[0]],
    ['Four-variable','Max-Eigen r=0',jo4.lr2[0],jo4.cvm[0,1],jo4.lr2[0]*ra4,boot4[1]],
    ['Four-variable','Trace r<=1',jo4.lr1[1],jo4.cvt[1,1],jo4.lr1[1]*ra4,''],
]

fit5,beta5,alpha5,beta5_t,alpha5_t = vecm_fit(Y5, kdiff=1, rank=1, det='co')
fit4,beta4,alpha4,beta4_t,alpha4_t = vecm_fit(Y4, kdiff=1, rank=1, det='co')
fit4_l12,beta4_l12,alpha4_l12,beta4_l12_t,alpha4_l12_t = vecm_fit(Y4, kdiff=2, rank=1, det='co')

vec5_rows = [[names5[i], beta5[i], '' if i==0 else beta5_t[i], alpha5[i], alpha5_t[i]] for i in range(5)]
prod4 = beta4 * alpha4
bpa = float(beta4 @ alpha4)
half_life = float(np.log(.5)/np.log(1+bpa)) if 0 < 1+bpa < 1 else np.nan
vec4_rows = [[names4[i], beta4[i], '' if i==0 else beta4_t[i], alpha4[i], alpha4_t[i], prod4[i], 'Error-correcting' if prod4[i] < 0 else 'Offsetting correction'] for i in range(4)]
vec4_rows.append(['System','','','','', bpa, f'Half-life = {half_life:.2f} months'])
lagrob_rows = [[names4[i], beta4[i], beta4_l12[i], alpha4[i], alpha4_l12[i]] for i in range(4)]


# ------------------------------------------------------------
# Residual diagnostics
# ------------------------------------------------------------
# Main residual diagnostics (LM, normality, heteroskedasticity and roots) are
# now reported from the EViews output. This Python layer is reserved for
# second-stage Q1 audit items not reliably generated in EViews PRG: unit-root
# and break tests, rank corrections/bootstrap, formal restrictions, half-life,
# recursive index, non-overlap and per-asset checks.

# ------------------------------------------------------------
# LR restrictions
# ------------------------------------------------------------
restrict_rows = []
for block,null,res in [
    ('5-var STOCK exclusion restrictions','beta_stock = 0',lr_restriction(Y5,beta5,fixed={2:0.0},df=1,seed=10)),
    ('5-var STOCK exclusion restrictions','alpha_stock = 0',lr_restriction(Y5,beta5,alpha_zero=(2,),df=1,seed=11)),
    ('5-var STOCK exclusion restrictions','joint beta_stock = 0 and alpha_stock = 0',lr_restriction(Y5,beta5,fixed={2:0.0},alpha_zero=(2,),df=2,seed=12)),
]:
    restrict_rows.append([block,null,res[0],res[1],res[2]])
for i,nm in enumerate(names4):
    # If testing beta_LUSD=0, normalize on LGCOIN to avoid fixing normalizing coefficient to zero
    if i == 0:
        res = lr_restriction(Y4,beta4,fixed={0:0.0},norm_idx=1,df=1,seed=20+i)
    else:
        res = lr_restriction(Y4,beta4,fixed={i:0.0},df=1,seed=20+i)
    restrict_rows.append(['4-var membership',f'beta_{nm} = 0',res[0],res[1],res[2]])
for i,nm in enumerate(names4):
    res = lr_restriction(Y4,beta4,alpha_zero=(i,),df=1,seed=30+i)
    restrict_rows.append(['4-var weak exogeneity',f'alpha_{nm} = 0',res[0],res[1],res[2]])
res = lr_restriction(Y4,beta4,homog=True,df=1,seed=50)
restrict_rows.append(['4-var homogeneity','sum(beta) = 0',res[0],res[1],res[2]])

# ------------------------------------------------------------
# Disequilibrium index and relative-adjustment regressions
# ------------------------------------------------------------
ect4 = Y4 @ beta4
z4 = (ect4 - ect4.mean()) / ect4.std(ddof=1)
rel_rows=[]; rel_dummy_rows=[]; rel_no_rows=[]; per_rows=[]
# Jalali event months aligned with the four crisis episodes formerly expressed in Gregorian months
# 1397m02: sanctions announcement / currency pressure; 1399m04: equity boom; 1401m06: currency crisis; 1404m03: exchange-rate jump / regional shock.
events = ['1397m02','1399m04','1401m06','1404m03']
event_idx = {e: months.index(e) if e in months else None for e in events}
for h in [3,6,12]:
    liquid = 0.5*((Y4[h:,0]-Y4[:-h,0]) + (Y4[h:,1]-Y4[:-h,1]))
    illiquid = 0.5*((Y4[h:,2]-Y4[:-h,2]) + (Y4[h:,3]-Y4[:-h,3]))
    y = 100*(liquid - illiquid)
    x = z4[:-h]
    m,se,t,p = ols_hac(y,x,bw=5)
    mh,seh,th,ph = ols_hac(y,x,bw=h)
    rel_rows.append([h,m.params[1],t[1],p[1],th[1],ph[1],m.rsquared,len(y)])
    # event dummies only if within valid y range and not collinear
    D=[]; used=[]
    for ev,idx in event_idx.items():
        if idx is not None and idx < len(y):
            d=np.zeros(len(y)); d[idx]=1
            # avoid all zero
            D.append(d); used.append(ev)
    X = np.column_stack([x]+D) if D else x
    md,sed,td,pdv = ols_hac(y,X,bw=5)
    rel_dummy_rows.append([h,md.params[1],td[1],pdv[1],md.rsquared,len(y),', '.join(used)])
    ix = np.arange(0,len(y),h)
    mno = sm.OLS(y[ix], sm.add_constant(x[ix])).fit()
    rel_no_rows.append([h,mno.params[1],mno.tvalues[1],mno.pvalues[1],mno.rsquared,len(ix)])
    for j,nm in enumerate(names4):
        yy = 100*(Y4[h:,j]-Y4[:-h,j])
        mp,sep,tp,pp = ols_hac(yy,x,bw=max(5,h))
        per_rows.append([h,nm,mp.params[1],tp[1],pp[1],mp.rsquared,len(yy)])

# Recursive index
zrec = np.full(Y4.shape[0], np.nan)
recbeta_rows=[]
for t in range(60, Y4.shape[0]):
    try:
        _, b, _, _, _ = vecm_fit(Y4[:t+1], kdiff=1, rank=1, det='co')
        ect = Y4[:t+1] @ b
        zrec[t] = (ect[-1] - np.mean(ect)) / np.std(ect, ddof=1)
        recbeta_rows.append([months[t]] + list(b))
    except Exception:
        recbeta_rows.append([months[t]] + [np.nan]*4)
recursive_rows=[]
for h in [3,6,12]:
    liquid = 0.5*((Y4[h:,0]-Y4[:-h,0]) + (Y4[h:,1]-Y4[:-h,1]))
    illiquid = 0.5*((Y4[h:,2]-Y4[:-h,2]) + (Y4[h:,3]-Y4[:-h,3]))
    y = 100*(liquid - illiquid)
    x = zrec[:-h]
    mask = ~np.isnan(x)
    if mask.sum() > 12:
        m,se,t,p = ols_hac(y[mask], x[mask], bw=max(5,h))
        recursive_rows.append([h,m.params[1],t[1],p[1],m.rsquared,int(mask.sum())])

# EViews is the primary source for IRF/FEVD; no Python FEVD table is exported here.
fevd_rows = []

# ------------------------------------------------------------
# Figures
# ------------------------------------------------------------
def savefig(path):
    plt.tight_layout(); plt.savefig(path, dpi=220, bbox_inches='tight'); plt.close()

x = np.arange(Traw)
plt.figure(figsize=(9,5))
for j,nm in enumerate(names5):
    plt.plot(x, 100*(Y5[:,j]-Y5[0,j]), label=nm)
plt.xticks(x[::12], [months[i] for i in x[::12]], rotation=45, ha='right')
plt.ylabel('100 × cumulative log change')
plt.title('Cumulative log changes of asset prices (Jalali monthly sample)')
plt.legend(ncol=2, fontsize=8)
savefig(FIG/'fig1_cumulative_log_changes.png')

plt.figure(figsize=(9,5))
for j,nm in enumerate(names5):
    plt.plot(x[1:], R5[:,j], label=ret_names5[j], linewidth=1.0)
plt.xticks(x[1::12], [months[i] for i in x[1::12]], rotation=45, ha='right')
plt.ylabel('Monthly log return, percent')
plt.title('Monthly log returns')
plt.legend(ncol=2, fontsize=8)
savefig(FIG/'fig2_monthly_returns.png')

plt.figure(figsize=(9,4.5))
plt.plot(x, z4, label='Standardized ECT')
plt.axhline(0, linewidth=0.8)
plt.axhline(2, linewidth=0.6, linestyle='--')
plt.axhline(-2, linewidth=0.6, linestyle='--')
plt.xticks(x[::12], [months[i] for i in x[::12]], rotation=45, ha='right')
plt.ylabel('Standard deviations')
plt.title('Four-market long-run disequilibrium index')
savefig(FIG/'fig3_long_run_disequilibrium_index.png')

# Recursive vs full-sample index
plt.figure(figsize=(9,4.5))
plt.plot(x, z4, label='Full-sample ECT index')
plt.plot(x, zrec, label='Recursive look-ahead-free index', alpha=.8)
plt.axhline(0, linewidth=0.8)
plt.xticks(x[::12], [months[i] for i in x[::12]], rotation=45, ha='right')
plt.ylabel('Standard deviations')
plt.title('Full-sample and recursive disequilibrium indices')
plt.legend(fontsize=8)
savefig(FIG/'fig4_recursive_vs_full_index.png')

# ------------------------------------------------------------
# Export results
# ------------------------------------------------------------
results = {
    'sample': {'start_jalali': months[0], 'end_jalali': months[-1], 'n_levels': int(Traw), 'n_returns': int(len(R5))},
    'lag_selection': {'five_variable': lags5, 'four_variable': lags4},
    'rank_tests': rank_rows,
    'beta5': beta5.tolist(), 'alpha5': alpha5.tolist(),
    'beta4': beta4.tolist(), 'alpha4': alpha4.tolist(), 'beta_prime_alpha': bpa, 'half_life_months': half_life,
    'bootstrap': {'five_variable': {'trace_p': boot5[0], 'maxeig_p': boot5[1], 'reps_used': boot5[2]}, 'four_variable': {'trace_p': boot4[0], 'maxeig_p': boot4[1], 'reps_used': boot4[2]}},
    'restriction_tests': restrict_rows,
    'rel_hac': rel_rows,
    'rel_event_dummies': rel_dummy_rows,
    'rel_nonoverlap': rel_no_rows,
    'per_asset': per_rows,
    'recursive_index': recursive_rows,
    'adf': adf_rows,
    'zivot_andrews': za_rows,
    'auxiliary_adf': aux_adf_rows,
    'auxiliary_zivot_andrews': aux_za_rows,
    'auxiliary_unit_root_summary': aux_summary_rows,
    'vec5': vec5_rows,
    'vec4': vec4_rows,
    'lag_robustness': lagrob_rows
}
(OUT/'Q1_Jalali_results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')

# Excel tables
with pd.ExcelWriter(OUT/'Q1_Jalali_secondstage_final_tables.xlsx', engine='xlsxwriter') as writer:
    def sheet(name, headers, rows):
        pd.DataFrame(rtab(rows), columns=headers).to_excel(writer, sheet_name=name[:31], index=False)
    sheet('Sample', ['Metric','Value'], [[k,v] for k,v in results['sample'].items()])
    sheet('Descriptive_returns',['Series','Mean','Std dev','Min','Max'], desc)
    sheet('Return_correlations',['Series']+ret_names5, corr_rows)
    sheet('ADF_tests',['Series','ADF c stat','ADF c p','ADF ct stat','ADF ct p','ADF diff stat','ADF diff p'], adf_rows)
    sheet('Zivot_Andrews',['Series','ZA c stat','ZA c p','ZA c break','ZA ct stat','ZA ct p','ZA ct break'], za_rows)
    sheet('Aux_ADF',[
        'Series','ADF c stat','ADF c p','ADF c lag',
        'ADF ct stat','ADF ct p','ADF ct lag',
        'ADF diff c stat','ADF diff c p','ADF diff c lag'
    ], aux_adf_rows)
    sheet('Aux_ZA',[
        'Series',
        'ZA level c stat','ZA level c p','ZA level c break','ZA level c lag',
        'ZA level ct stat','ZA level ct p','ZA level ct break','ZA level ct lag',
        'ZA diff c stat','ZA diff c p','ZA diff c break','ZA diff c lag',
        'ZA diff ct stat','ZA diff ct p','ZA diff ct break','ZA diff ct lag'
    ], aux_za_rows)
    sheet('Aux_UR_summary',['Series','Classification'], aux_summary_rows)
    sheet('Lag_selection',['System','AIC','FPE','HQ','SC/BIC','Adopted'], lag_rows)
    sheet('Rank_tests',['System','Test','Statistic','5% critical value','RA corrected stat','Wild bootstrap p'], rank_rows)
    sheet('Five_var_VECM',['Asset','Beta','t(Beta)','Alpha','t(Alpha)'], vec5_rows)
    sheet('Four_var_core',['Asset','Beta','t(Beta)','Alpha','t(Alpha)','Beta x Alpha','Role'], vec4_rows)
    sheet('LR_restrictions',['Block','Null hypothesis','LR','df','p-value'], restrict_rows)
    sheet('Lag_robustness',['Asset','Beta main kdiff1','Beta robustness kdiff2','Alpha main','Alpha robustness'], lagrob_rows)
    sheet('REL_HAC',['Horizon','Slope','t NW bw5','p bw5','t NW bw=h','p bw=h','R2','N'], rel_rows)
    sheet('REL_dummies',['Horizon','Slope','t NW','p-value','R2','N','Dummies'], rel_dummy_rows)
    sheet('REL_nonoverlap',['Horizon','Slope','t','p-value','R2','N'], rel_no_rows)
    sheet('Per_asset',['Horizon','Asset','Slope','t HAC','p-value','R2','N'], per_rows)
    sheet('Recursive_index',['Horizon','Slope','t HAC','p-value','R2','N'], recursive_rows)
    sheet('Recursive_betas',['Month','Beta LUSD','Beta LGCOIN','Beta LVEHICLE','Beta LHOUSING'], recbeta_rows)

# Standalone, simple auxiliary unit-root report.
with pd.ExcelWriter(OUT/'Auxiliary_unit_root_audit.xlsx', engine='xlsxwriter') as writer:
    pd.DataFrame(rtab(aux_adf_rows), columns=[
        'Series','ADF c stat','ADF c p','ADF c lag',
        'ADF ct stat','ADF ct p','ADF ct lag',
        'ADF diff c stat','ADF diff c p','ADF diff c lag'
    ]).to_excel(writer, sheet_name='ADF', index=False)
    pd.DataFrame(rtab(aux_za_rows), columns=[
        'Series',
        'ZA level c stat','ZA level c p','ZA level c break','ZA level c lag',
        'ZA level ct stat','ZA level ct p','ZA level ct break','ZA level ct lag',
        'ZA diff c stat','ZA diff c p','ZA diff c break','ZA diff c lag',
        'ZA diff ct stat','ZA diff ct p','ZA diff ct break','ZA diff ct lag'
    ]).to_excel(writer, sheet_name='Zivot_Andrews', index=False)
    pd.DataFrame(aux_summary_rows, columns=['Series','Classification']).to_excel(
        writer, sheet_name='Summary', index=False
    )

# Markdown summary
core_eq = f"ECT_t = LUSD_t {beta4[1]:+.4f} LGCOIN_t {beta4[2]:+.4f} LVEHICLE_t {beta4[3]:+.4f} LHOUSING_t + c"
stock_joint = next(r for r in restrict_rows if 'joint' in r[1])
summary = f"""# Jalali-calendar Q1 Python second-stage audit results

Sample: {months[0]} to {months[-1]} (Jalali monthly), N={Traw} levels and {len(R5)} returns.

Core four-market relation:

`{core_eq}`

System feedback: beta'alpha = {bpa:.4f}; half-life = {half_life:.2f} months.

Joint STOCK restriction test: LR = {stock_joint[2]:.4f}, p = {stock_joint[4]:.4f}.

Four-variable rank bootstrap p-values: Trace = {boot4[0]:.4f}; Max-Eigen = {boot4[1]:.4f}.

Relative-adjustment HAC slopes:
"""
for r in rel_rows:
    summary += f"- h={r[0]}: slope={r[1]:.4f}, p(bw=h)={r[5]:.4f}, R2={r[6]:.3f}, N={r[7]}\n"
summary += "\nRecursive look-ahead-free slopes:\n"
for r in recursive_rows:
    summary += f"- h={r[0]}: slope={r[1]:.4f}, p={r[3]:.4f}, N={r[5]}\n"
(OUT/'Q1_Jalali_summary.md').write_text(summary, encoding='utf-8')

print(summary)
print('Saved Python second-stage outputs:', OUT)
