# -*- coding: utf-8 -*-
"""Regime C (0<c<=1/3): check bracketed lower bound for (star) inequality.
Want: (mu+c)^2 [4pi e2lo - 2pi e1hi - e2hi^2 + e1lo^2] > 3pi^2(2mu c + c^2)
with e1 in [arctan(tan(c pi/2)/mu), arctan(tan(c pi)/mu)]
     e2 in [e2lo, e2hi], e2lo = arctan(tan(3c pi/2)/mu) if 3c pi/2 <= pi/2 else 2pi - pi/(2c)
                            (use 0 if tan(3cpi/2)<0? 3cpi/2 < pi/2 for c<1/3 always, ok)
     e2hi = arctan(tan(2c pi)/mu) if 2c pi <= pi/2 else pi/2
"""
import numpy as np

def arct(t):
    return np.arctan(t)

for mu in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0]:
    worst_margin = 1.0; worst_c = None
    ok = True
    for c in np.linspace(1e-6, 1/3, 2000):
        e1lo = arct(np.tan(c*np.pi/2)/mu)
        e1hi = arct(np.tan(c*np.pi)/mu)
        if 2*c*np.pi <= np.pi/2:
            e2hi = arct(np.tan(2*c*np.pi)/mu)
        else:
            e2hi = np.pi/2
        if 3*c*np.pi/2 <= np.pi/2:
            e2lo = arct(np.tan(3*c*np.pi/2)/mu)
        else:
            e2lo = 0.0  # fallback
        LHS = (mu+c)**2*(4*np.pi*e2lo - 2*np.pi*e1hi - e2hi**2 + e1lo**2)
        RHS = 3*np.pi**2*(2*mu*c + c*c)
        m = LHS - RHS
        if m < worst_margin: worst_margin, worst_c = m, c
        if m <= 0: ok = False
    print(f"mu={mu:6.3f}: bracketed lower bound works? {ok}  worst margin = {worst_margin:+.6e} at c={worst_c:.6f}")
