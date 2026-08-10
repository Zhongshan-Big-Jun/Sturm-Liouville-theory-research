# -*- coding: utf-8 -*-
"""H3 v21: corrected backward iteration (runs j down to 4, then j=3)."""
import numpy as np, math

def coeffs(c, j, par):
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
    return A, B, C

def backward_min(c, par, M):
    r = np.array((1.0, 0.0, 0.0))
    logacc = 0.0
    j = M
    while j > 3:
        A, B, C = coeffs(c, j, par)
        newv = (r[0] - A*r[1] - B*r[2])/C
        r = np.array((r[1], r[2], newv))
        s = abs(r[2]) if abs(r[2]) > 1e-300 else 1.0
        r = r/s
        logacc += math.log10(s)
        j -= 1
    A, B, C = coeffs(c, 3, par)
    newv = (r[0] - A*r[1] - B*r[2])/C
    r = np.array((r[1], r[2], newv))
    return r[2], r[1], r[0], logacc

c0, par = 3.0, 'e'
print("=== corrected backward iteration: convergence vs M ===")
for M in (10, 30, 100, 1000, 10000, 100000):
    z0, z1, z2, la = backward_min(c0, par, M)
    print("M={:7d}: (z0,z1,z2) = ({:.10e}, {:.10e}, {:.10e})".format(M, z0, z1, z2))
# forward check of the large-M result
M = 100000
z0, z1, z2, la = backward_min(c0, par, M)
N = 5000
z = np.zeros(N+1); z[0], z[1], z[2] = z0, z1, z2
for j in range(3, N+1):
    A, B, C = coeffs(c0, j, par)
    z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
print("forward from (z0,z1,z2) = ({}, {}, {}):".format(z0, z1, z2))
lam = 4.0/c0
for m in (10, 50, 100, 500, 1000, 5000):
    lognu = math.log10(abs(z[m])) + 2*math.lgamma(m+1)/math.log(10.0) + m*math.log10(lam)
    print("  m={:5d}: z_m = {:.6e}  log10|nu_m| = {:.4f}".format(m, z[m], lognu))
