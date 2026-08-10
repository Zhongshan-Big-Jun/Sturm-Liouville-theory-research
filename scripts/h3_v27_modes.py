# -*- coding: utf-8 -*-
"""H3 v27: mode structure verification.
A) exact moderate-m: u,v (even/odd), u/v -> c/2, w=u-(c/2)v ~ m^{-1/2}?
B) float large-m: w computed directly from its own initial data (no cancellation),
   check w_m*sqrt(m) convergence vs log m growth (log-factor test).
C) minimal solution: exact backward iteration, h*_0 != 0, forward moments bounded?
"""
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

print("=== A) exact moderate-m mode structure, c = 3 ===")
for par, solve in (("even", solve_even), ("odd", solve_odd)):
    N = 240
    u = solve(C, 1, 0, N)
    v = solve(C, 0, 1, N)
    lam = F(4)/C
    # z-scaled
    zu = [u[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    zv = [v[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    print(f"--- {par} ---")
    print("  u/v at m=40,80,160,240:", [round(float(u[m]/v[m]), 8) for m in (40,80,160,240)], "(target c/2 = 1.5)")
    w = [u[m] - F(3,2)*v[m] for m in range(N+1)]
    # z-scale of w
    zw = [w[m]/F(math.factorial(m))**2/lam**m for m in range(N+1)]
    vals = [(m, float(zw[m]*math.sqrt(m))) for m in (10, 40, 80, 160, 240)]
    print("  z^w*sqrt(m):", vals)
    print("  z^w signs [2..240] all equal:", all((zw[m]>0)==(zw[2]>0) for m in range(3, N+1)), "sign =", zw[2]>0)
    print("  z^u/z^v at m=240:", round(float(zu[240]/zv[240]), 8), "(target 2/c = 2/3)")

print()
print("=== B) float large-m: direct w-direction (no cancellation), log test ===")
lam = 4.0/3.0
def zcoeffs(c, par, j):
    if par == 'e':
        Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
        Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
        Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
        Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
        Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
    A = Pm/(c*c*j*j*lam)
    B = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    C = Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam*lam*lam)
    return A, B, C

for par in ('e', 'o'):
    # exact initial data for w-direction (up to m=2), from exact solutions
    Nu = solve_even(C, 1, 0, 4) if par == 'e' else solve_odd(C, 1, 0, 4)
    Nv = solve_even(C, 0, 1, 4) if par == 'e' else solve_odd(C, 0, 1, 4)
    wm = [Nu[m] - F(3,2)*Nv[m] for m in range(5)]
    # z-scaled initial data: z_m = nu_m/(m!)^2 lam^m
    lamF = F(4)/C
    z0 = F(0); z1 = wm[1]/lamF; z2 = wm[2]/(F(4)*lamF*lamF)
    N = 10_000_000
    z = [0.0]*(N+1); z[0] = float(z0); z[1] = float(z1); z[2] = float(z2)
    for j in range(3, N+1):
        A, B, Cc = zcoeffs(3.0, par, j)
        z[j] = A*z[j-1] + B*z[j-2] + Cc*z[j-3]
    print(f"  {par}: z^w*sqrt(m) at m=10^4,10^5,10^6,10^7:",
          [round(z[m]*math.sqrt(m), 8) for m in (10**4, 10**5, 10**6, 10**7)],
          " (log10 m: 4,5,6,7)")
    print(f"      z^w*sqrt(m)/log10(m):", [round(z[m]*math.sqrt(m)/math.log10(m), 6) for m in (10**4, 10**5, 10**6, 10**7)])
