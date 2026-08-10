# -*- coding: utf-8 -*-
"""tail bound for phi' on (0.999, 1): verify phi'/eps^2 >= C_tail with explicit constants.
phi'*60pi = P + T, P = 2 sin^2(pi e)(2 m cos^2(pi e) + n), T = -2 s15 pi e (4 cos(2pi e)-1) sin(2pi e),
m = 56 pi a0 - 6 s15, n = 2 pi a0 + 3 s15, e = 1-b."""
import mpmath as mp
import numpy as np
mp.mp.prec = 120
pi = mp.pi; s15 = mp.sqrt(15); a0 = mp.acos(mp.mpf(1)/4)/pi
m = 56*pi*a0 - 6*s15; n = 2*pi*a0 + 3*s15
d1 = (pi/1000)**2/6; d2 = (pi/1000)**2/2
# rigorous C_tail lower bound via interval arithmetic
iv = mp.iv
iv.prec = 200
piI = iv.pi; s15I = iv.sqrt(15)
a0I = iv.atan2(s15I/4, iv.mpf(1)/4)/piI
mI = 56*piI*a0I - 6*s15I; nI = 2*piI*a0I + 3*s15I
d1I = iv.mpf((mp.pi/1000)**2/6); d2I = iv.mpf((mp.pi/1000)**2/2)
Plb = 2*piI**2*(1-d1I)**2*(2*mI*(1-d2I)**2 + nI)
Tub = 12*s15I*piI**2
Ctail = (Plb - Tub)/(60*piI)
print("m =", mp.nstr(m, 12), " n =", mp.nstr(n, 12))
print("C_tail interval =", mp.nstr(Ctail, 15))
Ctail_lb = float(mp.mpf(Ctail.a))
print("C_tail lower bound =", mp.nstr(Ctail.a, 15))
# numeric check: phi'/eps^2 vs C_tail on (0, 0.001]
def dphi_eps(e):
    b = 1 - e
    u = np.cos(2*np.pi*b); v = np.sin(2*np.pi*b)
    N = (56*np.pi*a0 - 6*s15)*u**2 + (2*np.pi*a0 + 3*s15)*u + (3*s15 - 58*np.pi*a0) + 2*s15*np.pi*(1-b)*(1-4*u)*v
    return -N/(60*np.pi)
es = np.logspace(-7, -3, 200)
vals = np.array([dphi_eps(e)/e**2 for e in es])
print("min phi'/eps^2 on (1e-7, 1e-3]: %.6f  vs C_tail_lb %.6f : %s" % (vals.min(), Ctail_lb, vals.min() > Ctail_lb))
# also show phi'(b) itself near 0.999
print("phi'(0.9991) =", dphi_eps(0.0009))
print("C_tail*eps^2 at eps=0.001 =", Ctail_lb*1e-6)
