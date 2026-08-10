import numpy as np

def fd_all(rho, N=1500, k=8):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    w, V = np.linalg.eigh(B)
    U = V[:, :k] / s[:, None]
    return w[:k], U

def bangbang_iter(R, n, N=1500, itmax=80):
    rho = np.full(N, (1.0+R)/2)
    for it in range(itmax):
        w, U = fd_all(rho, N, n+1)
        u_n = U[:, n-1]; u_np1 = U[:, n]
        d = u_n**2 - u_np1**2
        rho_new = np.where(d > 0, R, 1.0)
        rho = 0.5*rho + 0.5*rho_new
    w, U = fd_all(rho, N, n+1)
    u_n = U[:, n-1]; u_np1 = U[:, n]
    d = u_n**2 - u_np1**2
    rho_f = np.where(d > 0, R, 1.0)
    w, U = fd_all(rho_f, N, n+1)
    ratio = w[n-1]/w[n-2]
    Nloc = len(rho_f)
    inside = (rho_f > 1.5)
    seg = []
    cur = inside[0]; start = 0
    for i in range(1, Nloc):
        if inside[i] != cur:
            if cur: seg.append((start, i))
            cur = inside[i]; start = i
    if cur: seg.append((start, Nloc))
    return w, U, rho_f, ratio, seg, Nloc

for R in [4.0, 10.0, 100.0]:
    print(f"=== R={R} ===")
    for n in [2,3,4]:
        w, U, rho_f, ratio, seg, Nloc = bangbang_iter(R, n)
        x = np.linspace(0, 1, Nloc)
        print(f"  n={n}: fixed-point ratio={ratio:.5f}, #A-intervals={len(seg)}, A-regions={[(round(float(x[s]),3),round(float(x[e-1]),3)) for s,e in seg]}")
