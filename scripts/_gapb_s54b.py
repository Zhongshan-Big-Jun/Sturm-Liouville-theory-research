# -*- coding: utf-8 -*-
"""Session 54b: fast continuation-based exhaustive critical point search.
EVIDENCE only.
"""
import numpy as np
from scipy.optimize import brentq, least_squares
from _well_rigid_verify import well_secular_vec

def Fsec(s,a,b,R):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    return (np.cos(psi)*np.sin(A)+m*np.sin(psi)*np.cos(A))*np.cos(B) \
         + (-np.sin(psi)*np.sin(A)/m+np.cos(psi)*np.cos(A))*np.sin(B)

def eigs_cont(a,b,R,prev):
    """find s1<s2 using continuation brackets prev=(s1,s2) if plausible."""
    m=np.sqrt(R)
    out=[]
    for k,(p0,lo,hi) in enumerate([(prev[0],1e-9,1e9),(prev[1],1e-9,1e9)]):
        if p0 is not None and 1e-9<p0<1e9:
            w=max(0.02, 0.15*p0)
            if Fsec(p0-w,a,b,R)*Fsec(p0+w,a,b,R)<0:
                out.append(brentq(lambda z:Fsec(z,a,b,R), p0-w,p0+w, xtol=1e-13,rtol=1e-13)**2); continue
        # fallback: scan window around p0 or global
        lo2=max(1e-9,p0-4 if p0 else 1e-9); hi2=p0+4 if p0 else 2+k*np.pi*m+4
        sp_=np.linspace(lo2,hi2,400)
        d=Fsec(sp_,a,b,R); sg=np.signbit(d[1:])!=np.signbit(d[:-1]); idx=np.nonzero(sg)[0]
        if len(idx)>k:
            i=idx[k]; out.append(brentq(lambda z:Fsec(z,a,b,R),sp_[i],sp_[i+1],xtol=1e-13,rtol=1e-13)**2); continue
        # global fallback
        sp_=np.linspace(1e-9,2+k*np.pi*m+4,1200)
        d=Fsec(sp_,a,b,R); sg=np.signbit(d[1:])!=np.signbit(d[:-1]); idx=np.nonzero(sg)[0]
        if len(idx)>k:
            i=idx[k]; out.append(brentq(lambda z:Fsec(z,a,b,R),sp_[i],sp_[i+1],xtol=1e-13,rtol=1e-13)**2)
        else:
            out.append(np.nan)
    return out

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

def res_ab(ab,R):
    a,b=ab
    lam=eigs_cont(a,b,R,(None,None))
    s1=np.sqrt(lam[0]); s2=np.sqrt(lam[1])
    tau=s2/s1; m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    R1=(np.sin(tau*A)**2/n2-np.sin(A)**2/n1)/m**2
    W=lambda t: np.sin(t)**2+m*m*np.cos(t)**2
    C1sq=W(A)/W(B); C2sq=W(tau*A)/W(tau*B)
    R2=(C2sq*np.sin(tau*B)**2/n2 - C1sq*np.sin(B)**2/n1)/m**2
    return np.array([R1,R2])

def full(a,b,R):
    lam=eigs_cont(a,b,R,(None,None))
    s1=np.sqrt(lam[0]); s2=np.sqrt(lam[1])
    tau=s2/s1; m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    Xb1=np.cos(psi)*np.sin(A)/m+np.sin(psi)*np.cos(A)
    Xb2=np.cos(tau*psi)*np.sin(tau*A)/m+np.sin(tau*psi)*np.cos(tau*A)
    h_a=np.sin(tau*A)/(tau*np.sin(A)); h_b=Xb2/(tau*Xb1)
    return dict(a=a,b=b,lam1=lam[0],lam2=lam[1],s1=s1,s2=s2,tau=tau,A=A,B=B,psi=psi,
                n1=n1,n2=n2,ha=h_a,hb=h_b,sg=(h_a>0 and h_b<0))

import time
for R in [1.52,1.6,2.0,3.0,4.0,10.0,100.0]:
    t0=time.time()
    ng=55
    aa=np.linspace(0.004,0.8,ng); bb=np.linspace(0.004,0.996,ng)
    found=[]
    for a in aa:
        for b in bb:
            if not (a+0.004 < b < 0.996): continue
            r=res_ab(np.array([a,b]),R)
            if max(abs(r))<0.05:  # coarse attractor
                sol=least_squares(lambda ab:res_ab(ab,R),[a,b],bounds=([1e-3,1e-3],[0.999,0.999]),xtol=1e-12,ftol=1e-12,max_nfev=60)
                a2,b2=sol.x
                if 1e-3<a2<b2<0.999:
                    r2=res_ab(np.array([a2,b2]),R)
                    if max(abs(r2))<1e-9:
                        key=(round(a2,4),round(b2,4))
                        if not any(abs(key[0]-f[0])<3e-3 and abs(key[1]-f[1])<3e-3 for f in found):
                            found.append((a2,b2))
    print(f"R={R}: {len(found)} critical pts in {time.time()-t0:.0f}s")
    for (a,b) in found:
        d=full(a,b,R)
        print(f"   (a,b)=({a:.6f},{b:.6f}) a+b={a+b:.6f} sg={d['sg']} D={d['lam2']-d['lam1']:.6f} tau={d['tau']:.4f} |A-B|={abs(d['A']-d['B']):.1e}")
