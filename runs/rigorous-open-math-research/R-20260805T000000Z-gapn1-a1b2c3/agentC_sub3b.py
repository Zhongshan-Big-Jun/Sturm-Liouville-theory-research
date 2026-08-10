# -*- coding: utf-8 -*-
"""Subclaim 3: hunt for asymmetric critical points with random seeds."""
import numpy as np
from scipy.optimize import brentq, root
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3")
exec(open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3\agentC_sub3.py").read().split('print("Solve f(a)=f(b)=0')[0])

rng = np.random.default_rng(42)
for R in [1.5, 2.0, 4.0, 10.0]:
    found = []
    for trial in range(40):
        a0 = rng.uniform(0.02, 0.48)
        b0 = rng.uniform(a0+0.03, 0.98)
        try:
            sol = root(lambda v: [f_at(v[0], v[1], R, v[0]), f_at(v[0], v[1], R, v[1])], [a0, b0], method='hybr')
        except Exception:
            continue
        if sol.success:
            a, b = sol.x
            resid = abs(sol.fun[0]) + abs(sol.fun[1])
            if resid < 1e-8:
                # check sign consistency: {f>0} = (a,b) single interval?
                xs = np.linspace(0.001, 0.999, 400)
                fv = np.array([f_at(a, b, R, x) for x in xs])
                pos = fv > 0
                # sign pattern: -,+,-
                pat = ''.join('+' if p else '-' for p in pos)
                # collapse
                collapsed = pat[0]
                for c in pat[1:]:
                    if c != collapsed[-1]: collapsed += c
                found.append((a, b, resid, collapsed))
    # dedupe
    print(f"R={R}: {len(found)} critical points found from 40 random seeds")
    for a, b, r, pat in found:
        print(f"   a={a:.9f} b={b:.9f} a+b={a+b:.12f} resid={r:.1e} sign-pattern={pat}")
