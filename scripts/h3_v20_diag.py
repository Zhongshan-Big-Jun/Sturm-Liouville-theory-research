# -*- coding: utf-8 -*-
"""H3 v20: diagnose backward dynamics - eigenvalues/vectors of M_j, backward product."""
import numpy as np, math

def M_of(c, j, par):
    if par == 'e':
        Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
        Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
        Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
        Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
        Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
    lam = 4.0/c
    A = Pm/(c*c*j*j*lam)
    B = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    C = Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam*lam*lam)
    return np.array([[A, B, C], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

c0, par = 3.0, 'e'
print("=== eigenvalues of M_j (c=3, even) ===")
for j in (10, 100, 1000, 10000):
    M = M_of(c0, j, par)
    ev = np.linalg.eigvals(M)
    print("j={:6d}: eigenvalues = {} ; moduli = {}".format(j, np.round(ev, 6), np.round(np.abs(ev), 8)))
    # backward eigenvalues
    evb = np.linalg.eigvals(np.linalg.inv(M))
    print("    backward eigenvalues moduli = {}".format(np.round(np.abs(evb), 6)))

print()
print("=== backward product P = M_3^{-1} ... M_M^{-1} applied to e1 ===")
for M in (10, 50, 100):
    P = np.eye(3)
    for j in range(M, 2, -1):
        P = np.linalg.inv(M_of(c0, j, par)) @ P
    v = P @ np.array([1.0, 0.0, 0.0])
    v = v/np.linalg.norm(v)
    print("M={:3d}: direction = {}".format(M, np.round(v, 6)))
print()
print("=== forward solution from the converged direction (16.06,1,0.0337): early values ===")
z = np.zeros(30)
z[0], z[1], z[2] = 16.06, 1.0, 0.0337
for j in range(3, 30):
    M = M_of(c0, j, par)
    z[j] = M[0,0]*z[j-1] + M[0,1]*z[j-2] + M[0,2]*z[j-3]
print("z[0..20] =", np.round(z[:21], 6))
print()
print("=== if (16.06,1,0.0337) were the minimal direction, z_j*(j!)^2*lam^j should stay bounded ===")
lam = 4.0/c0
for m in (5, 10, 15, 20, 25):
    nu = abs(z[m])*math.factorial(m)**2*lam**m
    print("m={:2d}: nu_m = {:.3e}".format(m, nu))
