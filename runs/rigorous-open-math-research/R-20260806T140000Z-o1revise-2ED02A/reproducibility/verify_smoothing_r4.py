# verify_smoothing_r4.py (fixed) - R4 repair check (evidence)
# Single-jump reference [1, R] with jump at x_j = 0.3.  Smoothed family
# rho_eps^delta(x) = 1 + (R-1) H((x - x_j - eps)/delta); the derivative
# d lambda_k / d eps must converge to lambda_k (c_+ - c_-) u_k(x_j)^2 as
# delta -> 0 (Dirac measure limit).  Piecewise-constant block approximation.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
from sl_lib import eigenvalues, state_at
from numpy.polynomial.legendre import leggauss

R = 4.0
out = {}

def sigmoid(t):
    t = np.clip(t, -1.0, 1.0)
    return np.where(t <= -1, 0.0, np.where(t >= 1, 1.0, 0.5 + 0.5 * np.tanh(np.tanh(t * np.pi / 2) * 2)))

def smoothed_blocks(xj, delta, c_minus, c_plus, nblocks=800):
    xs = np.linspace(0.0, 1.0, nblocks + 1)
    mids = 0.5 * (xs[1:] + xs[:-1])
    vals = c_minus + (c_plus - c_minus) * sigmoid((mids - xj) / delta)
    return xs, vals

def fast_lams(breaks, values, k_max=2, lam_max=None, step=0.004):
    if lam_max is None:
        lam_max = (k_max ** 2) * np.pi ** 2 * 1.02 + 0.5
    grid = np.linspace(1e-9, lam_max, int(lam_max / step) + 1)
    L = grid
    M00 = np.ones_like(L); M01 = np.zeros_like(L)
    M10 = np.zeros_like(L); M11 = np.ones_like(L)
    for i in range(len(breaks) - 1):
        le = breaks[i + 1] - breaks[i]
        if le <= 0: continue
        k = np.sqrt(L * values[i])
        ck = np.cos(k * le); sk = np.sin(k * le)
        A00 = ck; A01 = sk / k; A10 = -k * sk; A11 = ck
        n00 = A00 * M00 + A01 * M10; n01 = A00 * M01 + A01 * M11
        n10 = A10 * M00 + A11 * M10; n11 = A10 * M01 + A11 * M11
        M00, M01, M10, M11 = n00, n01, n10, n11
    F = M01
    def sec(l):
        Ls = np.array([l]); M0 = np.ones(1); M1 = np.zeros(1); M2 = np.zeros(1); M3 = np.ones(1)
        for i in range(len(breaks) - 1):
            le = breaks[i + 1] - breaks[i]
            if le <= 0: continue
            k = np.sqrt(Ls * values[i])
            ck = np.cos(k * le); sk = np.sin(k * le)
            n0 = ck * M0 + (sk / k) * M2; n1 = ck * M1 + (sk / k) * M3
            n2 = -k * sk * M0 + ck * M2; n3 = -k * sk * M1 + ck * M3
            M0, M1, M2, M3 = n0, n1, n2, n3
        return float(M1[0])
    roots = []
    for i in range(len(grid) - 1):
        if F[i] * F[i + 1] < 0:
            r = brentq(sec, grid[i], grid[i + 1], xtol=1e-12, rtol=1e-11)
            roots.append(r)
    roots = sorted(roots)
    if len(roots) < k_max:
        raise RuntimeError(f"only {len(roots)} roots")
    return roots[:k_max]

# reference: single-jump [1, R] at 0.3
breaks0 = [0.0, 0.3, 1.0]
values0 = [1.0, R]
lam0 = eigenvalues(breaks0, values0, k_max=2)
xg = np.linspace(0, 1, 20001)
def norm_eig(lam, br, va):
    u = np.array([state_at(x, lam, br, va)[0] for x in xg])
    norm2 = 0.0
    for i in range(len(br) - 1):
        a, b = br[i], br[i + 1]
        if b - a <= 0: continue
        nodes, wts = leggauss(24)
        xs_ = 0.5 * (a + b) + 0.5 * (b - a) * nodes
        vals_ = np.array([state_at(x, lam, br, va)[0] for x in xs_])
        norm2 += 0.5 * (b - a) * np.sum(wts * va[i] * vals_ ** 2)
    return u / np.sqrt(norm2)
u1 = norm_eig(lam0[0], breaks0, values0)
u2 = norm_eig(lam0[1], breaks0, values0)
u1j = np.interp(0.3, xg, u1); u2j = np.interp(0.3, xg, u2)
pred1 = lam0[0] * (R - 1.0) * u1j ** 2
pred2 = lam0[1] * (R - 1.0) * u2j ** 2
out["reference"] = {"lams": lam0, "target_dlam1": pred1, "target_dlam2": pred2}

rows = []
for delta in (0.05, 0.02, 0.01, 0.005, 0.002):
    nblocks = 1200
    eps = 2e-3 if delta >= 0.01 else (1e-3 if delta >= 0.005 else 5e-4)
    derivs = []
    for k in (1, 2):
        def lam_of_eps(e):
            bs, vs = smoothed_blocks(0.3 + e, delta, 1.0, R, nblocks=nblocks)
            return fast_lams(bs, vs, k_max=2)[k - 1]
        d = (lam_of_eps(eps) - lam_of_eps(-eps)) / (2 * eps)
        derivs.append(d)
    rows.append({"delta": delta, "nblocks": nblocks, "eps": eps,
                 "dlam1_num": derivs[0], "dlam2_num": derivs[1],
                 "rel1": abs(derivs[0] - pred1) / abs(pred1),
                 "rel2": abs(derivs[1] - pred2) / abs(pred2)})
out["smoothed_derivatives"] = rows

def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_smoothing_r4_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)
