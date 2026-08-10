import numpy as np, time

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

def eigs_exact(jumps, vals, k=8, lam_hi=None):
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

# 1) verify: periodic extension of well (c=0.399, R=4), 2 periods
c = 0.399; R = 4.0
# phi_2(x) = phi_0(2(x-1/2)): A on [c/2, (1-c)/2] U [1/2+c/2, 1/2+(1-c)/2] = [0.1995,0.3005] U [0.6995,0.8005]
jumps = [c/2, (1-c)/2, 0.5+c/2, 0.5+(1-c)/2]
vals = [1.0, R, 1.0, R, 1.0]
lam = eigs_exact(jumps, vals, k=5)
print("period-2 well config: lam:", np.round(lam,5))
print("  lam4/lam2 =", lam[3]/lam[1], " (should be ~7.4812 = nu(1/4))")
print("  lam3/lam2 =", lam[2]/lam[1])
print("  lam2/lam1 =", lam[1]/lam[0])

# 2) verify nu(1/R): max lambda2/lambda1 over [1,R] via well scan (R=4: 7.4812; R=100: 39.51)
def well_ratio(c, R):
    lam = eigs_exact([c,1-c],[1.0,R,1.0], k=3)
    return lam[1]/lam[0]
for Rv in [4.0, 100.0]:
    best = (0.0,None)
    for c in np.linspace(0.01, 0.49, 300):
        r = well_ratio(c, Rv)
        if r > best[0]: best = (r, c)
    print(f"nu(1/{Rv:.0f}) ~ {best[0]:.5f} at c={best[1]:.4f}")

# 3) check lambda3/lambda2 for random smooth and periodic configs never exceeds nu
rng = np.random.default_rng(3)
N=900
def fd_eigs(rho, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]
worst = 0.0
x = np.linspace(0,1,N)
for trial in range(200):
    v = np.zeros(N)
    for kk in range(1,8):
        v += rng.normal(0,1)*np.sin(kk*np.pi*x)
    rho = np.clip(1.0 + 3.0*(0.5+0.5*np.tanh(2*v)), 1.0, 4.0)
    lam = fd_eigs(rho)
    worst = max(worst, lam[2]/lam[1])
print("worst random smooth lam3/lam2 (R=4):", worst, " vs nu(1/4)=7.4812")
