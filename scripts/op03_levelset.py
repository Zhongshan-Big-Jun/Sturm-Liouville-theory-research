# -*- coding: utf-8 -*-
"""Check structure of {n^2 sin^2(n pi x) > (n+1)^2 sin^2((n+1) pi x)} for rho=1 (n=1..4)."""
import numpy as np
for n in range(1, 5):
    x = np.linspace(1e-6, 1-1e-6, 20001)
    f = n**2*np.sin(n*np.pi*x)**2 - (n+1)**2*np.sin((n+1)*np.pi*x)**2
    pos = f > 0
    # find intervals where pos=True
    edges = np.nonzero(pos[1:] != pos[:-1])[0] + 1
    bounds = [0.0]
    for e in edges:
        bounds.append(x[e])
    bounds.append(1.0)
    comps = []
    for i in range(len(bounds)-1):
        if pos[(np.abs(x - 0.5*(bounds[i]+bounds[i+1]))).argmin()]:
            comps.append((bounds[i], bounds[i+1]))
    print(f"n={n}: {len(comps)} components: {[f'({a:.4f},{b:.4f})' for a,b in comps]}")
