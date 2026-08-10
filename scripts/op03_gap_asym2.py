# -*- coding: utf-8 -*-
"""#3: asymmetric configs vs symmetric values (n=1), reduced trials."""
import numpy as np
from scipy.optimize import minimize
from op03_gap_fixed import lams_precise

R = 4.0
def gap_asym(p, sup):
    uL, uR = np.abs(p)
    if uL + uR > 0.98:
        uL, uR = uL/(uL+uR)*0.49, uR/(uL+uR)*0.49
    a = R if not sup else 1.0
    b = 1.0 if not sup else R
    blocks = [(uL, a), (1-uL-uR, b), (uR, a)]
    lam = lams_precise(blocks, 3)**2
    return lam[1]-lam[0]

rng = np.random.default_rng(5)
for sup, ref in [(True, 32.61398362), (False, 6.78448234)]:
    best = (1e9, None)
    for t in range(8):
        p0 = rng.uniform(0.2, 0.46, 2)
        fn = (lambda p: -gap_asym(p, sup)) if sup else (lambda p: gap_asym(p, sup))
        r = minimize(fn, p0, method='Nelder-Mead', options={'maxiter':200, 'xatol':1e-8, 'fatol':1e-10})
        val = -r.fun if sup else r.fun
        if val < best[0]: best = (val, np.abs(r.x))
    print(f"{'SUP' if sup else 'INF'}: asymmetric best={best[0]:.8f} (ref={ref:.8f}) uL,uR={best[1]}")
