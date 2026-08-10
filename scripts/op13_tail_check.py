# -*- coding: utf-8 -*-
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

def check_tail(parity, alpha, gamma, cval, N=60):
    cF = F(cval)
    E = [None]*(N+1)
    E[0] = F(1); E[1] = None; E[2] = F(1) + F(alpha)/(F(2)+gamma)
    for j in range(3, N+1):
        E[j] = E[j-1]*(F(1)+F(alpha)/(j+gamma))
    bad = []
    for j in range(5, N+1):  # j>=5: all indices >=2 available
        a1,a2,a3 = a_f(parity, j, cF)
        if E[j] != a1*E[j-1] + a2*E[j-2] + a3*E[j-3]:
            bad.append(j)
    return f"tail-recurrence j>=5 ok, failures at {bad[:5]}"

for parity in ('e','o'):
    a2 = F(1,2) if parity=='e' else F(3,2)
    print(f"parity={parity} alpha={a2} gamma=-1: {check_tail(parity, a2, -1, 3)}")

cF = F(3)
def E_plus(parity, j):
    e = lambda k: F(1)+F(1,2*k) if parity=='e' else F(1)+F(3,2*k)
    E = F(1)
    for k in range(1, j+1): E *= e(k)
    return E
def E_minus(parity, j):
    e = lambda k: F(1)-F(1,2*k) if parity=='e' else F(1)+F(1,2*k)
    E = F(1)
    for k in range(1, j+1): E *= e(k)
    return E
def tail(parity, j):
    a2 = F(1,2) if parity=='e' else F(3,2)
    T = F(1)
    for k in range(2, j+1): T *= F(1) + a2/(k-1)
    return T
for parity in ('e','o'):
    for j in (5, 6, 7):
        Ep, Em = E_plus(parity,j), E_minus(parity,j)
        T = tail(parity, j)
        print(f"parity={parity} j={j}: T/E+={T/Ep}  T/E-={T/Em}")
