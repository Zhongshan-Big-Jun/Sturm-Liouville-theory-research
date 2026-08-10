import numpy as np, time
from itertools import combinations

def fd_eigs(rho, N=600, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def build_ints(pts, R, N):
    """pts: 2*m ordered points; A on [pts[0],pts[1]], [pts[2],pts[3]], ..."""
    rho = np.ones(N)
    for k in range(0, len(pts), 2):
        rho[int(round(pts[k]*N)):int(round(pts[k+1]*N))] = R
    return rho

def scan_asym(R, m, gridpts=18, N=600):
    """m = number of A-intervals (2m ordered jump points). Global scan."""
    g = np.linspace(0.02, 0.98, gridpts)
    best = (0.0, None)
    cnt = 0
    for comb in combinations(range(len(g)), 2*m):
        pts = [g[i] for i in comb]
        # ensure gaps >= 2 grid steps between intervals
        ok = all(pts[2*i+1] + 2*(g[1]-g[0]) < pts[2*i+2] for i in range(m-1))
        if not ok: continue
        cnt += 1
        rho = build_ints(pts, R, N)
        lam = fd_eigs(rho, N, 4)
        r = lam[2]/lam[1]
        if r > best[0]: best = (r, pts)
    return best, cnt

t0=time.time()
# R=4: asymmetric 1 and 2 interval configs for lambda3/lambda2
best1, cnt1 = scan_asym(4.0, 1, 40)
print(f"R=4 asym 1-interval (lam3/lam2): best={best1[0]:.5f} at {[round(p,3) for p in best1[1]]}  ({time.time()-t0:.0f}s, {cnt1} configs)")
best2, cnt2 = scan_asym(4.0, 2, 18)
print(f"R=4 asym 2-interval (lam3/lam2): best={best2[0]:.5f} at {[round(p,3) for p in best2[1]]}  ({time.time()-t0:.0f}s, {cnt2} configs)")
# R=10 quick
best1b, cnt1b = scan_asym(10.0, 1, 30)
print(f"R=10 asym 1-interval (lam3/lam2): best={best1b[0]:.5f} at {[round(p,3) for p in best1b[1]]}")
