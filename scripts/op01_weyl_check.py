# -*- coding: utf-8 -*-
"""#1 Weyl-constant check: lambda_n * (int sqrt(rho))^2 / (n pi)^2 -> 1."""
import numpy as np

def y1_piece(lam, xs, rhos):
    y, yp = 0.0, 1.0; x = 0.0
    for i, x1 in enumerate(xs):
        w = np.sqrt(lam*rhos[i])
        c, s = np.cos(w*(x1-x)), np.sin(w*(x1-x))
        y, yp = c*y + s/w*yp, -w*s*y + c*yp
        x = x1
    return y

def eigvals_piece(xs, rhos, N_eig, B=4096):
    lam_max = (N_eig+8)**2*np.pi**2*max(1.0/min(rhos), 1.0)*1.2
    out = []; lam = 1e-4; step = 1.0005
    while len(out) < N_eig and lam < lam_max:
        batch = lam * step**np.arange(B)
        batch = batch[batch < lam_max]
        ys = np.array([y1_piece(l, xs, rhos) for l in batch])
        sgn = np.sign(ys)
        idx = np.where((sgn[:-1]*sgn[1:]) < 0)[0]
        for i in idx:
            lo, hi = batch[i], batch[i+1]
            for _ in range(70):
                mid = 0.5*(lo+hi)
                if y1_piece(lo, xs, rhos)*y1_piece(mid, xs, rhos) <= 0: hi = mid
                else: lo = mid
            out.append(0.5*(lo+hi))
            if len(out) >= N_eig: break
        lam = batch[-1]*step
    return np.array(sorted(out))

print("=== Weyl constant check: lambda_n*(int sqrt rho)^2/(n pi)^2 -> 1 ===")
for name, xs, rhos in [
    ("const 4", [1.0], [4.0]),
    ("two-step [1,4,1] (0.25,0.25,0.5)", [0.25,0.5,0.75,1.0], [1,4,1,1]),
    ("alt [4,1]x4", [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0], [4,1,4,1,4,1,4,1]),
    ("three-step [1,2,4,2,1]", [0.2,0.4,0.6,0.8,1.0], [1,2,4,2,1]),
]:
    lams = eigvals_piece(xs, rhos, 40)
    L = 1.0
    I = sum(np.sqrt(r)*dx for r, dx in zip(rhos, np.diff([0.0]+xs)))
    c = (np.pi/L)**2 / I**2
    vals = lams / (np.arange(1, 41)**2)
    print(f"  {name}:  int sqrt rho = {I:.6f}")
    print(f"    n=1,5,10,20,30,40: {[round(float(vals[i]),4) for i in (0,4,9,19,29,39)]}")
    print(f"    lambda_n ~ C n^2 with C = {c:.6f};  ratios to C: "
          f"{[round(float(vals[i]/c),4) for i in (0,4,9,19,29,39)]}")
