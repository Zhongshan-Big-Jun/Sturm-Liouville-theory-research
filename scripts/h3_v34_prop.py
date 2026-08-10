# -*- coding: utf-8 -*-
"""H3 v34: verify propagator positivity g(j,k) >= 0 for all j>=k, and e_j >= src_3*g(j,3)."""
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

cF = F(3); par = 'e'; N = 200
# propagators: g(.,k) = homogeneous solution with data at (k-2,k-1,k) = (0,0,1)
# i.e. z_{k-2}=0, z_{k-1}=0, z_k=1
print("--- positivity of propagators g(j,k) for k=3,4,5,10,50 ---")
for k in (3,4,5,10,50):
    g = [F(0)]*(N+1)
    if k >= 2: g[k] = F(1)
    # extend: need values before k are 0; the homogeneous recurrence determines forward
    # but our solve_hom takes (z0,z1,z2); use direct forward from k
    for j in range(k+1, N+1):
        A, B, C, lam = coeffs_frac(cF, j, par)
        g[j] = A*g[j-1] + B*g[j-2] + C*g[j-3]
    pos = all(g[j] >= 0 for j in range(3, N+1))
    # count sign changes
    sgn = [1 if g[j]>0 else (-1 if g[j]<0 else 0) for j in range(3, N+1)]
    chg = sum(1 for j in range(1, len(sgn)) if sgn[j] != 0 and sgn[j] != sgn[j-1])
    print(f"  k={k}: all positive (j>=3): {pos}; sign changes: {chg}; g(100,k)={float(g[100]):.6e}")

# response e vs src_3*g(.,3)
e0 = [F(0)]*(N+1)
for j in range(2, N+1):
    A, B, C, lam = coeffs_frac(cF, j, par)
    if par == 'e': Tm = F(4)*j*(4*j-5)
    else: Tm = F(4)*j*(4*j-3)
    src = Tm/(cF*cF*F(math.factorial(j))**2*lam**j)
    e0[j] = A*e0[j-1] + B*e0[j-2] + (C*e0[j-3] if j>=3 else F(0)) + src
g3 = solve_hom(cF, par, 0, 0, 1, N)  # careful: this is data (z0,z1,z2)=(0,0,1) at j=0,1,2 NOT k=3
# fix: propagator from k=3 means data (z1,z2,z3) = (0,0,1): z1=0,z2=0,z3=1
g3b = [F(0)]*(N+1); g3b[3] = F(1)
for j in range(4, N+1):
    A, B, C, lam = coeffs_frac(cF, j, par)
    g3b[j] = A*g3b[j-1] + B*g3b[j-2] + C*g3b[j-3]
# src_3
A3,B3,C3,lam = coeffs_frac(cF, 3, par)
Tm3 = F(4)*3*(12-5) if par=='e' else F(4)*3*(12-3)
src3 = Tm3/(cF*cF*F(math.factorial(3))**2*lam**3)
print("src_3 =", float(src3), " g3b(100) =", float(g3b[100]))
print("compare e(100) vs src3*g3b(100):", float(e0[100]), "vs", float(src3*g3b[100]))
print("e(50)/ (src3*g3b(50)):", float(e0[50]/(src3*g3b[50])))
print("e(100)/(src3*g3b(100)):", float(e0[100]/(src3*g3b[100])))
print("e(200)/(src3*g3b(200)):", float(e0[200]/(src3*g3b[200])))
