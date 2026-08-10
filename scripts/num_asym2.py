import numpy as np, time

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

def build(intervals, R, N):
    rho = np.ones(N)
    for lo, hi in intervals:
        rho[int(round(lo*N)):int(round(hi*N))] = R
    return rho

R=4.0
# --- Scan asymmetric 2-interval configs for lam3/lam2: A on [c1,c2] U [c3,c4] ---
# coarse: 3 params. Use grid 30^3 with pruning.
grid = np.linspace(0.03, 0.97, 26)
best = (0.0, None)
t0=time.time(); cnt=0
Nfd=700
for c1 in grid:
    for c2 in grid:
        if c2 <= c1+0.03: continue
        for c3 in grid:
            if c3 <= c2+0.03: continue
            for c4 in grid:
                if c4 <= c3+0.03: continue
                cnt+=1
                rho = build([(c1,c2),(c3,c4)], R, Nfd)
                lam = fd_eigs(rho, Nfd, 4)
                r = lam[2]/lam[1]
                if r > best[0]: best = (r,(c1,c2,c3,c4))
    if grid.tolist().index(c1)%5==0:
        print(f"  c1={c1:.2f}, best so far {best[0]:.4f} at {best[1]}, {time.time()-t0:.0f}s")
print(f"asym 2-interval best lam3/lam2: {best[0]:.5f} at {best[1]}, configs={cnt}, {time.time()-t0:.0f}s")
