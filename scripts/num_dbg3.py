import numpy as np

def eigs_exact_old(jumps, vals, k=8, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    npts = 150000
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
                dm = transfer_prop(jumps, vals, m**2, 1.0)[0]
                if transfer_prop(jumps, vals, lo**2, 1.0)[0]*dm <= 0:
                    hi = m
                else:
                    lo = m
            roots.append(((lo+hi)/2)**2)
            if len(roots) >= k: break
    return np.array(sorted(roots)[:k])

def transfer_prop(jumps, vals, lam, x):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.eye(2)
    i = 0
    while i < len(xs)-1 and x > xs[i+1] + 1e-12:
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(lam*c)
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        i += 1
    c = vals[i]
    w = np.sqrt(lam*c)
    L = x - xs[i]
    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
    M = M @ T
    v = M @ np.array([0.0, 1.0])
    return v[0], v[1]

# test double well c=0.4 R=4
c=0.4; R=4.0
jumps=[c,1-c]; vals=[1.0,R,1.0]
print("old:", eigs_exact_old(jumps, vals, k=4))
print("ratio old:", eigs_exact_old(jumps, vals, k=4)[1]/eigs_exact_old(jumps, vals, k=4)[0])
