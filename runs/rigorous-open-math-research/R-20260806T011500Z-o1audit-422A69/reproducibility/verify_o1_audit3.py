# verify_o1_audit3.py - corrected O1f bang-bang direction (EVIDENCE ONLY)
import sys, math, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o1audit-422A69\reproducibility')
import numpy as np
from verify_o1_audit import D_of, eigenfunction
R = 4.0
# original: barrier (0.4,0.6) value 4, rest 1
blocks0 = [(0.4, 1.0), (0.2, R), (0.4, 1.0)]
D0, l1, l2 = D_of(blocks0, R)
ev1, _ = eigenfunction(blocks0, l1)
ev2, _ = eigenfunction(blocks0, l2)
xs = np.linspace(0.001, 0.999, 8001)
f = np.array([l1*ev1(x)[0]**2 - l2*ev2(x)[0]**2 for x in xs])
# {f>0} should be a single interval; find its endpoints by sign scan
sgn = np.sign(f)
z = np.where(np.diff(sgn) != 0)[0]
print('f zeros at:', xs[z], ' f(0.5) =', f[np.argmin(np.abs(xs-0.5))])
xp = 0.5                       # inside barrier, f>0
xm = float(xs[z[1]] + 0.02)    # right of the positive interval, f<0
print('xp', xp, ' f(xp) =', float(f[np.argmin(np.abs(xs-xp))]))
print('xm', xm, ' f(xm) =', float(f[np.argmin(np.abs(xs-xm))]))
w = 0.01

def raise_rho(x0):
    # x0 inside the right 1-block (0.6,1): split it
    return [(0.4, 1.0), (0.2, R), (x0-0.6, 1.0), (w, 1.0+1.0), (1-x0-w, 1.0)]

def raise_rho_in_barrier(x0):
    # x0 inside barrier (0.4,0.6): split barrier block
    return [(0.4, 1.0), (x0-0.4, R), (w, R+1.0), (0.6-x0-w, R), (0.4, 1.0)]

res = {}
for label, x0, maker in [('inc_where_f_pos', xp, raise_rho_in_barrier),
                         ('inc_where_f_neg', xm, raise_rho)]:
    Dp, _, _ = D_of(maker(x0), R)
    f0 = float(f[np.argmin(np.abs(xs-x0))])
    res[label] = dict(x0=x0, f_at_x0=f0, D0=D0, D_pert=Dp,
                      dD = Dp - D0,
                      pred_w_f = w*f0,
                      dD_positive = bool(Dp - D0 > 0))
print(json.dumps(res, indent=1))
