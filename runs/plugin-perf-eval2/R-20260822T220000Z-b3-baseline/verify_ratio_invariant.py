# -*- coding: utf-8 -*-
"""EVIDENCE: check ratio-energy invariant E = b(u_n'^2 + a r u_n^2)
- a(u_{n+1}'^2 + b r u_{n+1}^2) is constant on the alternating maximizer,
and q0 = 1/c, q1 = -1/c, H zero count = 2n (interior)."""
import numpy as np
from probe_ratio_structure3 import eigs, alt_config, sec_det

def states(jumps, vals, lam, npts=4001):
    xs=[0.0]+list(jumps)+[1.0]
    grid=np.linspace(0,1,npts)
    def one(L):
        s=np.sqrt(L); u,up=0.0,1.0
        y=np.zeros_like(grid); yp=np.zeros_like(grid)
        for i in range(len(xs)-1):
            L2=xs[i+1]-xs[i]; r=vals[i]; w=s*np.sqrt(r)
            sel=(grid>=xs[i])&(grid<=xs[i+1])
            if np.any(sel):
                t=grid[sel]-xs[i]; ph=w*t
                y[sel]=u*np.cos(ph)+up*np.sin(ph)/w
                yp[sel]=-u*w*np.sin(ph)+up*np.cos(ph)
            phi=w*L2
            u,up=u*np.cos(phi)+up*np.sin(phi)/w,-u*w*np.sin(phi)+up*np.cos(phi)
        rho=np.zeros_like(grid)
        for i in range(len(xs)-1):
            rho[(grid>=xs[i])&(grid<=xs[i+1])]=vals[i]
        norm=np.trapezoid(rho*y*y,grid)
        return y/np.sqrt(norm), yp/np.sqrt(norm)
    return one(lam)

print("n,R | ratio | q0 | 1/c | q1 | -1/c | Hzeros | E(block1) E(mid) E(block_last) | sign_end")
for R in (2.0,4.0,10.0):
    for n in (1,2,3,4):
        jumps,vals=alt_config(n,R)
        lam=eigs(jumps,vals,k=n+2)
        a,b=lam[n-1],lam[n]
        c=np.sqrt(a/b)
        un,unp=states(jumps,vals,a)
        un1,un1p=states(jumps,vals,b)
        un,unp=un,unp; un1,un1p=un1,un1p
        H=un**2-un1**2
        signs=np.signbit(H[1:]) != np.signbit(H[:-1])
        idx=np.nonzero(signs)[0]
        # interior sign changes; drop 0 and last
        idx=[i for i in idx if 0<i<len(H)-1]
        # E values on first/middle/last blocks
        xs=[0.0]+list(jumps)+[1.0]
        def Eval(x):
            # find block
            k=0
            for i in range(len(xs)-1):
                if xs[i] <= x <= xs[i+1]+1e-12:
                    k=i; break
            r=vals[k]
            # interpolate to y,y' at x (grid)
            j=np.argmin(abs(np.linspace(0,1,len(H))-x))
            return b*(unp[j]**2 + a*r*un[j]**2) - a*(un1p[j]**2 + b*r*un1[j]**2)
        mid=(xs[0]+xs[1])/2
        mid2=(xs[1]+xs[2])/2
        last=(xs[-2]+xs[-1])/2
        q0=un1p[0]/unp[0]; q1=un1p[-1]/unp[-1]
        print(f"{n},{R} | {b/a:.8f} | {q0:.6f} | {1/c:.6f} | {q1:.6f} | {-1/c:.6f} | {len(idx)} (2n={2*n}) | {Eval(mid):.6e} {Eval(mid2):.6e} {Eval(last):.6e} | {np.sign(H[1]):.0f} {np.sign(H[-2]):.0f}")
