import numpy as np

def transfer_step_eigs(jumps, vals, lam_lo=1e-8, lam_hi=1e5, k=8, npts=400000):
    """Exact eigenvalues via transfer matrices for piecewise-constant rho on [0,1].
    Dirichlet: y(0)=y(1)=0. Initial vector [y(0), y'(0)] = [0,1].
    y(1) = M[0,1] (first row, second col) since [y(1), y'(1)]^T = M @ [0,1]^T."""
    xs = [0.0] + list(jumps) + [1.0]
    def y1(lam):
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
        return M[0,1]
    lams = np.linspace(lam_lo, lam_hi, npts)
    d = np.array([y1(l) for l in lams])
    roots = []
    for i in range(len(lams)-1):
        if d[i]*d[i+1] < 0:
            a, b = lams[i], lams[i+1]
            for _ in range(60):
                m = 0.5*(a+b)
                if y1(a)*y1(m) <= 0: b = m
                else: a = m
            roots.append(0.5*(a+b))
    return roots[:k]

# sanity: constant rho = 1
print("transfer const rho=1:", np.round(np.array(transfer_step_eigs([], [1.0], k=4)), 6))
print("exact n^2 pi^2:      ", np.round(np.array([(n*np.pi)**2 for n in range(1,5)]), 6))
