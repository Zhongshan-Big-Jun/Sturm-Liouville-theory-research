# -*- coding: utf-8 -*-
"""H3 v28: verify the ratio recurrence for the minimal solution; check consistency."""
import math
from fractions import Fraction as F

def coeffs_frac(c, j, par):
    Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
    Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
    Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    lam = F(4)/c
    A = Pm/(c*c*j*j*lam)
    B = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    C = Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam*lam*lam)
    return A, B, C

def backward_frac(cF, par, M):
    r = [F(1), F(0), F(0)]
    j = M
    while j > 3:
        A, B, C = coeffs_frac(cF, j, par)
        newv = (r[0] - A*r[1] - B*r[2])/C
        r = [r[1], r[2], newv]
        s = abs(r[2])
        r = [x/s for x in r]
        j -= 1
    A, B, C = coeffs_frac(cF, 3, par)
    newv = (r[0] - A*r[1] - B*r[2])/C
    r = [r[1], r[2], newv]
    return r[2], r[1], r[0]

cF = F(3); par = 'e'
z0, z1, z2 = backward_frac(cF, par, 1500)
N = 120
z = [F(0)]*(N+1); z[0], z[1], z[2] = F(1), z1/z0, z2/z0
for j in range(3, N+1):
    A, B, C = coeffs_frac(cF, j, par)
    z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]

print("check recurrence residual at selected j (should be 0):")
for j in (10, 50, 100):
    A, B, C = coeffs_frac(cF, j, par)
    res = z[j] - (A*z[j-1] + B*z[j-2] + C*z[j-3])
    print(f"  j={j}: residual = {res}")

print("ratio recurrence check (r_j vs A_j + B_j/r_{j-1} + C_j/(r_{j-1} r_{j-2})):")
for j in (10, 50, 100):
    A, B, C = coeffs_frac(cF, j, par)
    rj = z[j]/z[j-1]
    rjm1 = z[j-1]/z[j-2]
    rjm2 = z[j-2]/z[j-3]
    rhs = A + B/rjm1 + C/(rjm1*rjm2)
    print(f"  j={j}: r_j = {float(rj):.6e} ; RHS = {float(rhs):.6e} ; A={float(A):.6f} B/r={float(B/rjm1):.6e} C/(rr)={float(C/(rjm1*rjm2)):.6e}")

print("ratios r_j = z_j/z_{j-1}:")
for j in (10, 30, 50, 70, 90, 100, 110, 120):
    rj = z[j]/z[j-1]
    print(f"  j={j}: r_j = {float(rj):.6e} ;  log10(z_j/z_{j-1}) = {math.log10(abs(float(rj))):.3f}")
