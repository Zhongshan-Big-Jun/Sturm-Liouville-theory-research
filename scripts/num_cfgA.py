import numpy as np

def fd_all(rho, N=3000, k=6):
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

def build(intervals, R, N):
    rho = np.ones(N)
    for lo, hi in intervals:
        rho[int(round(lo*N)):int(round(hi*N))] = R
    return rho

R=4.0; N=3000
x = np.linspace(0,1,N)
cfgA = [(0.249,0.374),(0.626,0.751)]
rho = build(cfgA, R, N)
w, U = fd_all(rho, N, 4)
print("ratio lam3/lam2:", w[2]/w[1])
u2, u3 = U[:,1], U[:,2]
d = u2**2 - u3**2
cross = np.where(np.diff(np.sign(d))!=0)[0]
print("sign-change points:", np.round(x[cross],4))
# sign intervals
print("sign of u2^2-u3^2 on: [0,0.249], [0.249,0.374], [0.374,0.626], [0.626,0.751], [0.751,1]")
for (a,b) in [(0,0.249),(0.249,0.374),(0.374,0.626),(0.626,0.751),(0.751,1.0)]:
    m = (x>a+1e-5)&(x<b-1e-5)
    print(f"  ({a},{b}): sign={np.sign(d[m][0] if len(d[m])>0 else 0):+.0f}  mean d={np.mean(d[m]):.3e}")

# Now check: is FP config a local max? Test perturbation: shrink A-intervals slightly inward
def ratio_of(intervals):
    rho2 = build(intervals, R, 3000)
    w2 = fd_all(rho2, 3000, 4)[0]
    return w2[2]/w2[1]

print("ratio cfgA:", ratio_of(cfgA))
print("ratio shrink inward (0.255,0.369),(0.631,0.745):", ratio_of([(0.255,0.369),(0.631,0.745)]))
print("ratio expand outward (0.243,0.380),(0.620,0.757):", ratio_of([(0.243,0.380),(0.620,0.757)]))
print("ratio shift left  (0.244,0.369),(0.621,0.746):", ratio_of([(0.244,0.369),(0.621,0.746)]))
print("ratio shift right (0.254,0.379),(0.631,0.756):", ratio_of([(0.254,0.379),(0.631,0.756)]))
