import numpy as np

def fd_eigs_vectors(rho, N=2000, k=3):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    w, V = np.linalg.eigh(B)
    # eigenvectors of B = M^{1/2} u; u = M^{-1/2} v
    U = V[:, :k] / s[:, None]
    return w[:k], U, h

# config
R=4.0; c=0.404
N=2000
rho = np.full(N, 1.0); i0=int(round(c*N)); i1=int(round((1-c)*N)); rho[i0:i1]=R
w, U, h = fd_eigs_vectors(rho, N, 3)
x_fd = np.linspace(h, 1-h, N)
print("FD lam:", np.round(w,5), "ratio:", w[1]/w[0])
u1 = U[:,0]; u2 = U[:,1]
# normalize u1 to have u1'(0)=1-ish? just look at sign of diff near ends
d = u1**2 - u2**2
print("sign of u1^2-u2^2 near left end (first 30 pts):", np.sign(d[:30]))
print("sign near right end:", np.sign(d[-30:]))
print("x_fd[0:3]:", x_fd[:3], "x_fd[-3:]:", x_fd[-3:])
print("ratio u1/u2 near left:", u1[:10]/u2[:10])
# find crossing points
cross = np.where(np.diff(np.sign(d)) != 0)[0]
print("crossings:", np.round(x_fd[cross],5))
# where u1^2 - u2^2 > 0
print("frac where u1^2>u2^2:", np.mean(d > 0))
