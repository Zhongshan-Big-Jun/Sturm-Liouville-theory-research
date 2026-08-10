# -*- coding: utf-8 -*-
import numpy as np, time
src = open(r"F:\LaTeX\BVE research\scripts\explore_e1.py", encoding="utf-8").read()
exec(src.split('a0 = np.arccos')[0])
t0=time.time()
for _ in range(10):
    roots2(0.45, 0.58, 4.0)
print("10x roots2:", time.time()-t0)
t0=time.time()
for _ in range(10):
    residual_both(0.45, 0.58, 4.0)
print("10x residual_both:", time.time()-t0)
t0=time.time()
for _ in range(3):
    band(0.45, 0.58, 4.0)
print("3x band:", time.time()-t0)