import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.linalg import eigh
from sl_lib import eigenvalues

rng = np.random.default_rng(20260806)
R = 4.0

def random_rho(nblocks, rng, R):
    xs = np.sort(rng.uniform(0, 1, nblocks - 1))
    breaks = np.concatenate([[0.0], xs, [1.0]])
    values = rng.uniform(1.0, R, nblocks)
    return breaks, values

def stepvals(x, breaks, values):
    fp = np.concatenate([values, [values[-1]]])
    return np.interp(x, breaks, fp, left=values[0], right=values[-1])

def fd_eigs(rho, N=6000, k=2):
    x = np.linspace(0, 1, N + 1)
    h = 1.0 / N
    rv = stepvals((x[1:] + x[:-1]) / 2, rho[0], rho[1])
    diag = 2.0 / h ** 2
    A = np.zeros((N, N))
    idx = np.arange(N)
    A[idx, idx] = diag
    A[idx[:-1], idx[:-1] + 1] = -1.0 / h ** 2
    A[idx[:-1] + 1, idx[:-1]] = -1.0 / h ** 2
    # generalized: A y = lam * rho * y  ->  M y = lam y with M = D rho^{-1} A? 
    # Use: A y = lam diag(rv) y  =>  (diag(rv)^{-1} A) y = lam y (not symmetric)
    # symmetrize: diag(rv^{-1/2}) A diag(rv^{-1/2}) (w, w) = lam w with w = rv^{1/2} y
    s = np.sqrt(rv)
    B = A / s[None, :] / s[:, None]   # careful with broadcasting
    B = A.copy()
    for i in range(N):
        B[i, :] /= s[i]
        B[:, i] /= s[i]
    w = eigh(B, eigvals_only=True, subset_by_index=(0, k - 1))
    return np.sort(w)

def hs_norm2(rho, sigma, n):
    x = np.linspace(0, 1, n)
    r1 = stepvals(x, rho[0], rho[1]); s1 = stepvals(x, sigma[0], sigma[1])
    G = np.minimum.outer(x, x) * (1 - np.maximum.outer(x, x))
    A = np.sqrt(np.outer(r1, r1)) - np.sqrt(np.outer(s1, s1))
    K = G * A
    h = 1.0 / (n - 1)
    w = np.ones(n); w[0] = w[-1] = 0.5
    return h * h * np.sum(np.outer(w, w) * K ** 2)

def op_norm(rho, sigma, n=4000, iters=200):
    x = np.linspace(0, 1, n)
    h = 1.0 / (n - 1)
    r1 = stepvals(x, rho[0], rho[1]); s1 = stepvals(x, sigma[0], sigma[1])
    G = np.minimum.outer(x, x) * (1 - np.maximum.outer(x, x))
    K = G * (np.sqrt(np.outer(r1, r1)) - np.sqrt(np.outer(s1, s1)))
    w = np.ones(n); w[0] = w[-1] = 0.5
    # symmetric discretization: tilde K_ij = sqrt(w_i) K_ij sqrt(w_j) h
    Sw = np.sqrt(w)
    S = (Sw[:, None] * K * Sw[None, :]) * h
    v = np.ones(n); v /= np.linalg.norm(v)
    lam_est = 0.0
    for _ in range(iters):
        u = S @ v
        lam_est = np.linalg.norm(u)
        v = u / lam_est
    return lam_est

out = {}
for trial in (2, 6):
    # regenerate the same configs: consume rng draws in same order
    pass
# regenerate by replaying rng from scratch
rng = np.random.default_rng(20260806)
configs = []
for trial in range(8):
    configs.append((random_rho(6, rng, R), random_rho(6, rng, R)))
for trial in (2, 6):
    rho, sigma = configs[trial]
    lr = eigenvalues(rho[0], rho[1], k_max=2)
    ls = eigenvalues(sigma[0], sigma[1], k_max=2)
    fd_r = fd_eigs(rho); fd_s = fd_eigs(sigma)
    hs4 = np.sqrt(hs_norm2(rho, sigma, 4000))
    hs8 = np.sqrt(hs_norm2(rho, sigma, 8000))
    opn = op_norm(rho, sigma, 4000, 300)
    out[f"trial{trial}"] = {
        "tm_lams_rho": lr, "fd_lams_rho": fd_r, "tm_lams_sigma": ls, "fd_lams_sigma": fd_s,
        "weyl_tm": abs(1/lr[0] - 1/ls[0]), "weyl_fd": abs(1/fd_r[0] - 1/fd_s[0]),
        "hs_4000": hs4, "hs_8000": hs8, "op_norm_4000": opn,
    }
def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))

