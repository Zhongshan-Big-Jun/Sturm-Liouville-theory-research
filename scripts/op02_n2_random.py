# -*- coding: utf-8 -*-
"""#2 n=2 R=4: search max lambda3/lambda2 over 5/7/9/11-block bang-bang configs."""
import numpy as np

def lams_vec(jumps, vals, k=6, npts=30000):
    xs = [0.0] + list(jumps) + [1.0]
    s = np.linspace(1e-8, np.sqrt(max(vals)*400), npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
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
        for _ in range(3):
            sg = np.linspace(lo, hi, 1500)
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
    return np.sort(out)[:k]

R = 4.0
def ratio32(nb, widths, R=4.0):
    widths = widths/np.sum(widths)
    vals = [1.0 if i%2==0 else R for i in range(nb)]
    jumps = np.cumsum(widths)[:-1]
    lam = lams_vec(jumps, vals, k=5)
    return lam[2]/lam[1]

rng = np.random.default_rng(13)
print("random search R=4 for max lambda3/lambda2:")
for nb in (3, 5, 7, 9, 11):
    best = (0, None)
    for trial in range(300):
        w = rng.dirichlet(np.ones(nb))
        r = ratio32(nb, w)
        if r > best[0]: best = (r, w)
    print(f"  {nb} blocks: best lambda3/lambda2 = {best[0]:.6f}")
print("conjectured 5-block value: 4.28466147")
