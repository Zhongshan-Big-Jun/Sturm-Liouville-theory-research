# -*- coding: utf-8 -*-
"""Direct check of dlambda/dt sign for 2-block (light left, heavy right)."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    B = np.sin(w1*t)/q1; Dm = np.cos(w1*t)
    E = np.cos(w2*(1-t)); F = np.sin(w2*(1-t))/q2
    return E*B + F*Dm

def lams_2block(t, c1, c2, k=2):
    smax = np.pi*np.sqrt(max(c1, c2))*(k+2)+10
    s = np.linspace(1e-9, smax, 120000)
    d = np.array([M01_2block(t, c1, c2, x) for x in s])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    roots = []
    for i in idx[:k]:
        roots.append(brentq(lambda x: M01_2block(t, c1, c2, x), s[i], s[i+1]))
    return np.array(roots)

R = 4.0
t = 0.999
h = 1e-6
for tk in [t, t+h, t+2*h, t+3*h]:
    s = lams_2block(tk, 1.0, R)
    print(f"t={tk:.9f}: lam1={s[0]**2:.12f} lam2={s[1]**2:.12f} D={s[1]**2-s[0]**2:.12f}")
# also heavy-left orientation
print("--- heavy LEFT (R on [0,t], 1 on (t,1]) ---")
t = 0.001
for tk in [t, t+h, t+2*h, t+3*h]:
    s = lams_2block(tk, R, 1.0)
    print(f"t={tk:.9f}: lam1={s[0]**2:.12f} lam2={s[1]**2:.12f} D={s[1]**2-s[0]**2:.12f}")
