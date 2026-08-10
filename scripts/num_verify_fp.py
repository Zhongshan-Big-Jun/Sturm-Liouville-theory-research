import numpy as np

def fd_eigs(rho, N=2000, k=8):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def build_int(intervals, R, N):
    """intervals: list of (lo, hi) where rho=R; else 1."""
    rho = np.ones(N)
    for lo, hi in intervals:
        rho[int(round(lo*N)):int(round(hi*N))] = R
    return rho

R=4.0; N=2000
# fixed point configs from iteration
configs = {
  "lam3/lam2 FP": (2, [ (0.249,0.374),(0.626,0.751) ]),
  "lam4/lam3 FP": (3, [ (0.182,0.272),(0.455,0.545),(0.728,0.818) ]),
  "lam5/lam4 FP": (4, [ (0.143,0.213),(0.357,0.428),(0.572,0.643),(0.787,0.857) ]),
}
for name,(idx, ints) in configs.items():
    rho = build_int(ints, R, N)
    lam = fd_eigs(rho, N, 8)
    print(f"{name}: ratio lam{idx+1}/lam{idx} = {lam[idx]/lam[idx-1]:.5f}  (lambda {idx+1}={lam[idx]:.3f}, lambda {idx}={lam[idx-1]:.3f})")

# also 1-interval best known:
print("1-interval symmetric well lam3/lam2 (c=0.285):", fd_eigs(build_int([(0.285,0.715)],R,N),N,4)[2]/fd_eigs(build_int([(0.285,0.715)],R,N),N,4)[1])
print("1-interval asymmetric (0.66,0.77) lam3/lam2:", fd_eigs(build_int([(0.66,0.77)],R,N),N,4)[2]/fd_eigs(build_int([(0.66,0.77)],R,N),N,4)[1])
