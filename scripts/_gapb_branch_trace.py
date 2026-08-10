# -*- coding: utf-8 -*-
"""Session 54: trace E=0 branches via continuation; check N1 sign, R1/R2, D monotonicity.
EVIDENCE only.
"""
import numpy as np
from scipy.optimize import brentq, root_scalar
from _gapb_s54 import well_data, eigs_fast, norm_closed, phases, Xb

def E_of(a,b,R):
    return well_data(a,b,R)['E']

def branch_point(a, R, bgrid=1400, lo=1e-6, hi=0.999):
    """for fixed a, find b-values with E=0 (off-axis) via sign scan + brentq"""
    bs=np.linspace(lo,hi,bgrid)
    Es=np.array([well_data(a,bb,R)['E'] for bb in bs])
    pts=[]
    for i in range(len(bs)-1):
        if Es[i]*Es[i+1]<0:
            b0=brentq(lambda bb: E_of(a,bb,R), bs[i], bs[i+1], xtol=1e-13)
            if abs(a+b0-1)>2e-3:  # off-axis
                pts.append(b0)
    return pts

def trace(R, amax=0.45, na=90):
    rows=[]
    for a in np.linspace(1e-4, amax, na):
        for b in branch_point(a,R):
            d=well_data(a,b,R)
            rows.append((a,b,d))
    return rows

for R in [1.6, 2.0, 3.0, 4.0, 10.0]:
    rows=trace(R)
    if not rows:
        print(f"R={R}: no off-axis E=0 branch found (a up to 0.45)"); continue
    Ns=np.array([r[2]['N1'] for r in rows]); Ds=np.array([r[2]['p']['lam2']-r[2]['p']['lam1'] for r in rows])
    aarr=np.array([r[0] for r in rows])
    print(f"R={R}: {len(rows)} branch pts, a in [{aarr.min():.4f},{aarr.max():.4f}]")
    print(f"   N1 in [{Ns.min():+.4f},{Ns.max():+.4f}]  N1>=0 count: {(Ns>=-1e-9).sum()}")
    print(f"   D in [{Ds.min():.4f},{Ds.max():.4f}]  sign-consistency all: {all(r[2]['sg_cons'] for r in rows)}")
    # D monotonicity along a
    order=np.argsort(aarr)
    da=np.diff(Ds[order]); aa=aarr[order]
    neg=(da< -1e-9).sum(); pos=(da>1e-9).sum()
    print(f"   D along branch (sorted by a): decreasing steps={neg}, increasing steps={pos}")
    # sample a few
    for (a,b,d) in rows[::max(1,len(rows)//6)][:6]:
        print(f"     a={a:.5f} b={b:.5f} a+b={a+b:.5f} N1={d['N1']:+.4f} R1={d['R1']:+.3e} R2={d['R2']:+.3e} D={d['p']['lam2']-d['p']['lam1']:.4f} sg={d['sg_cons']}")
