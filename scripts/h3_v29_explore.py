# -*- coding: utf-8 -*-
"""H3 v29: explore reachable family structure, response e = v - h_shadow, propagator asymptotics."""
import math
from fractions import Fraction as F

def coeffs_frac(c, j, par):
    if j < 3:
        return F(0), F(0), F(0), F(0), F(4)/c
    if par == 'e':
        Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Tm = F(4)*j*(4*j-5)
    else:
        Pm = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        Rm = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        Tm = F(4)*j*(4*j-3)
    lam = F(4)/c
    A = Pm/(c*c*j*j*lam)
    B = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    C = Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam*lam*lam)
    return A, B, C, Tm, lam

def solve_reach(cF, par, z1, D, N):
    c = cF; z = [F(0)]*(N+1)
    z[1] = F(z1)
    for j in range(2, N+1):
        A, B, C, Tm, lam = coeffs_frac(c, j, par)
        if j == 2:
            A2 = (F(8)*c*4 - F(4)*c*2 + c*c*2)/(c*c*4*lam)
            src = Tm*D/(c*c*4*lam*lam)
            z[j] = A2*z[1] + src
        else:
            src = Tm*D/(c*c*F(math.factorial(j))**2*lam**j)
            z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3] + src
    return z

def solve_hom(cF, par, z0, z1, z2, N):
    c = cF; z = [F(0)]*(N+1)
    z[0], z[1], z[2] = F(z0), F(z1), F(z2)
    for j in range(3, N+1):
        A, B, C, Tm, lam = coeffs_frac(c, j, par)
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

cF = F(3); N = 120
for par in ('e','o'):
    print(f"===== {par} (c=3) =====")
    u = solve_hom(cF, par, 0, 1, 0, N)
    v = solve_reach(cF, par, 0, 1, N)
    sh = solve_hom(cF, par, 0, 0, v[2], N)
    e = [v[j] - sh[j] for j in range(N+1)]
    w = [u[j] - F(3,2)*v[j] for j in range(N+1)]
    print("  z^u at m=60,120:", [float(u[m]) for m in (60,120)])
    print("  z^v at m=60,120:", [float(v[m]) for m in (60,120)])
    print("  z^e at m=60,120:", [float(e[m]) for m in (60,120)])
    print("  e/sqrt(j) at m=20,40,80,120:", [round(float(e[m]/math.sqrt(m)),8) for m in (20,40,80,120)])
    print("  e*sqrt(j) at m=20,40,80,120:", [round(float(e[m]*math.sqrt(m)),8) for m in (20,40,80,120)])
    print("  e signs all equal:", all((e[m]>0)==(e[3]>0) for m in range(4,N+1)))
    import numpy as np
    def est(ms):
        m1,m2 = ms
        s1,s2 = [float(e[m]) for m in ms]
        A = np.array([[math.sqrt(m1),1/math.sqrt(m1)],[math.sqrt(m2),1/math.sqrt(m2)]])
        return np.linalg.solve(A, np.array([s1,s2]))
    print("  e ~ a*j^1/2+b*j^-1/2: (20,60):", est((20,60)), " (60,120):", est((60,120)))
    import random
    random.seed(1)
    worst = None
    for trial in range(20):
        alpha, beta = random.uniform(-1,1), random.uniform(-1,1)
        z = [alpha*u[j] + beta*v[j] for j in range(N+1)]
        x1,x2 = math.log(60.0), math.log(120.0)
        l1,l2 = log10_frac(abs(z[60])), log10_frac(abs(z[120]))
        if l1 is None or l2 is None: continue
        slope = (l2-l1)/(x2-x1)
        if worst is None or slope < worst[0]: worst = (slope, alpha, beta)
    print("  min log-log slope over 20 random directions:", worst)
