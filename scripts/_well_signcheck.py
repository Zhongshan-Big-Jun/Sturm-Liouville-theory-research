# -*- coding: utf-8 -*-
"""Sign-consistency check at R=1.5 good root (E3)."""
import numpy as np
import sys; sys.path.insert(0, ".")
from _well_rigid_verify import eigs_well, y_well
R = 1.5; m = np.sqrt(R)
a, b = 0.40879841, 0.59120159
lam1, lam2 = eigs_well(a, b, R)
s1 = np.sqrt(lam1); s2 = np.sqrt(lam2); tau = s2/s1
A = m*s1*a; B = m*s1*(1-b)
print(f"lam1={lam1:.8f} lam2={lam2:.8f} s1={s1:.6f} s2={s2:.6f} tau={tau:.6f}")
print(f"y2(a)={y_well(a,b,R,s2,a):+.8f} (must be >0)")
print(f"y2(b)={y_well(a,b,R,s2,b):+.8f} (must be <0)")
# locate the zero of y2 in (a,b)
xs = np.linspace(a, b, 4001)
ys = np.array([y_well(a,b,R,s2,x) for x in xs])
i = np.nonzero(np.signbit(ys[1:]) != np.signbit(ys[:-1]))[0]
print(f"y2 zero in (a,b): x ~ {0.5*(xs[i[0]]+xs[i[0]+1]):.6f} (a={a:.6f}, b={b:.6f})")
print(f"tau*A = {tau*A:.6f} < pi = {np.pi:.6f}; tau*B = {tau*B:.6f} < pi")
print(f"y2 on left region at x=pi/(m*s2) = {np.pi/(m*s2):.6f} vs a={a:.6f} (would be zero before z if <= a)")
