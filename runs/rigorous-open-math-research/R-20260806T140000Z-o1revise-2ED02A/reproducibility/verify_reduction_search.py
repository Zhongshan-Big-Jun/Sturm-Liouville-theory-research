# verify_reduction_search.py - theorem-level adversarial search (evidence)
#  T1: max over barrier family (2-param scan + refine) vs contract values at R=4
#  T2: min over well family vs contract values at R=4
#  T3: random adversarial configs (2-8 blocks, bang-bang and continuous values)
#      never beat barrier max or undercut well min
# Seeds: 777.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize
from sl_lib import D_of

rng = np.random.default_rng(777)
out = {}

def secular_vec(lams, breaks, values):
    """Vectorized secular values F(lambda) for an array of lambdas."""
    L = np.asarray(lams, dtype=float)
    M00 = np.ones_like(L); M01 = np.zeros_like(L)
    M10 = np.zeros_like(L); M11 = np.ones_like(L)
    for i in range(len(breaks) - 1):
        le = breaks[i + 1] - breaks[i]
        if le <= 0:
            continue
        k = np.sqrt(L * values[i])
        ck = np.cos(k * le); sk = np.sin(k * le)
        A00 = ck; A01 = sk / k; A10 = -k * sk; A11 = ck
        # M = A @ M
        n00 = A00 * M00 + A01 * M10
        n01 = A00 * M01 + A01 * M11
        n10 = A10 * M00 + A11 * M10
        n11 = A10 * M01 + A11 * M11
        M00, M01, M10, M11 = n00, n01, n10, n11
    return M01

def fast_eigs(breaks, values, k_max=2, lam_max=None, step=0.002):
    if lam_max is None:
        lam_max = (k_max ** 2) * np.pi ** 2 * 1.01 + 0.5
    grid = np.linspace(1e-9, lam_max, int(lam_max / step) + 1)
    F = secular_vec(grid, breaks, values)
    roots = []
    for i in range(len(grid) - 1):
        if F[i] * F[i + 1] < 0:
            from scipy.optimize import brentq
            r = brentq(lambda l: float(secular_vec(np.array([l]), breaks, values)[0]), grid[i], grid[i + 1], xtol=1e-14, rtol=1e-13)
            roots.append(r)
    roots = sorted(roots)
    if len(roots) < k_max:
        raise RuntimeError(f"only {len(roots)} roots")
    return roots[:k_max]

def D_fast(breaks, values):
    l = fast_eigs(breaks, values, k_max=2)
    return l[1] - l[0]

def barrier_rho(a, b, R):
    return ([0.0, a, b, 1.0], [1.0, R, 1.0])

def well_rho(a, b, R):
    return ([0.0, a, b, 1.0], [R, 1.0, R])

def scan_family(R, kind, n=70):
    best = -1e9 if kind == "bar" else 1e9
    best_ab = None
    a_grid = np.linspace(0.0, 1.0, n)
    b_grid = np.linspace(0.0, 1.0, n)
    for a in a_grid:
        for b in b_grid[b_grid >= a]:
            rho = barrier_rho(a, b, R) if kind == "bar" else well_rho(a, b, R)
            D = D_fast(rho[0], rho[1])
            if (kind == "bar" and D > best) or (kind == "inf" and D < best):
                best, best_ab = D, (a, b)
    return best, best_ab

def refine_family(R, kind, ab):
    sign = -1.0 if kind == "bar" else 1.0
    def obj(x):
        a, b = x
        if not (0.0 <= a <= b <= 1.0):
            return 1e6
        rho = barrier_rho(a, b, R) if kind == "bar" else well_rho(a, b, R)
        return sign * D_fast(rho[0], rho[1])
    res = minimize(obj, np.array(ab), method="Nelder-Mead",
                   options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 400})
    a, b = res.x
    Dv = D_fast(barrier_rho(a, b, R)[0], barrier_rho(a, b, R)[1]) if kind == "bar" else D_fast(well_rho(a, b, R)[0], well_rho(a, b, R)[1])
    return Dv, (float(a), float(b))

for R in (2.0, 4.0, 10.0, 50.0):
    bbest, bab = scan_family(R, "bar", n=45)
    bD, bab2 = refine_family(R, "bar", bab)
    wbest, wab = scan_family(R, "inf", n=45)
    wD, wab2 = refine_family(R, "inf", wab)
    out[f"R={R}"] = {"bar_max": bD, "bar_at": bab2, "well_min": wD, "well_at": wab2}

# T3: adversarial random configs
R = 4.0
bar_max = out["R=4.0"]["bar_max"]
well_min = out["R=4.0"]["well_min"]
viol_up = []
viol_dn = []
maxD_seen = -1e9; minD_seen = 1e9
for t in range(300):
    nb = int(rng.integers(2, 9))
    xs = np.concatenate([[0.0], np.sort(rng.uniform(0, 1, nb - 1)), [1.0]])
    if t % 2 == 0:
        vals = rng.choice([1.0, R], nb)
    else:
        vals = rng.uniform(1.0, R, nb)
    D = D_fast(xs, vals)
    maxD_seen = max(maxD_seen, D); minD_seen = min(minD_seen, D)
    if D > bar_max + 1e-7:
        viol_up.append({"t": t, "D": D, "bar_max": bar_max, "breaks": xs, "values": vals})
    if D < well_min - 1e-7:
        viol_dn.append({"t": t, "D": D, "well_min": well_min, "breaks": xs, "values": vals})
out["T3_adversarial"] = {
    "n_configs": 300, "R": R,
    "maxD_seen": maxD_seen, "bar_max": bar_max, "minD_seen": minD_seen, "well_min": well_min,
    "n_violations_up": len(viol_up), "n_violations_dn": len(viol_dn),
    "violations_up": viol_up[:2], "violations_dn": viol_dn[:2],
}
# known values at R=4
out["contract_R4"] = {"SUP": 32.6139836177, "INF": 6.7844823391}
def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_reduction_search_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)

