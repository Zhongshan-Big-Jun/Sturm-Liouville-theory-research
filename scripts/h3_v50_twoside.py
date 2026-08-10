# -*- coding: utf-8 -*-
"""H3 v50: two-sided ratio induction for the u-mode (z-scale).
Goal: L_j <= rho_j <= U_j for all j>=2, with L_j=1+1/(2j), U_j=1+1/(2j)+delta/j^2.
rho_j = a1 + a2/rho_{j-1} + a3/(rho_{j-1} rho_{j-2}),  a2<0, a3>0.
Lower: rho_j >= a1 + a2/L_{j-1} + a3/(U_{j-1}U_{j-2})
Upper: rho_j <= a1 + a2/U_{j-1} + a3/(L_{j-1}L_{j-2})
We test numerically (float, then exact) whether these close for some delta."""
import math

def a1(j,c): return 2.0 - 1.0/j + c/(4.0*j*(j-1))
def a2(j,c):
    Q = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
    lam = 4.0/c
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j,c):
    R = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
    if j==2: return 0.0
    lam = 4.0/c
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

for c in (0.5,1,3,10):
    print("=== c=%g ===" % c)
    for delta in (0.5,1.0,2.0,4.0,8.0,16.0):
        # base: rho_2 exactly
        rho2 = a1(2,c) + a2(2,c)   # a3(2)=0, rho_1 term: z_1 free? u-mode z_0=0,z_1=nu1/lam
        # z_2 = a1(2)z_1 + a2(2)z_0 => rho_2 = z_2/z_1 = a1(2)
        rho2 = a1(2,c)
        # check induction from j=3
        ok=True; fail=[]
        L={2:1.0+1.0/(2*2)}; U={2:L[2]+delta/4.0}
        # rho_1 does not exist; for j=3 need rho_1 too. Use rho_1 = z_1/z_0: z_0=0 => infinite.
        # So ratio induction starts at j=3 using rho_2 and rho_1~infinity? No:
        # Better: prove bounds on z_j/z_{j-1} for j>=3 given z_0=0,z_1>0.
        # rho_3 = a1(3)+a2(3)/rho_2 + a3(3)/(rho_2*rho_1) with rho_1=z_1/z_0=inf => term 0.
        # Handle j=3 specially with rho_1=+inf.
        rho3 = a1(3,c) + a2(3,c)/rho2
        L3=1.0+1.0/6; U3=L3+delta/9.0
        if not (L3<=rho3<=U3): ok=False; fail.append((3,rho3,L3,U3))
        L={2:L[2],3:L3}; U={2:U[2],3:U3}
        for j in range(4,20000):
            lb = a1(j,c) + a2(j,c)/L[j-1] + a3(j,c)/(U[j-1]*U[j-2])
            ub = a1(j,c) + a2(j,c)/U[j-1] + a3(j,c)/(L[j-1]*L[j-2])
            Lj=1.0+1.0/(2*j); Uj=Lj+delta/(j*j)
            if lb < Lj: ok=False; fail.append((j,'lb',lb,Lj)); break
            if ub > Uj: ok=False; fail.append((j,'ub',ub,Uj)); break
            L[j]=Lj; U[j]=Uj
        print("  delta=%5.1f: %s %s" % (delta, "OK to j=20000" if ok else "FAIL", fail[:2]))
