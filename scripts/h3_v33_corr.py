# -*- coding: utf-8 -*-
"""H3 v33: exact correction system for n = a + b/j + u, psi = -b/j + v."""
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

cF = F(3); par = 'e'; N = 600
A2, B2, C2, lam = coeffs_frac(cF, 2, par)
u = solve_hom(cF, par, 0, 1, A2, N)
nn = [0.0]*(N+1)
for j in range(1, N+1):
    nn[j] = float(u[j])/math.sqrt(j)
def est_a(n):
    j1, j2 = 300, 600
    return (n[j1]*j1 - n[j2]*j2)/(j1 - j2)
a = est_a(nn)
psi = [0.0]*(N+1)
for j in range(1, N+1):
    psi[j] = j*(nn[j]-nn[j-1])
b = -psi[500]*500
print("dominant u: est a =", a, " est b =", b)
uj = [0.0]*(N+1); vj = [0.0]*(N+1)
for j in range(1, N+1):
    uj[j] = nn[j] - a - b/j
    vj[j] = psi[j] + b/j
print("u_corr at j=200,400,600:", [uj[j] for j in (200,400,600)])
print("u_corr*j^2 at j=200,400,600:", [uj[j]*j*j for j in (200,400,600)])
print("u_corr*j^3 at j=200,400,600:", [uj[j]*j**3 for j in (200,400,600)])
print("v at j=200,400,600:", [vj[j] for j in (200,400,600)])
print("v*j^2 at j=200,400,600:", [vj[j]*j*j for j in (200,400,600)])

# residual for n = a + b/j (u=v=0) target
print("--- residual R_j for ansatz n=a+b/j ---")
for j in (100, 300, 600):
    A, B, C, lam = coeffs_frac(cF, j, par)
    Ap = float(A)*math.sqrt((j-1)/j); Bp = float(B)*math.sqrt((j-2)/j); Cp = float(C)*math.sqrt((j-3)/j)
    alpha = Ap - 2 + 2/j; beta = Bp + 1 - 2/j; gamma = Cp
    a0, b0 = 1.0, 2.0
    njm1 = a0 + b0/(j-1); njm2 = a0 + b0/(j-2); njm3 = a0 + b0/(j-3); nj = a0 + b0/j
    Dn = njm1 - njm2
    R = (nj - 2*njm1 + njm2) + (2.0/j)*Dn - (alpha*njm1 + beta*njm2 + gamma*njm3)
    print(f"  j={j}: R_j = {R:.3e}  R*j^3 = {R*j**3:.4f}")
