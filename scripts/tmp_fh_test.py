# -*- coding: utf-8 -*-
"""Directly test FH formula d lambda_k/du = -lambda_k * int(d rho/du u_k^2) for INF [R,1,R]."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def lam_of(mode, R, u, k=2, npts=60000):
    b = 1-2*u
    bl = [(u,1.0),(b,R),(u,1.0)] if mode=="SUP" else [(u,R),(b,1.0),(u,R)]
    s = lams_fast(bl, k, npts=npts)
    return s**2, bl, s

R = 4.0
for u in (0.1, 0.2, 0.3, 0.38):
    lam, bl, s = lam_of("INF", R, u)
    u1 = y_at(bl, s[0], np.array([u, 1-u]))/np.sqrt(norm2(bl, s[0]))
    u2 = y_at(bl, s[1], np.array([u, 1-u]))/np.sqrt(norm2(bl, s[1]))
    print(f"u={u}: lam1={lam[0]:.8f} lam2={lam[1]:.8f}")
    print(f"   u1(u)^2={u1[0]**2:.6f} u1(1-u)^2={u1[1]**2:.6f}  u2(u)^2={u2[0]**2:.6f} u2(1-u)^2={u2[1]**2:.6f}")
    print(f"   f(u)={lam[0]*u1[0]**2 - lam[1]*u2[0]**2:+.6f}  f(1-u)={lam[0]*u1[1]**2 - lam[1]*u2[1]**2:+.6f}")
    # finite difference d lam/du (central, h=1e-5)
    h = 1e-5
    lam_p,_,_ = lam_of("INF", R, u+h)
    lam_m,_,_ = lam_of("INF", R, u-h)
    d1 = (lam_p[0]-lam_m[0])/(2*h)
    d2 = (lam_p[1]-lam_m[1])/(2*h)
    fh1 = lam[0]*(R-1)*(u1[0]**2 + u1[1]**2)
    fh2 = lam[1]*(R-1)*(u2[0]**2 + u2[1]**2)
    print(f"   d lam1/du = {d1:+.4f}  FH(lam1*(R-1)*sum u1^2) = {fh1:+.4f}")
    print(f"   d lam2/du = {d2:+.4f}  FH(lam2*(R-1)*sum u2^2) = {fh2:+.4f}")
    print(f"   dD/du = {d2-d1:+.4f}  FH(-2(R-1)f) = {-2*(R-1)*(lam[0]*u1[0]**2-lam[1]*u2[0]**2):+.4f}")
    print()
