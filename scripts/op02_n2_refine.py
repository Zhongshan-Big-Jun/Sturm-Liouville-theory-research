# -*- coding: utf-8 -*-
"""#2 n=2: refined local optimization + gradient check at conjectured point."""
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

def lams_of(jumps, vals, k=5, npts=90000, refine=6):
    A = max(vals)
    s = np.linspace(1e-7, np.sqrt(A*1200), npts)
    d = det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(refine):
            sg = np.linspace(slo, shi, 4000)
            dg = det_scan(jumps, vals, sg)
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_s)[0]
            if len(jj)==0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.sort(out)[:k]

def ratio_5block(a, b, c, R=4.0):
    jumps = [a, a+b, a+b+c, a+b+c+b]
    lams = lams_of(jumps, [1,R,1,R,1])
    return lams[2]/lams[1]

R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
x0 = np.array([s*t, t, s*t])
print("conjectured (a,b,c) =", x0, " t =", t)
print("ratio at conjectured:", ratio_5block(*x0))

# local search: coordinate descent with small steps (a+c+2b = 1 constraint -> free (a,b), c = 1-2b-a)
def obj(ab):
    a, b = ab
    c = 1 - 2*b - a
    if min(a,b,c) <= 0.005: return -1e9
    return ratio_5block(a, b, c)
# grid refine around x0
best = (-1, None)
for da in np.linspace(-0.03, 0.03, 25):
    for db in np.linspace(-0.03, 0.03, 25):
        a = x0[0]+da; b = x0[1]+db; c = 1-2*b-a
        if min(a,b,c) <= 0.005: continue
        r = ratio_5block(a, b, c)
        if r > best[0]: best = (r, (a,b,c))
print("local best:", best[0], "at", best[1], " vs conjectured 4.28466147")
print("  deviation:", np.array(best[1])-x0)

# gradient check: perturb each jump, finite difference of log-ratio
def ratio_of_jumps(jumps):
    lams = lams_of(jumps, [1,R,1,R,1])
    return lams[2]/lams[1]
jumps0 = np.array([x0[0], x0[0]+x0[1], x0[0]+x0[1]+x0[2], 1-x0[0]])
h = 1e-6
print("\nfinite-difference gradient of lambda3/lambda2 w.r.t. jump positions at conjectured config:")
for i in range(4):
    jp = jumps0.copy(); jp[i] += h
    g = (ratio_of_jumps(jp) - ratio_of_jumps(jumps0))/h
    print(f"  d/dx{i}: {g:+.6e}")
