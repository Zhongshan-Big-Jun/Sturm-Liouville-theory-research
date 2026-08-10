import numpy as np

def y1_vec(jumps, vals, lams):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.zeros((2,2,len(lams)))
    M[0,0]=1; M[1,1]=1
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(lams*c, 0.0))
        wL = w*L
        T = np.empty((2,2,len(lams)))
        T[0,0] = np.cos(wL); T[0,1] = np.sin(wL)/w
        T[1,0] = -w*np.sin(wL); T[1,1] = np.cos(wL)
        M00 = M[0,0]*T[0,0] + M[0,1]*T[1,0]
        M01 = M[0,0]*T[0,1] + M[0,1]*T[1,1]
        M10 = M[1,0]*T[0,0] + M[1,1]*T[1,0]
        M11 = M[1,0]*T[0,1] + M[1,1]*T[1,1]
        M[0,0],M[0,1],M[1,0],M[1,1] = M00,M01,M10,M11
    return M

def eigs_full(jumps, vals, k=6, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    npts = 40000
    s = np.linspace(1e-4, np.sqrt(lam_hi), npts)
    d = y1_vec(jumps, vals, s**2)[0,1]
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(80):
                m = 0.5*(lo+hi)
                dm = y1_vec(jumps, vals, np.array([m**2]))[0,1]
                if y1_vec(jumps, vals, np.array([lo**2]))[0,1]*dm <= 0:
                    hi = m
                else:
                    lo = m
            roots.append(((lo+hi)/2)**2)
    return np.array(sorted(roots)[:k])

def eigenfunc(jumps, vals, lam, xgrid):
    """Return eigenfunction values at xgrid (array), normalized L2."""
    xs = [0.0] + list(jumps) + [1.0]
    y = np.zeros(len(xgrid))
    for k, x in enumerate(xgrid):
        # propagate from 0 to x: state [y, y'] = M @ [0,1]
        M = np.eye(2)
        idx = 0
        for i in range(len(xs)-1):
            if x <= xs[i+1] + 1e-15:
                L = x - xs[i]
                break
            L = xs[i+1] - xs[i]
            c = vals[i]
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
            idx = i+1
        c = vals[idx]
        w = np.sqrt(lam*c)
        L = x - xs[idx]
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        y[k] = M[0,1]
    return y

# self-consistency check for n=2 max: symmetric two-step c=0.404, R=4
jumps, vals = [0.404, 0.596], [1.0, 4.0, 1.0]
lam = eigs_full(jumps, vals, k=3)
print("lam:", np.round(lam,6), "ratio:", lam[1]/lam[0])
x = np.linspace(0.001, 0.999, 500)
u1 = eigenfunc(jumps, vals, lam[0], x)
u2 = eigenfunc(jumps, vals, lam[1], x)
# sign pattern of u1^2 - u2^2
d = u1**2 - u2**2
cross = np.where(np.diff(np.sign(d)) != 0)[0]
print("crossings of u1^2-u2^2 at x =", np.round(x[cross],4))
# where is u1^2 > u2^2?
mid = (x > 0.404) & (x < 0.596)
print("u1^2>u2^2 in middle region:", np.all(d[mid] > 0))
print("u1^2>u2^2 on sides:", np.all(d[~mid] < 0))
