import numpy as np

def _det_scan(jumps, vals, s_grid):
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
    s = np.linspace(1e-6, np.sqrt(lam_hi), 30000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
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

def sym_config_ratio(p, R, n):
    """p: n-vector of jump positions in (0,0.5) (symmetric config, A on [p_{2k-1},p_{2k}])."""
    jumps = []
    vals = [1.0]
    prev = 0.0
    for k, pk in enumerate(p):
        jumps.append(pk); jumps.append(1.0-pk)
    jumps = sorted(jumps)
    # build vals: alternate a,A starting with a
    pts = [0.0]+jumps+[1.0]
    vals = [1.0 if i%2==0 else R for i in range(len(pts)-1)]
    lam = eigs_fast(jumps, vals, k=n+2)
    return lam[n]/lam[n-1], lam, jumps, vals

# coordinate descent refinement on p (exact solver)
def refine(p0, R, n, iters=8):
    p = np.array(p0, dtype=float)
    best, lam, jumps, vals = sym_config_ratio(p, R, n)
    for it in range(iters):
        improved = False
        for k in range(len(p)):
            lo = p[k-1]+0.002 if k>0 else 0.003
            hi = p[k+1]-0.002 if k<len(p)-1 else 0.497
            # golden section on p[k]
            g = (np.sqrt(5)-1)/2
            a_, b_ = lo, hi
            x1 = b_-g*(b_-a_); x2 = a_+g*(b_-a_)
            f1,_,_,_ = sym_config_ratio(np.concatenate([p[:k],[x1],p[k+1:]]), R, n)
            f2,_,_,_ = sym_config_ratio(np.concatenate([p[:k],[x2],p[k+1:]]), R, n)
            for _ in range(18):
                if f1 > f2:
                    b_ = x2; x2 = x1; f2 = f1
                    x1 = b_-g*(b_-a_); f1,_,_,_ = sym_config_ratio(np.concatenate([p[:k],[x1],p[k+1:]]), R, n)
                else:
                    a_ = x1; x1 = x2; f1 = f2
                    x2 = a_+g*(b_-a_); f2,_,_,_ = sym_config_ratio(np.concatenate([p[:k],[x2],p[k+1:]]), R, n)
            p[k] = 0.5*(a_+b_)
        best, lam, jumps, vals = sym_config_ratio(p, R, n)
    return best, p, lam, jumps, vals

for n in [2,3,4]:
    p0 = {
        2: [0.25021, 0.3751],
        3: [0.09534, 0.24604, 0.4567],
        4: [0.08035, 0.17027, 0.33014, 0.42007],
    }[n]
    best, p, lam, jumps, vals = refine(p0, 4.0, n)
    print(f"n={n}: ratio={best:.8f}  p={[round(q,6) for q in p]}")
    print("   lam_n, lam_{n+1}:", np.round(lam[n-1],4), np.round(lam[n],4))
