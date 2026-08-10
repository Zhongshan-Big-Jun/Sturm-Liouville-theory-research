import numpy as np, time

def fd_eigs_fast(rho, N=600, k=5):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def rho_asym(c1, c2, R, N):
    a, A = 1.0, R
    rho = np.full(N, a)
    i0 = int(round(c1*N)); i1 = int(round(c2*N))
    rho[i0:i1] = A
    return rho

def scan2d(R, ngrid=61, ns=(2,3,4)):
    best = {n: (0.0, None) for n in ns}
    grid = np.linspace(0.02, 0.98, ngrid)
    t0 = time.time()
    for i, c1 in enumerate(grid):
        for j, c2 in enumerate(grid):
            if c2 <= c1 + 0.01: continue
            rho = rho_asym(c1, c2, R, 600)
            lam = fd_eigs_fast(rho, 600, 5)
            for n in ns:
                r = lam[n-1]/lam[n-2]
                if r > best[n][0]:
                    best[n] = (r, (c1, c2))
        if i % 10 == 0: print(f"  row {i}/{ngrid-1}, elapsed {time.time()-t0:.0f}s")
    return best

for R in [4.0]:
    best = scan2d(R)
    print(f"R={R} asymmetric two-step (A on [c1,c2]):")
    for n in sorted(best):
        r, (c1,c2) = best[n]
        print(f"  n={n}: sup={r:.5f} at c1={c1:.3f}, c2={c2:.3f} (width={c2-c1:.3f})")
