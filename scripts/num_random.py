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

def build_smooth(coeffs, R, N):
    x = np.linspace(0,1,N)
    v = np.zeros(N)
    for k,c in enumerate(coeffs):
        v += c*np.sin((k+1)*np.pi*x)
    rho = np.clip(1.0 + (R-1.0)*(0.5+0.5*np.tanh(3*v)), 1.0, R)
    return rho

R=4.0; N=800
rng = np.random.default_rng(42)
best = (4.2844435, "symmetric FP")
t0=time.time()
# random smooth via tanh of random trig sums (near bang-bang)
for trial in range(300):
    coeffs = rng.normal(0,1,6)
    rho = build_smooth(coeffs, R, N)
    lam = fd_eigs(rho, N, 4)
    r = lam[2]/lam[1]
    if r > best[0]: best = (r, ("smooth", coeffs))
print(f"random smooth: best lam3/lam2 = {best[0]:.6f} ({time.time()-t0:.0f}s)")

# random bang-bang with 1-4 A-intervals
best2 = (0.0, None)
for trial in range(400):
    nint = rng.integers(1,5)
    pts = np.sort(rng.uniform(0.02, 0.98, 2*nint))
    ints = [(pts[2*i], pts[2*i+1]) for i in range(nint)]
    rho = build(ints, R, N)
    lam = fd_eigs(rho, N, 4)
    r = lam[2]/lam[1]
    if r > best2[0]: best2 = (r, ints)
print(f"random bang-bang: best lam3/lam2 = {best2[0]:.6f} at {best2[1]}")

# MIN direction: inf lam3/lam2. Start from symmetric barrier: A on ends
def Fmin(ints):
    lam = fd_eigs(build(ints,R,N), N, 4)
    return lam[2]/lam[1]
# scan symmetric barrier: A on [0,c]U[1-c,1] (1 param)
bestmin = (1e9, None)
for c in np.linspace(0.02, 0.48, 200):
    r = Fmin([(0.0,c),(1-c,1.0)])
    if r < bestmin[0]: bestmin = (r, c)
print(f"symmetric barrier min lam3/lam2: {bestmin[0]:.5f} at c={bestmin[1]:.3f}")
# also random bang-bang min
bestmin2 = (1e9, None)
for trial in range(300):
    nint = rng.integers(1,5)
    pts = np.sort(rng.uniform(0.02, 0.98, 2*nint))
    ints = [(pts[2*i], pts[2*i+1]) for i in range(nint)]
    r = Fmin(ints)
    if r < bestmin2[0]: bestmin2 = (r, ints)
print(f"random bang-bang min lam3/lam2: {bestmin2[0]:.5f} at {bestmin2[1]}")
