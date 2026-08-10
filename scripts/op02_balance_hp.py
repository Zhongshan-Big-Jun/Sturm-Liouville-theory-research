# -*- coding: utf-8 -*-
"""#2: high-precision balance y_n + y_{n+1} = pi for alternating configs, n=2..6, R=4."""
import mpmath as mp
import numpy as np
mp.mp.dps = 30

def lams_mp(jumps, vals, k, R, N=400000):
    s = np.linspace(1e-9, np.sqrt(R*400), N)
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(N); M01 = np.zeros(N); M10 = np.zeros(N); M11 = np.ones(N)
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(lo, hi, 4000)
            M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
            for jj in range(len(xs)-1):
                L = xs[jj+1]-xs[jj]; c = vals[jj]
                w = sg*np.sqrt(c); wL = w*L
                cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
                M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            dg = M01
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj2 = np.nonzero(sg_s)[0]
            if len(jj2)==0: break
            lo, hi = sg[jj2[0]], sg[jj2[0]+1]
        out.append(((lo+hi)/2)**2)
    return np.array(out[:k])

R = 4.0; s = np.sqrt(R)
print("R=4: y_n + y_{n+1} - pi")
for n in range(1, 7):
    t = 1.0/((n+1)*s + n)
    w1 = s*t; wR = t
    jumps = []; x = 0.0
    for _ in range(n):
        x += w1
        if x < 1.0: jumps.append(x)
        x += wR
        if x < 1.0: jumps.append(x)
    x += w1
    jumps = sorted(set(round(j,12) for j in jumps))
    vals = [R if i%2==1 else 1.0 for i in range(len(jumps)+1)]
    lam = lams_mp(jumps, vals, n+2, R)
    yn = s*t*np.sqrt(lam[n-1]); ynp = s*t*np.sqrt(lam[n])
    print(f"  n={n}: sum-pi = {yn+ynp-np.pi:+.3e}   ratio = {(ynp/yn)**2:.10f}")
