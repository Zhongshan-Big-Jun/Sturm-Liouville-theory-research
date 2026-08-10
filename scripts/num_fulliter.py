import numpy as np

def fd_all(rho, N=2400, k=8):
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

def full_iter(R, n, N=2400, itmax=200):
    rho = np.where(np.linspace(0,1,N) < 0.5, 1.0, R)  # generic start
    for it in range(itmax):
        w, U = fd_all(rho, N, n+1)
        u_n = U[:, n-1]; u_np1 = U[:, n]
        rho_new = np.where(u_n**2 > u_np1**2, R, 1.0)
        if np.array_equal(rho, rho_new):
            break
        rho = rho_new
    return rho, it+1

R=4.0
for n in [1,2,3,4]:
    rho, iters = full_iter(R, n)
    N = len(rho)
    w, U = fd_all(rho, N, n+1)
    ratio = w[n-1]/w[n-2]
    u_n = U[:, n-1]; u_np1 = U[:, n]
    d = u_n**2 - u_np1**2
    cross = np.where(np.diff(np.sign(d)) != 0)[0]
    x = np.linspace(0,1,N)
    # jump points of rho
    jumps = np.where(np.diff(rho) != 0)[0]
    print(f"n={n}: converged in {iters} iters, ratio={ratio:.6f}")
    print(f"   jumps at x = {np.round(x[jumps],4)}")
    print(f"   zeros of u_n^2-u_np1^2 at x = {np.round(x[cross],4)}")
    # check coincidence
    if len(jumps)==len(cross):
        print("   max |jump - zero| =", np.max(np.abs(x[jumps]-x[cross])))
