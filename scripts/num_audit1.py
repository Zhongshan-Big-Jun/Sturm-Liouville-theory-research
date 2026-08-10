import numpy as np

def fd_eigs(rho, N=1200, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def rho_two_step_sym(c, R, N):
    a, A = 1.0, R
    rho = np.full(N, a)
    i0 = int(round(c*N)); i1 = int(round((1-c)*N))
    rho[i0:i1] = A
    return rho

def rho_two_step_asym(c1, c2, R, N):
    # rho = A on [c1, c2], a elsewhere
    a, A = 1.0, R
    rho = np.full(N, a)
    i0 = int(round(c1*N)); i1 = int(round(c2*N))
    rho[i0:i1] = A
    return rho

print("=== Experiment 1: symmetric two-step, A in middle, scan c ===")
for R in [4.0, 10.0, 100.0]:
    best = {}
    for n in [2,3,4]:
        best[n] = (0.0, None)
    for c in np.linspace(0.0, 0.5, 401):
        rho = rho_two_step_sym(c, R, 1000)
        lam = fd_eigs(rho, 1000, 5)
        for n in [2,3,4]:
            r = lam[n-1]/lam[n-2]
            if r > best[n][0]:
                best[n] = (r, c)
    print(f"R={R}:")
    for n in sorted(best):
        r, c = best[n]
        print(f"  n={n}: sup ratio={r:.5f}  vs (n/(n-1))^2={((n/(n-1))**2):.4f} vs R*(n/(n-1))^2={R*((n/(n-1))**2):.4f}  at c={c:.3f}")
