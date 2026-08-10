# -*- coding: utf-8 -*-
"""Agent C: subclaim 2 - symmetric SUP/INF u*, D values vs 3pi^2, 3pi^2/R."""
import numpy as np
from scipy.optimize import brentq

def M_block(L, c, s):
    w = s*np.sqrt(c); q = np.sqrt(c)
    return np.array([[np.cos(w*L), np.sin(w*L)/q], [-q*np.sin(w*L), np.cos(w*L)]])

def M01_sym(u, R, s, sup):
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    return (M_block(u, c1, s) @ M_block(1-2*u, c2, s) @ M_block(u, c1, s))[0,1]

def lams_sym(u, R, sup, k=3):
    smax = np.pi*np.sqrt(max(1.0, R))*(k+2)+10
    s = np.linspace(1e-9, smax, 150000)
    d = np.array([M01_sym(u, R, x, sup) for x in s])
    sg = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(sg)[0]
    roots = []
    for i in idx[:k]:
        roots.append(brentq(lambda x: M01_sym(u, R, x, sup), s[i], s[i+1]))
    return np.array(roots)

def eig_sym(u, R, sup, s_vals, x):
    """normalized eigenfunctions at x."""
    out = []
    for s in s_vals:
        c1, c2 = (1.0, R) if sup else (R, 1.0)
        # y'(0)=1 solution
        if x <= u:
            y = np.sin(s*np.sqrt(c1)*x)/np.sqrt(c1)
        elif x <= 1-u:
            M1 = M_block(u, c1, s)
            w2 = s*np.sqrt(c2); d = x-u
            M2 = np.array([[np.cos(w2*d), np.sin(w2*d)/np.sqrt(c2)], [-np.sqrt(c2)*np.sin(w2*d), np.cos(w2*d)]])
            Mt = M2 @ M1
            y = Mt[0,1]
        else:
            M12 = M_block(1-2*u, c2, s) @ M_block(u, c1, s)
            w3 = s*np.sqrt(c1); d = x-(1-u)
            M3 = np.array([[np.cos(w3*d), np.sin(w3*d)/1.0], [-1.0*np.sin(w3*d), np.cos(w3*d)]])
            Mt = M3 @ M12
            y = Mt[0,1]
        # norm2 over full interval with density
        nrm = 0.0
        for (L0, c0) in [(u, c1), (1-2*u, c2), (u, c1)]:
            w = s*np.sqrt(c0)
            # need (y, y'/s) at block start; recompute transfer
            pass
        # simpler: numeric integration of the y-solution
        xs = np.linspace(0, 1, 6001)
        yy = np.array([ (lambda xi: (lambda M: M[0,1])( M_block(xi, c1, s) if xi<=u else (M_block(xi-(1-u), c1, s)@M_block(1-2*u,c2,s)@M_block(u,c1,s)) if xi>=1-u else (M_block(xi-u,c2,s)@M_block(u,c1,s)) ))(xi) for xi in xs])
        # above is convoluted; do clean version below
        ys = np.zeros_like(xs)
        for i, xi in enumerate(xs):
            if xi <= u: Mt = M_block(xi, c1, s)
            elif xi <= 1-u: Mt = M_block(xi-u, c2, s) @ M_block(u, c1, s)
            else: Mt = M_block(xi-(1-u), c1, s) @ M_block(1-2*u, c2, s) @ M_block(u, c1, s)
            ys[i] = Mt[0,1]
        rho = np.where((xs>u)&(xs<1-u), c2, c1)
        nrm = np.trapezoid(rho*ys**2, xs)
        out.append(y/np.sqrt(nrm))
    return np.array(out)

def f_at(u, R, sup, s=None):
    if s is None:
        s = lams_sym(u, R, sup, 2)
    uu = eig_sym(u, R, sup, s, u)
    return s[0]**2*uu[0]**2 - s[1]**2*uu[1]**2

def ustar(R, sup):
    # zero of f(u) in (0,1/2); f sign: SUP: f<0 near 0? find sign change
    uu = np.linspace(1e-5, 0.5-1e-5, 400)
    ff = np.array([f_at(u, R, sup) for u in uu])
    sg = np.signbit(ff)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    if len(idx) == 0:
        return None, ff[0], ff[-1]
    # choose the crossing in (0,1/2) -- for SUP f goes - to +; INF f goes + to -?
    # take the first crossing
    lo, hi = uu[idx[0]], uu[idx[0]+1]
    z = brentq(lambda u: f_at(u, R, sup), lo, hi)
    return z, ff[0], ff[-1]

PI2 = np.pi**2
print("R, SUP u*, D(u*), D-3pi^2,  | INF u*, D(u*), D*R, 3pi^2/R - D")
for R in [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 4.0, 10.0, 100.0, 1e4, 1e6]:
    us, f0, f1 = ustar(R, True)
    if us is None:
        print(f"R={R}: SUP no zero (f(0+)={f0:.3e}, f(1/2-)={f1:.3e})"); continue
    s = lams_sym(us, R, True, 2)
    Dsup = s[1]**2 - s[0]**2
    ui, g0, g1 = ustar(R, False)
    si = lams_sym(ui, R, False, 2)
    Dinf = si[1]**2 - si[0]**2
    print(f"R={R:8.1f}: SUP u*={us:.8f} D={Dsup:.8f} D-3pi^2={Dsup-3*PI2:+.6e} | INF u*={ui:.8f} D={Dinf:.8f} D*R={Dinf*R:.8f} 3pi^2/R-D={3*PI2/R-Dinf:+.6e}")
