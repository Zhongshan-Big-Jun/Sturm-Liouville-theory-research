# -*- coding: utf-8 -*-
"""#13(iii) verification v2: combo-family rational ratios with correct c1,c2; minimal f non-rational."""
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

def Ep(zlist, parity):
    b = 1 if parity=='e' else 3
    zlist[0] = F(1)
    for k in range(1, len(zlist)):
        zlist[k] = zlist[k-1]*(F(1)+F(b, 2*k))
def Em(zlist, parity):
    b = -1 if parity=='e' else 1
    zlist[0] = F(1)
    for k in range(1, len(zlist)):
        zlist[k] = zlist[k-1]*(F(1)+F(b, 2*k))

def check(parity, cval, tau, N=30):
    cF = F(cval)
    Eplus = [None]*(N+1); Eminus = [None]*(N+1)
    Ep(Eplus, parity); Em(Eminus, parity)
    E = [ (F(1)+F(j)/(tau+1))*Eminus[j] for j in range(N+1) ]
    # recurrence
    ok = all(E[j] == a_f(parity, j, cF)[0]*E[j-1] + a_f(parity, j, cF)[1]*E[j-2] + a_f(parity, j, cF)[2]*E[j-3] for j in range(3, N+1))
    # rational ratio formula: E = c1*Eplus + c2*Eminus
    if parity == 'e':
        c1 = F(1, 2*(tau+1)); c2 = F(2*tau+1, 2*(tau+1))
        rhs = lambda j: (F(1)-F(1,2*j))*((F(2*j+1)*c1 + c2)/((F(2*j-1))*c1 + c2))
    else:
        c1 = F(3, 2*(tau+1)); c2 = F(2*tau-1, 2*(tau+1))
        rhs = lambda j: (F(1)+F(1,2*j))*((F(2*j+3,3)*c1 + c2)/(F(2*j+1,3)*c1 + c2))
    rok = all(E[j]/E[j-1] == rhs(j) for j in range(2, N+1))
    # check E == c1 Eplus + c2 Eminus
    ek = all(E[j] == c1*Eplus[j] + c2*Eminus[j] for j in range(N+1))
    return ok, rok, ek

print("parity c tau | recurrence | rational-ratio | combo-decomp")
for parity in ('e','o'):
    for cv in (1, 3, 10):
        for tau in (0, 2, F(5,2), -F(1,2), -F(3,2)):
            o, r, ek = check(parity, cv, tau)
            print(f"  {parity} {cv} {tau}   {o}   {r}   {ek}")
