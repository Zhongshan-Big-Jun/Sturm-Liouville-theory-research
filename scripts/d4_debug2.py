# -*- coding: utf-8 -*-
from fractions import Fraction as F
import math

c = F(3); lam = F(4)/c

def a1(j,par):
    if par=='e': P=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    else:        P=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
    return P/(c*c*j*j*lam)
def a2(j,par):
    if par=='e': Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    else:        Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j,par):
    if par=='e': R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:        R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

for par in ('e','o'):
    beta = 1 if par=='e' else 3
    # product solution
    E=[F(1)]*(20)
    for j in range(1,20): E[j]=E[j-1]*(F(1)+F(beta)/(F(2)*j))
    e = lambda j: F(1)+F(beta)/(F(2)*j)
    print(f"par={par}:")
    # 1) fixed-point identity at j=3..8
    for j in range(3,9):
        a1v,a2v,a3v = a1(j,par),a2(j,par),a3(j,par)
        lhs = a1v + a2v/e(j-1) + a3v/(e(j-1)*e(j-2))
        print(f"  j={j}: fixed-pt resid = {float(lhs-e(j)):.3e}")
    # 2) E recurrence at j=3..8
    for j in range(3,9):
        a1v,a2v,a3v = a1(j,par),a2(j,par),a3(j,par)
        lhs = E[j]; rhs = a1v*E[j-1]+a2v*E[j-2]+a3v*E[j-3]
        print(f"  j={j}: E-rec resid = {float(lhs-rhs):.3e}")
    # 3) is the issue j=2 (base case)?
    for j in (2,):
        a1v,a2v = a1(j,par),a2(j,par)
        lhs = E[j]; rhs = a1v*E[j-1]+a2v*E[j-2]
        print(f"  j=2: E-rec (a3=0) resid = {float(lhs-rhs):.3e}")
