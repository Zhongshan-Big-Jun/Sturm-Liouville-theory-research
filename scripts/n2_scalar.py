# -*- coding: utf-8 -*-
"""Verify scalar identity tan(c x_k) = -alpha tan(x_k) and study sharp bounds."""
import numpy as np
from gap_lib import lams_fast

def check(R, t):
    alpha = np.sqrt(R)
    c = alpha*(1-t)/t
    s = lams_fast([(t,1.0),(1-t,R)], 2, npts=2500)
    x1, x2 = s[0]*t, s[1]*t
    e1 = np.tan(c*x1) + alpha*np.tan(x1)
    e2 = np.tan(c*x2) + alpha*np.tan(x2)
    return x1, x2, e1, e2, c, alpha

print("verify tan(c x_k) = -alpha tan(x_k):")
for R in (4.0, 2.0, 100.0):
    for t in (0.3, 0.5, 0.7, 0.9):
        x1, x2, e1, e2, c, a = check(R, t)
        print(f"R={R:6.1f} t={t:.2f} c={c:7.4f}: x1={x1:.6f} x2={x2:.6f} |res1|={abs(e1):.2e} |res2|={abs(e2):.2e}")

# Now: study upper bound.  Want x2^2-x1^2 <= 3 pi^2 alpha^2/(alpha+c)^2.
print()
print("upper bound analysis: deficit of (x2^2-x1^2) vs 3 pi^2 a^2/(a+c)^2")
print("and the two factors (x2-x1) vs pi a/(a+c), (x2+x1) vs 3 pi a/(a+c)")
worst = (1e9, None)
for R in (1.1, 1.5, 2.0, 4.0, 10.0, 100.0, 1000.0):
    a = np.sqrt(R)
    for t in np.linspace(0.005, 0.995, 200):
        c = a*(1-t)/t
        s = lams_fast([(t,1.0),(1-t,R)], 2, npts=1200)
        x1, x2 = s[0]*t, s[1]*t
        D = (a+c)**2/a**2*(x2**2-x1**2)
        err = D - 3*np.pi**2
        if err > worst[0]:
            worst = (err, (R, t, c, D))
print("max excess of D over 3 pi^2:", worst)
print()
print("factor check: ratios (x2-x1)*a/(pi*(a+c))  and (x2+x1)*a/(3*pi*(a+c)) must be <=1")
mx1 = mx2 = 0
for R in (1.5, 2.0, 4.0, 10.0, 100.0):
    a = np.sqrt(R)
    for t in np.linspace(0.005, 0.995, 100):
        c = a*(1-t)/t
        s = lams_fast([(t,1.0),(1-t,R)], 2, npts=1000)
        x1, x2 = s[0]*t, s[1]*t
        r1 = (x2-x1)*a/(np.pi*(a+c))
        r2 = (x2+x1)*a/(3*np.pi*(a+c))
        mx1 = max(mx1, r1); mx2 = max(mx2, r2)
print(f"max (x2-x1)*a/(pi(a+c)) = {mx1:.6f};  max (x2+x1)*a/(3pi(a+c)) = {mx2:.6f}")
