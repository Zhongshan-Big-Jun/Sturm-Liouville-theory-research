# -*- coding: utf-8 -*-
"""H3 v58: corrected mode structure.
- w' = u - 2v (z1=1 normalization) : gamma = lim sqrt(j) z^{w'} and sqrt(j^3) z for odd.
- odd dominant exponent: fit log u vs log j.
- s-recurrence debug at j=3 (exact fractions)."""
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

print("(A) w' = u - 2v, gamma' = lim j^p z^{w'} (p=1/2 even, p=3/2 odd):")
for par in ('e','o'):
    p = 0.5 if par=='e' else 1.5
    for c in (1.0,3.0,10.0):
        N=20000; m=15000
        u=solve_z_f(c,par,N,1.0,0.0)
        v=solve_z_f(c,par,N,0.0,1.0)
        w=[u[j]-2.0*v[j] for j in range(N+1)]
        Gw=w[m]*m**p
        print("   par=%s c=%-4g: gamma'(j^%.1f) = %.8f ; sign(w[3:]) const: %s"
              %(par,c,p,Gw, all((x>0)==(w[3]>0) for x in w[4:N])))

print()
print("(B) dominant exponent fit (log u vs log j, tail):")
for par in ('e','o'):
    for c in (3.0,):
        N=20000; u=solve_z_f(c,par,N,1.0,0.0)
        jj=range(10000,N,50)
        xs=[math.log(j) for j in jj]; ys=[math.log(abs(u[j])) for j in jj]
        n=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*y for x,y in zip(xs,xs)); sxy=sum(x*y for x,y in zip(xs,ys))
        b=(n*sxy-sx*sy)/(n*sxx-sx*sx)
        print("   par=%s: slope=%.6f (expect 0.5 even, 1.5 odd)"%(par,b))

print()
print("(C) s-recurrence debug: values at j=3,4 (exact, even, u):")
c=F(3); par='e'; N=12; lam=F(4)/c
z=[F(0)]*(N+1); z[1]=F(1)/lam
for j in range(2,N+1):
    Pm=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    A1=Pm/(c*c*j*j*lam); A2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    A3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
    z[j]=A1*z[j-1]+A2*z[j-2]+(A3*z[j-3] if j>=3 else F(0))
E=[F(1)]*(N+1)
for j in range(1,N+1): E[j]=E[j-1]*(F(1)+F(1)/(F(2)*j))
r=[z[j]/E[j] for j in range(N+1)]
s=[r[j]-r[j-1] for j in range(1,N+1)]
print("   z[0..5]=",[float(z[j]) for j in range(6)])
print("   r[0..5]=",[float(r[j]) for j in range(6)])
print("   s[1..5]=",[float(s[j]) for j in range(1,6)])
for j in range(3,6):
    e1=F(1)+F(1)/(F(2)*j); e2=F(1)+F(1)/(F(2)*(j-1)); e3=F(1)+F(1)/(F(2)*(j-2))
    b2=F(1)/(e1*e2); b3=F(1)/(e1*e2*e3)
    Pm=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3))
    beta=a2*b2; gamma=a3*b3
    Aj=-(beta+gamma); Bj=-gamma
    print("   j=%d: s[j]=%s  Aj*s[j-1]+Bj*s[j-2]=%s  (beta=%s gamma=%s alpha=a1/e_j=%s)"%(j,str(s[j]),str(Aj*s[j-1]+Bj*s[j-2]),str(beta),str(gamma),str(a1*E[j-1]/E[j])))
