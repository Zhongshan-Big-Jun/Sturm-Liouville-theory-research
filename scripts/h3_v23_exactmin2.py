# -*- coding: utf-8 -*-
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

def analyze(cF, par, M, N):
    z0, z1, z2 = backward_frac(cF, par, M)
    lam = F(4)/cF
    z = [F(0)]*(N+1)
    z[0], z[1], z[2] = z0, z1, z2
    for j in range(3, N+1):
        A, B, C = coeffs_frac(cF, j, par)
        z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
    print("c={} par={}: M={} (z1/z0, z2/z0) = ({:.12e}, {:.12e})".format(
        float(cF), par, M, float(z1/z0), float(z2/z0)))
    print("    m : log10|z| : log10|nu| : slope(ln nu vs ln m)")
    prev_m, prev_lnu = None, None
    for m in range(0, N+1):
        zm = z[m]/z0
        nu = zm * F(math.factorial(m))**2 * lam**m
        lnu = math.log10(abs(float(nu)))
        lz = math.log10(abs(float(zm))) if zm != 0 else -300.0
        sl = ""
        if prev_lnu is not None and m >= 2 and lnu != prev_lnu:
            sl = "{:+.4f}".format((lnu-prev_lnu)/(math.log10(m)-math.log10(prev_m)))
        print("m={:3d}: {:11.4f} {:11.4f}  {}".format(m, lz, lnu, sl))
        prev_m, prev_lnu = m, lnu

for cF, par in ((F(3),'e'), (F(3),'o')):
    analyze(cF, par, 300, 45)
    print()
