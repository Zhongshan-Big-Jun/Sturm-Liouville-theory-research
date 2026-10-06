# Source excerpt: scripts/op03_gap_fixed.py at ec45bf99, fetched turn394.
import numpy as np

def lams_precise(blocks, k, tol=1e-15, smax_scale=5.0):
    def D(s):
        M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
        for L, c in blocks:
            w = s*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
        return M01
    smax = np.pi*np.sqrt(max(c for _, c in blocks))* (k+2) + 20
    npts = 30000
    s = np.linspace(1e-7, smax, npts)
    ds = np.array([D(ss) for ss in s])
    signs = np.signbit(ds[1:]) != np.signbit(ds[:-1])
    idx = np.nonzero(signs)[0]
    roots = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(90):
            mid = 0.5*(lo+hi)
            if D(lo)*D(mid) <= 0: hi = mid
            else: lo = mid
        roots.append(0.5*(lo+hi))
    return np.array(roots)
