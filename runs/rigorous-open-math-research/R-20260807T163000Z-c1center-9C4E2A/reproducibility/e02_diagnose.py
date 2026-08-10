# -*- coding: utf-8 -*-
"""e02_diagnose.py: R=100 (0.812,0.847) artifact diagnosis + sign conjecture probe."""
import numpy as np, sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
from c1_lib import cfg, y_at, sec

def v(x, a, b, R):
    s1, s2, _, _ = cfg(a, b, R)
    return y_at(s2, a, b, R, x)/y_at(s1, a, b, R, x)

def qval(a, b, R):
    s1, s2, n1, n2 = cfg(a, b, R)
    return np.sqrt((s1**2/n1)/(s2**2/n2))

# 1. diagnose (0.812, 0.847, R=100)
for (a,b,R) in [(0.812,0.847,100.0), (0.515,0.535,1e4)]:
    s1, s2, n1, n2 = cfg(a, b, R)
    q = qval(a,b,R)
    print(f"--- config a={a} b={b} R={R}")
    print(f"  s1={s1:.6f} s2={s2:.6f} q={q:.6f}")
    xs = np.linspace(0.001, 0.999, 401)
    vs = np.array([v(x,a,b,R) for x in xs])
    print(f"  v(0+)~{vs[0]:.4f} v(1-)~{vs[-1]:.4f} min={vs.min():.4f} max={vs.max():.4f}")
    print(f"  v crosses +q: {(np.signbit(vs-q)[1:] != np.signbit(vs-q)[:-1]).sum()} times")
    print(f"  v crosses -q: {(np.signbit(vs+q)[1:] != np.signbit(vs+q)[:-1]).sum()} times")
    # eigenvalue check: is s2 really the 2nd root?
    ss = np.linspace(1e-9, 2*np.pi+1e-3, 6001)
    M = sec(ss, a, b, R)
    ch = np.nonzero(np.signbit(M[1:]) != np.signbit(M[:-1]))[0]
    roots = [0.5*(ss[i]+ss[i+1]) for i in ch[:6]]
    print(f"  first secular roots: {[round(float(r),6) for r in roots]}")