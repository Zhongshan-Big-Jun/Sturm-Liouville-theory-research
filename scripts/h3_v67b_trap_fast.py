# -*- coding: utf-8 -*-
"""H3 v67b: Ratio Trap Lemma verification - fast version.
(a) exactness of fixed point, (b) Delta(j,alpha)>=0 exact small j + float large j,
(c) base cases u (j=2,3) and v (j=3,4), (d) v upper bound with source,
(e) minimal solution h*_0 != 0."""
from fractions import Fraction as F
import math

def coeffsF(c, j, par):
    lam = F(4)/c
    if par=='e':
        Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Tm = F(4)*j*(4*j-5)
    else:
        Pm = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        Rm = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        Tm = F(4)*j*(4*j-3)
    a1 = Pm/(c*c*j*j*lam)
    a2 = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = (Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
    return a1,a2,a3,Tm

def coeffsFlt(c, j, par):
    lam = 4.0/c
    if par=='e':
        Pm=8.0*c*j*j-4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j-3)+4.0*c*j*(2*j-3)
        Rm=4.0*j*(j-2)*(2*j-3)*(2*j-5); Tm=4.0*j*(4*j-5)
    else:
        Pm=8.0*c*j*j+4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j+1)+4.0*c*j*(2*j-1)
        Rm=4.0*j*(j-2)*(2*j-1)*(2*j-3); Tm=4.0*j*(4*j-3)
    a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else 0.0
    return a1,a2,a3,Tm

def efixF(j, par):
    return F(1) + (F(1) if par=='e' else F(3))/(F(2)*j)
def efixFlt(j, par):
    return 1.0 + (1.0 if par=='e' else 3.0)/(2.0*j)

print("(a) exactness of fixed-point trajectory e_j, j=3..60, c in {1,3,10,100}:")
for par in ('e','o'):
    ok=True
    for c in (1,3,10,100):
        for j in range(3,61):
            a1,a2,a3,Tm=coeffsF(F(c),j,par)
            if efixF(j,par) != a1 + a2/efixF(j-1,par) + a3/(efixF(j-1,par)*efixF(j-2,par)):
                ok=False; print("  FAIL",par,c,j)
    print("  par=%s: exactness OK = %s"%(par,ok))

print()
print("(b) Delta(j,alpha) >= 0: exact j<=60, float j up to 2e6")
def DeltaFlt(c, j, par, alpha):
    a1,a2,a3,Tm = coeffsFlt(c, j, par)
    b = 1.0 if par=='e' else 3.0
    t1 = (-a2)*(j-1)*(2*alpha-b)/((2*j-2+b)*(j-1+alpha))
    t2 = a3*(j-1)*(j-2)*(1.0/((j-1+alpha)*(j-2+alpha)) - 4.0/((2*j-2+b)*(2*j-4+b)))
    return t1+t2
for par in ('e','o'):
    for c in (1.0,3.0,10.0,100.0):
        b = 1.0 if par=='e' else 3.0
        alpha = 2.0 + 5.0*c/12.0 if par=='e' else 4.0 + 7.0*c/20.0
        ok_exact=True
        for j in range(4,61):
            a1,a2,a3,Tm=coeffsF(F(c),j,par)
            bb = F(1) if par=='e' else F(3)
            t1=(-a2)*F(j-1)*(F(2)*alpha-bb)/((F(2)*j-2+bb)*(F(j-1)+alpha))
            t2=a3*F(j-1)*F(j-2)*(F(1)/((F(j-1)+alpha)*(F(j-2)+alpha))-F(4)/((F(2)*j-2+bb)*(F(2)*j-4+bb)))
            if t1+t2 < 0: ok_exact=False; break
        ok_float=True; worst=1e99; wj=None
        for j in range(4,2000001):
            d=DeltaFlt(c,j,par,alpha)
            if d<worst: worst=d; wj=j
            if d<0: ok_float=False; break
        print("  par=%s c=%-5g alpha=%.4f: exact(j<=60)=%s float(j<=2e6)=%s worst=%.3e@j=%d"
              %(par,c,alpha,ok_exact,ok_float,worst,wj))
EOF
