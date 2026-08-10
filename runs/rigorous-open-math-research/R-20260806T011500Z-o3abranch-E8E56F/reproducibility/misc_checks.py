# -*- coding: utf-8 -*-
"""misc_checks.py: (1) h(b0) at large R; (2) fine peak scan R=1e4; (3) 2-param good-root scan R=1e4."""
import sys, numpy as np, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from agentB_lib import config, f_at
from scipy.optimize import brentq

def R1(a, b, R):
    return float(np.ravel(f_at(a, b, R, a, config(a, b, R)))[0])
def R2(a, b, R):
    return float(np.ravel(f_at(a, b, R, b, config(a, b, R)))[0])
def v_at(a, b, R, x):
    from agentB_lib import y_L
    s = config(a, b, R)[0]
    y = y_L(a, b, R, s, np.array([x]))[:, 0]
    return float(y[1]/y[0])

def branch(a, R, which):
    f = (lambda b: R1(a, b, R)) if which=='g1' else (lambda b: R2(a, b, R))
    bb = np.linspace(a+1e-5, 1-1e-5, 40)
    vals = [f(b) for b in bb]
    for i in range(len(bb)-1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1] < 0:
            try:
                b0 = brentq(f, bb[i], bb[i+1], xtol=1e-12)
            except Exception:
                continue
            c = v_at(a, b0, R, a) if which=='g1' else v_at(a, b0, R, b0)
            if (which=='g1' and c > 0) or (which=='g2' and c < 0):
                return b0
    return None

# (1) h(b0) at large R
b0v = np.arccos(-0.25)/np.pi
print("=== h(b0) = g1(b0) - b0 ===")
for R in [1e4, 1e5, 1e6, 1e7]:
    g1 = branch(b0v-1e-6, R, 'g1')
    if g1:
        print(f"  R={R:.0e}: g1(b0)={g1:.8f} h(b0)={g1-b0v:+.6e} h*sqrt(R)={ (g1-b0v)*np.sqrt(R):.4f}")
    else:
        print(f"  R={R:.0e}: branch1 not found at b0")

# (2) fine peak scan at R=1e4: locate a_peak and h' sign changes
print("=== fine scan R=1e4 near peak ===")
R = 1e4
aa = np.linspace(0.545, 0.582, 38)
g1s = [branch(a, R, 'g1') for a in aa]
g2s = [branch(a, R, 'g2') for a in aa]
hs = np.array([g1-g2 if g1 and g2 else np.nan for g1, g2 in zip(g1s, g2s)])
ok = np.isfinite(hs)
imax = int(np.nanargmax(hs))
print(f"  h_peak={hs[imax]:+.6e} at a={aa[imax]:.5f}")
for i in range(1, len(aa)-1):
    if ok[i-1] and ok[i+1]:
        hp = (hs[i+1]-hs[i-1])/(aa[i+1]-aa[i-1])
        if i in (imax-2, imax-1, imax, imax+1, imax+2) or (abs(hp) < 1e-3 and hp < 0):
            print(f"    a={aa[i]:.5f}: h={hs[i]:+.3e} h'={hp:+.3e}")

json.dump(dict(hb0={str(int(R)): branch(b0v-1e-6, R, 'g1') for R in [1e4,1e5,1e6,1e7]}), open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility\h_b0.json","w"))
print("saved h_b0.json")
