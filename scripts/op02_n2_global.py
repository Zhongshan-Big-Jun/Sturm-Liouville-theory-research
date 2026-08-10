# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import minimize

def detfun(s, jumps, vals):
    xs = [0.0] + list(jumps) + [1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M01

def lams_fast(jumps, vals, k=6, npts=40000):
    A = max(vals)
    s = np.linspace(1e-8, np.sqrt(A*400), npts)
    d = np.array([detfun(x, jumps, vals) for x in s])
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(lo, hi, 2000)
            dg = np.array([detfun(x, jumps, vals) for x in sg])
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_s)[0]
            if len(jj)==0: break
            lo, hi = sg[jj[0]], sg[jj[0]+1]
        out.append(((lo+hi)/2)**2)
        if len(out) >= k: break
    return np.sort(out)[:k]

R = 4.0
def neg5(w):
    w = np.abs(w); w = w/np.sum(w)
    lam = lams_fast(np.cumsum(w)[:4], [1,R,1,R,1], k=6)
    return -lam[2]/lam[1]
def neg7(w):
    w = np.abs(w); w = w/np.sum(w)
    lam = lams_fast(np.cumsum(w)[:6], [1,R,1,R,1,R,1], k=7)
    return -lam[3]/lam[2]

rng = np.random.default_rng(7)
best5 = (1e9, None)
for trial in range(20):
    res = minimize(neg5, rng.dirichlet(np.ones(4)), method='Nelder-Mead', options={'maxiter':300, 'xatol':1e-7, 'fatol':1e-9})
    if res.fun < best5[0]: best5 = (res.fun, res.x/np.sum(np.abs(res.x)))
print("best 5-block:", -best5[0], " widths:", np.array2string(best5[1], precision=5))
print("conjectured 5-block [0.25,0.125,0.25,0.125,0.25]: 4.28466147")

best7 = (1e9, None)
for trial in range(20):
    res = minimize(neg7, rng.dirichlet(np.ones(6)), method='Nelder-Mead', options={'maxiter':300, 'xatol':1e-7, 'fatol':1e-9})
    if res.fun < best7[0]: best7 = (res.fun, res.x/np.sum(np.abs(res.x)))
print("best 7-block:", -best7[0], " widths:", np.array2string(best7[1], precision=5))
