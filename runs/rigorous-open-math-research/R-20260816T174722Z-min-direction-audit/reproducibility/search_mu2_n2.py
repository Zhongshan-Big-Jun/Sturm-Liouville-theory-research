# -*- coding: utf-8 -*-
"""Coarse numeric scan for n=2, mu=2 roots (EVIDENCE only)."""
import numpy as np, sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260816T174722Z-min-direction-audit\reproducibility')
from search_mu2_n3 import integrate

for R in [1.5, 2.0, 4.0, 10.0]:
    print('R=', R)
    for q in np.linspace(1.01, 10.0, 20):
        res = integrate(q, R, 2.0, 2, tmax=40)
        if res is None:
            continue
        TU, TV, IU, IV = res
        A = TU-TV; B = IU-IV
        print(f'  q={q:.3f}: A={A:+.4f} B={B:+.4f}')
