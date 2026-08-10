# -*- coding: utf-8 -*-
"""Verify v-monotonicity and single-band structure on several rho."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2, eigfuns, fd_check

def analyze(blocks, label, fine=4001):
    s = lams_fast(blocks, 3)
    lam = s**2
    xs = np.linspace(0,1,fine)
    u = eigfuns(blocks, s[:2], xs)
    u1, u2 = u[0], u[1]
    h = xs[1]-xs[0]
    # v = u2/u1 and W = u1*u2' - u1'*u2 (use exact TM derivatives instead of FD)
    # exact: y' in a block = n10 (=-w sin) times ... use central diff on fine grid for simplicity
    du1 = np.gradient(u1, h); du2 = np.gradient(u2, h)
    W = u1*du2 - du1*u2
    v = u2/u1
    f = lam[0]*u1**2 - lam[1]*u2**2
    pos = f > 1e-12
    # count components
    comps = 0; prev = False
    for p in pos:
        if p and not prev: comps += 1
        prev = p
    mid = slice(fine//5, 4*fine//5)
    dec = np.all(np.diff(v[mid]) < 1e-8)
    # where f>0 interval: find a,b
    nz = np.nonzero(pos)[0]
    a = xs[nz[0]] if len(nz) else np.nan
    b = xs[nz[-1]] if len(nz) else np.nan
    print(f"{label}: lam1={lam[0]:.5f} lam2={lam[1]:.5f} D={lam[1]-lam[0]:.5f} "
          f"comps(f>0)={comps} a={a:.4f} b={b:.4f} v-dec={dec} Wmax_mid={np.max(np.abs(W[mid])):.3e} "
          f"v(0)={v[2]:.4f} v(1)={v[-3]:.4f}")

R = 4.0
u_ = 0.451485; ui = 0.382598
analyze([(u_,1.0),(1-2*u_,R),(u_,1.0)], "SUP [1,4,1]")
analyze([(ui,R),(1-2*ui,1.0),(ui,R)], "INF [4,1,4]")
analyze([(0.3,1.0),(0.4,R),(0.3,1.0)], "[1,4,1] u=.3")
analyze([(0.4,1.0),(0.2,R),(0.4,1.0)], "[1,4,1] u=.4")
analyze([(0.1,R),(0.3,1.0),(0.6,R)], "[R,1,R] asym")
analyze([(0.2,2.0),(0.3,1.0),(0.5,2.0)], "[2,1,2] R=2")
# cross-check FD vs TM for one config
lam_fd, u_fd, xs = fd_check(lambda x: np.where((x>u_)&(x<1-u_), R, 1.0))
print("FD check [1,4,1]: lam =", lam_fd[:2], "vs TM", (lams_fast([(u_,1.0),(1-2*u_,R),(u_,1.0)],3)**2)[:2])
