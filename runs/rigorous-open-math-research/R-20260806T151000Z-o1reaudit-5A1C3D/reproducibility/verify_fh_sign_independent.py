# verify_fh_sign_independent.py (v2) - independent O1b checks (evidence only)
# Uses the exact transfer-matrix solver (tm_lib.py) so that jump motion is
# resolved exactly (no finite-difference grid-pinning).
#  V1: d lambda_k / d eps = lambda_k (c_+ - c_-) u_k(x_j)^2 (central diff)
#  V2: dD/d eps = -(c_+ - c_-) f(x_j); rightward/leftward distance derivatives
#      have the predicted opposite signs
#  V3: symmetric barrier dD/du = -2(R-1) f(u)
#  V4: stationarity at u*: f(u*) ~ 0, one-sided derivatives flip sign
# Written from scratch.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from tm_lib import eigenvalues, state_at, eigenfuncs

R = 4.0
out = {}

def move_jump(breaks, values, j, eps):
    br = list(breaks)
    br[j + 1] = br[j + 1] + eps
    return (br, list(values))

def lam_k(breaks, values, k):
    return eigenvalues(breaks, values, k_max=2)[k - 1]

def D_of(breaks, values):
    w = eigenvalues(breaks, values, k_max=2)
    return w[1] - w[0]

def f_at(x, breaks, values, lams=None, us=None, xg=None):
    if lams is None:
        lams = eigenvalues(breaks, values, k_max=2)
    if us is None:
        us, xg = eigenfuncs(breaks, values, lams)
    u1 = float(np.interp(x, xg, us[0]))
    u2 = float(np.interp(x, xg, us[1]))
    return lams[0] * u1 ** 2 - lams[1] * u2 ** 2

configs = {
    "barrier_1R1": (([0.0, 0.2, 0.65, 1.0], [1.0, R, 1.0]), [0.2, 0.65]),
    "well_R1R": (([0.0, 0.3, 0.7, 1.0], [R, 1.0, R]), [0.3, 0.7]),
    "alt_4block": (([0.0, 0.15, 0.4, 0.6, 0.85, 1.0], [1.0, R, 1.0, R, 1.0]),
                   [0.15, 0.4, 0.6, 0.85]),
}

epsilons = [1e-3, 1e-4]
V1, V2 = [], []
for tag, (cfg, jumps) in configs.items():
    breaks, values = cfg
    lams = eigenvalues(breaks, values, k_max=2)
    us, xg = eigenfuncs(breaks, values, lams)
    for xj in jumps:
        j = list(breaks).index(xj) - 1
        cminus = values[j]
        cplus = values[j + 1]
        dc = cplus - cminus
        u1j = float(np.interp(xj, xg, us[0]))
        u2j = float(np.interp(xj, xg, us[1]))
        fxj = lams[0] * u1j ** 2 - lams[1] * u2j ** 2
        for eps in epsilons:
            dlam1 = (lam_k(*move_jump(breaks, values, j, eps), 1) - lam_k(*move_jump(breaks, values, j, -eps), 1)) / (2 * eps)
            dlam2 = (lam_k(*move_jump(breaks, values, j, eps), 2) - lam_k(*move_jump(breaks, values, j, -eps), 2)) / (2 * eps)
            pred1 = lams[0] * dc * u1j ** 2
            pred2 = lams[1] * dc * u2j ** 2
            dD_num = dlam2 - dlam1
            predD = -dc * fxj
            V1.append({"tag": tag, "xj": xj, "c-": cminus, "c+": cplus, "eps": eps,
                       "dlam1": dlam1, "pred1": pred1, "err1": abs(dlam1 - pred1),
                       "dlam2": dlam2, "pred2": pred2, "err2": abs(dlam2 - pred2),
                       "ok1": abs(dlam1 - pred1) <= 1e-5, "ok2": abs(dlam2 - pred2) <= 1e-5})
            V2.append({"tag": tag, "xj": xj, "eps": eps, "dD_num": dD_num, "predD": predD,
                       "absdiff": abs(dD_num - predD), "ok": abs(dD_num - predD) <= 1e-5})
out["V1_lambda_derivatives"] = V1
out["V2_D_derivatives"] = V2

# V2b: one-sided distance derivatives sign flip (barrier, first jump)
breaks0, values0 = configs["barrier_1R1"][0]
xj0 = 0.2
lams0 = eigenvalues(breaks0, values0, k_max=2)
us0, xg0 = eigenfuncs(breaks0, values0, lams0)
fxj0 = lams0[0] * np.interp(xj0, xg0, us0[0]) ** 2 - lams0[1] * np.interp(xj0, xg0, us0[1]) ** 2
D0 = D_of(breaks0, values0)
V2b = []
for eps in epsilons:
    # rightward distance derivative: d/d delta D(jump at xj + delta)|_0 = -(c_+ - c_-) f
    # leftward distance derivative:  d/d delta D(jump at xj - delta)|_0 = +(c_+ - c_-) f
    right = (D_of(*move_jump(breaks0, values0, 0, eps)) - D0) / eps
    left = (D_of(*move_jump(breaks0, values0, 0, -eps)) - D0) / eps
    V2b.append({"eps": eps, "right_deriv": right, "right_pred": -(R - 1.0) * fxj0,
                "left_deriv": left, "left_pred": +(R - 1.0) * fxj0,
                "sign_flip_ok": bool(np.sign(right) != np.sign(left)),
                "right_ok": abs(right + (R - 1.0) * fxj0) <= 0.05,
                "left_ok": abs(left - (R - 1.0) * fxj0) <= 0.05})
out["V2b_one_sided"] = V2b

# V3: symmetric barrier family [1,R,1] on (u,1-u), dD/du = -2(R-1) f(u)
def D_sym(u):
    return D_of([0.0, u, 1.0 - u, 1.0], [1.0, R, 1.0])

def f_sym(u):
    return f_at(u, [0.0, u, 1.0 - u, 1.0], [1.0, R, 1.0])

V3 = []
for u in (0.2, 0.3, 0.4, 0.45148546584, 0.49):
    num = (D_sym(u + 1e-5) - D_sym(u - 1e-5)) / 2e-5
    pred = -2.0 * (R - 1.0) * f_sym(u)
    V3.append({"u": u, "dDdu_num": num, "pred": pred, "absdiff": abs(num - pred),
               "ok": abs(num - pred) <= 1e-3})
out["V3_symmetric_family"] = V3

# V4: stationarity at u* (one-sided derivatives flip sign; f(u*) ~ 0)
u_star = 0.45148546584
right = (D_sym(u_star + 1e-5) - D_sym(u_star)) / 1e-5
left = (D_sym(u_star) - D_sym(u_star - 1e-5)) / 1e-5
out["V4_stationarity_u*"] = {"u*": u_star, "right": right, "left": left,
                             "f(u*)": f_sym(u_star)}

def _conv(o):
    if isinstance(o, (np.bool_, np.integer)):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_fh_sign_independent_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)