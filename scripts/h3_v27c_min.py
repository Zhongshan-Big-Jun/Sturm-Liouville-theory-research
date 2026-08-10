# -*- coding: utf-8 -*-
"""H3 v27c: minimal solution via exact backward iteration.
- convergence in M (300, 800, 1500)
- h*_0 != 0 (normalized z0 = 1)
- forward decay: log10|z_m|, z_{m+1}/z_m -> 0
- moments nu_m = z_m (m!)^2 lam^m: bounded? limit?
"""
import math
from fractions import Fraction as F

def log10_frac(z):
    if z == 0:
        return None
    n, d = abs(z.numerator), z.denominator
    # log10(n) via bit_length
    def l10(i):
        bl = i.bit_length()
        if bl < 50:
            return math.log10(i)
        mant = i / (1 << (bl - 1))
        return (bl - 1) * math.log10(2.0) + math.log10(mant)
    return l10(n) - l10(d)

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
    return r[2], r[1], r[0]   # (z0, z1, z2)

for cF, par in ((F(3),'e'), (F(3),'o'), (F(1),'e'), (F(10),'e')):
    print(f"=== c={cF} {par} ===")
    prev = None
    for M in (300, 800, 1500):
        z0, z1, z2 = backward_frac(cF, par, M)
        r1, r2 = z1/z0, z2/z0
        print(f"  M={M:5d}: z0={float(z0):.6e} z1/z0={float(r1):.14f} z2/z0={float(r2):.14f}")
    # take the M=1500 result, normalize z0=1, forward exactly to m=100
    z0, z1, z2 = backward_frac(cF, par, 1500)
    scale = z0
    z = [F(0)]*101
    z[0], z[1], z[2] = F(1), z1/z0, z2/z0
    lam = F(4)/cF
    for j in range(3, 101):
        A, B, C = coeffs_frac(cF, j, par)
        z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
    print("  forward from h* (z0=1):")
    for m in (10, 30, 50, 70, 100):
        lz = log10_frac(abs(z[m]))
        nu = z[m] * F(math.factorial(m))**2 * lam**m
        lnu = log10_frac(abs(nu))
        print(f"    m={m:3d}: log10|z|={lz:10.3f}  log10|nu|={lnu:10.4f}  z_m/z_{m-1}={float(z[m]/z[m-1]):.3e}")
