# -*- coding: utf-8 -*-
"""#13(ii) fixed: exact d_j identity + two-sided box invariance (float)."""
from fractions import Fraction as F
import random, math

def d_exact_float(j, tau):
    return (1.0-1.0/(2*j))*(float(j+tau+1)/float(j+tau)) - (1.0+1.0/(2*j))

ok = True
for j in range(2, 30):
    for tau in (-1.0, -1.5, 3.0, -0.4, 5.0):
        if j + tau == 0: continue
        lhs = d_exact_float(j, tau)
        rhs = -(tau+0.5)/(j*(j+tau))
        if abs(lhs-rhs) > 1e-12: ok = False
print("d_j = -(tau+1/2)/(j(j+tau)) holds (float):", ok)

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

random.seed(2)
for parity in ('e','o'):
    for cv in (1, 3, 10):
        cF = F(cv)
        if parity=='e':
            alpha = F(2) + F(5)*cv/F(12); beta0 = F(1,2)
        else:
            alpha = F(4) + F(7)*cv/F(20); beta0 = F(1,2)
        nbad_lo = 0; nbad_hi = 0; worst = None
        for trial in range(3000):
            j = random.randint(30, 300)
            d1 = random.uniform(float(beta0)/(j-1)**2, float(alpha)/(j-1))
            d2 = random.uniform(float(beta0)/(j-2)**2, float(alpha)/(j-2))
            a1,a2,a3 = a_f(parity, j, cF)
            b = 1.0 if parity=='e' else 3.0
            e_j = 1.0 + b/(2*j); e1 = 1.0 + b/(2*(j-1)); e2 = 1.0 + b/(2*(j-2))
            rho1 = e1 + d1; rho2 = e2 + d2
            rhoj = float(a1) + float(a2)/rho1 + float(a3)/(rho1*rho2)
            dj = rhoj - e_j
            lo = float(beta0)/j**2; hi = float(alpha)/j
            if dj < lo: nbad_lo += 1; worst = ('lo', j, dj, lo)
            if dj > hi: nbad_hi += 1; worst = ('hi', j, dj, hi)
        print(f"par={parity} c={cv} alpha={float(alpha):.3f}: lo-viol={nbad_lo} hi-viol={nbad_hi} worst={worst}")
