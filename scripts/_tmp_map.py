# -*- coding: utf-8 -*-
"""Study the self-consistency map T(a,b) = (a',b') where {f>0} for rho_{a,b} = (a',b').
Check monotonicity / sign structure of the defect."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

R = 4.0

def fmap(a, b, npts=2001):
    blocks = [(a,1.0),(b-a,R),(1-b,1.0)]
    s = lams_fast(blocks, 3)
    lam = s**2
    xs = np.linspace(0,1,npts)
    u1 = y_at(blocks, s[0], xs)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], xs)/np.sqrt(norm2(blocks, s[1]))
    f = lam[0]*u1**2 - lam[1]*u2**2
    pos = f > 0
    nz = np.nonzero(pos)[0]
    if len(nz)==0: return (np.nan, np.nan)
    return (xs[nz[0]], xs[nz[-1]])

# grid of (a,b) with a<b: check defect signs
aa = np.linspace(0.05, 0.45, 9)
bb = np.linspace(0.55, 0.95, 9)
print("  a    b   ->  a'  b'   da db")
for a in aa:
    for b in bb:
        if a >= b: continue
        ap, bp = fmap(a,b)
        if np.isnan(ap): 
            print(f"{a:.2f} {b:.2f} -> nan"); continue
        print(f"{a:.2f} {b:.2f} -> {ap:.3f} {bp:.3f}  da={ap-a:+.3f} db={bp-b:+.3f}")
