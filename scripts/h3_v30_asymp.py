# -*- coding: utf-8 -*-
"""H3 v30: asymptotic structure of homogeneous solutions; nu-scale minimal decay; exact coefficients."""
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

def log10_frac(z):
    if z == 0: return None
    n, d = abs(z.numerator), z.denominator
    def l10(i):
        bl = i.bit_length()
        if bl < 50: return math.log10(i)
        mant = i / (1 << (bl - 1))
        return (bl - 1)*math.log10(2.0) + math.log10(mant)
    return l10(n) - l10(d)

cF = F(3); N = 200
for par in ('e','o'):
    print(f"===== {par} (c=3) =====")
    A2, B2, C2, lam = coeffs_frac(cF, 2, par)
    u = solve_hom(cF, par, 0, 1, A2, N)
    c = cF
    v = [F(0)]*(N+1); v[1] = F(0)
    for j in range(2, N+1):
        A, B, C, lam = coeffs_frac(c, j, par)
        if par == 'e': Tm = F(4)*j*(4*j-5)
        else: Tm = F(4)*j*(4*j-3)
        src = Tm/(c*c*F(math.factorial(j))**2*lam**j)
        v[j] = A*v[j-1] + B*v[j-2] + (C*v[j-3] if j>=3 else F(0)) + src
    print("  u signs u[2..20] positive:", all(u[j]>0 for j in range(2,21)))
    print("  u at m=60,120:", [float(u[m]) for m in (60,120)])
    print("  v at m=60,120:", [float(v[m]) for m in (60,120)])
    print("  u/v at m=40,80,120,200:", [round(float(u[m]/v[m]),8) for m in (40,80,120,200)])
    import numpy as np
    def fit(ms):
        m1,m2 = ms
        A = np.array([[math.sqrt(m1),1/math.sqrt(m1)],[math.sqrt(m2),1/math.sqrt(m2)]])
        b = np.array([float(u[m1]), float(u[m2])])
        return np.linalg.solve(A, b)
    print("  u fit a*j^1/2+b*j^-1/2: (60,120):", fit((60,120)), " (120,200):", fit((120,200)))
    w = [u[j] - F(3,2)*v[j] for j in range(N+1)]
    print("  w*sqrt(m):", [round(float(w[m]*math.sqrt(m)),6) for m in (40,80,120,200)])
    def backward_frac(cF, par, M):
        r = [F(1), F(0), F(0)]
        j = M
        while j > 3:
            A, B, C, lam = coeffs_frac(cF, j, par)
            newv = (r[0] - A*r[1] - B*r[2])/C
            r = [r[1], r[2], newv]
            s = abs(r[2])
            r = [x/s for x in r]
            j -= 1
        A, B, C, lam = coeffs_frac(cF, 3, par)
        newv = (r[0] - A*r[1] - B*r[2])/C
        r = [r[1], r[2], newv]
        return r[2], r[1], r[0]
    z0h, z1h, z2h = backward_frac(cF, par, 1000)
    hstar = [F(0)]*(N+1)
    hstar[0], hstar[1], hstar[2] = F(1), z1h/z0h, z2h/z0h
    for j in range(3, N+1):
        A, B, C, lam = coeffs_frac(cF, j, par)
        hstar[j] = A*hstar[j-1] + B*hstar[j-2] + C*hstar[j-3]
    print("  nu-scale h* log10|nu_m| m=10,30,60,100,200:",
          [round(log10_frac(abs(hstar[m]*F(math.factorial(m))**2*lam**m)),4) for m in (10,30,60,100,200)])
    for (m1,m2) in ((10,60),(60,200)):
        l1 = log10_frac(abs(hstar[m1]*F(math.factorial(m1))**2*lam**m1))
        l2 = log10_frac(abs(hstar[m2]*F(math.factorial(m2))**2*lam**m2))
        slope = (l2-l1)/(math.log10(m2)-math.log10(m1))
        print(f"    slope ({m1},{m2}): {slope:.4f}")
    print("  z-scale h* log10|z_m| m=10,100:", [round(log10_frac(abs(hstar[m])),3) for m in (10,100)])
