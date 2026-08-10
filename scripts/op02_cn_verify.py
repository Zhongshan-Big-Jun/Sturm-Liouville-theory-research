# -*- coding: utf-8 -*-
"""#2: verify the fixed-n conjecture c_n(R) and the alternating-extremizer structure.
For n=2: optimize lambda3/lambda2 over symmetric 5-block [1,R,1,R,1] widths (a,b,c,b,a).
Conjecture: a = c = s*t, b = t, s = sqrt(R), t = 1/(3s+2).
"""
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

def eigs(jumps, vals, k=8, npts=60000, refine=6):
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    s = np.linspace(1e-7, np.sqrt(lam_hi), npts)
    d = det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(refine):
            sg = np.linspace(slo, shi, 2000)
            dg = det_scan(jumps, vals, sg)
            sg_signs = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_signs)[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def alt_config(n, R, w_ratio=None):
    """alternating [1,R,1,...,1], n+1 blocks of 1, n blocks of R.
    widths: value-1 blocks have width w_ratio*t, value-R blocks width t (w_ratio=s default)."""
    s = np.sqrt(R) if w_ratio is None else w_ratio
    t = 1.0/((n+1)*s + n)
    w1 = s*t; wR = t
    jumps = []
    x = 0.0
    for _ in range(n):
        x += w1
        if x < 1.0: jumps.append(x)
        x += wR
        if x < 1.0: jumps.append(x)
    # final w1
    x += w1
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = [R if i%2==1 else 1.0 for i in range(len(pts)-1)]
    return jumps, vals

print("=== conjectured c_n(R) for R in {2,3,4,10,100} ===")
for R in (2.0, 3.0, 4.0, 10.0, 100.0):
    row = []
    for n in (1,2,3,4):
        jumps, vals = alt_config(n, R)
        lam = eigs(jumps, vals, k=n+3)
        row.append(lam[n]/lam[n-1])
    print(f"R={R:6.1f}: " + "  ".join(f"n={n}: {v:.6f}" for n,v in zip((1,2,3,4),row)))
