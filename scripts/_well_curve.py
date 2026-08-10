# -*- coding: utf-8 -*-
"""Along-curve analysis: E(A,B)=log r~_tau(A)-log r~_tau(B) = 0 curve in (a,b);
check R1=f(a) sign on it (E3 evidence only)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well, fval

def Jt(m, x):
    return np.sin(x)**2/(np.sin(x)**2 + m*m*np.cos(x)**2)

def E_resid(a, b, R):
    m = np.sqrt(R)
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
    A = m*s1*a; B = m*s1*(1-b)
    return np.log(Jt(m, tau*A)/Jt(m, A)) - np.log(Jt(m, tau*B)/Jt(m, B)), (A, B, tau)

if __name__ == '__main__':
    import sys
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    m = np.sqrt(R)
    # scan the triangle; find where E crosses 0
    N = 90
    curve = []
    for a in np.linspace(0.02, 0.97, N):
        evals = []
        for b in np.linspace(a+1e-4, 0.999, 60):
            E, _ = E_resid(a, b, R)
            evals.append((b, E))
        # sign changes of E along this vertical line
        for i in range(len(evals)-1):
            if evals[i][1]*evals[i+1][1] < 0:
                try:
                    b0 = brentq(lambda bb: E_resid(a, bb, R)[0], evals[i][0], evals[i+1][0], xtol=1e-10)
                    curve.append((a, b0))
                except Exception:
                    pass
    print(f"R={R}: E=0 curve points: {len(curve)}")
    # evaluate R1=f(a) and R2=f(b) along the curve
    vals = []
    for (a, b) in curve:
        R1 = fval(a, b, R, a)
        R2 = fval(a, b, R, b)
        vals.append((a, b, R1, R2))
    # report: which curve points have R1 ~ 0 (critical candidates)
    near = [(a,b,r1,r2) for (a,b,r1,r2) in vals if abs(r1) < 0.05 or abs(r2) < 0.05]
    print("  candidates with small residual:")
    for v in near[:20]:
        print(f"    a={v[0]:.5f} b={v[1]:.5f} a+b={v[0]+v[1]:.5f} R1={v[2]:.4e} R2={v[3]:.4e}")
    # sign pattern of R1 along the curve
    pos = sum(1 for v in vals if v[2] > 0); neg = len(vals)-pos
    print(f"  R1 sign along E=0 curve: positive={pos} negative={neg}")
    # R1 as function of a on the curve (sorted)
    sv = sorted(vals)
    print("  (a, b, R1) sample:")
    for v in sv[::max(1,len(sv)//12)]:
        print(f"    a={v[0]:.4f} b={v[1]:.4f} a+b={v[0]+v[1]:.4f} R1={v[2]:+.6f}")
