# -*- coding: utf-8 -*-
"""Iterate the SUP-rounding map T on the 3-block family [1,R,1]_{a,b}; check monotone D increase
and convergence to the fixed point. Also scan for 2-block fixed points and verify non-degeneracy."""
import numpy as np
from scipy.optimize import brentq, least_squares
from gap_lib import lams_fast, y_at, norm2, eigfuns

R = 4.0

def gap_D(blocks):
    s = lams_fast(blocks, 3)**2
    return s[1]-s[0]

def pos_interval(blocks, npts=4001):
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

def T(a, b):
    ap, bp = pos_interval([(a,1.0),(b-a,R),(1-b,1.0)])
    return ap, bp

# iterate from various starts
print("=== SUP-rounding iteration (R=4) ===")
starts = [(0.2,0.5),(0.3,0.8),(0.42,0.56),(0.45,0.55),(0.35,0.65),(0.1,0.9),(0.48,0.52)]
for (a0,b0) in starts:
    a,b = a0,b0
    D0 = gap_D([(a0,1.0),(b0-a0,R),(1-b0,1.0)])
    seq = []
    for it in range(60):
        ap, bp = T(a,b)
        Dp = gap_D([(ap,1.0),(bp-ap,R),(1-bp,1.0)])
        seq.append(Dp)
        if np.isnan(ap): break
        if abs(ap-a)+abs(bp-b) < 1e-9: break
        a,b = ap,bp
    # check monotone increase from D0
    mono = all(seq[i+1] >= seq[i]-1e-7 for i in range(len(seq)-1)) and seq[0] >= D0-1e-7
    print(f"({a0},{b0}): -> ({a:.6f},{b:.6f}) iters={it+1} D: {D0:.5f}->{seq[-1]:.5f} mono={mono}")

# 2-block fixed points: config [1,R] jump at c. f(c)=0 and pattern {f>0}=(c,1) or (0,c).
print("=== 2-block [1,R] self-consistent scan ===")
def f_at(blocks, x):
    s = lams_fast(blocks, 3)
    lam = s**2
    u1 = y_at(blocks, s[0], np.array([x]))[0]/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], np.array([x]))[0]/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2
for c in np.linspace(0.05,0.95,19):
    bl = [(c,1.0),(1-c,R)]
    fc = f_at(bl, c)
    a,b = pos_interval(bl)
    # fixed if f(c)=0 and positive set matches the R-band (c,1)
    match = (abs(fc) < 0.05) and (abs(a-c) < 0.03) and (b > 0.97)
    print(f"c={c:.2f}: f(c)={fc:+.4f} {f_at(bl,0.05):+.4f} {f_at(bl,0.95):+.4f}  pos=({a:.3f},{b:.3f}) fixed={match}")

# non-degeneracy condition at self-consistent points
print("=== non-degeneracy lambda1/lambda2 < min(V0^2, V1^2) ===")
def Vcheck(blocks):
    s = lams_fast(blocks, 3)
    lam = s**2
    # slopes at 0 and 1 via TM derivative: y'(0)=1 init, so u1'(0)=1/norm1 etc.
    y1 = y_at(blocks, s[0], np.array([1e-6, 1-1e-6]))[0]/np.sqrt(norm2(blocks, s[0]))
    y2 = y_at(blocks, s[1], np.array([1e-6, 1-1e-6]))[0]/np.sqrt(norm2(blocks, s[1]))
    V0 = y2[0]/y1[0]; V1 = y2[1]/y1[1]
    r = lam[0]/lam[1]
    return r, V0, V1, V0**2, V1**2
for label, blocks in [("SUP", [(0.451485,1.0),(0.09703,R),(0.451485,1.0)]),
                      ("INF", [(0.382598,R),(0.234804,1.0),(0.382598,R)])]:
    r, V0, V1, V0s, V1s = Vcheck(blocks)
    print(f"{label}: r={r:.6f} V0^2={V0s:.6f} V1^2={V1s:.6f} cond={r < min(V0s,V1s)}")
