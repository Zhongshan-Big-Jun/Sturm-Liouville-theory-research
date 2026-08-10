import numpy as np

def eigs_exact(jumps, vals, k=8, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    npts = 120000
    s = np.linspace(1e-5, np.sqrt(lam_hi), npts)
    M00 = np.ones(len(s)); M01 = np.zeros(len(s)); M10 = np.zeros(len(s)); M11 = np.ones(len(s))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    d = M01
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(60):
                m = 0.5*(lo+hi)
                M = np.eye(2)
                for j in range(len(xs)-1):
                    L = xs[j+1]-xs[j]; cc = vals[j]; w = np.sqrt(max(m*m*cc,0.0))
                    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
                    M = M @ T
                dm = M[0,1]
                Mlo = np.eye(2)
                for j in range(len(xs)-1):
                    L = xs[j+1]-xs[j]; cc = vals[j]; w = np.sqrt(max(lo*lo*cc,0.0))
                    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
                    Mlo = Mlo @ T
                dlo = Mlo[0,1]
                if dlo*dm <= 0: hi = m
                else: lo = m
            roots.append(((lo+hi)/2)**2)
            if len(roots) >= k: break
    return np.array(sorted(roots)[:k])

def periodic_double_well(n, c, R):
    # n periods of cell (a on [0,c], A on [c,1-c], a on [1-c,1]) on [0,1]
    jumps = []
    for i in range(n):
        jumps += [ (i+c)/n, (i+1-c)/n ]
    vals = []
    for i in range(2*n+1):
        vals.append(4.0 if i % 2 == 1 else 1.0)
    return eigs_exact(jumps, vals, k=2*n+3)

print("=== n-periodic double-well (c=0.4001, R=4) ===")
for n in [1,2,3,4,5,6,8,10,12]:
    lam = periodic_double_well(n, 0.4001, 4.0)
    r1 = lam[n]/lam[n-1]
    r2 = lam[2*n-1]/lam[n-1]
    print("n=%2d  lam_{n+1}/lam_n=%8.4f   lam_{2n}/lam_n=%8.4f" % (n, r1, r2))

print()
print("=== sup lambda3/lambda2, R=4: symmetric 2-interval scan (finer) ===")
best = (0.0, None)
for u in np.linspace(0.02, 0.47, 90):
    for v in np.linspace(u+0.005, 0.49, 90):
        if v <= u: continue
        lam = eigs_exact([u,v,1-v,1-u], [1.0,4.0,1.0,4.0,1.0], k=4)
        r = lam[2]/lam[1]
        if r > best[0]: best = (r, (u,v))
print("best symmetric 2-int:", best)
