# -*- coding: utf-8 -*-
"""Fix/refine: N1 at the R=1.5 good root (high-n integration) and off-axis branch N1 sign at R=4."""
import numpy as np
from scipy.optimize import brentq, least_squares
import sys
sys.path.insert(0, '.')
from _well_rigid_verify import eigs_well, y_well, norm2_well, fval

def phases(a, b, R):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); s2 = np.sqrt(lam2); tau = s2/s1
    A = m*s1*a; B = m*s1*(1-b)
    return m, s1, tau, A, B

def N1_high(a, b, R, n=4000):
    m, s1, tau, A, B = phases(a, b, R)
    n1 = norm2_well(a, b, R, s1, n=n)
    n2 = norm2_well(a, b, R, tau*s1, n=n)
    return n2/n1 - np.sin(tau*A)**2/np.sin(A)**2

# good root at R=1.5 refined
def good_root(R, a0, b0):
    def res(ab):
        aa, bb = ab
        return [fval(aa, bb, R, aa), fval(aa, bb, R, bb)]
    sol = least_squares(res, [a0, b0], bounds=([1e-6,1e-6],[0.999,0.999]), xtol=1e-12, ftol=1e-12, max_nfev=200)
    return sol.x, sol.cost

ab, cost = good_root(1.5, 0.30, 0.70)
a, b = ab
m, s1, tau, A, B = phases(a, b, 1.5)
print(f"R=1.5 good root: (a,b)=({a:.8f},{b:.8f}) a+b={a+b:.10f} cost={cost:.2e}")
print(f"  A={A:.8f} B={B:.8f} |A-B|={abs(A-B):.2e} tau={tau:.6f}")
for n in [2000, 4000, 8000]:
    print(f"  N1 (n={n}): {N1_high(a, b, 1.5, n):+.3e}")

# N1 on symmetric line vs identity sin^2(tau A)/sin^2 A: test whether N1==0 is an identity for symmetric configs
print("\nSymmetric line N1 at R=1.5 (should be 0 if identity):")
for v in [0.20, 0.30, 0.408798, 0.45]:
    print(f"  v={v:.4f}: N1={N1_high(v, 1-v, 1.5, 3000):+.3e}")

# off-axis E=0 branch at R=4: N1 sign
print("\nOff-axis E=0 branch at R=4 (N1 sign):")
R = 4.0
def rtau_val(a, b, R):
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = np.sqrt(R)*s1*a; B = np.sqrt(R)*s1*(1-b)
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + R*np.cos(t)**2)
    return np.log(J(tau*A)/J(A)) - np.log(J(tau*B)/J(B))
cnt = 0
for a in np.linspace(0.02, 0.16, 20):
    bs = np.linspace(a+0.3, 0.999, 300)
    E = np.array([rtau_val(a, b, R) for b in bs])
    for i in range(len(bs)-1):
        if E[i]*E[i+1] < 0 and abs(a+bs[i]-1) > 1e-2:
            b0 = brentq(lambda bb: rtau_val(a, bb, R), bs[i], bs[i+1], xtol=1e-11)
            n1v = N1_high(a, b0, R, 2000)
            print(f"  a={a:.3f} b={b0:.4f} a+b={a+b0:.4f} N1={n1v:+.3e}")
            cnt += 1
            if cnt >= 6: break
    if cnt >= 6: break
