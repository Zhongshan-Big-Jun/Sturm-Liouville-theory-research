# -*- coding: utf-8 -*-
"""EVIDENCE probe: ratio switching function H = u_n^2 - u_{n+1}^2 for
alternating [1,R,...,1] fixed-n configurations and for random bang-bang.
Computes zero count in (0,1), q0, q1, and sign pattern.  Numerical only."""
import numpy as np
from scipy.optimize import brentq

def transfer_apply(M, L, r, s):
    # M is 2x2, phase = s*sqrt(r)*L
    w = s*np.sqrt(r)
    wL = w*L
    cw = np.cos(wL); sw = np.sin(wL)/w
    return M @ np.array([[cw, sw], [-w*np.sin(wL), cw]])

def state_at(jumps, vals, lam, npoints=2000):
    """Return y,y' on grid for a given rho; starts y(0)=0,y'(0)=1, normalized later."""
    xs = [0.0] + list(jumps) + [1.0]
    s = np.sqrt(lam)
    # dense grid for sign tracking
    grid = np.linspace(0.0, 1.0, npoints)
    y = np.zeros_like(grid); yp = np.zeros_like(grid)
    # piecewise analytic propagation
    x0 = 0.0
    u, up = 0.0, 1.0
    grid_idx = 0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; r = vals[i]
        phi = s*np.sqrt(r)*L
        # apply to points in this block
        sel = (grid >= xs[i]) & (grid <= xs[i+1])
        if np.any(sel):
            t = grid[sel] - xs[i]
            ph = s*np.sqrt(r)*t
            # u = u0 cos(ph)+up0 sin(ph)/(s sqrt r)
            w = s*np.sqrt(r)
            y[sel] = u*np.cos(ph) + up*np.sin(ph)/w
            yp[sel] = -u*w*np.sin(ph) + up*np.cos(ph)
        # propagate to endpoint
        w = s*np.sqrt(r)
        u, up = u*np.cos(phi) + up*np.sin(phi)/w, -u*w*np.sin(phi) + up*np.cos(phi)
    return grid, y, yp

def eigs(jumps, vals, k=8, npts=30000):
    xs = [0.0] + list(jumps) + [1.0]
    ss = np.linspace(1e-7, np.sqrt(max(vals)*500), npts)
    d = np.ones_like(ss)*0.0
    # vectorized product
    M00=np.ones_like(ss); M01=np.zeros_like(ss); M10=np.zeros_like(ss); M11=np.ones_like(ss)
    for i in range(len(xs)-1):
        L=xs[i+1]-xs[i]; r=vals[i]
        w=ss*np.sqrt(r); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01,M10,M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out=[]
    for i in idx:
        lo,hi=ss[i],ss[i+1]
        for _ in range(4):
            sg=np.linspace(lo,hi,2000)
            M00=np.ones_like(sg); M01=np.zeros_like(sg); M10=np.zeros_like(sg); M11=np.ones_like(sg)
            for jj in range(len(xs)-1):
                L=xs[jj+1]-xs[jj]; r=vals[jj]
                w=sg*np.sqrt(r); wL=w*L
                cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
                M00,M01,M10,M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            dg=M01
            sg_s=np.signbit(dg[1:])!=np.signbit(dg[:-1])
            jj2=np.nonzero(sg_s)[0]
            if len(jj2)==0: break
            lo,hi=sg[jj2[0]],sg[jj2[0]+1]
        out.append(((lo+hi)/2)**2)
        if len(out)>=k: break
    return np.array(sorted(out)[:k])

def analyze(jumps, vals, n, R):
    lam = eigs(jumps, vals, k=n+3)
    a=lam[n-1]; b=lam[n]
    # normalized states
    grid, un, unp = state_at(jumps, vals, a)
    grid2, un1, un1p = state_at(jumps, vals, b)
    # normalize by integral rho u^2 = 1
    def norm_scale(y, yp, lam):
        xs = [0.0]+list(jumps)+[1.0]
        # approximate integral with grid (trapezoid)
        rho = np.interp(grid, xs, np.array([vals[j] for j in range(len(xs)-1)]+[vals[-1]]))
        # better use index midpoints
        rho = np.empty_like(grid)
        for i in range(len(xs)-1):
            m=(xs[i]+xs[i+1])/2
            # find val
            rv = vals[i]
            rho[(grid>=xs[i])&(grid<=xs[i+1])] = rv
        norm = np.trapz(rho*y*y, grid)
        return 1.0/np.sqrt(norm)
    cn = norm_scale(un, unp, a); cn1 = norm_scale(un1, un1p, b)
    un*=cn; unp*=cn; un1*=cn1; un1p*=cn1
    H = un**2 - un1**2
    # zero count via sign changes in dense grid
    signs = np.signbit(H[1:]) != np.signbit(H[:-1])
    zidx = np.nonzero(signs)[0]
    zlist=[]
    for i in zidx:
        try:
            z = brentq(lambda x: (np.interp(x,grid,un)**2 - np.interp(x,grid,un1)**2), grid[i], grid[i+1])
            zlist.append(z)
        except Exception:
            pass
    q0 = un1[0]/un[0] if un[0]!=0 else None # should avoid endpoint, use derivative
    # use derivatives at 0 from first grid dt
    dt=grid[1]-grid[0]
    q0v=un1p[0]/unp[0]
    q1v=un1p[-1]/unp[-1]
    # at x near 1 use last derivative
    c = np.sqrt(a/b)
    return dict(lam=(a,b), ratio=b/a, q0=q0v, q1=q1v, c=c,
                zcount=len(zlist), expected=2*n if (q0v>1 and q1v<-1) else None,
                zlist=zlist, sign_end=np.sign(H[0] if H[0]!=0 else H[1]),
                sign_end_right=np.sign(H[-1]))

def alt_config(n, R):
    s=np.sqrt(R); t=1.0/((n+1)*s+n); w1=s*t; wR=t
    jumps=[]; x=0.0
    for _ in range(n):
        x+=w1; jumps.append(x)
        x+=wR; jumps.append(x)
    jumps=jumps[:-1]
    vals=[R if i%2==1 else 1.0 for i in range(len(jumps)+1)]
    return jumps, vals

print("=== Alternating [1,R,1,...,1] ===")
for R in (2.0,4.0,10.0):
    print("R=",R)
    for n in (1,2,3,4,5):
        jumps, vals = alt_config(n,R)
        res=analyze(jumps,vals,n,R)
        print(f" n={n}: ratio={res['ratio']:.8f} q0={res['q0']:.6f} q1={res['q1']:.6f} c={res['c']:.6f} zcount={res['zcount']} (2n={2*n})")

print("=== Random bang-bang with 2n+1 alternating [1,R,1,...], random widths ===")
rng=np.random.default_rng(123)
for n in (2,3):
    for R in (2.0,4.0):
        print("n,R",n,R)
        for trial in range(5):
            w = rng.random(2*n+1)+0.05
            w /= w.sum()
            jumps=np.cumsum(w)[:-1]
            vals=[R if i%2==1 else 1.0 for i in range(len(w))]
            res=analyze(jumps,vals,n,R)
            print(f"  trial {trial}: ratio={res['ratio']:.6f} q0={res['q0']:.4f} q1={res['q1']:.4f} z={res['zcount']} (2n={2*n})")
