# -*- coding: utf-8 -*-
"""#2 n=2: is the max of lambda3/lambda2 over symmetric 5-block [1,R,1,R,1] (a,b,c,b,a) at a=c=s*t, b=t?"""
import numpy as np

def det_scan(jumps, vals, s_grid):
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0)); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2; n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2; n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def ratio_32(a, b, c, R):
    """lambda3/lambda2 for blocks widths (a,b,c,b,a), values (1,R,1,R,1)."""
    jumps = [a, a+b, a+b+c, a+b+c+b]
    vals = [1, R, 1, R, 1]
    s = np.linspace(1e-7, np.sqrt(1200), 80000)
    d = det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    lams = []
    for i in idx[:8]:
        slo, shi = s[i], s[i+1]
        for _ in range(5):
            sg = np.linspace(slo, shi, 3000)
            dg = det_scan(jumps, vals, sg)
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_s)[0]
            if len(jj)==0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        lams.append(((slo+shi)/2)**2)
        if len(lams) >= 5: break
    lams = np.sort(lams)
    return lams[2]/lams[1]

R = 4.0; s = np.sqrt(R)
t = 1.0/(3*s+2)
best = (0, None)
# scan over (a,b,c) with a+b+c+b+a=1 -> a+b = (1-c)/2
for c in np.linspace(0.05, 0.7, 60):
    for a in np.linspace(0.02, 0.5-0.5*c, 50):
        b = (1-c)/2 - a
        if b <= 0.01: continue
        r = ratio_32(a, b, c, R)
        if r > best[0]: best = (r, (a, b, c))
print("best over (a,b,c): ratio =", best[0], "at a,b,c =", best[1])
print("conjectured: a=c=s*t =", s*t, ", b=t =", t)
r0 = ratio_32(s*t, t, s*t, R)
print("conjectured ratio:", r0)
print("gap:", best[0]-r0)
