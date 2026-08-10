# -*- coding: utf-8 -*-
"""H3 v25: two-sided ratio traps for u (nu1=1,D=0) and w = u - (c/2)v."""
import numpy as np, math
from fractions import Fraction as F

def P_e(c, m): return F(8)*c*m*m - F(4)*c*m + c*c*F(m, m-1)
def Q_e(c, m): return F(4)*m*(m-1)*(2*m-1)*(2*m-3) + F(4)*c*m*(2*m-3)
def R_e(c, m): return F(4)*m*(m-2)*(2*m-3)*(2*m-5)
def T_e(c, m): return F(4)*m*(4*m-5)

def solve(cF, nu1, D, N):
    nu = [F(0)]*(N+1); nu[1] = F(nu1)
    for m in range(2, N+1):
        rhs = P_e(cF,m)*nu[m-1] - Q_e(cF,m)*nu[m-2] + (R_e(cF,m)*nu[m-3] if m>=3 else F(0)) + T_e(cF,m)*D
        nu[m] = rhs/(cF*cF)
    return nu

for cc in (1, 3, 10):
    cF = F(cc); N = 400
    u = solve(cF, 1, 0, N)
    v = solve(cF, 0, 1, N)
    w = [u[m] - F(cc,2)*v[m] for m in range(N+1)]
    lam = F(4)/cF
    print("=== c={}: ratio trap test ===".format(cc))
    for name, nu in (("u", u), ("w", w)):
        # ratios
        rs = [float(nu[m]/nu[m-1]) for m in range(2, N+1)]
        # fit r_m / ((4/c)m^2) vs 1/m
        ms = np.arange(2, N+1)
        rv = np.array(rs)
        target = (4.0/cc)*ms*ms
        ratio = rv/target
        # local estimate of the 1/m coefficient
        coef = (ratio-1)*ms
        print("  {}: r/target-1 times m at m=10,50,200,400: {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(
            name, coef[8], coef[48], coef[198], coef[398]))
        print("     min over m>=10 of (r/target): {:.6f} ; max: {:.6f}".format(ratio[8:].min(), ratio[8:].max()))
    # positivity of w
    print("  w sign:", "all positive" if all(w[m] > 0 for m in range(2, N+1)) else "mixed",
          "| min w_m/w_{m-1}-style check")
    # w at larger: sign of first 30
    print("  w[2..12] signs:", [">" if w[m]>0 else "<" for m in range(2,13)])
    print()
