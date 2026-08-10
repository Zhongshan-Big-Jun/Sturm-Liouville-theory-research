# -*- coding: utf-8 -*-
"""Convexity probe: eigenvalues of Hess(D^well) on a grid (E3 evidence only)."""
import numpy as np
from _well_landscape2 import eigs_well

def Dval(a, b, R):
    lam = eigs_well(a, b, R)
    return lam[1]-lam[0]

def hess(a, b, R, h=2e-4):
    f00 = Dval(a, b, R)
    fa = Dval(a+h, b, R); fb = Dval(a, b+h, R)
    fa_ = Dval(a-h, b, R); fb_ = Dval(a, b-h, R)
    daa = (fa - 2*f00 + fa_)/h**2
    dbb = (fb - 2*f00 + fb_)/h**2
    dab = (Dval(a+h, b+h, R) - fa - fb + f00)/h**2
    return np.array([[daa, dab], [dab, dbb]])

if __name__ == '__main__':
    import sys
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    N = 14
    worst = (1e9, None); min_eig_sum = 0
    count_posdef = 0; count_neg = 0; total = 0
    for a in np.linspace(0.05, 0.90, N):
        for b in np.linspace(a+0.05, 0.95, N):
            H = hess(a, b, R)
            w = np.linalg.eigvalsh(H)
            total += 1
            if w[0] > 0 and w[1] > 0: count_posdef += 1
            if w[1] < 0: count_neg += 1
            if w[0] < worst[0]:
                worst = (w[0], (a, b, w[0], w[1]))
    print(f"R={R}: grid {total} pts: posdef={count_posdef} neg-curvature={count_neg}")
    print(f"  worst min-eig = {worst[0]:.4f} at (a,b)=({worst[1][0]:.3f},{worst[1][1]:.3f}) eig=({worst[1][2]:.4f},{worst[1][3]:.4f})")
    # trace Hess at symmetric point
    a, b = 0.382598, 0.617402
    H = hess(a, b, R)
    print(f"  Hess at symmetric point: {np.linalg.eigvalsh(H)}")
