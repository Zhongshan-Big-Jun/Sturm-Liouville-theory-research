# -*- coding: utf-8 -*-
"""explore gap n=1 strict proof ingredients: V0>1, z(u), h(u)=z(u)-u, endpoints, 2-block bounds."""
import numpy as np
from scipy.optimize import brentq
from gap_lib import lams_fast, y_at, norm2

def blocks_of(mode, R, u):
    b = 1-2*u
    return [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]

def data(mode, R, u, npts=60000):
    bl = blocks_of(mode, R, u)
    s = lams_fast(bl, 2, npts=npts)
    lam = s**2
    n1 = norm2(bl, s[0]); n2 = norm2(bl, s[1])
    # u_i'(0) = 1/sqrt(norm) with y'(0)=1 normalization
    up1 = 1.0/np.sqrt(n1); up2 = 1.0/np.sqrt(n2)
    A = up2/up1
    V0 = np.sqrt(lam[1]/lam[0])*A
    return lam, A, V0, bl, s

def f_sym(mode, R, u, npts=60000):
    lam, A, V0, bl, s = data(mode, R, u, npts)
    u1 = y_at(bl, s[0], np.array([u]))[0]/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u]))[0]/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2, lam

def f_of_x(mode, R, u, xs, npts=60000):
    lam, A, V0, bl, s = data(mode, R, u, npts)
    xs = np.atleast_1d(np.asarray(xs,float))
    u1 = y_at(bl, s[0], xs)/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], xs)/np.sqrt(norm2(bl, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def z_of(mode, R, u, npts=60000):
    lo, hi = 1e-8, 0.5
    for _ in range(55):
        mid = 0.5*(lo+hi)
        fm = f_of_x(mode, R, u, [mid], npts)[0]
        if fm > 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

print("===== Part 1: V0(u) > 1 ?  (V0 = sqrt(lam2/lam1)*u2'(0)/u1'(0);  f(0+)<0 iff V0>1) =====")
for R in (1.5, 2.0, 4.0, 10.0, 100.0, 1000.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.005, 0.495, 12)
        V0s = []
        for u in us:
            lam,A,V0,_,_ = data(mode, R, float(u))
            V0s.append(V0)
        V0s = np.array(V0s)
        print(f"R={R:6.0f} {mode}: V0 min={V0s.min():.6f} max={V0s.max():.6f}  (need >1)")
print()
print("===== Part 2: h(u)=z(u)-u single crossing? =====")
for R in (1.5, 4.0, 100.0, 1000.0):
    for mode in ("SUP","INF"):
        us = np.linspace(0.005, 0.495, 40)
        prev = None; crosses = []
        for u in us:
            z = z_of(mode, R, float(u))
            d = z - u
            if prev is not None and prev[1]*d < 0:
                crosses.append((prev[0], u, prev[1], d))
            prev = (u, d)
        print(f"R={R:6.0f} {mode}: sign changes of h = {len(crosses)}", crosses if crosses else "")
print()
print("===== Part 3: endpoints of D_sym =====")
for R in (4.0,):
    for mode in ("SUP","INF"):
        vals = []
        for u in (1e-4, 0.49, 0.499):
            lam,_,_,_,_ = data(mode, R, u)
            vals.append((u, lam[1]-lam[0]))
        print(f"R={R} {mode}: D(1e-4)={vals[0][1]:.6f} D(0.49)={vals[1][1]:.6f} D(0.499)={vals[2][1]:.6f}")
        print(f"     3pi^2={3*np.pi**2:.6f} 3pi^2/R={3*np.pi**2/R:.6f}")
print()
print("===== Part 4: 2-block D(t) range =====")
R=4.0
t3=3*np.pi**2
ts = np.linspace(0.0005,0.9995,600)
d1 = [lams_fast([(t,1.0),(1-t,R)],2)[1]**2-lams_fast([(t,1.0),(1-t,R)],2)[0]**2 for t in ts]
d2 = [lams_fast([(t,R),(1-t,1.0)],2)[1]**2-lams_fast([(t,R),(1-t,1.0)],2)[0]**2 for t in ts]
d1=np.array(d1); d2=np.array(d2)
print(f"[1,R]_t: D in [{d1.min():.6f},{d1.max():.6f}];  [R,1]_t: D in [{d2.min():.6f},{d2.max():.6f}]")
print(f"3pi^2/R={t3/R:.6f} 3pi^2={t3:.6f}; SUP D*={32.6139836177:.6f} INF D*={6.7844823391:.6f}")
