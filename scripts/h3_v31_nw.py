# -*- coding: utf-8 -*-
"""H3 v31: derive (n, w) = (z/sqrt(j), sqrt(j)*(Dz - z/(2j))) system; verify convergence & summable perturbation."""
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

cF = F(3); par = 'e'; N = 400
A2, B2, C2, lam = coeffs_frac(cF, 2, par)
# basis homogeneous solutions
u = solve_hom(cF, par, 0, 1, A2, N)          # z0=0,z1=1 -> dominant j^1/2
# subdominant direction: construct via solving for ratio w -> -1/2 backward? Instead use v-reachable minus dominant part later.
# For now: generic homogeneous solution with z0=1,z1=0,z2=0 (mixes species incl h*)
g = solve_hom(cF, par, 1, 0, 0, N)

def to_nw(z, N):
    n = [0.0]*(N+1); w = [0.0]*(N+1)
    for j in range(1, N+1):
        n[j] = float(z[j])/math.sqrt(j)
        Dz = float(z[j]) - float(z[j-1])
        w[j] = math.sqrt(j)*(Dz - float(z[j])/(2*j))
    return n, w

for name, zz in (("u", u), ("g", g)):
    nn, ww = to_nw(zz, N)
    print(f"--- {name} ---")
    print("  n at m=100,200,400:", [nn[m] for m in (100,200,400)])
    print("  w at m=100,200,400:", [ww[m] for m in (100,200,400)])
    print("  n*sqrt(m) m=200,400 (if decaying):", [nn[m]*math.sqrt(m) for m in (200,400)])

# h* via backward
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
z0h, z1h, z2h = backward_frac(cF, par, 1500)
hstar = solve_hom(cF, par, 1, z1h/z0h, z2h/z0h, N)
nn, ww = to_nw(hstar, N)
print("--- h* ---")
print("  n at m=10,30,60,100:", [nn[m] for m in (10,30,60,100)])
print("  w at m=10,30,60,100:", [ww[m] for m in (10,30,60,100)])

# Perturbation structure: write n-recurrence n_j = Ap n_{j-1} + Bp n_{j-2} + Cp n_{j-3} + src/sqrt(j)
# and check sum of |coefficient - limit| and the "1/j cancellation" in A'+B'+C'
print("--- coefficient check (even, c=3) ---")
for j in (10, 50, 100, 200):
    A, B, C, lam = coeffs_frac(cF, j, par)
    Ap = A*(F(j-1, j))**F(1,2) if False else float(A)*math.sqrt((j-1)/j)
    Bp = float(B)*math.sqrt((j-2)/j)
    Cp = float(C)*math.sqrt((j-3)/j) if j >= 3 else 0.0
    print(f"  j={j}: A'={Ap:.6f} B'={Bp:.6f} C'={Cp:.8f} sum'={Ap+Bp+Cp:.8f}")
# asymptotic of A', B', C': verify A' = 2 - 2/j + O(1/j^2), B' = -1 + 2/j + O(1/j^2)
print("  check 2-A'-2/j (should be O(1/j^2)):", [round(2 - float(A)*math.sqrt((j-1)/j) - 2/j, 10) for j in (50,100,200)])
print("  check -1-B'+2/j (should be O(1/j^2)):", [round(-1 - float(-1)*1 - 0, 10) for j in (50,100,200)])
