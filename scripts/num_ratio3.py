import numpy as np

def _det_scan(jumps, vals, s_grid):
    """Vectorized M01(s) over s_grid."""
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigs_fast(jumps, vals, k=8):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    lo_s, hi_s = 1e-6, np.sqrt(lam_hi)
    s = np.linspace(lo_s, hi_s, 30000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    # refine each bracket by zooming 4 rounds
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(slo, shi, 400)
            dg = _det_scan(jumps, vals, sg)
            sg_signs = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_signs)[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

# sanity
lam = eigs_fast([0.4,0.6], [1.0,4.0,1.0], k=4)
print("double well lam:", np.round(lam,6), " ratio:", lam[1]/lam[0], "(expect 7.4815)")

print()
print("=== mu(1/R) = min lambda2/lambda1: Keller middle-well (a on [c,1-c], A ends) ===")
for R in [2.0, 3.0, 4.0, 10.0, 100.0]:
    best = (1e9, None)
    for c in np.linspace(0.005, 0.495, 200):
        lam = eigs_fast([c,1-c], [R,1.0,R], k=3)
        r = lam[1]/lam[0]
        if r < best[0]: best = (r, c)
    print("R=%6.1f  mu=%9.5f at c=%6.4f   elementary lower bound 4a/A=%6.4f" % (R, best[0], best[1], 4.0/R))

print()
print("=== inf lambda3/lambda2, R=4: A on [u,v]U[1-v,1-u] (a elsewhere) ===")
best = (1e9, None)
for u in np.linspace(0.01, 0.48, 50):
    for v in np.linspace(u+0.01, 0.49, 50):
        lam = eigs_fast([u,v,1-v,1-u], [4.0,1.0,4.0,1.0,4.0], k=4)
        r = lam[2]/lam[1]
        if r < best[0]: best = (r, (u,v))
print("best (A middle):", best)

print()
print("=== inf lambda3/lambda2, R=4: a on [u,v]U[1-v,1-u] (A elsewhere) ===")
best = (1e9, None)
for u in np.linspace(0.01, 0.48, 50):
    for v in np.linspace(u+0.01, 0.49, 50):
        lam = eigs_fast([u,v,1-v,1-u], [1.0,4.0,1.0,4.0,1.0], k=4)
        r = lam[2]/lam[1]
        if r < best[0]: best = (r, (u,v))
print("best (a middle):", best)
