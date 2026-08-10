# verify_fh_sign.py - O1b moving-jump FH derivative signs (evidence)
# Checks:
#  V1: signed derivative dD/deps at jump = -(c_+ - c_-) f(x_j)  (central diff)
#  V2: rightward distance derivative = -(c_+ - c_-) f(x_j); leftward = +(c_+ - c_-) f(x_j)
#  V3: d lambda_k/deps = lambda_k (c_+ - c_-) u_k(x_j)^2
#  V4: symmetric barrier family identity dD/du = -2(R-1) f(u)
#  V5: stationarity: at u* both one-sided derivatives vanish
# Seeds: none (deterministic configs).

import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs, f_of, D_of

R = 4.0
out = {}

# --- V1/V2/V3: 3-block config [1, R, 1], jumps at x1 = 0.2, x2 = 0.65 ---
x1, x2 = 0.2, 0.65
base = ([0.0, x1, x2, 1.0], [1.0, R, 1.0])
lams = eigenvalues(base[0], base[1], k_max=2)
us, up, xg = eigenfuncs(base[0], base[1], lams)
f, _, _ = f_of(base[0], base[1], lams, us, up)
# f at the jump point x1 (interpolate on grid)
fx1 = np.interp(x1, xg, f)

def D_jump_at_x1(delta):
    # move the FIRST jump (value 1 -> R at x1) right by delta
    breaks = [0.0, x1 + delta, x2, 1.0]
    values = [1.0, R, 1.0]
    if not (0.0 < x1 + delta < x2):
        return None
    return D_of(breaks, values)

epsilons = [1e-3, 1e-4, 1e-5]
central = (D_jump_at_x1(1e-4) - D_jump_at_x1(-1e-4)) / 2e-4
pred_central = -(R - 1.0) * fx1
out["V1_signed_central"] = {"numeric": central, "predicted": pred_central,
                            "absdiff": abs(central - pred_central)}

right = [(eps, D_jump_at_x1(eps) - D_of(base[0], base[1], lams)) for eps in epsilons]
left = [(eps, D_jump_at_x1(-eps) - D_of(base[0], base[1], lams)) for eps in epsilons]
out["V2_rightward"] = [
    {"eps": e, "dD": d, "pred": -(R - 1.0) * fx1 * e, "rel": abs(d + (R - 1.0) * fx1 * e) / max(abs(d), 1e-30)}
    for e, d in right]
out["V2_leftward"] = [
    {"eps": e, "dD": d, "pred": +(R - 1.0) * fx1 * e, "rel": abs(d - (R - 1.0) * fx1 * e) / max(abs(d), 1e-30)}
    for e, d in left]

# V3: d lambda_k / deps = lambda_k (c_+ - c_-) u_k(x_j)^2  at x1 (c_-=1, c_+=R)
def lamk_jump_at_x1(delta, k):
    breaks = [0.0, x1 + delta, x2, 1.0]
    values = [1.0, R, 1.0]
    return eigenvalues(breaks, values, k_max=2)[k - 1]

u1x1 = np.interp(x1, xg, us[0]); u2x1 = np.interp(x1, xg, us[1])
V3 = {}
for k in (1, 2):
    num = (lamk_jump_at_x1(1e-5, k) - lamk_jump_at_x1(-1e-5, k)) / 2e-5
    ux = np.interp(x1, xg, us[k - 1])
    pred = lams[k - 1] * (R - 1.0) * ux ** 2
    V3[f"lam{k}"] = {"numeric": num, "predicted": pred, "absdiff": abs(num - pred)}
out["V3_lambda_derivatives"] = V3

# --- V4: symmetric barrier family [1,R,1] on (u,1-u), dD/du = -2(R-1) f(u) ---
def D_sym(u):
    breaks = [0.0, u, 1.0 - u, 1.0]
    values = [1.0, R, 1.0]
    return D_of(breaks, values)

def f_sym(u):
    breaks = [0.0, u, 1.0 - u, 1.0]
    values = [1.0, R, 1.0]
    lams = eigenvalues(breaks, values, k_max=2)
    us, up, xg = eigenfuncs(breaks, values, lams)
    f, _, _ = f_of(breaks, values, lams, us, up)
    return np.interp(u, xg, f)

V4 = []
for u in (0.2, 0.3, 0.4, 0.45148546584, 0.49):
    num = (D_sym(u + 1e-5) - D_sym(u - 1e-5)) / 2e-5
    pred = -2.0 * (R - 1.0) * f_sym(u)
    V4.append({"u": u, "dDdu_num": num, "pred": pred, "absdiff": abs(num - pred)})
out["V4_symmetric_family"] = V4

# --- V5: stationarity at u* ---
u_star = 0.45148546584
right_u = (D_sym(u_star + 1e-5) - D_sym(u_star)) / 1e-5
left_u = (D_sym(u_star) - D_sym(u_star - 1e-5)) / 1e-5
out["V5_stationarity_u*"] = {"u*": u_star, "right": right_u, "left": left_u,
                             "f(u*)": f_sym(u_star)}

print(json.dumps(out, indent=1))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_fh_sign_out.json"), "w") as fp:
    json.dump(out, fp, indent=1)

