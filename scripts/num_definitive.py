import numpy as np, time
from itertools import combinations

def fd_eigs(rho, N=700, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def build_pts(pts, R, N):
    rho = np.ones(N)
    for k in range(0, len(pts), 2):
        rho[int(round(pts[k]*N)):int(round(pts[k+1]*N))] = R
    return rho

def scan(R, m, gridpts, N=700, idx=3):
    """m intervals; ratio = lam[idx]/lam[idx-1]. Return best (value, pts)."""
    g = np.linspace(0.015, 0.985, gridpts)
    step = g[1]-g[0]
    best = (0.0, None)
    cnt = 0
    for comb in combinations(range(len(g)), 2*m):
        pts = [g[i] for i in comb]
        ok = all(pts[2*i+1] + 1.5*step < pts[2*i+2] for i in range(m-1))
        if not ok: continue
        cnt += 1
        rho = build_pts(pts, R, N)
        lam = fd_eigs(rho, N, idx+1)
        r = lam[idx]/lam[idx-1]
        if r > best[0]: best = (r, pts)
    return best, cnt

t0=time.time()
best2, cnt2 = scan(4.0, 2, 24, 700, 3)
print(f"R=4 lam3/lam2 asym 2-interval (grid 24): best={best2[0]:.5f} at {[round(p,4) for p in best2[1]]} ({cnt2} configs, {time.time()-t0:.0f}s)")
print("   symmetric FP value = 4.2847")
best3, cnt3 = scan(4.0, 3, 14, 700, 4)
print(f"R=4 lam4/lam3 asym 3-interval (grid 14): best={best3[0]:.5f} at {[round(p,3) for p in best3[1]]} ({cnt3} configs, {time.time()-t0:.0f}s)")
print("   symmetric FP value = ~3.45 (verify)")
