# -*- coding: utf-8 -*-
"""E2/E1 = int(y2')^2/int(y1')^2 over well family; and tau^2 sin^2(tau A)/sin^2 A on off-axis branch (E3)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well, y_well, well_s

def E_ratio(a, b, R, n=2000):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    xs = np.linspace(1e-8, 1-1e-8, n)
    # y' via finite difference of y (accurate enough for E3)
    h = 1e-6
    E1 = 0.0; E2 = 0.0
    for x in xs:
        d1 = (y_well(a,b,R,s1,x+h)-y_well(a,b,R,s1,x-h))/(2*h)
        d2 = (y_well(a,b,R,tau*s1,x+h)-y_well(a,b,R,tau*s1,x-h))/(2*h)
        E1 += d1*d1; E2 += d2*d2
    E1 *= (xs[1]-xs[0]); E2 *= (xs[1]-xs[0])
    return E2/E1, tau, s1

def rtau_val(a, b, R):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = m*s1*a; B = m*s1*(1-b)
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    return np.log(J(tau*A)/J(A)) - np.log(J(tau*B)/J(B))

if __name__ == '__main__':
    R = 4.0
    print("=== E2/E1 range over well family triangle ===")
    vals = []
    for a in np.linspace(0.02, 0.9, 18):
        for b in np.linspace(a+0.02, 0.98, 18):
            r, tau, s1 = E_ratio(a, b, R)
            vals.append((r, a, b, tau))
    vals.sort()
    print(f"  min E2/E1 = {vals[0][0]:.4f} at (a,b)=({vals[0][1]:.3f},{vals[0][2]:.3f}) tau={vals[0][3]:.3f}")
    print(f"  max E2/E1 = {vals[-1][0]:.4f} at (a,b)=({vals[-1][1]:.3f},{vals[-1][2]:.3f}) tau={vals[-1][3]:.3f}")
    print("=== off-axis E=0 branch: tau^2 sin^2(tau A)/sin^2 A vs E2/E1 ===")
    for a in [0.02, 0.05, 0.08, 0.10, 0.115]:
        bs = np.linspace(a+0.2, 0.999, 300)
        E = np.array([rtau_val(a, b, R) for b in bs])
        for i in range(len(bs)-1):
            if E[i]*E[i+1] < 0 and abs((a+bs[i])-1) > 1e-3:
                b0 = brentq(lambda bb: rtau_val(a, bb, R), bs[i], bs[i+1], xtol=1e-11)
                m = 2.0
                lam1, lam2 = eigs_well(a, b0, R)
                s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
                A = m*s1*a
                rhs = tau*tau*np.sin(tau*A)**2/np.sin(A)**2
                er, _, _ = E_ratio(a, b0, R)
                print(f"  a={a:.3f} b={b0:.4f}: tau={tau:.4f} A={A:.4f} rhs(tau^2 sin^2/sin^2)={rhs:.4f} E2/E1={er:.4f}  N1 sign: {'FAIL(neg)' if rhs>er else 'pass'}")
