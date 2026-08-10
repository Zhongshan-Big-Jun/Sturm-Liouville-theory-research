# -*- coding: utf-8 -*-
"""n2_seeds.py: verify known symmetric seeds are self-consistent; D values."""
import numpy as np
from scipy.optimize import least_squares
from gap_lib import lams_fast, y_at, norm2

def s_of(blocks, npts=2000):
    return lams_fast(blocks, 2, npts=npts)

def f_at(blocks, x, s=None, npts=2000):
    if s is None:
        s = s_of(blocks, npts)
    lam = s**2
    x = np.atleast_1d(np.asarray(x, dtype=float))
    x = np.clip(x, 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    if mode == "SUP":
        return [(a,1.0),(b,R),(c,1.0)]
    return [(a,R),(b,1.0),(c,R)]

SEEDS = {  # (R, mode) -> a (symmetric, b = 1-2a)
    (2.0,"SUP"): 0.43669594, (4.0,"SUP"): 0.45148547, (10.0,"SUP"): 0.46693119, (100.0,"SUP"): 0.48852937,
    (2.0,"INF"): 0.40103739, (4.0,"INF"): 0.38259826, (10.0,"INF"): 0.36131311, (100.0,"INF"): 0.33480385,
}

for (R, mode), a0 in SEEDS.items():
    b0 = 1 - 2*a0
    bl = make_blocks(mode, R, a0, b0)
    s = s_of(bl)
    fv = f_at(bl, [a0, a0+b0], s=s)
    D = s[1]**2 - s[0]**2
    print(f"R={R:6.1f} {mode}: a={a0:.8f} b={b0:.8f} f(a)={fv[0]:+.3e} f(a+b)={fv[1]:+.3e} D={D:.10f}")
    # refine
    res = least_squares(lambda ab: f_at(make_blocks(mode,R,*ab), [ab[0], ab[0]+ab[1]]), [a0,b0], xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=300)
    a, b = res.x
    bl2 = make_blocks(mode, R, a, b)
    s2 = s_of(bl2)
    fv2 = f_at(bl2, [a, a+b], s=s2)
    print(f"   refined: a={a:.10f} b={b:.10f} sym_def={a-(1-a-b):+.2e} resid={np.max(np.abs(fv2)):.1e} D={s2[1]**2-s2[0]**2:.10f}")
