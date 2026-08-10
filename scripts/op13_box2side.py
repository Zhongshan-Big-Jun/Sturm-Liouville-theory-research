# -*- coding: utf-8 -*-
"""#13(ii): two-sided box invariance check for the homogeneous ratio map.
Claim: the region beta/j^2 <= d_j <= alpha/j (d_j = rho_j - e_j) is forward-invariant
for the homogeneous map with suitable (alpha, beta) for large j.
Also verify: d_j = -(tau+1/2)/(j(j+tau)) for the E^(tau) family (exact)."""
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

# exact d_j for E^(tau) family (even)
def d_exact(j, tau):
    # rho_j = (1-1/(2j))*(j+tau+1)/(j+tau); e_j = 1+1/(2j)
    return (F(1)-F(1,2*j))*(F(j+tau+1)/F(j+tau)) - (F(1)+F(1,2*j))

# check d_exact equals -(tau+1/2)/(j(j+tau))
ok = True
for j in range(2, 30):
    for tau in (-1, -F(3,2), -2, F(3)):
        if d_exact(j, tau) != -(F(tau)+F(1,2))/(F(j)*(F(j)+F(tau))):
            ok = False
print("d_j = -(tau+1/2)/(j(j+tau)) exact:", ok)

# Two-sided box invariance: for the homogeneous map, take d in [beta/j^2, alpha/j] for j-1, j-2
# and compute d_j = F_j(e_{j-1}+d1, e_{j-2}+d2) - e_j; check it stays in box.
import random
random.seed(1)
for parity in ('e','o'):
    for cv in (1, 3, 10):
        cF = F(cv)
        # alpha, beta choices: for E^(tau) family with tau < -1/2, d_j j^2 -> -(tau+1/2)
        # pick beta0 = 0.4, alpha = 2.0+5c/12 (even, from script)
        if parity=='e':
            alpha = F(2) + F(5)*cv/F(12)
            beta0 = F(1,2)
        else:
            alpha = F(4) + F(7)*cv/F(20)
            beta0 = F(1,2)
        worst_bad = None
        nbad_lo = 0; nbad_hi = 0
        for trial in range(2000):
            j = random.randint(30, 200)
            b_lo1 = beta0/(j-1)**2; b_hi1 = alpha/(j-1)
            b_lo2 = beta0/(j-2)**2; b_hi2 = alpha/(j-2)
            d1 = random.uniform(float(b_lo1), float(b_hi1))
            d2 = random.uniform(float(b_lo2), float(b_hi2))
            # evaluate F in floats
            a1,a2,a3 = a_f(parity, j, cF)
            e_j = 1.0 + (1.0 if parity=='e' else 3.0)/(2*j)
            e1  = 1.0 + (1.0 if parity=='e' else 3.0)/(2*(j-1))
            e2  = 1.0 + (1.0 if parity=='e' else 3.0)/(2*(j-2))
            rho1 = e1 + d1; rho2 = e2 + d2
            rhoj = float(a1) + float(a2)/rho1 + float(a3)/(rho1*rho2)
            dj = rhoj - e_j
            lo = beta0/j**2; hi = alpha/j
            if dj < lo: nbad_lo += 1; worst_bad = ('lo', j, dj, lo)
            if dj > hi: nbad_hi += 1; worst_bad = ('hi', j, dj, hi)
        print(f"par={parity} c={cv} alpha={float(alpha):.3f}: box violations lo={nbad_lo} hi={nbad_hi} worst={worst_bad}")
