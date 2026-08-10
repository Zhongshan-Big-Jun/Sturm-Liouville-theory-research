import numpy as np, time

def fd_eigs(rho, N=800, k=6):
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

R=4.0; N=800
rng = np.random.default_rng(7)
best = (0.0, None)
t0=time.time()
for trial in range(200):
    nint = rng.integers(5, 16)
    pts = np.sort(rng.uniform(0.005, 0.995, 2*nint))
    ints = [(pts[2*i], pts[2*i+1]) for i in range(nint)]
    rho = build(ints, R, N)
    lam = fd_eigs(rho, N, 4)
    r = lam[2]/lam[1]
    if r > best[0]: best = (r, nint, ints)
print(f"many-interval random bang-bang: best lam3/lam2 = {best[0]:.5f} (nint={best[1]})  [symmetric FP = 4.2844] ({time.time()-t0:.0f}s)")

# precise 2D scan for lambda3/lambda2 at R=4: symmetric config (x1,x2), grid
def ratio_sym2(x1, x2, R, N=600):
    rho = np.ones(N)
    rho[int(round(x1*N)):int(round(x2*N))] = R
    rho[int(round((1-x2)*N)):int(round((1-x1)*N))] = R
    lam = fd_eigs(rho, N, 4)
    return lam[2]/lam[1]

best = (0.0, None)
g = np.linspace(0.02, 0.48, 50)
t0=time.time()
for x1 in g:
    for x2 in g:
        if x2 <= x1+0.01: continue
        r = ratio_sym2(x1, x2, 4.0)
        if r > best[0]: best = (r, (x1,x2))
print(f"R=4 lambda3/lambda2 symmetric 2-interval: max={best[0]:.5f} at {best[1]} ({time.time()-t0:.0f}s)")
