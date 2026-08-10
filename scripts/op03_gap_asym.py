# -*- coding: utf-8 -*-
"""#3: asymmetric configs vs symmetric self-consistent values (n=1)."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_fixed import lams_precise

R = 4.0
def gap_asym(p, sup):
    uL, uR = np.abs(p)
    uL = min(uL, 0.98); uR = min(uR, 0.98)
    if uL + uR > 0.98: 
        uL, uR = uL/(uL+uR)*0.49, uR/(uL+uR)*0.49
    blocks = [(uL, R if not sup else 1.0), (1-uL-uR, 1.0 if not sup else R), (uR, R if not sup else 1.0)]
    lam = lams_precise(blocks, 3)**2
    return lam[1]-lam[0]

rng = np.random.default_rng(5)
for sup, ref in [(True, 32.61398362), (False, 6.78448234)]:
    best = (1e9, None)
    for t in range(20):
        p0 = rng.uniform(0.1, 0.48, 2)
        r = minimize(lambda p: -gap_asym(p, sup) if sup else gap_asym(p, sup), p0,
                     method='Nelder-Mead', options={'maxiter':400, 'xatol':1e-9, 'fatol':1e-11})
        val = -r.fun if sup else r.fun
        if val < best[0]: best = (val, np.abs(r.x))
    print(f"{'SUP' if sup else 'INF'}: asymmetric best={best[0]:.8f} (symmetric ref={ref:.8f}) params={best[1]}")
