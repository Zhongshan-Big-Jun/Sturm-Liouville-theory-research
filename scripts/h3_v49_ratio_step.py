# -*- coding: utf-8 -*-
"""H3 v49: ratio induction for u-mode in z-scale.
rho_j = a1 + a2/rho_{j-1} + a3/(rho_{j-1} rho_{j-2}), a2<0, a3>0.
If rho_{j-1} >= 1+s_{j-1}, then rho_j >= a1 + a2/(1+s_{j-1}) + 0.
Check F(j) := a1 + a2/(1+s_{j-1}) - (1+s_j), s_j=1/(2j), and the asymptotic."""
from fractions import Fraction as F

def a1e(j,c): return F(2) - F(1)/F(j) + F(c)/(F(4)*F(j)*F(j-1))
def a2e(j,c):
    Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
    return -Q/(c*c*j*j*(j-1)*(j-1))
def a3e(j,c):
    R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    if j==2: return F(0)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*(F(4)/c)**3)

for c in (1,3,10):
    print("=== c=%d ===" % c)
    bad=[]
    for j in range(2,5001):
        sjm1 = F(1)/(F(2)*(j-1))
        sj   = F(1)/(F(2)*j)
        Fv = a1e(j,c) + a2e(j,c)/(F(1)+sjm1) - (F(1)+sj)
        if Fv < 0: bad.append((j,float(Fv)))
    print("  F(j)<0 for j in [2,5000]:", bad[:5], "count:", len(bad))
    # asymptotics of F(j) for a few j
    for j in (10,100,1000):
        sjm1 = F(1)/(F(2)*(j-1)); sj=F(1)/(F(2)*j)
        Fv = a1e(j,c) + a2e(j,c)/(F(1)+sjm1) - (F(1)+sj)
        print("    j=%5d: F(j)=%.6e  F(j)*j=%.6f  F(j)*j^2=%.6f" % (j, float(Fv), float(Fv*j), float(Fv*j*j)))
