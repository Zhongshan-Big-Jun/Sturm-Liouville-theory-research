# -*- coding: utf-8 -*-
"""#2 n=2 R=4: Nelder-Mead optimization of lambda3/lambda2 over 5 and 7-block configs."""
import numpy as np
from scipy.optimize import minimize

def lams_vec(jumps, vals, k=5, npts=25000):
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
            sg = np.linspace(lo, hi, 1200)
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
def make_neg(nb):
    def neg(w):
        w = np.abs(w); w = w/np.sum(w)
        vals = [1.0 if i%2==0 else R for i in range(nb)]
        lam = lams_vec(np.cumsum(w)[:-1], vals, k=5)
        return -lam[2]/lam[1]
    return neg

rng = np.random.default_rng(5)
for nb in (5, 7):
    neg = make_neg(nb)
    best = (1e9, None)
    starts = [rng.dirichlet(np.ones(nb)) for _ in range(8)]
    # include the conjectured symmetric start for 5 blocks
    if nb == 5:
        s2 = np.sqrt(R); t2 = 1/(3*s2+2)
        starts.append(np.array([s2*t2, t2, s2*t2, t2, s2*t2]))
    for w0 in starts:
        res = minimize(neg, w0, method='Nelder-Mead', options={'maxiter':500, 'xatol':1e-9, 'fatol':1e-12})
        if res.fun < best[0]:
            best = (res.fun, res.x/np.sum(np.abs(res.x)))
    print(f"{nb}-block max lambda3/lambda2 = {-best[0]:.8f} at widths {np.array2string(best[1], precision=6)}")
print("conjectured 5-block: 4.28466147 at widths [0.25, 0.125, 0.25, 0.125, 0.25]")
