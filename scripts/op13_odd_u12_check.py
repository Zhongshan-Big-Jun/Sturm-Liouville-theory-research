# -*- coding: utf-8 -*-
"""Check whether odd u=1/2 branch e_j = (j^2+(tau+1/2)j-(tau+1)/2)/(j^2+tau j)
really satisfies the odd fixed-point identity (suspicious: same branches as even u=1/2)."""
from fractions import Fraction as F

def a_f(parity, j, cF):
    if parity == 'e':
        P = F(8)*cF*j*j - F(4)*cF*j + cF*cF*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3)
        R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        P = F(8)*cF*j*j + F(4)*cF*j + cF*cF*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1)
        R = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    lam = F(4)/cF
    a1 = P/(cF*cF*j*j*lam)
    a2 = -Q/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

def check_family(parity, tau, cval, N=40):
    cF = F(cval)
    # e_j = (j^2 + a*j + b)/(j^2 + cc*j + d), a = u + cc
    u = {'e': F(1,2), 'o': F(1,2)}[parity]
    cc = F(tau)
    a = u + cc
    b = -(F(2)*tau+1)/4 - F(1,4)   # minus branch: -(sqrt(4cc^2+4cc+1)+1)/4 for tau>=-1/2
    d = F(0)
    E = [F(1)]
    for j in range(1, N+1):
        ej = (F(j)*F(j)+a*F(j)+b)/(F(j)*F(j)+cc*F(j)+d)
        E.append(E[-1]*ej)
    bad = []
    for j in range(3, N+1):
        lhs = E[j]
        rhs = a_f(parity, j, cF)[0]*E[j-1] + a_f(parity, j, cF)[1]*E[j-2] + a_f(parity, j, cF)[2]*E[j-3]
        if lhs != rhs:
            bad.append((j, lhs, rhs))
    return bad

for parity in ('e','o'):
    for tau in (0, 1, 2):
        bad = check_family(parity, tau, 1)
        print(parity, "tau=", tau, "minus-branch failures:", len(bad), bad[:3])
