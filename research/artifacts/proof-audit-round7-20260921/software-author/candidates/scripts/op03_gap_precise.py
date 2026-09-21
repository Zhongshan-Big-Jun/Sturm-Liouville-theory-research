# -*- coding: utf-8 -*-
"""#3: high-precision eigenfunction machinery (exact per-block integrals)."""
import numpy as np

def lams_precise(blocks, k, tol=1e-14, s0=None):
    """Eigenvalues via scalar bisection on secular determinant. blocks: [(L, rho)].
    Returns s_j = sqrt(lambda_j), j=0..k-1."""
    def D(s):
        M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
        for L, c in blocks:
            w = s*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        return M01
    # scan for roots
    smax = s0 if s0 else 4*np.pi*np.sqrt(max(c for _, c in blocks)) + 20
    npts = 20000
    s = np.linspace(1e-7, smax, npts)
    ds = np.array([D(ss) for ss in s])
    signs = np.signbit(ds[1:]) != np.signbit(ds[:-1])
    idx = np.nonzero(signs)[0]
    roots = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if D(lo)*D(mid) <= 0: hi = mid
            else: lo = mid
        roots.append(0.5*(lo+hi))
    return np.array(roots)

def eigfuns_precise(blocks, s_vals, x_pts):
    """L^2(rho)-normalized eigenfunctions at x_pts, via exact per-block integrals.
    blocks: [(L, rho)]. Returns array (n_evals, n_pts)."""
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    out = np.zeros((len(s_vals), len(x_pts)))
    for ei, s in enumerate(s_vals):
        # propagate from 0 with (y,y')=(0,1) to block starts
        starts = []
        M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
        starts.append((0.0, M00, M01, M10, M11))
        for L, c in blocks:
            w = s*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            starts.append((xs[len(starts)], M00, M01, M10, M11))
        # normalization: sum over blocks of rho * int (y(x))^2 dx, exact
        norm = 0.0
        for bi, (L, c) in enumerate(blocks):
            x0, M00, M01, M10, M11 = starts[bi]
            w = s*np.sqrt(c)
            # y(x) = M01*cos(w*dx) + M11*sin(w*dx)/w  where dx = x - x0
            A = M01; B = M11/w
            # int_0^L (A cos(w t) + B sin(w t))^2 dt
            I1 = 0.5*L
            Icos = 0.5*(L + np.sin(2*w*L)/(2*w))
            Isin = 0.5*(L - np.sin(2*w*L)/(2*w))
            Icross = np.sin(w*L)**2/(2*w)  # int sin cos = sin^2(wL)/(2w)
            integ = A*A*Icos + B*B*Isin + 2*A*B*Icross
            norm += c*integ
        # evaluate at requested points
        for j, p in enumerate(x_pts):
            bi = max(i for i in range(len(xs)-1) if xs[i] <= p)
            x0, M00, M01, M10, M11 = starts[bi]
            L, c = blocks[bi]
            w = s*np.sqrt(c); d = p - x0
            cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
            n00, n01, n10, n11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            out[ei, j] = n01
        out[ei] /= np.sqrt(norm)
    return out

def f_edges(edges, R, n, sup, k=None):
    """residual f at boundaries (first n) for the alternating structure."""
    bd = np.sort(edges)
    full = np.concatenate((bd, 1 - bd[::-1]))
    xs = np.concatenate(([0.0], full, [1.0]))
    inside = np.zeros(len(xs)-1, dtype=bool)
    for kk in range(n): inside[2*kk+1] = True
    vals = np.where(inside, R if sup else 1.0, 1.0 if sup else R)
    blocks = [(xs[i+1]-xs[i], vals[i]) for i in range(len(xs)-1)]
    s = lams_precise(blocks, n+2)
    lam = s**2
    vals2 = eigfuns_precise(blocks, s[n-1:n+1], np.array(full))
    f = lam[n-1]*vals2[0]**2 - lam[n]*vals2[1]**2
    return f, lam, blocks, full

if __name__ == "__main__":
    # sanity: constant rho=1, n=1: lam = pi^2, 4pi^2
    blocks = [(1.0, 1.0)]
    s = lams_precise(blocks, 3)
    print("const: s^2 =", s**2, " expect 9.8696, 39.4784, 88.8264")
