# -*- coding: utf-8 -*-
"""EVIDENCE: ratio and H residual at internal switches for the equal-within-type alternating family as r varies.
For n=2,R=4, the conjectured maximum is at r=sqrt(R)=2."""
import numpy as np
from probe_ratio_structure3 import eigs, alt_config, sec_det

def alt_jumps(R, n, r):
    # r = w1 / wR; wR=t
    t=1.0/((n+1)*r+n)
    w1=r*t; wR=t
    jumps=[]; x=0
    for _ in range(n):
        x+=w1; jumps.append(x)
        x+=wR; jumps.append(x)
    vals=[R if i%2==1 else 1.0 for i in range(len(jumps)+1)]
    return jumps, vals

def state_at(jumps, vals, lam, npts=4001):
    xs=[0.0]+list(jumps)+[1.0]
    grid=np.linspace(0,1,npts)
    def one(L):
        s=np.sqrt(L); u,up=0.,1.
        y=np.zeros_like(grid); yp=np.zeros_like(grid)
        for i in range(len(xs)-1):
            L2=xs[i+1]-xs[i]; rr=vals[i]; w=s*np.sqrt(rr)
            sel=(grid>=xs[i])&(grid<=xs[i+1])
            if np.any(sel):
                t=grid[sel]-xs[i]; ph=w*t
                y[sel]=u*np.cos(ph)+up*np.sin(ph)/w
                yp[sel]=-u*w*np.sin(ph)+up*np.cos(ph)
            phi=w*L2
            u,up=u*np.cos(phi)+up*np.sin(phi)/w,-u*w*np.sin(phi)+up*np.cos(phi)
        rho=np.zeros_like(grid)
        for i in range(len(xs)-1): rho[(grid>=xs[i])&(grid<=xs[i+1])]=vals[i]
        norm=np.trapezoid(rho*y*y,grid)
        return y/np.sqrt(norm), yp/np.sqrt(norm)
    return one(lam)

for R in (4.0,10.0):
    for n in (2,3):
        print(f"\nR={R}, n={n}")
        s=np.sqrt(R)
        for r in [0.5,0.8,1.0,1.5,2.0,2.5,3.0,4.0]:
            jumps,vals=alt_jumps(R,n,r)
            lam=eigs(jumps,vals,k=n+2)
            a,b=lam[n-1],lam[n]
            un,unp=state_at(jumps,vals,a)
            un1,un1p=state_at(jumps,vals,b)
            # H at internal switches
            Hvals=[]
            for x in jumps:
                Hvals.append(np.interp(x,np.linspace(0,1,len(un)),un**2-un1**2))
            print(f" r={r:4.1f} ratio={b/a:.6f} Hres={['%.3e'%h for h in Hvals]}")
