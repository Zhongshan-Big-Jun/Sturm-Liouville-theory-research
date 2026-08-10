# -*- coding: utf-8 -*-
"""#1 verify: ratios -> 1 via Weyl asymptotics (correct root finder)."""
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

print("=== ratios lambda_{n+1}/lambda_n, should -> 1 ===")
for name, xs, rhos in [
    ("two-step [1,4,1]  (0.25,0.25,0.5)", [0.25,0.5,0.75,1.0], [1,4,1,1]),
    ("alt [4,1]x4", [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0], [4,1,4,1,4,1,4,1]),
    ("const 4", [1.0], [4.0]),
]:
    lams = eigvals_piece(xs, rhos, 60)
    ratios = lams[1:]/lams[:-1]
    print(f"  {name}:")
    print(f"    n=1..5: {[round(float(r),4) for r in ratios[:5]]}")
    for n in (10, 20, 30, 40, 50):
        print(f"    n={n}: ratio = {float(ratios[n-1]):.6f}  (1 + {float(ratios[n-1])-1:.2e})")
