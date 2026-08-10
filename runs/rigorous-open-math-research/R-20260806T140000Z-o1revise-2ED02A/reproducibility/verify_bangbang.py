# verify_bangbang.py - O1f checks (evidence)
#  B1: pointwise FH formula dD/dt = int delta-rho f dx at a non-extremal config
#      (delta-rho = eta chi_J, strips inside blocks, both signs of f)
#  B2: saturation at the global barrier maximizer: rho = R on {f>0}, 1 on {f<0}
#  B3: saturation at the global well minimizer: rho = 1 on {f>0}, R on {f<0}
# Seeds: none (fixed configs).

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs, f_of, D_of

R = 4.0
out = {}

# ---- B1: formula test on the barrier config with u = 0.3 ----
u = 0.3
breaks = [0.0, u, 1.0 - u, 1.0]
values = [1.0, R, 1.0]
lams = eigenvalues(breaks, values, k_max=2)
us, up, xg = eigenfuncs(breaks, values, lams)
f, _, _ = f_of(breaks, values, lams, us, up)

def stepvals(x):
    idx = np.clip(np.searchsorted(breaks, x, side='right') - 1, 0, len(values) - 1)
    return np.asarray(values, dtype=float)[idx]

def perturb_D(J, eta):
    # rho + eta * chi_J
    b2 = sorted([0.0, u, 1.0 - u, 1.0] + [J[0], J[1]])
    v2 = []
    for i in range(len(b2) - 1):
        mid = 0.5 * (b2[i] + b2[i + 1])
        base = stepvals(mid)
        v2.append(base + (eta if J[0] <= mid <= J[1] else 0.0))
    return D_of(b2, v2)

# strips: inside the barrier (rho=4, f>0 near z0), and inside (0,u) (rho=1)
strips = []
# find a maximal subinterval of (0.3, 0.7) where f > 0
mask = (xg > 0.31) & (xg < 0.69) & (f > 0)
if mask.any():
    idx = np.where(mask)[0]
    strips.append(("barrier_fpos", (float(xg[idx[0]]), float(xg[idx[-1]])), 4.0))
# strip inside (0, u) where f < 0
mask2 = (xg > 0.02) & (xg < 0.28) & (f < 0)
if mask2.any():
    idx = np.where(mask2)[0]
    strips.append(("left_fneg", (float(xg[idx[0]]), float(xg[idx[-1]])), 1.0))

B1 = []
for name, J, base_val in strips:
    eta = 0.1
    D0 = D_of(breaks, values, lams)
    D1 = perturb_D(J, eta)
    pred = eta * np.trapezoid(f * ((xg > J[0]) & (xg < J[1])), xg)
    B1.append({
        "name": name, "J": J, "eta": eta, "base_rho": base_val,
        "dD_num": D1 - D0, "dD_pred": pred, "absdiff": abs((D1 - D0) - pred),
    })
out["B1_fh_pointwise"] = B1

# ---- B2: saturation at global maximizer (symmetric u*) ----
u_star = 0.451485468013
breaks = [0.0, u_star, 1.0 - u_star, 1.0]
values = [1.0, R, 1.0]
lams = eigenvalues(breaks, values, k_max=2)
us, up, xg = eigenfuncs(breaks, values, lams)
f, _, _ = f_of(breaks, values, lams, us, up)
rho_x = stepvals(xg)
# interior samples away from jumps
interior = (xg > 1e-6) & (xg < 1 - 1e-6)
fp = f[interior] > 1e-9
fn = f[interior] < -1e-9
rp = rho_x[interior]
bad_fp = np.any((fp) & (np.abs(rp - R) > 1e-9))
bad_fn = np.any((fn) & (np.abs(rp - 1.0) > 1e-9))
out["B2_maximizer_saturation"] = {
    "rho_eq_R_on_{f>0}": not bool(bad_fp), "rho_eq_1_on_{f<0}": not bool(bad_fn),
    "D": lams[1] - lams[0],
}

# ---- B3: saturation at global minimizer (symmetric well) ----
u_inf = 0.3825982560
breaks = [0.0, u_inf, 1.0 - u_inf, 1.0]
values = [R, 1.0, R]
lams = eigenvalues(breaks, values, k_max=2)
us, up, xg = eigenfuncs(breaks, values, lams)
f, _, _ = f_of(breaks, values, lams, us, up)
def stepvals2(x):
    idx = np.clip(np.searchsorted(breaks, x, side='right') - 1, 0, len(values) - 1)
    return np.asarray(values, dtype=float)[idx]
rho_x = stepvals2(xg)
interior = (xg > 1e-6) & (xg < 1 - 1e-6)
fp = f[interior] > 1e-9
fn = f[interior] < -1e-9
rp = rho_x[interior]
bad_fp = np.any((fp) & (np.abs(rp - 1.0) > 1e-9))
bad_fn = np.any((fn) & (np.abs(rp - R) > 1e-9))
out["B3_minimizer_saturation"] = {
    "rho_eq_1_on_{f>0}": not bool(bad_fp), "rho_eq_R_on_{f<0}": not bool(bad_fn),
    "D": lams[1] - lams[0],
}

def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_bangbang_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)
