# -*- coding: utf-8 -*-
"""H3 v18: corrected backward iteration + Casoratian analysis."""
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
    samples = []
    j = M
    while j > 4:
        A, B, C = coeffs(c, j, par)
        newv = (r[0] - A*r[1] - B*r[2])/C
        r = np.array((r[1], r[2], newv))
        s = abs(r[2]) if abs(r[2]) > 1e-300 else 1.0
        r = r/s
        logacc += math.log10(s)
        if j in (10000, 50000, 100000, 200000, 300000, 399000):
            samples.append((j, logacc + math.log10(abs(r[0]))))
        j -= 1
    A, B, C = coeffs(c, 3, par)
    newv = (r[0] - A*r[1] - B*r[2])/C
    r = np.array((r[1], r[2], newv))
    z0, z1, z2 = r[2], r[1], r[0]
    return z0, z1, z2, samples

print("=== minimal solution: (z0,z1,z2) and moment behavior ===")
for c0 in (1.0, 3.0, 10.0):
    for par, nm in (('e','even'), ('o','odd')):
        z0, z1, z2, samples = backward_min(c0, par, 400000)
        z1, z2 = z1/z0, z2/z0
        lam = 4.0/c0
        N = 30000
        z = np.zeros(N+1); z[0], z[1], z[2] = 1.0, z1, z2
        for j in range(3, N+1):
            A, B, C = coeffs(c0, j, par)
            z[j] = A*z[j-1] + B*z[j-2] + C*z[j-3]
        print("c={} {}: (z0,z1,z2) = (1, {:.6e}, {:.6e})".format(c0, nm, z1, z2))
        print("    samples (j, log10|z_j|):", [(j, round(v,2)) for j, v in samples])
        for m in (1000, 5000, 10000, 30000):
            lognu = math.log10(abs(z[m])) + 2*math.lgamma(m+1)/math.log(10.0) + m*math.log10(lam)
            print("    m={:6d}: log10|z_m|={:8.2f}  log10|nu_m|={:9.2f}  log10(nu_m/m)={:9.4f}".format(
                m, math.log10(abs(z[m])), lognu, lognu - math.log10(m)))
