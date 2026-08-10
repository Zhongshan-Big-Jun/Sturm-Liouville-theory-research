import numpy as np

N = 1200
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

def ratio_of(rho, n):
    w, V = fd_eig(rho, n+1)
    return w[n]/w[n-1], w, V

def bm_update(rho, n, w, V, a, A_):
    yn = V[:, n-1]; ynp = V[:, n]
    return np.where(np.abs(yn) >= np.abs(ynp), A_, a)

def run_fp(rho0, n, a, A_, niter=40):
    rho = rho0.copy()
    best = 0.0; bestrho = None
    for it in range(niter):
        r, w, V = ratio_of(rho, n)
        if r > best: best, bestrho = r, rho.copy()
        rho = bm_update(rho, n, w, V, a, A_)
    return best, bestrho, w, V

def jumps_of(rho):
    d = np.nonzero(np.abs(np.diff(rho)) > 1e-9)[0]
    return [round((x[i]+x[i+1])/2, 5) for i in d]

print("=== n=2,3,4: fixed point from symmetric multi-interval starts, R=4 ===")
for n in [2,3,4]:
    best_overall = 0.0
    for start in range(3):
        rho0 = np.ones(N)
        # symmetric start: A on m alternating symmetric intervals
        m = n
        for k in range(1, m+1):
            c0 = (2*k-1)/(2*m+0.0)  # centers around antinode positions
            u = max(0.001, c0-0.045); v = min(0.999, c0+0.045)
            rho0[(x>=u)&(x<=v)] = 4.0
            rho0[(x>=1-v)&(x<=1-u)] = 4.0
        r, rr, w, V = run_fp(rho0, n, 1.0, 4.0)
        best_overall = max(best_overall, r)
        if r > best_overall - 1e-6:
            jp = jumps_of(rr)
            print(f"n={n} start {start}: ratio={r:.6f} jumps={jp}")
    print(f"n={n}: best={best_overall:.6f}")
    print()
