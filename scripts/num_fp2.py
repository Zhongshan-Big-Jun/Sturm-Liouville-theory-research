import numpy as np

N = 700
h = 1.0/(N+1)
x = np.linspace(h, 1-h, N)

def fd_eig(rho, k):
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    w, V = np.linalg.eigh(B)
    return w[:k], V[:, :k]

def fd_ratio(rho, n):
    w, V = fd_eig(rho, n+1)
    return w[n]/w[n-1], w, V

def bangbang_update(rho, n, w, V, a, A_):
    yn = V[:, n-1]; ynp = V[:, n]
    # careful: eigenvector mass normalization differs; ratio test |y_n| vs |y_{n+1}| uses same norm
    return np.where(np.abs(yn) >= np.abs(ynp), A_, a)

def fixed_point(n, a, A_, niter=25, seed=0, smooth=True, njumps=6):
    rng = np.random.default_rng(seed)
    if smooth:
        v = np.zeros(N)
        for kk in range(1,12):
            v += rng.normal(0,1)*np.sin(kk*np.pi*x)
        rho0 = np.clip(a + (A_-a)*(0.5+0.5*np.tanh(1.5*v)), a, A_)
    else:
        jumps = sorted(rng.uniform(0,1, njumps))
        rho0 = np.ones(N)*a
        seg = 0
        for i in range(N):
            while seg < len(jumps) and x[i] > jumps[seg]: seg += 1
            if seg % 2 == 0: rho0[i] = a
            else: rho0[i] = A_
    rho = rho0.copy()
    best = 0.0
    for it in range(niter):
        r, w, V = fd_ratio(rho, n)
        best = max(best, r)
        rho = bangbang_update(rho, n, w, V, a, A_)
    return best, rho, w, V

print("=== fixed-point multi-start: sup lambda_{n+1}/lambda_n, R=4, n=2,3 ===")
for n in [2,3]:
    b1, rho1, w1, V1 = fixed_point(n, 1.0, 4.0, seed=1)
    b2, rho2, w2, V2 = fixed_point(n, 1.0, 4.0, seed=2)
    best = max(b1, b2)
    print(f"n={n}: smooth seeds 1,2 -> {b1:.6f}, {b2:.6f}")
    bj = 0.0
    for s in range(6):
        bb, rhob, wb, Vb = fixed_point(n, 1.0, 4.0, seed=100+s, smooth=False, njumps=2*n+2)
        bj = max(bj, bb)
    print(f"n={n}: bang-bang seeds -> {bj:.6f}")
