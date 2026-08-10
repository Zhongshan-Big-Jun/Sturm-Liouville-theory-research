# verify_hs_bound.py - O1a/P4/P5 checks (evidence)
#  H1: Hilbert-Schmidt bound ||S_rho - S_sigma||_HS <= (R/4)||rho-sigma||_1^{1/2}
#  H2: Weyl |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
#  H3: comparison bounds lambda_k(rho) in [k^2 pi^2/R, k^2 pi^2]
#  H4: eigenvalues of the discretized symmetric kernel S_rho = 1/lambda_k(rho)
#  H5: continuity of eigenfunctions in L1 (uniform convergence rate check)
# Seeds: 20260806.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs

rng = np.random.default_rng(20260806)
R = 4.0
out = {}

def random_rho(nblocks, rng, R):
    xs = np.sort(rng.uniform(0, 1, nblocks - 1))
    breaks = np.concatenate([[0.0], xs, [1.0]])
    values = rng.uniform(1.0, R, nblocks)
    return breaks, values

def hs_norm2(rho, sigma, R):
    """int int G^2 (sqrt(rho x rho t) - sqrt(sigma x sigma t))^2 via 2D trapezoid."""
    n = 4000
    x = np.linspace(0, 1, n)
    r1, s1 = rho[1], sigma[1]
    br, vr = rho[0], rho[1]
    bs, vs = sigma[0], sigma[1]
    rho_x = stepvals(x, br, vr)
    sigma_x = stepvals(x, bs, vs)
    G = np.minimum.outer(x, x) * (1 - np.maximum.outer(x, x))
    A = np.sqrt(np.outer(rho_x, rho_x)) - np.sqrt(np.outer(sigma_x, sigma_x))
    K = G * A
    h = 1.0 / (n - 1)
    w = np.ones(n); w[0] = w[-1] = 0.5
    val = h * h * np.sum(np.outer(w, w) * K ** 2)
    return val

def stepvals(x, breaks, values):
    # true step function: value values[i] on (breaks[i], breaks[i+1])
    idx = np.searchsorted(breaks, x, side='right') - 1
    idx = np.clip(idx, 0, len(values) - 1)
    return np.asarray(values, dtype=float)[idx]

def l1_dist(rho, sigma):
    # ||rho - sigma||_1 via fine grid
    n = 200000
    x = np.linspace(0, 1, n)
    a = stepvals(x, rho[0], rho[1])
    b = stepvals(x, sigma[0], sigma[1])
    return np.trapezoid(np.abs(a - b), x)

H1 = []
H2 = []
H3 = []
for trial in range(8):
    rho = random_rho(6, rng, R)
    sigma = random_rho(6, rng, R)
    d1 = l1_dist(rho, sigma)
    hs = np.sqrt(hs_norm2(rho, sigma, R))
    bound = (R / 4.0) * np.sqrt(d1)
    H1.append({"trial": trial, "hs": hs, "bound": bound, "ratio": hs / bound})
    lr = eigenvalues(rho[0], rho[1], k_max=2)
    ls = eigenvalues(sigma[0], sigma[1], k_max=2)
    for k in (0, 1):
        weyl = abs(1.0 / lr[k] - 1.0 / ls[k])
        H2.append({"trial": trial, "k": k + 1, "weyl_diff": weyl, "hs": hs, "ok": weyl <= hs + 1e-12})
        ub = (k + 1) ** 2 * np.pi ** 2
        lb = ub / R
        ok = (lb - 1e-9 <= lr[k] <= ub + 1e-9) and (lb - 1e-9 <= ls[k] <= ub + 1e-9)
        H3.append({"trial": trial, "k": k + 1, "lam": lr[k], "lb": lb, "ub": ub, "ok": ok})

out["H1_HS_bound"] = H1
out["H2_Weyl"] = H2
out["H3_comparison_bounds"] = H3

# H4: discretized symmetric kernel eigenvalue spot check
n = 1200
x = np.linspace(0, 1, n)
h = 1.0 / (n - 1)
rho = ([0.0, 0.3, 0.7, 1.0], [1.0, R, 1.0])
lam = eigenvalues(rho[0], rho[1], k_max=2)
rho_x = stepvals(x, rho[0], rho[1])
G = np.minimum.outer(x, x) * (1 - np.maximum.outer(x, x))
K = np.sqrt(np.outer(rho_x, rho_x)) * G
w = np.ones(n); w[0] = w[-1] = 0.5
Sw = np.sqrt(w)
# symmetric quadrature discretization: tilde S_ij = sqrt(w_i) K_ij sqrt(w_j) h
S = (Sw[:, None] * K * Sw[None, :]) * h
eig = np.linalg.eigvalsh(S)[::-1]
out["H4_kernel_eigs"] = {
    "mu1_disc": float(eig[0]), "1/lam1": 1.0 / lam[0], "rel": abs(eig[0] - 1.0 / lam[0]) / (1.0 / lam[0]),
    "mu2_disc": float(eig[1]), "1/lam2": 1.0 / lam[1], "rel2": abs(eig[1] - 1.0 / lam[1]) / (1.0 / lam[1]),
}

# H5: eigenfunction continuity: rho_eps = rho with a jump moved by eps; check max|u_k(eps) - u_k(0)|
def rho_eps(eps):
    return ([0.0, 0.3 + eps, 0.7, 1.0], [1.0, R, 1.0])
base = rho_eps(0.0)
lams0 = eigenvalues(base[0], base[1], k_max=2)
us0, up0, xg = eigenfuncs(base[0], base[1], lams0)
H5 = []
for eps in (1e-3, 1e-4, 1e-5):
    r = rho_eps(eps)
    lr = eigenvalues(r[0], r[1], k_max=2)
    us, up, xg = eigenfuncs(r[0], r[1], lr)
    d1 = np.max(np.abs(us[0] - us0[0]))
    d2 = np.max(np.abs(us[1] - us0[1]))
    H5.append({"eps": eps, "maxdiff_u1": d1, "maxdiff_u2": d2, "ratio_u1": d1 / eps, "ratio_u2": d2 / eps})
out["H5_eigenfunction_continuity"] = H5

def _conv(o):
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_hs_bound_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)








