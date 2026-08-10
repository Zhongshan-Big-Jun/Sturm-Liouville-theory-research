# -*- coding: utf-8 -*-
"""H3 v32: exact (n, psi) system: n_j = z_j/sqrt(j), psi_j = j*(n_j - n_{j-1}).
Verify: convergence, subdominant detection, summable perturbation, response limit."""
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

def npsi(z, N):
    n = [0.0]*(N+1); ps = [0.0]*(N+1)
    for j in range(1, N+1):
        n[j] = float(z[j])/math.sqrt(j)
        ps[j] = j*(n[j] - n[j-1])
    return n, ps

cF = F(3); par = 'e'; N = 500
A2, B2, C2, lam = coeffs_frac(cF, 2, par)
u = solve_hom(cF, par, 0, 1, A2, N)
# subdominant direction (z1, D) = (c/4, -c/2) in z-scale -> z_j ~ gamma j^-1/2
c = cF
w0 = [F(0)]*(N+1); w0[1] = F(c,4)
for j in range(2, N+1):
    A, B, C, lam = coeffs_frac(c, j, par)
    if par == 'e': Tm = F(4)*j*(4*j-5)
    else: Tm = F(4)*j*(4*j-3)
    src = (-F(c,2))*Tm/(c*c*F(math.factorial(j))**2*lam**j)
    w0[j] = A*w0[j-1] + B*w0[j-2] + (C*w0[j-3] if j>=3 else F(0)) + src
nn, pp = npsi(w0, N)
print("--- subdominant w0 = (z1=c/4, D=-c/2) ---")
print("  n at m=50,100,200,400:", [nn[m] for m in (50,100,200,400)])
print("  psi at m=50,100,200,400:", [pp[m] for m in (50,100,200,400)])
print("  z*sqrt(m) at m=100,200,400:", [float(w0[m])*math.sqrt(m) for m in (100,200,400)])

nn, pp = npsi(u, N)
print("--- dominant u ---")
print("  n at m=50,100,200,400:", [nn[m] for m in (50,100,200,400)])
print("  psi at m=50,100,200,400:", [pp[m] for m in (50,100,200,400)])

# response e: D=1, z1=0
e0 = [F(0)]*(N+1)
for j in range(2, N+1):
    A, B, C, lam = coeffs_frac(c, j, par)
    if par == 'e': Tm = F(4)*j*(4*j-5)
    else: Tm = F(4)*j*(4*j-3)
    src = Tm/(c*c*F(math.factorial(j))**2*lam**j)
    e0[j] = A*e0[j-1] + B*e0[j-2] + (C*e0[j-3] if j>=3 else F(0)) + src
nn, pp = npsi(e0, N)
print("--- response e (D=1, z1=0) ---")
print("  n at m=50,100,200,400:", [nn[m] for m in (50,100,200,400)])
print("  psi at m=50,100,200,400:", [pp[m] for m in (50,100,200,400)])
print("  n positive:", all(nn[m]>0 for m in range(3,N+1)))
# convergence of n: differences
print("  n diff m=200->400:", nn[400]-nn[200])
# check the limiting value vs sum of sources with propagator->1 hypothesis: sum src_k/sqrt(k)
tot = 0.0
for k in range(2, N+1):
    A, B, C, lam = coeffs_frac(c, k, par)
    if par == 'e': Tm = F(4)*k*(4*k-5)
    else: Tm = F(4)*k*(4*k-3)
    tot += float(Tm/(c*c*F(math.factorial(k))**2*lam**k))/math.sqrt(k)
print("  sum_{k} src_k/sqrt(k) (to N):", tot)
