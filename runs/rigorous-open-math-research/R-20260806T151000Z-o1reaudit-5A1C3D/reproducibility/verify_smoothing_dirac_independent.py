# verify_smoothing_dirac_independent.py - R4 repair checks (evidence only)
#  D1: Dirac family: int (1/delta) H'((x - a)/delta) g(x) dx -> g(a) as delta -> 0
#  D2: smoothed moving-jump derivative converges to lambda_k (c_+ - c_-) u_k(x_j)^2
# H = smoothstep polynomial, H' = 30 s^2 (1-s)^2 on [0,1], supported in [-1,1].
# Written from scratch.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fd_lib import fd_eigs, grid_rho_from_steps

R = 4.0
N = 4000
out = {}

def H(s):
    s = np.clip(s, -1.0, 1.0)
    t = np.clip((s + 1.0) / 2.0, 0.0, 1.0)
    return 10.0 * t ** 3 - 15.0 * t ** 4 + 6.0 * t ** 5

def Hp(s):
    # d/ds H(s); nonzero on (-1,1), integral 1
    s = np.clip(s, -1.0, 1.0)
    t = np.clip((s + 1.0) / 2.0, 0.0, 1.0)
    return (30.0 * t ** 2 * (1.0 - t) ** 2) / 2.0

def dirac_apply(g, a, delta, n=20001):
    x = np.linspace(0.0, 1.0, n)
    vals = (1.0 / delta) * Hp((x - a) / delta) * g(x)
    return np.trapezoid(vals, x)

g = lambda x: 1.0 + x + x ** 3 + np.sin(7.0 * x)
D1 = []
for a in (0.3, 0.55, 0.8):
    ga = g(a)
    row = {"a": a, "target": ga}
    for delta in (0.05, 0.02, 0.01, 0.005, 0.002, 0.001):
        v = dirac_apply(g, a, delta)
        row["d" + str(delta)] = {"value": v, "err": abs(v - ga)}
    D1.append(row)
out["D1_dirac_family"] = D1

# D2: single jump [1, R] at xj = 0.3; smoothed rho_eps^delta.
# Target: d lambda_k / d eps -> lambda_k (R - 1) u_k(xj)^2.
xj = 0.3
breaks0 = [0.0, xj, 1.0]
values0 = [1.0, R]
w0, us, xg, rho_int, h = None, None, None, None, None

def smoothed_blocks(xj_, eps, delta, nblocks=4000):
    xs = np.linspace(0.0, 1.0, nblocks + 1)
    mids = 0.5 * (xs[1:] + xs[:-1])
    vals = 1.0 + (R - 1.0) * H((mids - xj_ - eps) / delta)
    return (xs.tolist(), vals.tolist())

# reference eigenfunctions of the unsmoothed single-jump config
def eig_ref():
    w, v = fd_eigs(grid_rho_from_steps(breaks0, values0, N), N, k_max=2)
    rho_int = grid_rho_from_steps(breaks0, values0, N)
    funcs = []
    for k in (0, 1):
        norm2 = h * np.sum(rho_int * v[:, k] ** 2)
        uu = np.concatenate(([0.0], v[:, k] / np.sqrt(norm2), [0.0]))
        funcs.append(uu)
    return w, funcs

h = 1.0 / N
xg = np.linspace(0.0, 1.0, N + 1)
w_ref, us_ref = eig_ref()
u1j = float(np.interp(xj, xg, us_ref[0]))
u2j = float(np.interp(xj, xg, us_ref[1]))
target1 = w_ref[0] * (R - 1.0) * u1j ** 2
target2 = w_ref[1] * (R - 1.0) * u2j ** 2
out["D2_reference"] = {"lams": w_ref.tolist(), "u1j": u1j, "u2j": u2j,
                       "target_dlam1": target1, "target_dlam2": target2}

def lam_smoothed(eps, delta, k, nblocks=4000):
    br, va = smoothed_blocks(xj, eps, delta, nblocks=nblocks)
    w = fd_eigs(grid_rho_from_steps(br, va, N), N, k_max=2)[0]
    return w[k - 1]

D2 = []
for delta in (0.04, 0.02, 0.01, 0.005, 0.002):
    eps = delta / 4.0
    row = {"delta": delta, "eps": eps}
    for k in (1, 2):
        d = (lam_smoothed(eps, delta, k) - lam_smoothed(-eps, delta, k)) / (2 * eps)
        tgt = target1 if k == 1 else target2
        row["dlam" + str(k)] = d
        row["rel" + str(k)] = abs(d - tgt) / abs(tgt)
    D2.append(row)
out["D2_smoothed_derivatives"] = D2

def _conv(o):
    if isinstance(o, (np.bool_, np.integer)):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_smoothing_dirac_independent_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)