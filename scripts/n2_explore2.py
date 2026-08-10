# -*- coding: utf-8 -*-
"""Fine analysis of 2-block family: D(t), f(t) at jump, critical points."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

NPT = 1500
def s_of(blocks, npts=NPT):
    return lams_fast(blocks, 2, npts=npts)
def D_of(blocks, s=None):
    if s is None: s = s_of(blocks)
    return s[1]**2 - s[0]**2
def f_at(blocks, x, s=None):
    if s is None: s = s_of(blocks)
    lam = s**2
    x = np.clip(np.atleast_1d(np.asarray(x, float)), 1e-12, 1-1e-12)
    u1 = y_at(blocks, s[0], x)/np.sqrt(norm2(blocks, s[0]))
    u2 = y_at(blocks, s[1], x)/np.sqrt(norm2(blocks, s[1]))
    return lam[0]*u1**2 - lam[1]*u2**2

for R in (4.0, 2.0, 10.0):
    ts = np.linspace(1e-3, 1-1e-3, 800)
    bls = [[(t,1.0),(1-t,R)] for t in ts]
    # vectorize eigenvalues roughly
    Ds = []
    fs = []
    for t, bl in zip(ts, bls):
        s = s_of(bl)
        Ds.append(s[1]**2 - s[0]**2)
        fs.append(f_at(bl, t, s)[0])
    Ds = np.array(Ds); fs = np.array(fs)
    # critical points: f=0 crossings
    sc = np.nonzero((fs[1:]*fs[:-1]) < 0)[0]
    print(f"R={R}: #f-crossings={len(sc)}; D range [{Ds.min():.6f},{Ds.max():.6f}]; D(0)={Ds[0]:.4f} D(1)={Ds[-1]:.4f}")
    for i in sc:
        t0 = (ts[i]+ts[i+1])/2
        print(f"   f-crossing at t={t0:.5f}: D={np.interp(t0, ts, Ds):.6f}  (3pi^2={3*np.pi**2:.4f})")
    # where is f>0?
    pos = np.where(fs > 0)[0]
    if len(pos):
        print(f"   f>0 region: t in [{ts[pos[0]]:.4f}, {ts[pos[-1]]:.4f}], max f={fs.max():.3f}")
    # derivative check: numerical dD/dt vs -(R-1) f
    dD = np.gradient(Ds, ts)
    rel = dD[10:-10] / (-(R-1)*fs[10:-10])
    print(f"   dD/dt vs -(R-1)f: median ratio={np.median(rel):.6f}")
