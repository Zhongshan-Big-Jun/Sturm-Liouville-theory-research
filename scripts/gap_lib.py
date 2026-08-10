# -*- coding: utf-8 -*-
"""gap_lib.py: fast exact TM solver for block-constant rho (used by session 13 proofs)."""
import numpy as np
from scipy.linalg import eigh

def lams_fast(blocks, k, npts=30000, smax=None):
    """First k eigenvalues (as s=sqrt(lam)) of Dirichlet -y''=s^2 rho y, block-constant rho."""
    if smax is None:
        smax = np.pi*np.sqrt(max(c for _, c in blocks))*(k+2) + 20
    s = np.linspace(1e-7, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for L, c in blocks:
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    cs = np.array([c for _, c in blocks]); Ls = np.array([L for L, _ in blocks])
    roots = []
    for i in idx[:k]:
        lo, hi = s[i], s[i+1]
        for _ in range(3):
            sg = np.linspace(lo, hi, 700)
            w = sg[:,None]*np.sqrt(cs[None,:]); wL = w*Ls[None,:]
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
            for jj in range(len(blocks)):
                M00, M01, M10, M11 = cw[:,jj]*M00+sw[:,jj]*M10, cw[:,jj]*M01+sw[:,jj]*M11, sw2[:,jj]*M00+cw[:,jj]*M10, sw2[:,jj]*M01+cw[:,jj]*M11
            dg = M01
            sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            j2 = np.nonzero(sg_s)[0]
            if len(j2) == 0: break
            lo, hi = sg[j2[0]], sg[j2[0]+1]
        roots.append(0.5*(lo+hi))
    return np.sort(np.array(roots))[:k]

def blocks_xs(blocks):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    return xs

def y_at(blocks, s, pts):
    """unnormalized Dirichlet y (y(0)=0,y'(0)=1) at pts."""
    xs = blocks_xs(blocks)
    out = np.zeros(len(pts))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs)-1) if xs[i] <= p)
        M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
        for L, c in blocks[:bi]:
            w = s*np.sqrt(c); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
        L, c = blocks[bi]; w = s*np.sqrt(c); d = p - xs[bi]
        cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
        out[j] = M01
    return out

def norm2(blocks, s):
    xs = blocks_xs(blocks)
    nrm = 0.0
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    for bi, (L, c) in enumerate(blocks):
        w = s*np.sqrt(c)
        A = M01; B = M11/w
        Icos = 0.5*(L + np.sin(2*w*L)/(2*w)); Isin = 0.5*(L - np.sin(2*w*L)/(2*w)); Icross = np.sin(w*L)**2/(2*w)
        nrm += c*(A*A*Icos + B*B*Isin + 2*A*B*Icross)
        wL = w*L; cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    return nrm

def eigfuns(blocks, s_vals, x_pts):
    """L2(rho)-normalized eigenfunctions at x_pts."""
    out = np.zeros((len(s_vals), len(x_pts)))
    for ei, s in enumerate(s_vals):
        y = y_at(blocks, s, np.asarray(x_pts, dtype=float))
        out[ei] = y/np.sqrt(norm2(blocks, s))
    return out

def fd_check(rho, N=1201):
    """FD generalized eigenproblem for arbitrary rho (cross-check)."""
    xs = np.linspace(0,1,N); h = xs[1]-xs[0]
    r = rho(xs)
    n = N-2
    A = 2*np.eye(n) - np.diag(np.ones(n-1),1) - np.diag(np.ones(n-1),-1)
    B = np.diag(h*h*r[1:-1])
    w, V = eigh(A, B)
    lam = w[:2]
    u = []
    for k in range(2):
        y = np.zeros(N); y[1:-1] = V[:,k]
        nrm = np.sqrt(np.trapezoid(rho(xs)*y**2, xs))
        u.append(y/nrm)
    return lam, u, xs
