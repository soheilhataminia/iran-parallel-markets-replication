# CORRECTED 2026-09-06: DGP-implied LP centering for both bootstrap schemes.
# Earlier correction notes below are historical; current numerical results are
# generated at runtime. Keep bootstrap_targets.py beside this script.
"""
=====================================================================================
 STAGE 6 (VERSION 4, FINAL OVERLAP-CORRECTED) - UNANTICIPATED USD AND COIN-PREMIUM
 SHOCKS: TRANSMISSION TO HOUSING AND VEHICLES

 Self-contained (data embedded; numpy/scipy only; relative outputs; fixed seed).
 Supersedes V1-V3.

 V3 referee round, resolutions:
  Q1  s_USD restored to the LOCKED definition: the USD-equation residual of the
      four-variable VECM (rank 1, one lag, Case 3). The two-lag side equation is
      demoted to a robustness column. s_CPREM stays as agreed: residual of the
      TWO-LAG innovation equation for dLCPREM (= dLGCOIN - dLUSD - dLXAU) with
      ECT_{t-1} and two lags of (dLUSD, dLCPREM, dLVEH, dLHOUS, dLXAU);
      one-lag robustness retained.
  Q2  Confirmatory forecast family corrected: CW(M2 vs M0) for
      {housing, vehicles} x {h = 1, 3, 6} -> six tests, Holm over these six.
      Vehicle forecasting added. M1 (raw changes) and M2-vs-M1 are supplements.
  Q3  Holm shown for BOTH bootstrap schemes (wild and block-wild); figures and
      tables lead with adjusted values. Agreed reading: the USD->housing path is
      significant before family correction but is NOT confirmed at the 5% level
      within the four-path family.
  Q4  Origin information rule: ECT_tau = beta_{tau-1}' y_tau. All vintage objects
      (beta, VECM, premium equation, standardization) are estimated on months
      1..tau-1 only; beta_{tau-1} is applied to training rows as well.
  Q5  Historical training shocks: ORIGIN-SPECIFIC in-vintage residuals are the
      main design; the fully recursive real-time shock series is the robustness
      variant (reported side by side).
  Q6  Conditional nowcast restored (both markets, supplementary CW). Window
      sensitivity (TAU0 = 60, 84) and leave-one-episode-out LP added as light
      robustness.
  Q7  Proper Engle ARCH-LM implemented (n*R^2 of e^2 on its lags); the previous
      statistic is reported under its correct name, McLeod-Li.
  Q8  Stability split corrected to use non-overlapping halves. Equality remains REJECTED
      (chi2(3) = 14.236, p = 0.00260); no other Stage-6 result changes.

 FINAL CORRECTION (2026-08-25):
  - Fixed the split-sample stability code so observation 62 is not included in both halves.
  - First half now uses observations 1..61; second half uses observations 62..122.
  - Corrected stability result: chi2(3)=14.235860, p=0.002601; sUSD loading
    1.531% in the first half and 0.582% in the second half.
  - All other archived V4 results are unchanged.
=====================================================================================
"""
import csv, io, json, os, sys
import numpy as np
from scipy import linalg, stats
from bootstrap_targets import lp_targets

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "stage6_v4_out")
os.makedirs(OUT, exist_ok=True)
B_MAIN = int(os.environ.get("S6_B_MAIN", "2000"))
B_BLOCK = int(os.environ.get("S6_B_BLOCK", "10000"))

DATA_CSV = """
date,tedpix,usd,goldcoin,housing,vehicle,cpi,xau
1395/01,80193.68421,34700.14286,10236730,41317486,12.65964382,27.31365619,1233.6309
1395/02,77453.52381,34486.55,10305952.38,42135246,12.6801475,27.33861446,1265.27347
1395/03,75435.23809,34602.71429,10167271.43,42445751,12.66008024,27.52318421,1249.830481
1395/04,73895.05,34988.66667,10868715.79,42588469,12.67775521,27.81799219,1327.649135
1395/05,77307.95238,35325.95455,11100828.57,42809232,12.77004824,28.10230105,1342.032857
1395/06,76926,35549.73684,11154238.1,42496061,12.8714978,28.19583595,1324.981743
1395/07,77415.77778,35802.16667,10984173.68,43191738,12.93659395,28.33243072,1284.283182
1395/08,79295.23809,36329.7619,11135852.38,43211137,12.97567373,28.4033875,1262.025495
1395/09,80285.42105,38645.63158,11312625,43335507,13.03057054,28.62520803,1169.36
1395/10,79284.05,39487.05,11781114.29,44133117,13.11150065,28.85861291,1169.503627
1395/11,77564.23809,38316.38095,11892723.81,44140984,13.11817077,29.00166,1219.320952
1395/12,77123.65,37677.9,11981895,44627525,13.16921409,29.35814865,1228.820462
1396/01,77917.47059,37564.4375,12099998.82,43258124,13.19403233,29.78028841,1262.195643
1396/02,79947.23809,37580.25,12129170,44592486,13.25245556,29.74655184,1246.867143
1396/03,79996.38095,37393.95238,12049818.1,44914554,13.2781336,29.79611965,1264.20913
1396/04,79229.73684,37811.61111,12098554.74,45390798,13.31673092,30.10798024,1234.5909
1396/05,81550.86364,38138.65217,12147165.65,45862328,13.35598639,30.2244605,1271.991359
1396/06,83615.15,38869.7,12459280,46846337,13.42389018,30.22839357,1316.898678
1396/07,85448.25,39750.4,12847040,47157588,13.50211008,30.62979263,1285.38949
1396/08,87647.8,40769.6,13549452.38,48095658,13.51942036,30.94453952,1277.82045
1396/09,92396.47619,41794.31579,13956165,50001074,13.5334135,31.17580202,1268.427714
1396/10,97105.52381,43479.7619,14702680.95,51481867,13.60406161,31.30474305,1313.14761
1396/11,98425.28571,46382.18182,15182863.5,54067640,13.69373546,31.38866871,1338.467605
1396/12,96983.94737,47085.95455,15744545.45,56288507,13.90718527,31.45802626,1322.91761
1397/01,96433.73333,51537.72222,17914444.44,55839522,14.00348944,31.87578523,1338.979086
1397/02,94236.68182,61040.56,19196923.08,59843838,14.22463329,32.22021279,1310.582862
1397/03,98127.33333,66817.31818,22982173.91,64900102,14.85793889,32.8208482,1292.55217
1397/04,110310.7143,81677.68,28998600,69874753,15.34368838,34.27359646,1247.927148
1397/05,123805.9583,103004.9231,36982880.77,74301929,18.01674097,36.06262186,1207.333913
1397/06,144624.2,129219.2381,43391739.13,81223596,23.02287117,38.0062761,1200.121818
1397/07,181837.5909,142900.72,45302333.33,86337581,22.16069516,40.68584217,1205.901448
1397/08,181037.2,122009.0909,42082090.91,91857644,22.45585243,41.75101174,1222.805905
1397/09,164431.4211,109450.75,36735857.14,96314357,23.35666674,42.82894552,1237.1309
1397/10,161850.9545,109244,37429181.82,97784109,23.81051959,43.6946383,1284.772632
1397/11,159225.45,118814.5833,42301526.32,100661546,25.44527221,44.65113267,1308.670441
1397/12,166757.15,130269.5652,45719631.58,110092974,31.45291989,46.40576052,1306.821914
1398/01,191126.0625,134547.8947,47772062.5,114116598,29.76405046,48.25959436,1295.912852
1398/02,211700.9091,145948.0769,49644318.18,127125592,34.02876588,48.99466744,1281.957727
1398/03,227900.7222,134615.5,46068437.5,134253535,33.31876859,49.37691602,1323.637835
1398/04,247256.8636,127636,44368318.18,136156500,32.67550792,50.73509818,1413.527619
1398/05,256353.5,118705.4783,41670222.22,131872735,31.63098576,51.063529,1471.371735
1398/06,290020.05,114116.25,40588157.89,127226350,30.7145684,51.31989801,1515.339524
1398/07,316564.381,114352.8,39855285.71,128481201,30.45437544,52.21436306,1496.772268
1398/08,305587.5,115539.1304,40330388.89,126175831,32.34795215,53.0308583,1482.187709
1398/09,328353.9048,128555.6,44541190.48,134743944,34.66988291,54.72216349,1468.462857
1398/10,376789.2857,133814.6154,47784818.18,138827000,36.15128078,55.18593521,1536.647619
1398/11,442791.9,137581.25,50641500,144057000,40.02597507,55.79571973,1573.857727
1398/12,516826.7895,154107.8261,59553043.48,156587733,42.67924007,56.61125287,1605.236667
1399/01,590234.4706,155946.2,63773000,155457113,43.16801422,57.82837802,1641.03809
1399/02,921318.1739,165174.4444,67658518.52,170066211,50.49983305,59.29519868,1713.521287
1399/03,1084496.529,178892.381,75080900,190718765,49.32087028,60.47759121,1721.730895
1399/04,1657673.87,217190,97992115.38,209860676,54.36459522,64.36162146,1789.749532
1399/05,1940474.95,226971.2,109076400,229405325,59.82111464,66.60268481,1963.555204
1399/06,1643801.667,250366,118886875,245349207,69.84689813,68.99384725,1944.5455
1399/07,1532150.619,296335.0435,144984565.2,270033068,90.33853911,73.85304794,1896.091518
1399/08,1278576.778,273529.5909,131223136.4,278282330,86.8702668,77.65791529,1890.249695
1399/09,1447596.409,256970.04,118715560,269257382,79.4795483,79.22522611,1835.401325
1399/10,1335007.857,250447.6667,114550291.7,277312291,79.01796232,80.6722127,1875.520659
1399/11,1219526.1,243506,111238400,282997657,79.39740765,82.68960322,1831.231059
1399/12,1215112.4,248514.5455,108726666.7,304788799,80.27797584,84.17977568,1739.691443
1400/01,1256697.056,248907.9524,106732857.1,293227000,84.02274995,87.38353669,1737.652341
1400/02,1181387.4,227003.7391,99201913.04,287966000,84.26838864,88.17046234,1815.350187
1400/03,1141726.333,237314.8,105524400,296736000,86.5804927,89.96382244,1869.603095
1400/04,1266209.15,247717.28,106105560,300447000,89.60728604,92.88071386,1795.664822
1400/05,1406234.188,261071.3636,114163478.3,309701000,94.79796088,95.68995352,1786.20651
1400/06,1500982.391,274651.1111,119788518.5,317034000,100.3460526,99.24786566,1794.446509
1400/07,1445776.444,276270.2857,117769800,316311000,100.4405549,102.4271994,1762.854364
1400/08,1405729.81,279696,121695600,320090000,105.2046051,104.5351363,1822.48848
1400/09,1339646.636,295543.4615,129362307.7,325908000,111.0651333,106.3327138,1784.868464
1400/10,1351534.762,283784.6087,126629200,329364000,114.3837636,109.0779965,1813.222114
1400/11,1274276.2,270528.3182,120312409.1,330562000,115.2699491,111.2631561,1833.173619
1400/12,1313482.632,259928.6957,121571782.6,351200000,114.0130631,113.0274434,1943.33452
1401/01,1458297.211,274992.7273,128699545.5,342727000,118.0769358,116.1101901,1945.3859
1401/02,1549367.389,284614.381,136422409.1,363515000,126.6520734,119.9981636,1865.96035
1401/03,1545722,314238.5238,151930733.3,394145000,128.3092645,132.7083309,1846.563882
1401/04,1498058.526,315837.6667,150405416.7,417049000,129.1791913,138.4824833,1762.095783
1401/05,1446004.81,308950.3333,144600000,427299000,129.3388486,141.474077,1765.460424
1401/06,1411496,306236.84,140671538.5,432169000,127.8210243,144.5909443,1707.352491
1401/07,1318095.944,326417.5455,149252954.5,437249000,129.3033721,148.2830016,1664.16281
1401/08,1344733.182,346721.56,158382692.3,467048000,133.910366,151.4953643,1699.354424
1401/09,1431938.273,371325.28,177687160,480737000,145.9583549,154.8255225,1779.924009
1401/10,1620455.895,410590.6667,210781428.6,519814000,177.3372329,160.7486743,1858.727227
1401/11,1573749.053,450395.7368,249105473.7,571444000,185.7802464,166.2350639,1890.772365
1401/12,1787448,510005.2632,291396105.3,652414000,206.2274818,174.0780053,1861.813186
1402/01,2162883,512881.3684,318478157.9,664400000,229.0221756,180.5159817,1991.053532
1402/02,2373097.211,529363.8696,323922227.3,753200000,222.3392458,185.4993721,2003.758824
1402/03,2238705.762,500240.8,295176000,783000000,204.5001092,189.2614766,1954.207761
1402/04,2120824.429,494227.2,282198800,765400000,198.2157058,193.0038686,1935.2224
1402/05,1992791.318,492445.2,282846240,757900000,194.9006677,197.7298426,1926.520959
1402/06,2101480.211,494222.6087,279816521.7,753300000,193.1770099,201.7326265,1924.11087
1402/07,2046556.3,505855.087,283542173.9,760600000,194.0093332,206.4621945,1883.356745
1402/08,2016702.636,511505.3846,291476538.5,757700000,195.3572002,210.9113981,1974.83485
1402/09,2125611.05,504429.75,291991875,740900000,196.3155643,217.0056911,2021.713632
1402/10,2176320.857,515226.1538,305908076.9,753900000,207.0318667,222.6517623,2044.216229
1402/11,2104630,561256.8636,326835590.9,784800000,218.7192396,225.7348843,2023.319543
1402/12,2124936.579,593417.2727,357312000,814400000,228.8550367,230.2470479,2105.048629
1403/01,2235167.188,623795.7,423586500,816300000,240.0561973,236.2937384,2290.530468
1403/02,2234730.727,614919.2308,413981153.8,847500000,242.251604,242.9728971,2339.271476
1403/03,2073244.111,606078.2609,402951521.7,859100000,240.0126489,249.7275076,2339.260717
1403/04,2142929.684,593144.1667,411628750,874600000,240.3814146,255.1721889,2371.536033
1403/05,2053255.5,594792.3077,420735000,885000000,238.6785663,260.2010618,2434.671339
1403/06,2083915.059,594083.3333,434588095.2,950000000,237.5315081,264.7311606,2529.557314
1403/07,2100072.682,624332.6923,493067307.7,960000000,240.3563495,271.7864959,2657.6088
1403/08,2092621.864,683417.3077,518903846.2,980000000,244.836842,279.4725234,2685.189241
1403/09,2494783.5,723904.1667,527729166.7,990000000,257.3808128,285.1209277,2648.494782
1403/10,2831455.619,801408,560426000,1010000000,262.4227947,293.3715084,2653.508744
1403/11,2777380.737,864977.0833,672197916.7,1030000000,269.1864726,305.5230685,2826.42965
1403/12,2766307.8,921897.8261,785186956.5,1070000000,273.8488316,315.6911686,2941.461277
1404/01,2860957.875,952690,891266666.7,1062000000,283.7537136,328.1147139,3114.94106
1404/02,3153188.522,827661.5385,737511538.5,1140000000,281.5429731,336.922645,3299.720113
1404/03,3059180.944,825046.875,737766666.7,1120000000,288.1651811,348.0585874,3348.576345
1404/04,2805394.35,880670.4545,792645833.3,1110000000,294.3342019,360.2368233,3338.635909
1404/05,2610007.333,919010.4167,827110416.7,1100000000,295.3405655,370.5359265,3348.021752
1404/06,2537229.7,1005047.917,934700000,1100000000,303.7211006,384.55935,3571.902848
1404/07,2871553.136,1109580.769,1128396154,1180000000,328.8009221,403.784114,3995.614132
1404/08,3160949.35,1094718,1134042000,1230000000,343.0916565,417.5422415,4047.881827
1404/09,3493649.571,1229150,1309404000,1220000000,380.0787797,435.084401,4235.396455
1404/10,4234804.3,1417688,1593354000,1300000000,418.2381934,469.3638947,4497.650032
1404/11,4048153.947,1561676.667,1891418750,1450000000,479.9898878,513.637392,5002.196258
1404/12,3702776.167,1624947.917,2009472917,1390000000,485.7001616,542.3414344,5084.1888
1405/01,3713956,1563352.083,1858568000,1477000000,497.319039,569.3288044,4652.870435
1405/02,3716222.818,1736209.259,1918511111,1570000000,635.8631785,619.5740766,4641.8632
"""

rows = list(csv.DictReader(io.StringIO(DATA_CSV.strip())))
assert len(rows) == 122
dates = [r["date"] for r in rows]
def col(n): return np.array([float(r[n]) for r in rows])
LUSD, LGC = np.log(col("usd")), np.log(col("goldcoin"))
LVEH, LHOUS, LXAU = np.log(col("vehicle")), np.log(col("housing")), np.log(col("xau"))
Y = np.column_stack([LUSD, LGC, LVEH, LHOUS])
T, K = Y.shape
DY = np.diff(Y, axis=0)                    # row i = return of month i+2
dX = np.diff(LXAU)
iU, iG, iV, iH = 0, 1, 2, 3
OUTC = {"HOUS": 3, "VEH": 2}

def ols(y, X):
    b = linalg.lstsq(X, y)[0]; e = y - X @ b
    return b, e, linalg.inv(X.T @ X), X.shape[0], X.shape[1]

def hac_cov(X, e, XtXi, bw):
    Xe = X * e[:, None]; S = Xe.T @ Xe
    for l in range(1, bw + 1):
        w = 1 - l / (bw + 1); G = Xe[l:].T @ Xe[:-l]; S += w * (G + G.T)
    return XtXi @ S @ XtXi

def johansen(Ylev):
    dY = np.diff(Ylev, axis=0)
    Z0, Z1 = dY[1:], Ylev[1:-1]
    Z2 = np.column_stack([dY[:-1], np.ones(len(Z0))])
    Teff = len(Z0)
    R0 = Z0 - Z2 @ linalg.lstsq(Z2, Z0)[0]
    R1 = Z1 - Z2 @ linalg.lstsq(Z2, Z1)[0]
    S00, S11, S01 = R0.T @ R0 / Teff, R1.T @ R1 / Teff, R0.T @ R1 / Teff
    L = linalg.cholesky(S11, lower=True); Li = linalg.inv(L)
    M = Li @ S01.T @ linalg.inv(S00) @ S01 @ Li.T
    lam, V = linalg.eigh((M + M.T) / 2)
    o = np.argsort(lam)[::-1]; lam = lam[o]
    beta = (Li.T @ V[:, o])[:, :1]; beta = beta / beta[0, 0]
    X = np.column_stack([Z1 @ beta, dY[:-1], np.ones(Teff)])
    Bf = linalg.lstsq(X, Z0)[0]; U = Z0 - X @ Bf
    return dict(eig=lam, trace=-Teff * np.cumsum(np.log(1 - lam)[::-1])[::-1],
                beta=beta, alpha=Bf[0:1].T, Gamma1=Bf[1:1 + K].T, c=Bf[-1],
                U=U, Sigma=U.T @ U / (Teff - X.shape[1]), Teff=Teff)

def prem_equation(Ylev, dXs, nlags=2):
    """Two-lag innovation equation for dLCPREM (agreed). Returns residuals,
    coefficient vector, sd, and the regressor builder order."""
    dYs = np.diff(Ylev, axis=0)
    dCPs = dYs[:, 1] - dYs[:, 0] - dXs
    R = np.column_stack([dYs[:, 0], dCPs, dYs[:, 2], dYs[:, 3], dXs])
    v = johansen(Ylev)
    ECTs = (Ylev @ v["beta"]).ravel()
    n = len(R)
    Xl = [np.ones(n - nlags), np.array([ECTs[i] for i in range(nlags, n)])]
    for l in range(1, nlags + 1):
        Xl.append(R[nlags - l:n - l])
    Xm = np.column_stack(Xl)
    b, e, XtXi, nn, kk = ols(R[nlags:, 1], Xm)
    return v, dict(resid=e, b=b, sd=float(e.std(ddof=1)), nlags=nlags)

# -------------------------------------------------------------------------
# 1. LOCKED SHOCKS (Q1): s_USD = VECM USD-eq residual; s_CPREM = 2-lag prem eq
#    alignment: months 4..122 (j = 0..118); VECM U row k <-> month k+3
# -------------------------------------------------------------------------
vec, pr = prem_equation(Y, dX, nlags=2)
beta, alpha = vec["beta"], vec["alpha"]
sdU_full = float(vec["U"][:, iU].std(ddof=1))
sU = vec["U"][1:, iU] / sdU_full                 # months 4..122
sC = pr["resid"] / pr["sd"]                      # months 4..122
ECT_full = (Y @ beta).ravel()
NS = len(sU); assert NS == len(sC) == 119

res = {"validation": dict(trace_r0=float(vec["trace"][0]),
                          beta=beta.ravel().tolist(), alpha=alpha.ravel().tolist()),
       "shocks_locked": dict(def_sUSD="VECM USD-equation residual (rank1, 1 lag, Case 3)",
                             def_sCPREM="two-lag innovation eq for dLCPREM = dLGC - dLUSD - dLXAU",
                             sd_uUSD=sdU_full, sd_uCPREM=pr["sd"],
                             corr_sUSD_sCPREM=float(np.corrcoef(sU, sC)[0, 1]))}

# diagnostic gate (Q7): Engle ARCH-LM (proper) + McLeod-Li (renamed)
def mcleod_li(e, m=6):
    n = len(e); e2 = e ** 2
    ac = [float(np.corrcoef(e2[l:], e2[:-l])[0, 1]) for l in range(1, m + 1)]
    Q = n * (n + 2) * sum(a * a / (n - l) for l, a in zip(range(1, m + 1), ac))
    return float(Q), float(1 - stats.chi2.cdf(Q, m))
def arch_lm(e, m=6):
    e2 = e ** 2
    Xa = np.column_stack([np.ones(len(e2) - m)] + [e2[m - l:len(e2) - l] for l in range(1, m + 1)])
    ya = e2[m:]
    b, r, XtXi, nn, kk = ols(ya, Xa)
    ss_tot = float(((ya - ya.mean()) ** 2).sum()); ss_res = float((r ** 2).sum())
    R2 = 1 - ss_res / ss_tot
    LM = nn * R2
    return float(LM), float(1 - stats.chi2.cdf(LM, m))
def ljung_box(e, m=6):
    n = len(e); ac = [float(np.corrcoef(e[l:], e[:-l])[0, 1]) for l in range(1, m + 1)]
    Q = n * (n + 2) * sum(a * a / (n - l) for l, a in zip(range(1, m + 1), ac))
    return float(Q), float(1 - stats.chi2.cdf(Q, m))
res["diagnostic_gate"] = {}
for nm, e in [("sUSD", sU), ("sCPREM", sC)]:
    lb = ljung_box(e); ml = mcleod_li(e); al = arch_lm(e)
    res["diagnostic_gate"][nm] = dict(ljung_box_Q6=lb[0], ljung_box_p=lb[1],
                                      mcleod_li_Q6=ml[0], mcleod_li_p=ml[1],
                                      arch_lm_Engle_LM6=al[0], arch_lm_Engle_p=al[1])

# -------------------------------------------------------------------------
# 2. PRIMARY MONTHLY LP (h = 1..12), cumulative secondary
#    shock j <-> month m = j + 4 <-> return row i = j + 2
# -------------------------------------------------------------------------
HP = 12
def lp_family(dYs, dXs, sUv, sCv, ECTs, outc_col, joff=2, hmax=HP,
              cumulative=False, Lser=None, keep=None):
    n = len(dYs); outr = []
    for h in range(1, hmax + 1):
        dep, Xr = [], []
        for j in range(len(sUv)):
            i = j + joff
            if i + h > n - 1: break
            if keep is not None and not keep[j]: continue
            if cumulative:
                dep.append(Lser[i + 1 + h] - Lser[i + 1])
            else:
                dep.append(dYs[i + h, outc_col])
            Xr.append([1.0, sUv[j], sCv[j], dXs[i], ECTs[i],
                       dYs[i - 1, 0], dYs[i - 1, 1], dYs[i - 1, 2], dYs[i - 1, 3]])
        Xr, dep = np.array(Xr), np.array(dep)
        b, e, XtXi, nn, kk = ols(dep, Xr)
        V = hac_cov(Xr, e, XtXi, bw=h + 1)
        se = np.sqrt(np.diag(V))
        outr.append(dict(h=h, n=nn, bU=float(b[1]), seU=float(se[1]),
                         bC=float(b[2]), seC=float(se[2])))
    return outr

lp_m = {o: lp_family(DY, dX, sU, sC, ECT_full, c) for o, c in OUTC.items()}
lp_cum = {o: lp_family(DY, dX, sU, sC, ECT_full, c, cumulative=True, Lser=Y[:, c])
          for o, c in OUTC.items()}
def pv(b, se): return float(2 * (1 - stats.norm.cdf(abs(b / se))))
for o in OUTC:
    for r in lp_m[o] + lp_cum[o]:
        r["pU"], r["pC"] = pv(r["bU"], r["seU"]), pv(r["bC"], r["seC"])

# robustness shocks: (a) two-lag USD side equation (V3 def); (b) one-lag premium
def usd_side_eq(Ylev, dXs, nlags=2):
    dYs = np.diff(Ylev, axis=0)
    dCPs = dYs[:, 1] - dYs[:, 0] - dXs
    R = np.column_stack([dYs[:, 0], dCPs, dYs[:, 2], dYs[:, 3], dXs])
    v = johansen(Ylev); ECTs = (Ylev @ v["beta"]).ravel()
    n = len(R)
    Xl = [np.ones(n - nlags), np.array([ECTs[i] for i in range(nlags, n)])]
    for l in range(1, nlags + 1): Xl.append(R[nlags - l:n - l])
    Xm = np.column_stack(Xl)
    b, e, XtXi, nn, kk = ols(R[nlags:, 0], Xm)
    return e / e.std(ddof=1)
sU_2lag = usd_side_eq(Y, dX, 2)
_, pr1 = prem_equation(Y, dX, nlags=1)
sC_1lag = (pr1["resid"] / pr1["sd"])[1:]         # align to months 4..122
lp_rob = {"usd2lag": {o: lp_family(DY, dX, sU_2lag, sC, ECT_full, c) for o, c in OUTC.items()},
          "prem1lag": {o: lp_family(DY, dX, sU, sC_1lag, ECT_full, c) for o, c in OUTC.items()}}

# leave-one-episode-out (episodes from Stage-1 event dummies), USD->HOUS path
episodes = {"1397/02": 26, "1399/04": 52, "1401/06": 78, "1404/03": 111}
res["leave_one_episode_out_USD_HOUS"] = {}
for nm, m0 in episodes.items():
    keep = np.array([abs((j + 4) - m0) > 2 for j in range(NS)])
    lpe = lp_family(DY, dX, sU, sC, ECT_full, OUTC["HOUS"], keep=keep)
    res["leave_one_episode_out_USD_HOUS"][nm] = dict(
        b_h1=float(lpe[0]["bU"]), p_h1=pv(lpe[0]["bU"], lpe[0]["seU"]),
        maxT=float(max(abs(r["bU"] / r["seU"]) for r in lpe)))

# -------------------------------------------------------------------------
# 3. FULL-CHAIN BOOTSTRAP (wild + block-wild), max-t per path, Holm on 4
# -------------------------------------------------------------------------
Uv, cvec, Gamma1 = vec["U"], vec["c"], vec["Gamma1"]
A1 = np.eye(K) + alpha @ beta.T + Gamma1; A2 = -Gamma1
bx, exr, _, _, _ = ols(dX[1:], np.column_stack([np.ones(len(dX) - 1), dX[:-1]]))
RES = np.column_stack([Uv, exr])

def simulate(eta):
    Rb = RES * eta[:, None]
    Ys = np.zeros_like(Y); Ys[0], Ys[1] = Y[0], Y[1]
    dxs = np.zeros(T - 1); dxs[0] = dX[0]
    for t in range(2, T):
        Ys[t] = A1 @ Ys[t - 1] + A2 @ Ys[t - 2] + cvec + Rb[t - 2, :K]
        dxs[t - 1] = bx[0] + bx[1] * dxs[t - 2] + Rb[t - 2, K]
    return Ys, dxs

paths = [("USD", "HOUS"), ("CPREM", "HOUS"), ("USD", "VEH"), ("CPREM", "VEH")]
bhat = {p: np.array([r["b" + ("U" if p[0] == "USD" else "C")] for r in lp_m[p[1]]]) for p in paths}
sehat = {p: np.array([r["se" + ("U" if p[0] == "USD" else "C")] for r in lp_m[p[1]]]) for p in paths}
maxT_data = {p: float(np.max(np.abs(bhat[p] / sehat[p]))) for p in paths}

boot_centers = {
    "wild": lp_targets(beta, alpha, Gamma1, bx[1], RES, HP),
    "blockwild": lp_targets(beta, alpha, Gamma1, bx[1], RES, HP, block=6)
}
res["bootstrap_centering"] = dict(
    method="Studentized bootstrap LP minus the fitted-DGP population LP coefficient",
    wild_reference="Stationary VECM/AR(1), covariance RES.T @ RES / n",
    blockwild_reference="Phase-averaged periodic residual schedule; independent signs by block; population shock projections refitted",
    scope="Block wild remains a sensitivity analysis; finite initialization is retained in draws",
    centers={scheme: {"%s->%s" % p: center[p].tolist() for p in paths}
             for scheme, center in boot_centers.items()})

def boot_run(B, block=None, seed=1):
    scheme = "wild" if block is None else "blockwild"
    center = boot_centers[scheme]
    rg = np.random.default_rng(seed)
    mx = {p: np.zeros(B) for p in paths}
    kept = 0
    while kept < B:
        if block is None:
            eta = rg.choice([-1.0, 1.0], size=len(RES))
        else:
            nb = int(np.ceil(len(RES) / block))
            eta = np.repeat(rg.choice([-1.0, 1.0], size=nb), block)[:len(RES)]
        Ys, dxs = simulate(eta)
        try:
            vb, prb = prem_equation(Ys, dxs, nlags=2)
        except linalg.LinAlgError:
            continue
        sUb = vb["U"][1:, iU] / vb["U"][:, iU].std(ddof=1)
        sCb = prb["resid"] / prb["sd"]
        ECTb = (Ys @ vb["beta"]).ravel()
        dYb = np.diff(Ys, axis=0)
        for o, c in OUTC.items():
            lpb = lp_family(dYb, dxs, sUb, sCb, ECTb, c)
            for p in paths:
                if p[1] != o: continue
                bb = np.array([r["b" + ("U" if p[0] == "USD" else "C")] for r in lpb])
                ss = np.array([r["se" + ("U" if p[0] == "USD" else "C")] for r in lpb])
                mx[p][kept] = np.max(np.abs((bb - center[p]) / ss))
        kept += 1
        if kept % 250 == 0:
            print(f"Bootstrap {scheme}: {kept}/{B}", flush=True)
    np.savez_compressed(os.path.join(OUT, f"S6v4_bootstrap_maxt_{scheme}.npz"),
                        **{"%s_%s" % p: mx[p] for p in paths})
    return mx

mx_main = boot_run(B_MAIN, block=None, seed=101)
mx_block = boot_run(B_BLOCK, block=6, seed=202)
def path_p(mx): return {("%s->%s" % p): float((mx[p] >= maxT_data[p]).mean()) for p in paths}
p_main, p_block = path_p(mx_main), path_p(mx_block)
def holm_dict(pd_):
    ks = list(pd_); ps = np.array([pd_[k] for k in ks]); adj = {}
    order = np.argsort(ps); mxv = 0.0
    for r, ii in enumerate(order):
        mxv = max(mxv, (len(ks) - r) * ps[ii]); adj[ks[ii]] = float(min(1.0, mxv))
    return adj
res["path_tests"] = dict(
    maxT={("%s->%s" % p): maxT_data[p] for p in paths},
    p_wild=p_main, p_wild_holm4=holm_dict(p_main),
    p_blockwild=p_block, p_blockwild_holm4=holm_dict(p_block),
    B_main=B_MAIN, B_block=B_BLOCK, block_len=6,
    agreed_reading={scheme: dict(
        paths_significant_05=[key for key, value in values.items() if value < 0.05],
        paths_significant_holm4_05=[key for key, value in holm_dict(values).items() if value < 0.05])
        for scheme, values in [("wild", p_main), ("blockwild", p_block)]})
supt = {p: float(np.percentile(mx_main[p], 95)) for p in paths}
supt_block = {p: float(np.percentile(mx_block[p], 95)) for p in paths}
res["path_tests"]["critical95_wild"] = {"%s->%s" % p: supt[p] for p in paths}
res["path_tests"]["critical95_blockwild"] = {"%s->%s" % p: supt_block[p] for p in paths}
with open(os.path.join(OUT, "S6v4_lp_simultaneous_both_schemes.csv"), "w") as f:
    writer = csv.writer(f)
    writer.writerow(["scheme", "shock", "outcome", "h", "b", "se", "center", "critical95", "lower95", "upper95"])
    for scheme, critical in [("wild", supt), ("blockwild", supt_block)]:
        for p in paths:
            for h in range(HP):
                b, se = bhat[p][h], sehat[p][h]
                writer.writerow([scheme, *p, h+1, b, se, boot_centers[scheme][p][h],
                                 critical[p], b-critical[p]*se, b+critical[p]*se])
res["timing"] = {}
for p in paths:
    b, se = bhat[p], sehat[p]
    pw = [pv(b[h], se[h]) for h in range(HP)]
    res["timing"]["%s->%s" % p] = dict(
        peak_month=int(np.argmax(np.abs(b)) + 1), peak_coef=float(b[np.argmax(np.abs(b))]),
        first_month_pointwise05=next((h + 1 for h in range(HP) if pw[h] < 0.05), None),
        months_signif_supt95=[h + 1 for h in range(HP) if abs(b[h] / se[h]) > supt[p]],
        months_signif_block_supt95=[h + 1 for h in range(HP) if abs(b[h] / se[h]) > supt_block[p]])

# -------------------------------------------------------------------------
# 4. PSEUDO-OOS (Q2, Q4, Q5): beta_{tau-1}; origin-specific shocks (main),
#    fully recursive (robustness); confirmatory family = CW(M2 vs M0) for
#    {HOUS, VEH} x {1, 3, 6}; M1 and M2-vs-M1 supplementary; nowcast restored.
# -------------------------------------------------------------------------
def vintage(tauminus1):
    """All objects from months 1..tauminus1 only."""
    Yv = Y[:tauminus1]; dXv = dX[:tauminus1 - 1]
    vv, prv = prem_equation(Yv, dXv, nlags=2)
    sdUv = float(vv["U"][:, iU].std(ddof=1))
    return vv, prv, sdUv

def rt_shocks_at(vv, prv, sdUv, m):
    """Real-time forecast-error shocks for month m (vintage through m-1 or older)."""
    ectm1 = float((Y[m - 2] @ vv["beta"])[0])
    xu = np.concatenate([[ectm1], DY[m - 3], [1.0]])
    predU = float(xu @ np.concatenate([vv["alpha"][iU], vv["Gamma1"][iU], [vv["c"][iU]]]))
    uU = DY[m - 2, iU] - predU
    xreg = [1.0, ectm1]
    for l in range(1, 3):
        i = m - 2 - l
        xreg += [DY[i, 0], DY[i, 1] - DY[i, 0] - dX[i], DY[i, 2], DY[i, 3], dX[i]]
    uC = (DY[m - 2, 1] - DY[m - 2, 0] - dX[m - 2]) - float(np.array(xreg) @ prv["b"])
    return uU / sdUv, uC / prv["sd"]

# fully recursive real-time series (robustness, Q5)
TMIN = 48
srtU = np.full(T + 2, np.nan); srtC = np.full(T + 2, np.nan)
for m in range(TMIN, T + 1):
    try:
        vv, prv, sdUv = vintage(m - 1)
        srtU[m], srtC[m] = rt_shocks_at(vv, prv, sdUv, m)
    except linalg.LinAlgError:
        pass

TAU0_MAIN = 72
HFC = [1, 3, 6]
def clark_west(e0, e1, y0, y1, bw):
    f = np.array(e0) ** 2 - np.array(e1) ** 2 + (np.array(y0) - np.array(y1)) ** 2
    n = len(f); fb = f - f.mean(); var = float(fb @ fb) / n
    for l in range(1, bw + 1):
        var += 2 * (1 - l / (bw + 1)) * float(fb[l:] @ fb[:-l]) / n
    cw = f.mean() / np.sqrt(var / n)
    return float(cw), float(1 - stats.norm.cdf(cw))
def dm(e0, e1, bw):
    d = np.array(e0) ** 2 - np.array(e1) ** 2
    n = len(d); db = d - d.mean(); var = float(db @ db) / n
    for l in range(1, bw + 1):
        var += 2 * (1 - l / (bw + 1)) * float(db[l:] @ db[:-l]) / n
    t = d.mean() / np.sqrt(var / n)
    return float(t), float(2 * (1 - stats.norm.cdf(abs(t))))

def run_oos(tau0, shock_mode="origin"):
    """shock_mode: 'origin' = in-vintage residuals for training (main);
                   'recursive' = fully recursive real-time series (robustness)."""
    out = {}
    for oc, ic in OUTC.items():
        out[oc] = {}
        for h in HFC:
            E = {m: [] for m in ["M0", "M1", "M2"]}; YHp = {m: [] for m in ["M0", "M1", "M2"]}
            for tau in range(tau0, T - h + 1):
                vv, prv, sdUv = vintage(tau - 1)              # Q4: beta_{tau-1}
                bt = vv["beta"]
                # in-vintage historical shocks: months 4..tau-1
                sUo = vv["U"][1:, iU] / sdUv
                sCo = prv["resid"] / prv["sd"]
                rows_y, r0, r1, r2 = [], [], [], []
                for t in range(4, tau - h + 1):
                    if shock_mode == "recursive" and (t < TMIN or np.isnan(srtU[t])):
                        continue
                    ya = Y[t - 1 + h, ic] - Y[t - 1, ic]
                    base = [1.0, DY[t - 2, ic], float((Y[t - 1] @ bt)[0]), dX[t - 2]]
                    su = sUo[t - 4] if shock_mode == "origin" else srtU[t]
                    sc = sCo[t - 4] if shock_mode == "origin" else srtC[t]
                    rows_y.append(ya); r0.append(base)
                    r1.append(base + [DY[t - 2, 0], DY[t - 2, 1] - DY[t - 2, 0] - dX[t - 2]])
                    r2.append(base + [su, sc])
                rows_y = np.array(rows_y)
                suT, scT = rt_shocks_at(vv, prv, sdUv, tau)   # real-time current shock
                baseT = [1.0, DY[tau - 2, ic], float((Y[tau - 1] @ bt)[0]), dX[tau - 2]]
                xT = {"M0": np.array(baseT),
                      "M1": np.array(baseT + [DY[tau - 2, 0], DY[tau - 2, 1] - DY[tau - 2, 0] - dX[tau - 2]]),
                      "M2": np.array(baseT + [suT, scT])}
                ya = Y[tau - 1 + h, ic] - Y[tau - 1, ic]
                for nm, Xtr in [("M0", r0), ("M1", r1), ("M2", r2)]:
                    b = linalg.lstsq(np.array(Xtr), rows_y)[0]
                    yh = float(xT[nm] @ b)
                    YHp[nm].append(yh); E[nm].append(ya - yh)
            sse0 = float((np.array(E["M0"]) ** 2).sum())
            out[oc][f"h{h}"] = dict(
                n=len(E["M0"]),
                rmse_M0=float(np.sqrt(np.mean(np.array(E["M0"]) ** 2))),
                R2_M1=float(1 - (np.array(E["M1"]) ** 2).sum() / sse0),
                R2_M2=float(1 - (np.array(E["M2"]) ** 2).sum() / sse0),
                CW_M2vsM0=clark_west(E["M0"], E["M2"], YHp["M0"], YHp["M2"], bw=h + 1),
                CW_M1vsM0_suppl=clark_west(E["M0"], E["M1"], YHp["M0"], YHp["M1"], bw=h + 1),
                DM_M2vsM1_suppl=dm(E["M1"], E["M2"], bw=h + 1))
            if oc == "HOUS" and h == 1 and shock_mode == "origin" and tau0 == TAU0_MAIN:
                with open(os.path.join(OUT, "S6v4_oos_errors_HOUS_h1.csv"), "w") as f:
                    f.write("origin,e_M0,e_M1,e_M2\n")
                    for j, tau in enumerate(range(tau0, T - h + 1)):
                        f.write(f"{dates[tau-1]},{E['M0'][j]:.6f},{E['M1'][j]:.6f},{E['M2'][j]:.6f}\n")
    return out

oos_main = run_oos(TAU0_MAIN, "origin")
fam = {f"{oc}_h{h}": oos_main[oc][f"h{h}"]["CW_M2vsM0"][1] for oc in OUTC for h in HFC}
res["pseudo_oos_main"] = oos_main
res["confirmatory_family_CW_M2vsM0"] = dict(p=fam, holm6=holm_dict(fam))
res["pseudo_oos_recursive_robustness"] = run_oos(TAU0_MAIN, "recursive")
res["window_sensitivity"] = {}
for t0 in (60, 84):
    oo = run_oos(t0, "origin")
    res["window_sensitivity"][f"TAU0_{t0}"] = {f"{oc}_h{h}": dict(
        R2_M2=oo[oc][f"h{h}"]["R2_M2"], CW_p=oo[oc][f"h{h}"]["CW_M2vsM0"][1])
        for oc in OUTC for h in HFC}

# conditional nowcast (Q6): predict dln y_tau with same-month hard-asset info
def run_nowcast(tau0):
    out = {}
    for oc, ic in OUTC.items():
        Eb, Em, Yb, Ym = [], [], [], []
        for tau in range(tau0, T + 1):
            vv, prv, sdUv = vintage(tau - 1)
            bt = vv["beta"]
            sUo = vv["U"][1:, iU] / sdUv; sCo = prv["resid"] / prv["sd"]
            rows_y, rb, rm = [], [], []
            for t in range(4, tau):
                ya = DY[t - 2, ic]
                base = [1.0, DY[t - 3, ic], float((Y[t - 2] @ bt)[0]), dX[t - 2]]
                rows_y.append(ya); rb.append(base)
                rm.append(base + [sUo[t - 4], sCo[t - 4]])
            rows_y = np.array(rows_y)
            suT, scT = rt_shocks_at(vv, prv, sdUv, tau)
            baseT = [1.0, DY[tau - 3, ic], float((Y[tau - 2] @ bt)[0]), dX[tau - 2]]
            xb = np.array(baseT); xm = np.array(baseT + [suT, scT])
            ya = DY[tau - 2, ic]
            bb = linalg.lstsq(np.array(rb), rows_y)[0]
            bm = linalg.lstsq(np.array(rm), rows_y)[0]
            yhb, yhm = float(xb @ bb), float(xm @ bm)
            Yb.append(yhb); Ym.append(yhm); Eb.append(ya - yhb); Em.append(ya - yhm)
        sseb = float((np.array(Eb) ** 2).sum())
        out[oc] = dict(n=len(Eb),
                       R2_vs_bench=float(1 - (np.array(Em) ** 2).sum() / sseb),
                       CW=clark_west(Eb, Em, Yb, Ym, bw=4))
    return out
res["nowcast_supplementary"] = run_nowcast(TAU0_MAIN + 1)

# -------------------------------------------------------------------------
# 5. STABILITY (unchanged from V3; ECT standardized per half)
# -------------------------------------------------------------------------
def half_eq(Ylev, dXs):
    vv, prv = prem_equation(Ylev, dXs, nlags=2)
    sUv = vv["U"][1:, iU] / vv["U"][:, iU].std(ddof=1)
    sCv = prv["resid"] / prv["sd"]
    ECTv = (Ylev @ vv["beta"]).ravel()
    ECTv = (ECTv - ECTv.mean()) / ECTv.std(ddof=1)
    dYs = np.diff(Ylev, axis=0)
    dep, Xr = [], []
    for j in range(len(sUv)):
        i = j + 2
        if i + 1 > len(dYs) - 1: break
        dep.append(dYs[i + 1, iH])
        Xr.append([1.0, sUv[j], sCv[j], dXs[i], ECTv[i],
                   dYs[i - 1, 0], dYs[i - 1, 1], dYs[i - 1, 2], dYs[i - 1, 3]])
    Xr, dep = np.array(Xr), np.array(dep)
    b, e, XtXi, nn, kk = ols(dep, Xr)
    V = hac_cov(Xr, e, XtXi, bw=4)
    return b, V
mid = T // 2
b1, V1 = half_eq(Y[:mid], dX[:mid - 1])
b2, V2 = half_eq(Y[mid:], dX[mid:])
Rsel = np.zeros((3, 9)); Rsel[0, 1] = 1; Rsel[1, 2] = 1; Rsel[2, 4] = 1
dd = Rsel @ b1 - Rsel @ b2
Wsp = float(dd @ linalg.inv(Rsel @ V1 @ Rsel.T + Rsel @ V2 @ Rsel.T) @ dd)
psp = float(1 - stats.chi2.cdf(Wsp, 3))
res["stability_split_full_reestimation"] = dict(
    chi2=Wsp, df=3, p=psp,
    first_half=dict(sUSD=float(b1[1]), sCPREM=float(b1[2]), ECT_std=float(b1[4])),
    second_half=dict(sUSD=float(b2[1]), sCPREM=float(b2[2]), ECT_std=float(b2[4])),
    reading=("REJECTED: significant parameter instability across halves" if psp < 0.05
             else "no significant instability detected"))

with open(os.path.join(OUT, "S6v4_recursive_paths.csv"), "w") as f:
    f.write("through_month,b_sUSD_h1,se\n")
    for tau in range(60, T + 1):
        try:
            btq, Vtq = half_eq(Y[:tau], dX[:tau - 1])
            f.write(f"{dates[tau-1]},{btq[1]:.6f},{np.sqrt(Vtq[1,1]):.6f}\n")
        except linalg.LinAlgError:
            pass

# -------------------------------------------------------------------------
# 6. SAVE + REPORT
# -------------------------------------------------------------------------
with open(os.path.join(OUT, "S6v4_lp_monthly.csv"), "w") as f:
    f.write("outcome,h,n,b_sUSD,se,p,supt_lo95,supt_hi95,b_sCPREM,seC,pC,supt_loC,supt_hiC\n")
    for o in OUTC:
        cU = supt[("USD", o)]; cC = supt[("CPREM", o)]
        for r in lp_m[o]:
            f.write(f'{o},{r["h"]},{r["n"]},{r["bU"]:.6f},{r["seU"]:.6f},{r["pU"]:.6f},'
                    f'{r["bU"]-cU*r["seU"]:.6f},{r["bU"]+cU*r["seU"]:.6f},'
                    f'{r["bC"]:.6f},{r["seC"]:.6f},{r["pC"]:.6f},'
                    f'{r["bC"]-cC*r["seC"]:.6f},{r["bC"]+cC*r["seC"]:.6f}\n')
with open(os.path.join(OUT, "S6v4_lp_cumulative_secondary.csv"), "w") as f:
    f.write("outcome,h,n,b_sUSD,se,p,b_sCPREM,seC,pC\n")
    for o in OUTC:
        for r in lp_cum[o]:
            f.write(f'{o},{r["h"]},{r["n"]},{r["bU"]:.6f},{r["seU"]:.6f},{r["pU"]:.6f},'
                    f'{r["bC"]:.6f},{r["seC"]:.6f},{r["pC"]:.6f}\n')
with open(os.path.join(OUT, "S6v4_lp_robustness_shockdefs.csv"), "w") as f:
    f.write("variant,outcome,h,b_sUSD,p_sUSD,b_sCPREM,p_sCPREM\n")
    for vr, dd_ in lp_rob.items():
        for o in OUTC:
            for r in dd_[o]:
                f.write(f'{vr},{o},{r["h"]},{r["bU"]:.6f},{pv(r["bU"],r["seU"]):.6f},'
                        f'{r["bC"]:.6f},{pv(r["bC"],r["seC"]):.6f}\n')
with open(os.path.join(OUT, "S6v4_results.json"), "w") as f:
    json.dump(res, f, indent=2, default=float)

print("=== ANCHOR ===  trace r0 = %.5f  beta =" % res["validation"]["trace_r0"], np.round(beta.ravel(), 6))
print("\n=== LOCKED SHOCKS ===")
print(json.dumps(res["shocks_locked"], indent=1, default=float))
print("gate:", json.dumps(res["diagnostic_gate"], indent=1, default=float))
print("\n=== PRIMARY MONTHLY LP ===")
for o in OUTC:
    print("outcome", o)
    for r in lp_m[o]:
        print("  h=%2d  b_sUSD=%+.5f (p=%.4f)   b_sCPREM=%+.5f (p=%.4f)" %
              (r["h"], r["bU"], r["pU"], r["bC"], r["pC"]))
print("\n=== PATH TESTS ===")
print(json.dumps(res["path_tests"], indent=1, default=float))
print("timing:", json.dumps(res["timing"], indent=1, default=float))
print("\n=== CONFIRMATORY FAMILY: CW(M2 vs M0), {HOUS,VEH} x {1,3,6} ===")
print(json.dumps(res["confirmatory_family_CW_M2vsM0"], indent=1, default=float))
print("\nOOS main (origin-specific shocks):")
print(json.dumps(res["pseudo_oos_main"], indent=1, default=float))
print("\nRecursive-shock robustness:")
print(json.dumps({oc: {h: dict(R2_M2=v2["R2_M2"], CW_p=v2["CW_M2vsM0"][1])
                        for h, v2 in d.items()} for oc, d in res["pseudo_oos_recursive_robustness"].items()},
                 indent=1, default=float))
print("\nWindow sensitivity:", json.dumps(res["window_sensitivity"], indent=1, default=float))
print("\nNowcast (supplementary):", json.dumps(res["nowcast_supplementary"], indent=1, default=float))
print("\nLeave-one-episode-out (USD->HOUS):",
      json.dumps(res["leave_one_episode_out_USD_HOUS"], indent=1, default=float))
print("\n=== STABILITY ===")
print(json.dumps(res["stability_split_full_reestimation"], indent=1, default=float))
print("\nDone. Outputs in", OUT)
