import numpy as np, time

def fd_all(rho, N=1200, k=8):
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

def full_iter(R, n, N=1200, itmax=60):
    x = np.linspace(0,1,N)
    rho = np.where(x < 0.5, 1.0, R)
    hist = {}
    for it in range(itmax):
        w, U = fd_all(rho, N, n+1)
        u_n = U[:, n-1]; u_np1 = U[:, n]
        rho_new = np.where(u_n**2 > u_np1**2, R, 1.0)
        if np.array_equal(rho, rho_new):
            return rho, it+1, "fixed"
        key = rho_new.tobytes()
        if key in hist:
            return rho_new, it+1, "cycle(len=%d)" % (it-hist[key])
        hist[key] = it
        rho = rho_new
    return rho, itmax, "no-conv"

R=4.0
for n in [1,2,3]:
    t0=time.time()
    rho, iters, status = full_iter(R, n)
    N = len(rho)
    w, U = fd_all(rho, N, n+1)
    ratio = w[n-1]/w[n-2]
    u_n = U[:, n-1]; u_np1 = U[:, n]
    d = u_n**2 - u_np1**2
    cross = np.where(np.diff(np.sign(d)) != 0)[0]
    x = np.linspace(0,1,N)
    jumps = np.where(np.diff(rho) != 0)[0]
    print(f"n={n}: {status}, {iters} iters, ratio={ratio:.6f} ({time.time()-t0:.0f}s)")
    print(f"   jumps: {np.round(x[jumps],4)}")
    print(f"   zeros: {np.round(x[cross],4)}")
