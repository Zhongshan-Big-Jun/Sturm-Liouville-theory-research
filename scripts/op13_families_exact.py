# -*- coding: utf-8 -*-
"""Corrected exhaustive check of genuine rational-ratio families."""
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

def solves_recurrence(E, parity, cF, N=40):
    for j in range(3, N+1):
        rhs = a_f(parity, j, cF)[0]*E[j-1] + a_f(parity, j, cF)[1]*E[j-2] + a_f(parity, j, cF)[2]*E[j-3]
        if E[j] != rhs:
            return False
    return True

def build_ratios(ratios, N):
    E = [F(1)]
    for j in range(1, N+1):
        E.append(E[-1]*ratios(j))
    return E

cF = F(1)
base = {'e': F(-1,2), 'o': F(1,2)}   # rigid-base factor: e = 1 + base/j
print("=== E^(tau) families: e_j = (1 + base/j)((tau+1+j)/(tau+j)) ===")
for parity in ('e','o'):
    bb = base[parity]
    for tau in (0, 2, F(5,2), -F(1,2), -F(3,2)):
        E = build_ratios(lambda j, tau=tau, bb=bb: (F(1)+F(bb)/j)*(F(j+tau+1)/F(j+tau)), 40)
        print(f"  {parity} tau={tau}: {solves_recurrence(E, parity, cF)}")

print("=== E+ / E- ===")
# even: E+ = 1+1/(2j), E- = 1-1/(2j); odd: E+ = 1+3/(2j), E- = 1+1/(2j)
for parity in ('e','o'):
    for name, b in (('E+', {'e':1,'o':3}[parity]), ('E-', {'e':-1,'o':1}[parity])):
        E = build_ratios(lambda j, b=b: F(1)+F(b,2*j), 40)
        print(f"  {parity} {name} (b={b}): {solves_recurrence(E, parity, cF)}")

print("=== odd E^(tau) in 4-param form a=tau+3/2, b=(tau+1)/2, cc=tau, d=0 ===")
for tau in (0, 1, 2, -F(1,2)):
    cc = F(tau); a = F(3,2)+cc; b = (cc+1)/2; d = F(0)
    E = [F(1)]
    for j in range(1, 41):
        ej = (F(j)*F(j)+a*F(j)+b)/(F(j)*F(j)+cc*F(j)+d)
        E.append(E[-1]*ej)
    print(f"  tau={tau}: {solves_recurrence(E, 'o', cF)}")

print("=== even u=-1/2 4-param: b=-cc/2, d=0 (E^- rep) ===")
for tau in (0, 1, 2):
    cc = F(tau); a = -F(1,2)+cc; b = -cc/2; d = F(0)
    E = [F(1)]
    for j in range(1, 41):
        ej = (F(j)*F(j)+a*F(j)+b)/(F(j)*F(j)+cc*F(j)+d)
        E.append(E[-1]*ej)
    print(f"  tau={tau}: {solves_recurrence(E, 'e', cF)}")
