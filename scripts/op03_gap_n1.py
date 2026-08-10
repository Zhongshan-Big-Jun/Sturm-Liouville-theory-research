# -*- coding: utf-8 -*-
"""#3 gap exploration: sup/inf of lambda_{n+1}-lambda_n over rho in [1,R].
Variational prediction: rho* = R on {lambda_n u_n^2 > lambda_{n+1} u_{n+1}^2} (sup),
rho* = 1 there (inf). n=1 => 3-block [1,R,1] / [R,1,R] with self-consistency.
"""
import numpy as np

def lams_blocks(blocks, k=6, npts=40000, smax=200.0):
    """blocks = list of (width, rho). Returns first k eigenvalues."""
    s = np.linspace(1e-9, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for L, c in blocks:
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(lo, hi, 2000)
            M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
            for L, c in blocks:
                w = sg*np.sqrt(c); wL = w*L
                cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
                M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            dg = M01
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            j2 = np.nonzero(sg_s)[0]
            if len(j2) == 0: break
            lo, hi = sg[j2[0]], sg[j2[0]+1]
        out.append(((lo+hi)/2)**2)
    return np.sort(out)[:k]

def eigfuns_at(blocks, lam, points):
    """For eigenvalues lam (array), compute L^2(rho)-normalized eigenfunctions at points.
    points: array of x coords (sorted). Returns (u values at points, normalized)."""
    s = np.sqrt(lam)
    res = np.zeros((len(s), len(points)))
    for i, (L, c) in enumerate(blocks):
        x0 = sum(w for w, _ in blocks[:i])
        # evaluate at points within this block: need y(x), y'(x) via propagator from 0
        pass
    # build propagator to each requested point
    xs = [0.0]
    for L, c in blocks:
        xs.append(xs[-1] + L)
    # compute y(x) for Dirichlet y(0)=0, y'(0)=1: (y,y')^T = M(0->x) (0,1)^T
    for j, p in enumerate(points):
        bi = max(i for i in range(len(xs)-1) if xs[i] <= p)
        x0 = xs[bi]
        # propagate from 0 to x0 through full blocks 0..bi-1
        M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
        for L, c in blocks[:bi]:
            w = s*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        L, c = blocks[bi]
        w = s*np.sqrt(c); d = p - x0
        cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
        n00, n01, n10, n11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        y = n01  # (0,1) initial
        res[:, j] = y
    # L2(rho) norm: integrate rho*y^2 over [0,1]
    norm = np.zeros(len(s))
    for j in range(len(points)-1):
        pass
    # integrate using trapezoid on a fine grid per block
    for bi, (L, c) in enumerate(blocks):
        x0 = xs[bi]
        # sample inside block
        ns = 200
        xsamp = x0 + L*np.linspace(0, 1, ns+1)
        ysamp = np.zeros((len(s), ns+1))
        for si, ss in enumerate(s):
            yv = np.zeros(ns+1)
            # propagate 0 -> x0
            M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
            for L2, c2 in blocks[:bi]:
                w = ss*np.sqrt(c2); wL = w*L2
                cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
                M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            for jj, xx in enumerate(xsamp):
                d = xx - x0
                w = ss*np.sqrt(c); 
                cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
                n00, n01, n10, n11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
                yv[jj] = n01
            ysamp[si] = yv
        # trapezoid
        for si in range(len(s)):
            norm[si] += c * np.trapezoid(ysamp[si]**2, xsamp)
    return res / np.sqrt(norm)[:, None]

if __name__ == "__main__":
    R = 4.0
    # n=1 max: [1,R,1], central width v, u=(1-v)/2.  Scan u.
    print("=== n=1, R=4: max config [1,R,1], scan u = end width ===")
    results = []
    for u in np.linspace(0.05, 0.48, 44):
        v = 1 - 2*u
        blocks = [(u, 1.0), (v, R), (u, 1.0)]
        lam = lams_blocks(blocks, k=3)
        pts = np.array([u, 0.5, 1-u])
        vals = eigfuns_at(blocks, lam[:2], pts)
        u1, u2 = vals[0], vals[1]
        f_junc = lam[0]*u1[0]**2 - lam[1]*u2[0]**2   # at x = u
        results.append((u, lam[1]-lam[0], f_junc))
    for u, D, f in results:
        print(f"u={u:.4f}  D={D:.6f}  f_junc={f:+.4e}")
    # find f=0 crossings
    for i in range(1, len(results)):
        if results[i-1][2]*results[i][2] < 0:
            print(f"  -> f=0 crossing between u={results[i-1][0]:.4f} and u={results[i][0]:.4f}")
