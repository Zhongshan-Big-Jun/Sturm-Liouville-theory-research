# -*- coding: utf-8 -*-
"""Verify the simplified secular equation sin(w T+) = mu sin(w T-) for 3-block [1,R,1].
Also test the symmetric case reduces to the known balanced-phase form."""
import numpy as np
from gap_lib import lams_fast

def sec_roots(a, b, R, k=6):
    s = np.sqrt(R); mu = (s-1)/(s+1)
    Tp = (1-b) + s*(b-a) + a
    Tm = (1-b) + s*(b-a) - a
    # find roots of F(w) = sin(w Tp) - mu sin(w Tm), w>0
    w = np.linspace(1e-6, np.pi*3, 20000)
    F = np.sin(w*Tp) - mu*np.sin(w*Tm)
    signs = np.signbit(F[1:]) != np.signbit(F[:-1])
    idx = np.nonzero(signs)[0]
    roots = []
    for i in idx[:k]:
        lo, hi = w[i], w[i+1]
        for _ in range(60):
            mid = 0.5*(lo+hi)
            if (np.sin(mid*Tp)-mu*np.sin(mid*Tm))*(np.sin(lo*Tp)-mu*np.sin(lo*Tm)) <= 0: hi = mid
            else: lo = mid
        roots.append(0.5*(lo+hi))
    return np.array(roots[:k])

for (a,b,R) in [(0.451485,0.548515,4.0),(0.382598,0.617402,4.0),(0.3,0.7,4.0),(0.2,0.6,2.0),(0.1,0.35,4.0)]:
    lam_tm = lams_fast([(a,1.0),(b-a,R),(1-b,1.0)], 3)**2
    lam_sec = sec_roots(a,b,R,3)**2
    print(f"(a,b,R)=({a},{b},{R}): TM={np.round(lam_tm,6)} sec={np.round(lam_sec,6)} "
          f"maxdiff={np.max(np.abs(lam_tm-lam_sec)):.2e}")

# symmetric case: a = u, b = 1-u. Check T+ and T- simplify
u = 0.451485; R = 4.0; s = 2.0
Tp = (1-(1-u)) + s*((1-u)-u) + u
Tm = (1-(1-u)) + s*((1-u)-u) - u
print("symmetric: T+ =", Tp, " T- =", Tm, " u(1+s)=", u*(1+s), " (1-u)(s-1)+u(s+1)=", (1-u)*(s-1)+u*(s+1))
