import numpy as np

def fd_eigs(rho, N=900, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def ratio_sym_fd(c, R, n, N=900):
    if c < 1e-9:
        rho = np.ones(N)
    elif c > 0.5-1e-9:
        rho = np.full(N, R)
    else:
        rho = np.ones(N)
        i0 = int(round(c*N)); i1 = int(round((1-c)*N))
        rho[i0:i1] = R
    lam = fd_eigs(rho, N, n+1)
    return lam[n-1]/lam[n-2]

# grid scan with FD for n=2,3,4; several R
print("=== max lam_n/lam_{n-1} over symmetric two-step (well in middle) ===")
for R in [2.0, 4.0, 10.0, 100.0, 10000.0]:
    for n in [2,3,4]:
        cs = np.linspace(0.0, 0.5, 250)
        vals = np.array([ratio_sym_fd(c, R, n) for c in cs])
        i = np.argmax(vals)
        print(f"R={R:8.0f} n={n}: sup~{vals[i]:.5f} at c~{cs[i]:.4f}")
