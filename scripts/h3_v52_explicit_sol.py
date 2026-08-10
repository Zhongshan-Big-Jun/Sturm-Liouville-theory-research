# -*- coding: utf-8 -*-
"""H3 v52: test the exact identity R(j)=0 and the explicit solution
z_j = prod_{k=1..j} (1+1/(2k))."""
from fractions import Fraction as F

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
    print("=== c=%d: R(j) exact zero? ===" % c)
    allzero=True
    for j in range(3,50):
        sj=F(1)/(F(2)*j); sjm1=F(1)/(F(2)*(j-1)); sjm2=F(1)/(F(2)*(j-2))
        R = a1(j,c) + a2(j,c)/(F(1)+sjm1) + a3(j,c)/((F(1)+sjm1)*(F(1)+sjm2)) - (F(1)+sj)
        if R != 0:
            allzero=False; print("  NOT zero at j=%d: %s" % (j, R))
    print("  all zero (j=3..49):", allzero)
    # now verify the explicit solution z_j = prod (1+1/(2k)) satisfies the recurrence exactly
    N=40
    z=[F(0)]*(N+1); z[0]=F(1)
    for j in range(1,N+1):
        z[j]=z[j-1]*(F(1)+F(1)/(F(2)*j))
    ok=True
    for j in range(3,N+1):
        lhs = z[j]
        rhs = a1(j,c)*z[j-1] + a2(j,c)*z[j-2] + a3(j,c)*z[j-3]
        if lhs!=rhs:
            ok=False; print("  recur FAIL j=%d: %s vs %s" % (j, lhs, rhs)); break
    print("  explicit z_j=prod(1+1/(2k)) solves homogeneous z-recurrence exactly:", ok)
    # check j=2
    lhs = z[2]; rhs = a1(2,c)*z[1] + a2(2,c)*z[0]
    print("  j=2 check:", lhs==rhs, lhs, rhs)
