# -*- coding: utf-8 -*-
"""On the E=0 curve: evaluate norm equation N1 = n2/n1 - sin^2(tau A)/sin^2 A (E3)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well, y_well, norm2_well

def phases(a, b, R):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = m*s1*a; B = m*s1*(1-b); psi = s1*(b-a)
    return m, s1, tau, A, psi, B

def N1(a, b, R):
    m, s1, tau, A, psi, B = phases(a, b, R)
    n1 = norm2_well(a, b, R, s1, n=1200)
    n2 = norm2_well(a, b, R, tau*s1, n=1200)
    return n2/n1 - np.sin(tau*A)**2/np.sin(A)**2

def rtau_val(a, b, R):
    m, s1, tau, A, psi, B = phases(a, b, R)
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    return np.log(J(tau*A)/J(A)) - np.log(J(tau*B)/J(B))

if __name__ == '__main__':
    R = 4.0
    # find off-axis E=0 branch by scanning a in (0.01, 0.16)
    for a in np.linspace(0.015, 0.16, 30):
        bs = np.linspace(a+0.3, 0.999, 400)
        E = np.array([rtau_val(a, b, R) for b in bs])
        # find zeros
        for i in range(len(bs)-1):
            if E[i]*E[i+1] < 0:
                b0 = brentq(lambda bb: rtau_val(a, bb, R), bs[i], bs[i+1], xtol=1e-11)
                n1 = N1(a, b0, R)
                print(f"off-axis branch: a={a:.4f} b={b0:.4f} a+b={a+b0:.4f} N1={n1:+.6e}")
    # symmetric branch: N1 along the line
    print("symmetric branch:")
    for v in [0.20, 0.30, 0.3826, 0.45]:
        a = v; b = 1-v
        n1 = N1(a, b, R)
        print(f"  v={v:.4f} N1={n1:+.6e}")
