# -*- coding: utf-8 -*-
"""H3 v49b: CORRECTED ratio induction coefficients.
z_j = a1 z_{j-1} + a2 z_{j-2} + a3 z_{j-3}
a1 = P/(c^2 j^2 lam), a2 = -Q/(c^2 j^2 (j-1)^2 lam^2), a3 = R/(c^2 j^2 (j-1)^2 (j-2)^2 lam^3)."""
from fractions import Fraction as F

def a1e(j,c):
    P = F(8)*c*j*j - F(4)*c*j + c*c*F(j,j-1)
    lam = F(4)/c
    return P/(c*c*j*j*lam)
def a2e(j,c):
    Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
    lam = F(4)/c
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3e(j,c):
    R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    if j==2: return F(0)
    lam = F(4)/c
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

for c in (1,3,10):
    print("=== c=%d ===" % c)
    bad=[]
    for j in range(2,5001):
        sjm1 = F(1)/(F(2)*(j-1))
        sj   = F(1)/(F(2)*j)
        Fv = a1e(j,c) + a2e(j,c)/(F(1)+sjm1) - (F(1)+sj)
        if Fv < 0: bad.append((j,float(Fv)))
    print("  F(j)=a1+a2/(1+s_{j-1})-(1+s_j) < 0 for j in [2,5000]:", bad[:4], "count:", len(bad))
    for j in (10,100,1000):
        sjm1 = F(1)/(F(2)*(j-1)); sj=F(1)/(F(2)*j)
        Fv = a1e(j,c) + a2e(j,c)/(F(1)+sjm1) - (F(1)+sj)
        print("    j=%5d: F(j)=% .6e  F(j)*j=% .6f  F(j)*j^2=% .6f" % (j, float(Fv), float(Fv*j), float(Fv*j*j)))
    # check the a3 term size: a3/((1+s_{j-1})(1+s_{j-2}))
    for j in (10,100,1000):
        a3v = a3e(j,c)/((F(1)+F(1)/(F(2)*(j-1)))*(F(1)+F(1)/(F(2)*(j-2))))
        print("    j=%5d: a3/((1+s)(1+s)) = % .6e" % (j, float(a3v)))
