import numpy as np

def y1_vec(jumps, vals, lams):
    """Vectorized y(1) for all lam values. lams: array."""
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
        # M = M @ T (matrix mult over last axis)
        M00 = M[0,0]*T[0,0] + M[0,1]*T[1,0]
        M01 = M[0,0]*T[0,1] + M[0,1]*T[1,1]
        M10 = M[1,0]*T[0,0] + M[1,1]*T[1,0]
        M11 = M[1,0]*T[0,1] + M[1,1]*T[1,1]
        M[0,0],M[0,1],M[1,0],M[1,1] = M00,M01,M10,M11
    return M[0,1]

def eigs_step_fast(jumps, vals, k=6, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    # scan grid in sqrt(lam) for better resolution
    npts = 30000
    s = np.linspace(1e-4, np.sqrt(lam_hi), npts)
    d = y1_vec(jumps, vals, s**2)
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(80):
                m = 0.5*(lo+hi)
                dm = y1_vec(jumps, vals, np.array([m**2]))[0]
                if y1_vec(jumps, vals, np.array([lo**2]))[0]*dm <= 0:
                    hi = m
                else:
                    lo = m
            roots.append(((lo+hi)/2)**2)
    return np.array(sorted(roots)[:k])

# time test
import time
t0=time.time()
lam = eigs_step_fast([0.4,0.6],[1.0,4.0,1.0],k=4)
print("time per call: %.4f s" % (time.time()-t0))
print("lam:", np.round(lam,6), "ratio:", lam[1]/lam[0])

# precise max lambda2/lambda1 over symmetric two-step via golden section
def ratio2_sym(c, R):
    if c < 1e-7:
        lam = eigs_step_fast([], [1.0], k=3)
    elif c > 0.5-1e-7:
        lam = eigs_step_fast([], [R], k=3)
    else:
        lam = eigs_step_fast([c,1-c],[1.0,R,1.0],k=3)
    return lam[1]/lam[0]

def golden(f, a, b, tol=1e-10, itmax=200):
    gr = (np.sqrt(5)-1)/2
    c = b - gr*(b-a); d = a + gr*(b-a)
    fc, fd = f(c), f(d)
    for _ in range(itmax):
        if fc > fd:
            a, c, fd = c, d, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, d, fc = d, c, fd
            d = a + gr*(b-a); fd = f(d)
        if b-a < tol: break
    return 0.5*(a+b)

for R in [4.0, 10.0, 100.0]:
    cbest = golden(lambda c: ratio2_sym(c,R), 1e-6, 0.5)
    val = ratio2_sym(cbest, R)
    print(f"R={R}: max lam2/lam1 = {val:.8f} at c={cbest:.8f}, 4*sqrt(R)={4*np.sqrt(R):.4f}, 4R/(pi^2/?) ")
