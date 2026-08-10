# -*- coding: utf-8 -*-
"""H3 v22: exact-arithmetic backward iteration -> minimal solution's exact moments."""
from fractions import Fraction as F
import math

def coeffs_frac(c, j, par):
    if par == 'e':
        Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        Pm = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        Rm = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
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

cF = F(3)
par = 'e'
M = 300
z0, z1, z2 = backward_frac(cF, par, M)
print("M={}: (z0,z1,z2) = ({}, {}, {})".format(M, z0, z1, z2))
print("floats: z0={:.10e} z1={:.10e} z2={:.10e}".format(float(z0), float(z1), float(z2)))
print("ratios z1/z0 = {:.10e}  z2/z0 = {:.10e}".format(float(z1/z0), float(z2/z0)))
print("(compare float64 backward: z1/z0 = {:.10e} z2/z0 = {:.10e})".format(1.0/15.438123464223258, 0.050535704714507475/15.438123464223258))

# forward exactly, moments nu_m = z_m (m!)^2 lam^m
lam = F(4)/cF
N = 40
z = [F(0)]*(N+1)
z[0], z[1], z[2] = z0, z1, z2
for j in range(3, N+1):
    A, B, C = coeffs_frac(cF, j, par)
    z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
print()
print("m : log10|z_m| : log10|nu_m| : nu_m (exact, up to normalization)")
scale = z0  # normalization factor; the solution with z0=1 is z/scale
for m in range(0, N+1):
    zm = z[m]/scale
    nu = zm * F(math.factorial(m))**2 * lam**m
    lz = math.log10(abs(float(zm)))
    lnu = math.log10(abs(float(nu)))
    print("m={:2d}: log10|z|={:10.4f}  log10|nu|={:10.4f}  nu={}".format(m, lz, lnu, nu))
