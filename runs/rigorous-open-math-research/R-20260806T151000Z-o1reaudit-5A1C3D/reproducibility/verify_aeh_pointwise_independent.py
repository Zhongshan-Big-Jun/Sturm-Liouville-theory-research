# verify_aeh_pointwise_independent.py (v2) - AEH Lemma 2.1 pointwise perturbation,
# H^2 uniform bounds, and R=4 contract sanity check (evidence only).
# Eigenvalues via the exact transfer-matrix solver (tm_lib.py); eigenfunctions
# via tm_lib.eigenfuncs with numerical derivatives on the fine grid.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from tm_lib import eigenvalues, eigenvalues_vec, eigenfuncs

R = 4.0
out = {}

# A1: pointwise FH: w(kappa) = rho + kappa * chi_J, d lambda_k/d kappa|_0
#     = -lambda_k int_J u_k^2 dx (AEH Lemma 2.1, V = 0)
base = ([0.0, 0.4, 0.7, 1.0], [1.0, R, 1.0])
J = (0.3, 0.45)

def lam_bump(kappa):
    pts = sorted(set(base[0]) | set(J))
    vals = []
    for i in range(len(pts) - 1):
        mid = 0.5 * (pts[i] + pts[i + 1])
        idx = np.searchsorted(base[0], mid, side="right") - 1
        v = base[1][idx]
        if pts[i] >= J[0] and pts[i + 1] <= J[1]:
            v += kappa
        vals.append(v)
    return (pts, vals)

lams0 = eigenvalues(*base, k_max=2)
us0, xg = eigenfuncs(*base, lams0)
A1 = []
for k in (0, 1):
    mask = (xg >= J[0]) & (xg <= J[1])
    intJ = np.trapezoid(us0[k][mask] ** 2, xg[mask])
    kappa = 1e-4
    lam_plus = eigenvalues(*lam_bump(kappa), k_max=2)[k]
    lam_minus = eigenvalues(*lam_bump(-kappa), k_max=2)[k]
    num = (lam_plus - lam_minus) / (2 * kappa)
    pred = -lams0[k] * intJ
    A1.append({"k": k + 1, "numeric": num, "predicted": pred, "absdiff": abs(num - pred),
               "ok": abs(num - pred) <= 1e-3})
out["A1_pointwise_FH"] = A1

# A2: H^2 uniform bounds on hostile configs: ||u_k||_2 <= 1,
#     ||u_k'||_2 <= k pi, ||u_k''||_2 <= (k pi)^2 R (numerical derivatives)
configs = [
    ("barrier", ([0.0, 0.2, 0.65, 1.0], [1.0, R, 1.0])),
    ("well", ([0.0, 0.3, 0.7, 1.0], [R, 1.0, R])),
    ("alt", ([0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0], [1.0, R, 1.0, R, 1.0, R, 1.0, R])),
    ("step_up", ([0.0, 0.5, 1.0], [1.0, R])),
]
A2 = []
for tag, (br, va) in configs:
    lams = eigenvalues(br, va, k_max=2)
    us, xg = eigenfuncs(br, va, lams, xgrid=np.linspace(0.0, 1.0, 40001))
    h = xg[1] - xg[0]
    for k in (0, 1):
        u = us[k]
        up = np.gradient(u, h)
        upp = np.gradient(up, h)
        n2 = np.sqrt(np.trapezoid(u ** 2, xg))
        nup = np.sqrt(np.trapezoid(up ** 2, xg))
        nupp = np.sqrt(np.trapezoid(upp ** 2, xg))
        A2.append({"tag": tag, "k": k + 1, "lam": lams[k],
                   "||u||_2": n2, "||u'||_2": nup, "||u''||_2": nupp,
                   "ok_u": n2 <= 1.0 + 1e-6,
                   "ok_up": nup <= (k + 1) * np.pi * (1 + 1e-3),
                   "ok_upp": nupp <= (k + 1) ** 2 * np.pi ** 2 * R * (1 + 1e-3)})
out["A2_H2_bounds"] = A2

# A3: R = 4 contract sanity check (evidence; O2/O3 territory, not part of O1)
def D_barrier(a, b):
    l = eigenvalues_vec([0.0, a, b, 1.0], [1.0, R, 1.0], k_max=2)
    return l[1] - l[0]

def D_well(a, b):
    l = eigenvalues_vec([0.0, a, b, 1.0], [R, 1.0, R], k_max=2)
    return l[1] - l[0]

best_bar = (-1.0, None)
best_well = (1e9, None)
for a in np.linspace(0.0, 0.5, 51):
    for b in np.linspace(max(a, 0.5), 1.0, 51):
        db = D_barrier(a, b)
        if db > best_bar[0]:
            best_bar = (db, (float(a), float(b)))
        dw = D_well(a, b)
        if dw < best_well[0]:
            best_well = (dw, (float(a), float(b)))
for _ in range(2):
    a0, b0 = best_bar[1]
    for a in np.linspace(max(0.0, a0 - 0.02), min(0.5, a0 + 0.02), 41):
        for b in np.linspace(max(a, b0 - 0.02), min(1.0, b0 + 0.02), 41):
            db = D_barrier(a, b)
            if db > best_bar[0]:
                best_bar = (db, (float(a), float(b)))
    a0, b0 = best_well[1]
    for a in np.linspace(max(0.0, a0 - 0.02), min(0.5, a0 + 0.02), 41):
        for b in np.linspace(max(a, b0 - 0.02), min(1.0, b0 + 0.02), 41):
            dw = D_well(a, b)
            if dw < best_well[0]:
                best_well = (dw, (float(a), float(b)))
out["A3_contract_sanity"] = {
    "sup_barrier_D": best_bar[0], "argmax": best_bar[1],
    "inf_well_D": best_well[0], "argmin": best_well[1],
    "contract_sup": 32.6139836177, "contract_inf": 6.7844823391,
    "rel_err_sup": abs(best_bar[0] - 32.6139836177) / 32.6139836177,
    "rel_err_inf": abs(best_well[0] - 6.7844823391) / 6.7844823391,
}

def _conv(o):
    if isinstance(o, (np.bool_, np.integer)):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_aeh_pointwise_independent_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)