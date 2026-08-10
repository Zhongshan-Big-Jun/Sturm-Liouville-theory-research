# -*- coding: utf-8 -*-
"""H3 v35: high-precision fit of n_j for dominant solution: n = a + b/j + c/j^2 + ..."""
import math
from fractions import Fraction as F

def coeffs_frac(c, j, par):
    lam = F(4)/c
    if j == 2:
        Pm = F(8)*c*4 - F(4)*c*2 + c*c*2
        A = Pm/(c*c*4*lam)
        Qm = F(4)*2*1*3*1 + F(4)*c*2*1
        B = -Qm/(c*c*4*1*1*lam*lam)
        return A, B, F(0), lam
    if par == 'e':
        Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        Pm = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        Rm = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    A = Pm/(c*c*j*j*lam)
    B = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    C = Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam*lam*lam)
    return A, B, C, lam

def solve_hom(cF, par, z0, z1, z2, N):
    c = cF; z = [F(0)]*(N+1)
    z[0], z[1], z[2] = F(z0), F(z1), F(z2)
    for j in range(3, N+1):
        A, B, C, lam = coeffs_frac(c, j, par)
        z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
    return z

cF = F(3); par = 'e'; N = 2000
A2, B2, C2, lam = coeffs_frac(cF, 2, par)
u = solve_hom(cF, par, 0, 1, A2, N)
nn = [0.0]*(N+1)
for j in range(1, N+1):
    nn[j] = float(u[j])/math.sqrt(j)

# Richardson extrapolation for a = lim n_j: a_m = (j1*n(j1) - j2*n(j2))/(j1-j2) with j1,j2 -> N
def rich_a(j1, j2):
    return (nn[j1]*j1 - nn[j2]*j2)/(j1 - j2)
a1 = rich_a(1000, 2000)
a2 = rich_a(1500, 2000)
print("a estimates:", a1, a2)
a = a2
# b = lim j*(n_j - a): Richardson
def rich_b(j1, j2):
    return (nn[j1]*j1*j1 - nn[j2]*j2*j2 - a*(j1*j1 - j2*j2))/(j1 - j2)
b1 = rich_b(1000, 2000); b2 = rich_b(1500, 2000)
print("b estimates:", b1, b2)
b = b2
# c = lim j^2*(n_j - a - b/j)
def rich_c(j1, j2):
    v1 = (nn[j1]-a)*j1*j1 - b*j1
    v2 = (nn[j2]-a)*j2*j2 - b*j2
    # if n = a+b/j+c/j^2+d/j^3: v_j = c + d/j + ...: Richardson on v
    return (v1*j1 - v2*j2)/(j1-j2)
c1 = rich_c(1000, 2000); c2 = rich_c(1500, 2000)
print("c estimates:", c1, c2)
# check residuals
for j in (500, 1000, 2000):
    r = nn[j] - a - b/j
    print(f"  j={j}: n-a-b/j = {r:.3e}; *j^2 = {r*j*j:.4f}; *j^3 = {r*j**3:.2f}")
print("a,b,c =", a, b, c1)
