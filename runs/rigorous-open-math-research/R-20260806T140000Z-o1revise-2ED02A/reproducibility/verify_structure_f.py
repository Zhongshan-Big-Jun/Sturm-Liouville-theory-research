# verify_structure_f.py (fixed) - O1c structure checks on the OPEN interval (0,1)
#  S1: u_1 > 0 on (0,1); u_2 has exactly one interior zero z_0 (Sturm, P7)
#  S2: W = u_1 u_2' - u_1' u_2 < 0 on (0,1)
#  S3: v = u_2/u_1 strictly decreasing on (0,1)
#  S4: f has at most two zeros in (0,1); {f>0} single interval containing z_0
#  S5: normalization int rho u_k^2 = 1
# Seeds: 4242.  Boundary points excluded (Dirichlet zeros are at 0,1).

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs, f_of

rng = np.random.default_rng(4242)
R = 4.0
out = {}

def interior_sign_changes(vals, xg, margin=1e-9):
    # count sign changes between consecutive samples strictly inside (0,1),
    # ignoring numerical noise (require |values| > margin on both sides)
    n = len(vals)
    cnt = 0
    for i in range(1, n - 2):
        if vals[i] * vals[i + 1] < 0 and abs(vals[i]) > margin and abs(vals[i + 1]) > margin:
            cnt += 1
        elif abs(vals[i]) <= margin and vals[i - 1] * vals[i + 1] < 0:
            cnt += 1
    return cnt

def check_config(breaks, values, tag):
    lams = eigenvalues(breaks, values, k_max=2)
    us, up, xg = eigenfuncs(breaks, values, lams)
    f, _, _ = f_of(breaks, values, lams, us, up)
    u1, u2, u1p, u2p = us[0], us[1], up[0], up[1]
    def stepvals(x):
        idx = np.clip(np.searchsorted(breaks, x, side='right') - 1, 0, len(values) - 1)
        return np.asarray(values, dtype=float)[idx]
    rv = stepvals(xg)
    s5 = (float(np.trapezoid(rv * u1 ** 2, xg)), float(np.trapezoid(rv * u2 ** 2, xg)))
    # interior only
    lo, hi = 1, len(xg) - 2
    xi = xg[lo:hi]
    u1i, u2i, u1pi, u2pi = u1[lo:hi], u2[lo:hi], u1p[lo:hi], u2p[lo:hi]
    fi = f[lo:hi]
    z1 = interior_sign_changes(u1, xg)
    z2 = interior_sign_changes(u2, xg)
    # locate z0: sign change of u2, including zeros exactly on grid points
    z0 = None
    for i in range(1, len(xg) - 2):
        if (u2[i] * u2[i + 1] < 0 and abs(u2[i]) > 1e-9 and abs(u2[i + 1]) > 1e-9):
            z0 = float(0.5 * (xg[i] + xg[i + 1])); break
        if abs(u2[i]) <= 1e-9 and u2[i - 1] * u2[i + 1] < 0:
            z0 = float(xg[i]); break
    # W < 0 on interior
    W = u1i * u2pi - u1pi * u2i
    Wneg = bool(np.all(W < 0))
    # v strictly decreasing on interior (u1 bounded away from 0 away from boundary)
    v = u2i / u1i
    vdec = bool(np.all(np.diff(v) < 0))
    # f zeros interior + positive set
    fz = []
    for i in range(len(fi) - 1):
        if fi[i] * fi[i + 1] < 0:
            fz.append(float(0.5 * (xi[i] + xi[i + 1])))
    pos = fi > 0
    trans = int(np.sum(pos[1:] != pos[:-1]))
    single = bool(trans <= 2)
    contains = None
    if z0 is not None:
        idx0 = int(np.searchsorted(xg, z0))
        contains = bool(f[idx0] > 0)
    return {
        "tag": tag, "nblocks": len(values), "lams": lams,
        "u1_interior_zeros": z1, "u2_interior_zeros": z2, "z0": z0,
        "W_neg": Wneg, "v_strictly_decreasing": vdec,
        "f_interior_zero_count": len(fz),
        "f_positive_single_interval": single, "f_positive_contains_z0": contains,
        "norm_u1": s5[0], "norm_u2": s5[1],
    }

results = []
for nb in (3, 5, 7):
    for shift in (0, 1):
        xs = np.linspace(0, 1, nb + 1)
        vals = [R if (i + shift) % 2 == 0 else 1.0 for i in range(nb)]
        results.append(check_config(xs, vals, f"alt_{nb}_{shift}"))
for t in range(8):
    nb = int(rng.integers(4, 9))
    xs = np.concatenate([[0.0], np.sort(rng.uniform(0, 1, nb - 1)), [1.0]])
    vals = rng.uniform(1.0, R, nb)
    results.append(check_config(xs, vals, f"rand_{t}_nb{nb}"))
for t in range(8):
    nb = int(rng.integers(3, 9))
    xs = np.concatenate([[0.0], np.sort(rng.uniform(0, 1, nb - 1)), [1.0]])
    vals = rng.choice([1.0, R], nb)
    results.append(check_config(xs, vals, f"bang_{t}_nb{nb}"))

out["configs"] = results
out["summary"] = {
    "all_u1_interior_zero_free": all(r["u1_interior_zeros"] == 0 for r in results),
    "all_u2_one_interior_zero": all(r["u2_interior_zeros"] == 1 for r in results),
    "all_W_neg": all(r["W_neg"] for r in results),
    "all_v_decreasing": all(r["v_strictly_decreasing"] for r in results),
    "all_f_zero_count_le2": all(r["f_interior_zero_count"] <= 2 for r in results),
    "all_f_pos_single": all(r["f_positive_single_interval"] for r in results),
    "all_f_pos_contains_z0": all(r["f_positive_contains_z0"] for r in results),
    "norm_tol": max(max(abs(r["norm_u1"] - 1), abs(r["norm_u2"] - 1)) for r in results),
}
def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_structure_f_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)


