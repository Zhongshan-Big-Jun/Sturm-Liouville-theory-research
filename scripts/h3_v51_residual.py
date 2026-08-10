# -*- coding: utf-8 -*-
"""H3 v51: exact residual R(j) = a1 + a2/(1+s_{j-1}) + a3/((1+s_{j-1})(1+s_{j-2})) - (1+s_j)
and its asymptotic order.  Also R with delta-corrected denominators."""
from fractions import Fraction as F
import math

def a1(j,c):
    P = F(8)*c*j*j - F(4)*c*j + c*c*F(j,j-1)
    return P/(c*c*j*j*(F(4)/c))
def a2(j,c):
    Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
    lam=F(4)/c
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j,c):
    R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    if j==2: return F(0)
    lam=F(4)/c
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

for c in (1,3,10):
    print("=== c=%d ===" % c)
    for j in (10,100,1000,10000):
        sj=F(1)/(F(2)*j); sjm1=F(1)/(F(2)*(j-1)); sjm2=F(1)/(F(2)*(j-2))
        R = a1(j,c) + a2(j,c)/(F(1)+sjm1) + a3(j,c)/((F(1)+sjm1)*(F(1)+sjm2)) - (F(1)+sj)
        print("  j=%6d: R(j)=% .4e  R*j^3=% .4f  R*j^4=% .4f" % (j, float(R), float(R*j**3), float(R*j**4)))
