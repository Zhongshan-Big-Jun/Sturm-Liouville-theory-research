# -*- coding: utf-8 -*-
"""H3 v27a: exact mode structure (part A only)."""
import math
from fractions import Fraction as F

C = F(3)
def P_e(j, c): return F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
def Q_e(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
def R_e(j, c): return F(4)*j*(j-2)*(2*j-3)*(2*j-5)
def T_e(j, c): return F(4)*j*(4*j-5)
def P_o(j, c): return F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
def Q_o(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
def R_o(j, c): return F(4)*j*(j-2)*(2*j-1)*(2*j-3)
def T_o(j, c): return F(4)*j*(4*j-3)

def solve_even(cF, nu1, D, N):
    c = cF; nu = [F(0)]*(N+1); nu[1] = F(nu1)
    for j in range(2, N+1):
        rhs = P_e(j,c)*nu[j-1] - Q_e(j,c)*nu[j-2] + (R_e(j,c)*nu[j-3] if j>=3 else F(0)) + T_e(j,c)*D
        nu[j] = rhs/(c*c)
    return nu

def solve_odd(cF, w1, S, N):
    c = cF; w = [F(0)]*(N+1); w[1] = F(w1)
    for j in range(2, N+1):
        rhs = P_o(j,c)*w[j-1] - Q_o(j,c)*w[j-2] + (R_o(j,c)*w[j-3] if j>=3 else F(0)) + T_o(j,c)*S
        w[j] = rhs/(c*c)
    return w

for par, solve in (("even", solve_even), ("odd", solve_odd)):
    N = 240
    u = solve(C, 1, 0, N)
    v = solve(C, 0, 1, N)
    lam = F(4)/C
    zu = [u[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    zv = [v[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    print(f"--- {par} (c=3) ---")
    print("  u/v (nu-scale) at m=40,80,160,240:", [round(float(u[m]/v[m]), 8) for m in (40,80,160,240)], "(target c/2 = 1.5)")
    print("  z^u/z^v at m=40,240:", [round(float(zu[m]/zv[m]), 8) for m in (40,240)], "(target 2/c = 0.6667)")
    w = [u[m] - F(3,2)*v[m] for m in range(N+1)]
    zw = [w[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    print("  z^w*sqrt(m):", [(m, round(float(zw[m]*math.sqrt(m)), 8)) for m in (10, 40, 80, 160, 240)])
    print("  z^w signs all equal:", all((zw[m]>0)==(zw[2]>0) for m in range(3, N+1)))
    # second combination to check dimension: ratio of z^u to z^v consistency
    r40 = float(zu[40]/zv[40]); r240 = float(zu[240]/zv[240])
    print("  u/v (z-scale) drift 40->240:", r40, "->", r240)
