# -*- coding: utf-8 -*-
"""Session 54i: continuation of R1=0 and R2=0 curves in (a,b)-space.
EVIDENCE only. Uses accurate eigs (global scan + brentq)."""
import numpy as np
from scipy.optimize import brentq, least_squares
from _well_rigid_verify import well_secular_vec

def eigs_acc(a,b,R,k=2,N=1500):
    m=np.sqrt(R); smax=2+k*np.pi*m+4
    sp_=np.linspace(1e-9,smax,N)
    d=well_secular_vec(sp_,a,b,R)
    sg=np.signbit(d[1:])!=np.signbit(d[:-1])
    idx=np.nonzero(sg)[0]
    out=[]
    for i in idx[:k]:
        lo,hi=sp_[i],sp_[i+1]
        out.append(brentq(lambda z: well_secular_vec(z,a,b,R),lo,hi,xtol=1e-13,rtol=1e-13)**2)
    return np.sort(out)[:k]

def norm_closed(a,b,R,s):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    W=lambda t: np.sin(t)**2 + m*m*np.cos(t)**2
    X0=np.sin(A)/m; Y0=np.cos(A)
    nL=a/(2*s*s) - np.sin(2*A)/(4*m*s**3)
    nM=(1/s**3)*(W(A)*psi/(2*m*m) + (X0**2-Y0**2)*np.sin(2*psi)/4 + X0*Y0*np.sin(psi)**2)
    C2=W(A)/W(B)
    nR=C2*((1-b)/(2*s*s) - np.sin(2*B)/(4*m*s**3))
    return nL+nM+nR

def Rs(a,b,R):
    lam=eigs_acc(a,b,R)
    s1=np.sqrt(lam[0]); s2=np.sqrt(lam[1])
    tau=s2/s1; m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    R1=(np.sin(tau*A)**2/n2-np.sin(A)**2/n1)/m**2
    W=lambda t: np.sin(t)**2+m*m*np.cos(t)**2
    C1sq=W(A)/W(B); C2sq=W(tau*A)/W(tau*B)
    R2=(C2sq*np.sin(tau*B)**2/n2 - C1sq*np.sin(B)**2/n1)/m**2
    return R1,R2,tau,A,B,psi,lam[0],lam[1]

def trace_curve(R, start, which, step=0.02, nmax=400, tol=1e-11):
    """trace zero curve of residual 'which' (0->R1, 1->R2) by arclength continuation."""
    pts=[start]
    t=None
    for it in range(nmax):
        a,b=pts[-1]
        # tangent: from previous two points
        if len(pts)>=2:
            v=np.array(pts[-1])-np.array(pts[-2])
            v=v/np.linalg.norm(v)
        else:
            v=np.array([0.0,1.0])
        # predictor
        cand=np.array([a,b])+step*v
        # corrector: solve residual=0 along line perpendicular to v
        def F(ab):
            r1,r2=Rs(ab[0],ab[1],R)[:2]
            return (r1,r2)[which]
        def Jdir(s):
            ab=cand+s*np.array([-v[1],v[0]])
            return F(ab)
        # find s with Jdir(s)=0 by scanning
        ss=np.linspace(-3*step,3*step,41)
        ff=np.array([Jdir(s) for s in ss])
        best=None
        for i in range(len(ss)-1):
            if ff[i]*ff[i+1]<0:
                s0=brentq(Jdir,ss[i],ss[i+1],xtol=1e-12)
                best=cand+s0*np.array([-v[1],v[0]])
                break
        if best is None:
            # try smaller step / fallback
            break
        a2,b2=best
        if not (1e-4<a2<b2<1-1e-4): break
        if np.linalg.norm([a2-a,b2-b])<1e-8: break
        # check not revisiting
        if any(np.linalg.norm(np.array([a2,b2])-np.array(p))<1e-5 for p in pts[-8:]):
            break
        pts.append((a2,b2))
        if it>nmax-3: break
    return pts

R=4.0
a0=0.382598; b0=0.617402
# R1=0 curve through symmetric root: trace both directions
for which,name in [(0,'R1'),(1,'R2')]:
    for sgn in [1,-1]:
        pts=trace_curve(R,(a0,b0),which,step=sgn*0.015,nmax=300)
        # check R2/R1 along curve for zero crossings (good roots)
        print(f"R=4 curve {name} dir={sgn}: {len(pts)} pts, a range [{min(p[0] for p in pts):.4f},{max(p[0] for p in pts):.4f}], b range [{min(p[1] for p in pts):.4f},{max(p[1] for p in pts):.4f}]")
        # endpoints
        for p in [pts[0],pts[-1]]:
            r1,r2,tau,A,B,psi,l1,l2=Rs(*p,R)
            print(f"    pt a={p[0]:.5f} b={p[1]:.5f}: R1={r1:+.3e} R2={r2:+.3e} |A-B|={abs(A-B):.2e} a+b={p[0]+p[1]:.5f}")
