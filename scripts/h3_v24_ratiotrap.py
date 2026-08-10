# -*- coding: utf-8 -*-
"""H3 v24: test elementary ratio-trap lemma for solution u (nu1=1, D=0)."""
from fractions import Fraction as F
import math

def P_e(c, m): return F(8)*c*m*m - F(4)*c*m + c*c*F(m, m-1)
def Q_e(c, m): return F(4)*m*(m-1)*(2*m-1)*(2*m-3) + F(4)*c*m*(2*m-3)
def R_e(c, m): return F(4)*m*(m-2)*(2*m-3)*(2*m-5)

def solve_u(cF, N):
    nu = [F(0)]*(N+1); nu[1] = F(1)
    for m in range(2, N+1):
        rhs = P_e(cF,m)*nu[m-1] - Q_e(cF,m)*nu[m-2] + (R_e(cF,m)*nu[m-3] if m>=3 else F(0))
        nu[m] = rhs/(cF*cF)
    return nu

for cc in (1, 3, 10):
    cF = F(cc); N = 200
    nu = solve_u(cF, N)
    print("=== c={}: ratios r_m = nu_m/nu_(m-1) vs (4/c)m^2 ===".format(cc))
    rtarget = 4.0/cc
    ok = True
    for m in range(2, 26):
        r = float(nu[m]/nu[m-1])
        t = rtarget*m*m
        if r < t: ok = False
        print("  m={:2d}: r_m = {:12.4f}  target = {:12.4f}  r/target = {:.6f} {}".format(m, r, t, r/t, "FAIL" if r<t else "ok"))
    print("  looser bound r_m >= (4/c)m^2(1-3/m) for m in [3,200]:",
          all(float(nu[m]/nu[m-1]) >= rtarget*m*m*(1-3.0/m) for m in range(3, N+1)))
    for m in (50, 100, 200):
        lognu = math.log10(abs(float(nu[m])))
        logpred = m*math.log10(rtarget) + 2*math.lgamma(m+1)/math.log(10.0) - 0.5*math.log10(m)
        print("  m={}: log10|nu|={:.2f} vs log10[(4/c)^m (m!)^2 m^-1/2]={:.2f}  diff={:.2f}".format(m, lognu, logpred, lognu-logpred))
    print()
