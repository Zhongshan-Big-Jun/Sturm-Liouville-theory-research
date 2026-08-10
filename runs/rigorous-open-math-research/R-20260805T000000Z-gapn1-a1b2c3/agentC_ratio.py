# -*- coding: utf-8 -*-
"""Check lambda2/lambda1 <= 4 for 2-block strings (all t, R)."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lams_direct(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1,c2))*(k+2)+10
    s = np.linspace(1e-9, smax, 60000)
    M = M01_2block(t, c1, c2, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0][:k]
    roots = [brentq(lambda x: M01_2block(t, c1, c2, x), s[idx[j]], s[idx[j]+1]) for j in range(k)]
    return np.array(roots)

worst = 0.0; worst_arg = None
for R in [1.05, 1.2, 1.5, 2.0, 4.0, 10.0, 100.0, 1e4]:
    for t in np.linspace(1e-4, 1-1e-4, 200):
        for hl in (False, True):
            c1, c2 = (R,1.0) if hl else (1.0,R)
            s = lams_direct(t, c1, c2)
            r = s[1]**2/s[0]**2
            if r > worst: worst, worst_arg = r, (R,t,hl,s[0]**2,s[1]**2)
print(f"max lambda2/lambda1 over grid = {worst:.10f} at R={worst_arg[0]}, t={worst_arg[1]:.6f}, HL={worst_arg[2]}, lam1={worst_arg[3]:.6f}, lam2={worst_arg[4]:.6f}")
