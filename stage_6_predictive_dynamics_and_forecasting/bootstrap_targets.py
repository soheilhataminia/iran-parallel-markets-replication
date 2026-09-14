"""Population LP centers for the fitted Stage-6 bootstrap DGP.

The target is the coefficient of the *same LP*, including both generated
standardized residuals and all controls. It is not a Cholesky response or the
original sample LP coefficient. Constants disappear after centering.

Wild: use the stationary fitted VECM/AR(1) with covariance RES'RES/n.
Block wild: retain the exact within-block second moments of RES[t]*eta[block].
Periodically extend the observed residual schedule, with independent signs
for every new block; average over schedule phase. This defines a stationary
population reference for the fixed-design bootstrap (which itself retains
the original finite-sample initialization). Refit both shock projections in
population: block multipliers can make fitted disturbances predictable.

The periodic reference is a centering convention for the block sensitivity
analysis, not a proof of finite-sample coverage or a new identification claim.
"""
import numpy as np
from scipy.linalg import solve_discrete_lyapunov


def state_matrices(beta, alpha, gamma, rho):
    beta, alpha = np.ravel(beta), np.ravel(alpha)
    F = np.zeros((6, 6))
    F[0, 0] = 1 + beta @ alpha
    F[0, 1:5] = beta @ gamma
    F[1:5, 0] = alpha
    F[1:5, 1:5] = gamma
    F[5, 5] = rho
    G = np.zeros((6, 5))
    G[0, :4] = beta
    G[1:5, :4] = np.eye(4)
    G[5, 4] = 1
    if max(abs(np.linalg.eigvals(F))) >= 1:
        raise ValueError('The ECT/differences state must be stationary')
    return F, G


def state_autocovariances(F, G, residuals, maxlag, block=None):
    """Return C[l] = E[state_t state_(t-l)']; state=(ECT, dY[4], dXAU)."""
    n = len(residuals)
    if block is None:
        omega = residuals.T @ residuals / n
        P = solve_discrete_lyapunov(F, G @ omega @ G.T)
        return np.array([np.linalg.matrix_power(F, lag) @ P
                         for lag in range(maxlag + 1)])
    if block < 1 or n % block:
        raise ValueError('Periodic block reference requires a full number of blocks')
    # Augment state by the current block sign. At a block boundary this
    # sign is replaced with an independent Rademacher draw, not propagated.
    As, Qs = [], []
    for t, e in enumerate(residuals):
        q = G @ e
        A = np.zeros((7, 7)); A[:6, :6] = F
        Q = np.zeros((7, 7))
        if t % block == 0:
            v = np.r_[q, 1.0]
            Q = np.outer(v, v)
        else:
            A[:6, 6] = q
            A[6, 6] = 1
        As.append(A); Qs.append(Q)
    cycle_A, cycle_Q = np.eye(7), np.zeros((7, 7))
    for A, Q in zip(As, Qs):
        cycle_A = A @ cycle_A
        cycle_Q = A @ cycle_Q @ A.T + Q
    P = solve_discrete_lyapunov(cycle_A, cycle_Q)
    initial = P.copy()
    Ps = []
    for A, Q in zip(As, Qs):
        P = A @ P @ A.T + Q
        Ps.append(P.copy())
    if not np.allclose(P, initial, rtol=1e-9, atol=1e-11):
        raise ArithmeticError('Periodic covariance did not close')
    C = []
    for lag in range(maxlag + 1):
        total = np.zeros((7, 7))
        for t in range(n):
            transition = np.eye(7)
            for step in range(lag):
                transition = transition @ As[(t - step) % n]
            total += transition @ Ps[(t - lag) % n]
        C.append((total / n)[:6, :6])
    return np.array(C)


def lp_targets(beta, alpha, gamma, rho, residuals, hmax=12, block=None):
    """Exact second-moment projection under the chosen population reference."""
    F, G = state_matrices(beta, alpha, gamma, rho)
    C = state_autocovariances(F, G, residuals, hmax + 2, block)
    # z_t stacks states at t, t-1, t-2. All original shock/LP regressors
    # are linear functions of these 18 coordinates.
    V = np.block([[C[b-a] if b >= a else C[a-b].T
                   for b in range(3)] for a in range(3)])
    V = (V + V.T) / 2
    eye = np.eye(18)
    wu = eye[[6, 7, 8, 9, 10]]  # ECT_(t-1), four lagged changes
    u = eye[1] - np.linalg.solve(wu @ V @ wu.T, wu @ V @ eye[1]) @ wu
    premium = eye[2] - eye[1] - eye[5]
    # The original lag vector (USD, premium, vehicle, housing, XAU).
    wc = [eye[6]]
    for offset in (6, 12):
        wc.extend([eye[offset+1], eye[offset+2]-eye[offset+1]-eye[offset+5],
                   eye[offset+3], eye[offset+4], eye[offset+5]])
    wc = np.array(wc)
    c = premium - np.linalg.solve(wc @ V @ wc.T, wc @ V @ premium) @ wc
    sd_u, sd_c = np.sqrt(u @ V @ u), np.sqrt(c @ V @ c)
    if not (sd_u > 0 and sd_c > 0):
        raise ArithmeticError('Nonpositive population shock variance')
    X = np.vstack([u / sd_u, c / sd_c, eye[5], wu])
    XX = X @ V @ X.T
    out = {(shock, outcome): [] for shock in ('USD', 'CPREM')
           for outcome in ('HOUS', 'VEH')}
    for h in range(1, hmax + 1):
        yz = np.column_stack([C[h], C[h+1], C[h+2]])
        coeff = np.linalg.solve(XX, X @ yz.T).T
        for outcome, row in [('HOUS', 4), ('VEH', 3)]:
            for shock, col in [('USD', 0), ('CPREM', 1)]:
                out[(shock, outcome)].append(float(coeff[row, col]))
    return {key: np.array(value) for key, value in out.items()}
