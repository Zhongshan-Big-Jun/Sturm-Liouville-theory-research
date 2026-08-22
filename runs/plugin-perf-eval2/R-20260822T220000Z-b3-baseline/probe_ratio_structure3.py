# -*- coding: utf-8 -*-
"""EVIDENCE probe v3 (robust): ratio switching function H = u_n^2 - u_{n+1}^2.
Uses robust eigenvalue bracketing via sign changes of M01.""" 
import numpy as np

def sec_det(ss, jumps, vals):
    xs=[0.0]+list(jumps)+[1.0]
    M00=np.ones_like(ss); M01=np.zeros_like(ss); M10=np.zeros_like(ss); M11=np.ones_like(ss)
    for i in range(len(xs)-1):
        L=xs[i+1]-xs[i]; r=vals[i]
        w=ss*np.sqrt(r); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        # M_new = M_old * T_block (same as project's det_scan)
        M00,M01,M10,M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M01

def bisect_root(lo, hi, jumps, vals, iters=60):
    for _ in range(iters):
        mid=(lo+hi)/2
        dlo=float(sec_det(np.array([lo]), jumps, vals)[0])
        dmid=float(sec_det(np.array([mid]), jumps, vals)[0])
        if dlo*dmid <= 0:
            hi=mid
        else:
            lo=mid
    return (lo+hi)/2

def eigs(jumps, vals, k=8, npts=40000, smax=25.0):
    ss=np.linspace(1e-7, smax, npts)
    d=sec_det(ss, jumps, vals)
    signs=np.signbit(d[1:]) != np.signbit(d[:-1])
    idx=np.nonzero(signs)[0]
    out=[]
    for i in idx:
        lo,hi=float(ss[i]),float(ss[i+1])
        # further subdivide to ensure single root
        for _ in range(1):
            sg=np.linspace(lo,hi,2000)
            dg=sec_det(sg,jumps,vals)
            s_sub=np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj=np.nonzero(s_sub)[0]
            if len(jj)>0:
                lo,hi=float(sg[jj[0]]),float(sg[jj[0]+1])
        root=bisect_root(lo,hi,jumps,vals,iters=50)
        out.append(root*root)
        if len(out)>=k:
            break
    return np.array(sorted(out)[:k])

def analyze(jumps, vals, n, npts=3000):
    xs=[0.0]+list(jumps)+[1.0]
    lam=eigs(jumps, vals, k=n+2)
    if len(lam)<n+2:
        return None
    a=lam[n-1]; b=lam[n]
    grid=np.linspace(0.0,1.0,npts)
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
        rho=np.zeros_like(grid)
        for i in range(len(xs)-1):
            rho[(grid>=xs[i])&(grid<=xs[i+1])]=vals[i]
        norm=np.trapezoid(rho*y*y,grid)
        return y/np.sqrt(norm), yp/np.sqrt(norm)
    un,unp=state(a); un1,un1p=state(b)
    H=un**2-un1**2
    signs=np.signbit(H[1:]) != np.signbit(H[:-1])
    zcount=int(np.count_nonzero(signs))
    q0=un1p[0]/unp[0]
    q1=un1p[-1]/unp[-1]
    c=np.sqrt(a/b)
    return dict(ratio=b/a, q0=q0, q1=q1, c=c, zcount=zcount, H0=H[0], H1=H[-1], lam=lam)

def alt_config(n, R):
    s=np.sqrt(R); t=1.0/((n+1)*s+n); w1=s*t; wR=t
    jumps=[]; x=0.0
    for _ in range(n):
        x+=w1; jumps.append(x)
        x+=wR; jumps.append(x)
    # keeps all 2n internal points
    vals=[R if i%2==1 else 1.0 for i in range(len(jumps)+1)]
    return jumps, vals

print("=== Alternating [1,R,1,...,1] ===")
for R in (2.0,4.0,10.0):
    print("R=",R)
    for n in (1,2,3,4,5):
        jumps, vals = alt_config(n,R)
        res=analyze(jumps,vals,n)
        if res:
            print(f" n={n}: ratio={res['ratio']:.8f} q0={res['q0']:.6f} q1={res['q1']:.6f} c={res['c']:.6f} zcount={res['zcount']} (2n={2*n}) lam={res['lam']}")

print("=== Random alternating widths (2n+1 blocks) ===")
rng=np.random.default_rng(123)
for n in (2,3):
    for R in (2.0,4.0):
        print("n,R",n,R)
        for trial in range(5):
            w=rng.random(2*n+1)+0.05; w/=w.sum()
            jumps=np.cumsum(w)[:-1]
            vals=[R if i%2==1 else 1.0 for i in range(len(w))]
            res=analyze(jumps,vals,n)
            if res:
                print(f"  trial {trial}: ratio={res['ratio']:.6f} q0={res['q0']:.4f} q1={res['q1']:.4f} z={res['zcount']} (2n={2*n})")
