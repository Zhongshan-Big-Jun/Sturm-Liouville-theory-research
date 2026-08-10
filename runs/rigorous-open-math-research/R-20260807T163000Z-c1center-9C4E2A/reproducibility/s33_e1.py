# -*- coding: utf-8 -*-
"""s33_e1.py - reproduce the E1-inf constants and the generic S(a) table.
Outputs s33_e1.json.  Numerical evidence only (no proof role)."""
import numpy as np, json, os
from scipy.optimize import brentq
pi = np.pi
HERE = os.path.dirname(os.path.abspath(__file__))

def u_L(a):
    return brentq(lambda u: np.sin(u)/u - np.sqrt(2*a), 1e-9, pi/2 - 1e-9)
def x_R(a):
    return brentq(lambda x: x**2/np.tan(x)**2 - 1/(2*(1-a)), pi/2 + 1e-9, pi - 1e-9)
def W_L(a): return u_L(a)*(1-a)/pi
def W_R(a): return a*x_R(a)/pi
def Wp_L(a):
    u = u_L(a)
    return u/pi*((1-a)/(np.sqrt(2*a)*(np.cos(u)-np.sqrt(2*a))) - 1)
def Wp_R(a):
    x = x_R(a); cot = 1/np.tan(x)
    return x/pi*(1 + a*cot/(2*(1-a)*(cot - x/np.sin(x)**2)))

a0 = float(np.arccos(0.25)/pi)
u = u_L(a0); x = x_R(1-a0)
out = dict(a0=a0, u=u, x=x, x_gt_u=bool(x>u),
           W_L_a0=W_L(a0), W_R_1ma0=W_R(1-a0), gap=W_R(1-a0)-W_L(a0),
           Y1_u=-u/np.tan(u), u_over_sinu=u/np.sin(u), Y1_x=-x/np.tan(x))
Srows = []
for a in [a0+1e-6, 0.43, 0.45, 0.47, 0.48, 0.49]:
    Srows.append(dict(a=a, WpL=Wp_L(a), WpR_at_1ma=Wp_R(1-a), S=Wp_L(a)+Wp_R(1-a)))
out["S_table"] = Srows
with open(os.path.join(HERE, "s33_e1.json"), "w") as f:
    json.dump(out, f, indent=1)
print("u=%.7f x=%.7f gap=%.7f" % (u, x, out["gap"]))
for r in Srows: print("a=%.4f S=%.5f" % (r["a"], r["S"]))
