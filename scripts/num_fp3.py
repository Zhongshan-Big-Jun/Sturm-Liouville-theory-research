import numpy as np

N = 900
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

def run_fp(rho0, n, a, A_, niter=30, label=""):
    rho = rho0.copy()
    print(f"--- {label}: n={n} ---")
    prev = None
    for it in range(niter):
        r, w, V = ratio_of(rho, n)
        if it % 5 == 0 or it == niter-1:
            print(f"  it {it:2d}: ratio={r:.6f}  jumps={np.sum(np.abs(np.diff(rho))>1e-9)}")
        rho = bm_update(rho, n, w, V, a, A_)
    return rho, w, V

# start from best symmetric 2-interval
rho0 = np.ones(N)
rho0[(x>=0.2526)&(x<=0.3751)] = 4.0
rho0[(x>=0.6249)&(x<=0.7474)] = 4.0
run_fp(rho0, 2, 1.0, 4.0, label="from best sym 2-int")

# start from 3-interval symmetric guess
rho0 = np.ones(N)
for (u1,v1,u2,v2) in [(0.15,0.22,0.38,0.45)]:
    rho0[(x>=u1)&(x<=v1)] = 4.0
    rho0[(x>=1-v1)&(x<=1-u1)] = 4.0
    rho0[(x>=u2)&(x<=v2)] = 4.0
    rho0[(x>=1-v2)&(x<=1-u2)] = 4.0
run_fp(rho0, 2, 1.0, 4.0, label="from 4-symmetric-int guess")

# start from periodic double well (2 periods)
rho0 = np.ones(N)
c = 0.4001
for u,v in [(c/2,(1-c)/2), ((1+c)/2,(2-c)/2)]:
    rho0[(x>=u)&(x<=v)] = 4.0
run_fp(rho0, 2, 1.0, 4.0, label="from period-2 double well")
