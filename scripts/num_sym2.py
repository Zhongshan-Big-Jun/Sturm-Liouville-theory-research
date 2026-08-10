import numpy as np, time

def fd_eigs(rho, N=800, k=7):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def rho_sym2(c1, c2, R, N):
    # A on [c1,c2] U [1-c2,1-c1]
    rho = np.ones(N)
    i0=int(round(c1*N)); i1=int(round(c2*N)); i2=int(round((1-c2)*N)); i3=int(round((1-c1)*N))
    rho[i0:i1]=R; rho[i2:i3]=R
    return rho

# symmetric 2 A-intervals, scan (c1,c2) with 0<c1<c2<0.5
print("=== symmetric 2-interval A-regions: max lam_n/lam_{n-1} ===")
for R in [4.0, 10.0, 100.0]:
    for n in [2,3]:
        best=(0.0,None)
        grid = np.linspace(0.02, 0.48, 40)
        t0=time.time()
        for c1 in grid:
            for c2 in grid:
                if c2 <= c1+0.02: continue
                rho = rho_sym2(c1,c2,R,800)
                lam = fd_eigs(rho,800,n+1)
                r = lam[n-1]/lam[n-2]
                if r > best[0]: best=(r,(c1,c2))
        print(f"  R={R} n={n}: max={best[0]:.5f} at c1,c2={best[1]}  ({(time.time()-t0):.0f}s)")
