# -*- coding: utf-8 -*-
"""H3 v57b: structural exploration in float64 (z grows only like j^1/2, safe).
(2) mode constants A=lim u/sqrt(j), B=lim v/sqrt(j), gamma=lim sqrt(j) z^w, w=u-(c/2)v.
(3) ratio u/v -> c/2 and monotonicity.
(4) minimal solution h* backward iteration: h*_0 != 0.
(5) corrected reduced 2nd-order s-recurrence (exact, even)."""
import math
from fractions import Fraction as F

def coeffs_f(c, j, par):
    lam = 4.0/c
    if par=='e':
        Pm=8.0*c*j*j-4.0*c*j+c*c*j/(j-1)
        Qm=4.0*j*(j-1)*(2*j-1)*(2*j-3)+4.0*c*j*(2*j-3)
        Rm=4.0*j*(j-2)*(2*j-3)*(2*j-5)
        Tm=4.0*j*(4*j-5)
    else:
        Pm=8.0*c*j*j+4.0*c*j+c*c*j/(j-1)
        Qm=4.0*j*(j-1)*(2*j-1)*(2*j+1)+4.0*c*j*(2*j-1)
        Rm=4.0*j*(j-2)*(2*j-1)*(2*j-3)
        Tm=4.0*j*(4*j-3)
    a1=Pm/(c*c*j*j*lam)
    a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else 0.0
    return a1,a2,a3,lam,Tm

def solve_z_f(c,par,N,z1,D):
    z=[0.0]*(N+1); z[1]=z1
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
        if D==0.0:
            src=0.0
        else:
            logsrc=math.log(abs(Tm*D))-2*math.lgamma(j+1)-j*math.log(lam)-2*math.log(c)
            src=math.copysign(math.exp(logsrc),Tm*D) if logsrc>-740 else 0.0
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else 0.0)+src
    return z

print("(2)(3) mode constants, both parities, N=20000:")
for par in ('e','o'):
    for c in (1.0,3.0,10.0):
        N=20000
        z1=1.0
        u=solve_z_f(c,par,N,z1,0.0)
        v=solve_z_f(c,par,N,0.0,1.0)
        w=[u[j]-(c/2.0)*v[j] for j in range(N+1)]
        m=15000
        A=u[m]/math.sqrt(m); B=v[m]/math.sqrt(m); G=w[m]*math.sqrt(m)
        ruv=u[m]/v[m]
        mono=True
        prev=u[50]/v[50]
        for j in range(51,3000):
            cur=u[j]/v[j]
            if cur>prev: mono=False; break
            prev=cur
        # sign checks
        upos=all(x>0 for x in u[3:N]); vpos=all(x>0 for x in v[3:N]); wpos=all(x>0 for x in w[3:N])
        print("   par=%s c=%-4g: A=%.8f B=%.8f gamma=%.8f u/v=%.8f (c/2=%g) mono:%s u>0:%s v>0:%s w>0:%s"
              %(par,c,A,B,G,ruv,c/2.0,mono,upos,vpos,wpos))

print()
print("(4) minimal solution h* backward iteration (float), z-ratios at M=2000:")
def backward_f(c,par,M):
    r=[1.0,0.0,0.0]
    for j in range(M,3,-1):
        a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
        newv=(r[0]-a1*r[1]-a2*r[2])/a3
        s=max(abs(newv),1e-300); r=[r[1]/s,r[2]/s,newv/s]
    return r[2],r[1],r[0]
for par in ('e','o'):
    for c in (1.0,3.0,10.0):
        z0,z1,z2=backward_f(c,par,2000)
        print("   par=%s c=%-4g: h* (z0,z1,z2)=(%.6f,%.6f,%.6f) z1/z0=%.10f z2/z0=%.10f"
              %(par,c,z0,z1,z2,z1/z0,z2/z0))

print()
print("(5) corrected reduced 2nd-order s-recurrence (exact Fractions, even, j=3..60):")
c=F(3); par='e'; N=60; lam=F(4)/c
E=[F(1)]*(N+1)
for j in range(1,N+1): E[j]=E[j-1]*(F(1)+F(1)/(F(2)*j))
for (name,nu1,D) in (("u",1,0),("v",0,1)):
    # z-scale init: z1 = nu1/lam
    zz=solve_z_f(3.0,par,60,float(F(nu1)/lam),float(D))
    r=[F(0)]*(N+1)
    for j in range(1,N+1):
        r[j]=F(zz[j]).limit_denominator(10**12)/E[j] if False else F(0)
    # do exact instead: rebuild z exactly
    cF=F(3); z=[F(0)]*(N+1); z[1]=F(nu1)/lam
    for j in range(2,N+1):
        a1,a2,a3,lam2,Tm=coeffs_f(3.0,j,par)
        # exact coefficients
        if par=='e':
            Pm=F(8)*cF*j*j-F(4)*cF*j+cF*cF*F(j,j-1)
            Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*cF*j*(2*j-3)
            Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
            Tm2=F(4)*j*(4*j-5)
        else:
            Pm=F(8)*cF*j*j+F(4)*cF*j+cF*cF*F(j,j-1)
            Qm=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*cF*j*(2*j-1)
            Rm=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
            Tm2=F(4)*j*(4*j-3)
        A1=Pm/(cF*cF*j*j*lam)
        A2=-Qm/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
        A3=(Rm/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
        src=Tm2*D/(cF*cF*F(math.factorial(j))**2*lam**j)
        z[j]=A1*z[j-1]+A2*z[j-2]+(A3*z[j-3] if j>=3 else F(0))+src
    r=[z[j]/E[j] for j in range(N+1)]
    s=[r[j]-r[j-1] for j in range(1,N+1)]
    ok=True; bad=None
    for j in range(3,N+1):
        e1=F(1)+F(1)/(F(2)*j); e2=F(1)+F(1)/(F(2)*(j-1)); e3=F(1)+F(1)/(F(2)*(j-2))
        b2=F(1)/(e1*e2); b3=F(1)/(e1*e2*e3)
        if par=='e':
            Pm=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
            Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
            Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        else:
            Pm=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
            Qm=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
            Rm=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
        a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
        Aj=-(a2*b2+a3*b3); Bj=-a3*b3
        if s[j]!=Aj*s[j-1]+Bj*s[j-2]:
            ok=False; bad=j; break
    print("   %s: s-recurrence exact j=3..%d: %s %s"%(name,N,ok,"" if ok else "FAIL at j=%d"%bad))
