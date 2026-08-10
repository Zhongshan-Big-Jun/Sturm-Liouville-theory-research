# -*- coding: utf-8 -*-
"""Direct check at R=4, a=b0, for b in {0.60086, 0.84685}."""
import numpy as np
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
a0 = np.arccos(0.25)/np.pi; b0 = 1-a0
R = 4.0
for b in [0.60086, 0.84685, 0.5806, 0.59, 0.65, 0.7, 0.75, 0.8, 0.9]:
    try:
        R1, R2 = residual_both(b0, b, R)
        xm, xp = band(b0, b, R)
        s1, s2 = cfg(b0, b, R)
        print(f"b={b:.5f}: R1={R1:+.6e} R2={R2:+.6e} x-={xm:.6f} x+={xp:.6f} s1={s1:.5f} s2={s2:.5f}  (a=x-? {abs(b0-xm)<3e-4}, b=x+? {abs(b-xp)<3e-4})")
    except Exception as e:
        print(f"b={b:.5f}: ERROR {e}")
# also the fp good root
a_f = 0.451485
R1, R2 = residual_both(a_f, 1-a_f, R)
print("fp (0.451485, 0.548515): R1,R2 =", R1, R2)