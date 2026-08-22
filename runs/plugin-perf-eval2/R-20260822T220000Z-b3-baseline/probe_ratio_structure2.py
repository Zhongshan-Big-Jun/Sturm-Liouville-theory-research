# -*- coding: utf-8 -*-
"""EVIDENCE probe v2 (no scipy): ratio switching function H zero count."""
import numpy as np

def eigs(jumps, vals, k=8, npts=30000):
    xs = [0.0] + list(jumps) + [1.0]
    ss = np.linspace(1e-7, np.sqrt(max(vals)*500), npts)
    M00=np.ones_like(ss); M01=np.zeros_like(ss); M10=np.zeros_like(ss); M11=np.ones_like(ss)
    for i in range(len(xs)-1):
        L=xs[i+1]-xs[i]; r=vals[i]
        w=ss*np.sqrt(r); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01,M10,M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    d=M01
    signs=np.signbit(d[1:]) != np.signbit(d[:-1])
    idx=np.nonzero(signs)[0]
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

def analyze(jumps, vals, n, npts=3000):
    xs = [0.0] + list(jumps) + [1.0]
    lam = eigs(jumps, vals, k=n+2, npts=20000)
    a=lam[n-1]; b=lam[n]
    grid=np.linspace(0.0,1.0,npts)
    # compute states via direct initial value on grid with transfer applied piecewise
    def state(lam):
        s=np.sqrt(lam)
        u,up=0.0,1.0
        y=np.zeros_like(grid); yp=np.zeros_like(grid)
        for i in range(len(xs)-1):
            L=xs[i+1]-xs[i]; r=vals[i]; w=s*np.sqrt(r)
            sel=(grid>=xs[i])&(grid<=xs[i+1])
            if np.any(sel):
                t=grid[sel]-xs[i]; ph=w*t
                y[sel]=u*np.cos(ph)+up*np.sin(ph)/w
                yp[sel]=-u*w*np.sin(ph)+up*np.cos(ph)
            phi=w*L
            u,up = u*np.cos(phi)+up*np.sin(phi)/w, -u*w*np.sin(phi)+up*np.cos(phi)
        # normalize weighted
        rho=np.zeros_like(grid)
        for i in range(len(xs)-1):
            rho[(grid>=xs[i])&(grid<=xs[i+1])]=vals[i]
        norm=np.trapezoid(rho*y*y,grid)
        return y/np.sqrt(norm), yp/np.sqrt(norm)
    un,unp=state(a); un1,un1p=state(b)
    H=un**2-un1**2
    signs=np.signbit(H[1:]) != np.signbit(H[:-1])
    zcount=int(np.count_nonzero(signs))
    # q0,q1 from first/last derivative
    q0=un1p[0]/unp[0]
    q1=un1p[-1]/unp[-1]
    c=np.sqrt(a/b)
    return dict(ratio=b/a, q0=q0, q1=q1, c=c, zcount=zcount, H0=H[0], H1=H[-1])

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
        res=analyze(jumps,vals,n)
        print(f" n={n}: ratio={res['ratio']:.8f} q0={res['q0']:.6f} q1={res['q1']:.6f} c={res['c']:.6f} zcount={res['zcount']} (2n={2*n})")

print("=== Random alternating widths (2n+1 blocks) ===")
rng=np.random.default_rng(123)
for n in (2,3):
    for R in (2.0,4.0):
        print("n,R",n,R)
        for trial in range(5):
            w = rng.random(2*n+1)+0.05
            w /= w.sum()
            jumps=np.cumsum(w)[:-1]
            vals=[R if i%2==1 else 1.0 for i in range(len(w))]
            res=analyze(jumps,vals,n)
            print(f"  trial {trial}: ratio={res['ratio']:.6f} q0={res['q0']:.4f} q1={res['q1']:.4f} z={res['zcount']} (2n={2*n})")
