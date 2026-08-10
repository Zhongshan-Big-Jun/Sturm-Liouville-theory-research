import numpy as np

def y1_vec(jumps, vals, lams):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.zeros((2,2,len(lams)))
    M[0,0]=1; M[1,1]=1
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(lams*c, 0.0))
        wL = w*L
        T = np.empty((2,2,len(lams)))
        T[0,0] = np.cos(wL); T[0,1] = np.sin(wL)/w
        T[1,0] = -w*np.sin(wL); T[1,1] = np.cos(wL)
        M00 = M[0,0]*T[0,0] + M[0,1]*T[1,0]
        M01 = M[0,0]*T[0,1] + M[0,1]*T[1,1]
        M10 = M[1,0]*T[0,0] + M[1,1]*T[1,0]
        M11 = M[1,0]*T[0,1] + M[1,1]*T[1,1]
        M[0,0],M[0,1],M[1,0],M[1,1] = M00,M01,M10,M11
    return M[0,1]

def eigs_fast(jumps, vals, k=6, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    npts = 40000
    s = np.linspace(1e-4, np.sqrt(lam_hi), npts)
    d = y1_vec(jumps, vals, s**2)
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(80):
                m = 0.5*(lo+hi)
                dm = y1_vec(jumps, vals, np.array([m**2]))[0]
                if y1_vec(jumps, vals, np.array([lo**2]))[0]*dm <= 0:
                    hi = m
                else:
                    lo = m
            roots.append(((lo+hi)/2)**2)
    return np.array(sorted(roots)[:k])

def ratio2_sym(c, R, k=3):
    if c < 1e-9:
        lam = eigs_fast([], [1.0], k=k)
    elif c > 0.5-1e-9:
        lam = eigs_fast([], [R], k=k)
    else:
        lam = eigs_fast([c,1-c],[1.0,R,1.0],k=k)
    return lam[1]/lam[0]

def ratio3_sym(c, R):
    if c < 1e-9:
        lam = eigs_fast([], [1.0], k=4)
    elif c > 0.5-1e-9:
        lam = eigs_fast([], [R], k=4)
    else:
        lam = eigs_fast([c,1-c],[1.0,R,1.0],k=4)
    return lam[2]/lam[1]

def refine_max_1d(f, lo, hi, n=400):
    # fine grid then local golden refine at best point
    xs = np.linspace(lo, hi, n)
    vals = np.array([f(x) for x in xs])
    i = np.argmax(vals)
    return xs[i], vals[i], xs, vals

# ---- max lambda2/lambda1 for several R (symmetric two-step) ----
print("=== max lam2/lam1, symmetric two-step well [c,1-c], rho=R there ===")
print("R, max_ratio, c*, 4*sqrt(R), 2+2*sqrt(R), (sqrt(R)+1)^2")
for R in [2.0, 4.0, 10.0, 100.0, 10000.0]:
    c0, v0, _, _ = refine_max_1d(lambda c: ratio2_sym(c,R), 1e-6, 0.5, 300)
    # local refine
    from math import sqrt
    gr = (sqrt(5)-1)/2
    a, b = max(1e-9, c0-0.01), min(0.5, c0+0.01)
    f = lambda c: ratio2_sym(c,R)
    c = b - gr*(b-a); d = a + gr*(b-a); fc, fd = f(c), f(d)
    for _ in range(200):
        if fc > fd:
            a, c, fd = c, d, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, d, fc = d, c, fd
            d = a + gr*(b-a); fd = f(d)
    cbest = 0.5*(a+b)
    print(f"R={R:8.0f}: {f(cbest):.8f}  c*={cbest:.6f}  4sqrt(R)={4*sqrt(R):.4f}  (sqrt(R)+1)^2={(sqrt(R)+1)**2:.4f}")
