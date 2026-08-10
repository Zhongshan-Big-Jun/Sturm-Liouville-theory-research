import numpy as np

def fd_eigs(rho, N=2000, k=6):
    """Finite-difference eigenvalues of -u'' = lam*rho*u, u(0)=u(1)=0.
    rho: array of length N (values at interior points). Returns smallest k eigenvalues."""
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    M = np.diag(rho)
    # standardize: w = M^{1/2} v
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]   # M^{-1/2} A M^{-1/2}
    w = np.linalg.eigvalsh(B)
    lam = w[:k]
    return lam

def transfer_step_eigs(jumps, vals, lam_lo=1e-8, lam_hi=1e5, k=8, npts=200000):
    """Exact eigenvalues via transfer matrices for piecewise-constant rho on [0,1].
    jumps: sorted list of interface positions (excluding 0 and 1).
    vals: values of rho on intervals [0,j1], [j1,j2], ..., [jk,1].
    Returns eigenvalues found by bracketing det M(lam)=0 on [lam_lo, lam_hi]."""
    xs = [0.0] + list(jumps) + [1.0]
    def det(lam):
        M = np.eye(2)
        for i in range(len(xs)-1):
            L = xs[i+1]-xs[i]
            c = vals[i]
            w = np.sqrt(lam*c)
            if w*L < 1e-6:
                T = np.array([[1.0, L],[0.0, 1.0]])
            else:
                T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        # y(1)=0: y = a sin + b cos on first interval; y(0)=0 => b=0, a=1
        # value at 1: M[0,0] (since initial [1,0]^T)
        return M[0,0]
    lams = np.linspace(lam_lo, lam_hi, npts)
    d = np.array([det(l) for l in lams])
    roots = []
    for i in range(len(lams)-1):
        if d[i]*d[i+1] < 0:
            a, b = lams[i], lams[i+1]
            for _ in range(60):
                m = 0.5*(a+b)
                if det(a)*det(m) <= 0: b = m
                else: a = m
            roots.append(0.5*(a+b))
    return roots[:k]

# sanity check: constant rho=1
print("FD const rho=1, N=2000:", np.round(fd_eigs(np.ones(2000), 2000, 4), 8))
print("exact n^2 pi^2:        ", np.round(np.array([(n*np.pi)**2 for n in range(1,5)]), 8))
print("transfer const rho=1:  ", np.round(np.array(transfer_step_eigs([], [1.0], k=4)), 8))
