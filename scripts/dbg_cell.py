# -*- coding: utf-8 -*-
import numpy as np
# independent secular solver for piecewise constant rho on [-1/2,1/2]
def transfer(xs, rhos, lam):
    # return (A,B) such that y = A*cos(w*x)+B*sin(w*x) representation per segment
    # start: y(-1/2)=0, y'(-1/2)=1
    xs_in = [-0.5] + [x for x in xs if -0.5 < x < 0.5] + [0.5]
    yy, yyp = 0.0, 1.0
    cur = -0.5
    for i in range(len(xs_in)-1):
        x1 = xs_in[i+1]
        w = np.sqrt(lam*rhos[i])
        d = x1 - cur
        c, s = np.cos(w*d), np.sin(w*d)
        y1 = yy*c + yyp/w*s
        yp1 = -w*yy*s + yyp*c
        yy, yyp = y1, yp1
        cur = x1
    return yy  # y(1/2)

def eigval_N_sec(xs, rhos, N):
    # find roots of f(lam)=y(1/2;lam) ; the N-th positive root
    roots = []
    lam = 1e-6
    step = 0.5
    prev = transfer(xs, rhos, lam)
    # adaptive scan
    while len(roots) < N and lam < 1e6:
        lam += step
        v = transfer(xs, rhos, lam)
        if prev*v < 0:
            lo, hi = lam-step, lam
            for _ in range(60):
                mid = 0.5*(lo+hi)
                if transfer(xs, rhos, lo)*transfer(xs, rhos, mid) <= 0: hi = mid
                else: lo = mid
            roots.append(0.5*(lo+hi))
        prev = v
        step = min(step*1.05, 5.0)
    return roots

# phi_0: rho=1 on (-1/2,0), rho=2 on (0,1/2)
xs0 = [0.0]; rhos0 = [1.0, 2.0]
r1 = eigval_N_sec(xs0, rhos0, 4)
print("phi_0 evals:", r1[:4])
print("ratio base lam2/lam1:", r1[1]/r1[0])

# phi_n for n=2: rho 1 on (-1/2,-1/4), 2 on (-1/4,1/4), 1 on (1/4,1/2)
xs2 = [-0.25, 0.25]; rhos2 = [1.0, 2.0, 1.0]
r2 = eigval_N_sec(xs2, rhos2, 8)
print("phi_2 evals:", r2[:8])
print("ratio lam4/lam2:", r2[3]/r2[1])
print("lam_2(phi_2)=? 4*lam1(phi0)=", 4*r1[0], " lam_4=? 4*lam2(phi0)=", 4*r1[1])
print("lam2/lam1 of phi2:", r2[1]/r2[0])
