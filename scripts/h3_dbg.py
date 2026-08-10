# -*- coding: utf-8 -*-
import numpy as np, math

def coeffs(c, j, par):
    try:
        if par == 'e':
            Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
            Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
            Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
        else:
            Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
            Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
            Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
    except TypeError:
        print("TYPE ERROR: c =", repr(c), type(c).__name__, " j =", repr(j), " par =", repr(par))
        raise
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
        A, B, C = coeffs(c, par, j)
        newv = (r[0] - A*r[1] - B*r[2])/C
        r = np.array((r[1], r[2], newv))
        s = abs(r[2]) if abs(r[2]) > 1e-300 else 1.0
        r = r/s
        logacc += math.log10(s)
        if j in (10000, 50000, 100000, 200000, 300000, 399000):
            samples.append((j, logacc + math.log10(abs(r[0]))))
        j -= 1
    A, B, C = coeffs(c, par, 3)
    newv = (r[0] - A*r[1] - B*r[2])/C
    r = np.array((r[1], r[2], newv))
    z0, z1, z2 = r[2], r[1], r[0]
    return z0, z1, z2, samples

for idx, c0 in enumerate((1.0, 3.0, 10.0)):
    for par, nm in (('e','even'), ('o','odd')):
        print("calling backward_min c0={} par={}".format(c0, par))
        z0, z1, z2, samples = backward_min(c0, par, 400000)
        print("  done: z0={} z1={} z2={}".format(z0, z1, z2))
