# -*- coding: utf-8 -*-
"""Check G(mu,c) decreasing in mu for c>=1. G = (mu+c)^2/(3mu^2)*[2mu^2/(1+mu c)^2 + mu/((1+mu c)(1+c))]."""
import numpy as np

def G(mu, c):
    A = 1 + mu*c
    return (mu+c)**2/(3*mu**2)*(2*mu**2/A**2 + mu/(A*(1+c)))

worst = 1.0
for c in np.linspace(1.0, 100.0, 60):
    mus = np.linspace(1.0001, 100.0, 200)
    vals = np.array([G(m, c) for m in mus])
    dec = np.all(np.diff(vals) < 0)
    if not dec:
        print(f"NOT decreasing: c={c}")
    worst = min(worst, vals[-1])
print(f"G decreasing in mu for all tested c: check above; G(mu->inf,c) min = {worst:.6f}")
print("G at mu=1 (any c) =", G(1.0, 5.0))
print("G(1.001,1) =", G(1.001, 1.0), " G(1.001,10) =", G(1.001, 10.0))
