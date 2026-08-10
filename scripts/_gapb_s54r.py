# -*- coding: utf-8 -*-
"""Session 54r: comprehensive off-axis E=0 branch survey + R1=0 curve + R2 sign.
EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from _gapb_s54 import well_data

def E_of(a,b,R): return well_data(a,b,R)['E']

def branch_roots(a,R,ng=900):
    """all b in (a+0.003, 0.999) with E=0, excluding diagonal and symmetric line"""
    bs=np.linspace(a+0.003,0.999,ng)
    Es=np.array([E_of(a,bb,R) for bb in bs])
    out=[]
    for i in range(len(bs)-1):
        if Es[i]*Es[i+1]<0:
            b0=brentq(lambda bb:E_of(a,bb,R),bs[i],bs[i+1],xtol=1e-12)
            if abs(a+b0-1)>1e-3 and abs(a-b0)>1e-3:
                out.append(b0)
    return out

print("Off-axis E=0 branch survey (a-grid 0.01..0.5):")
for R in [1.52,1.6,2.0,3.0,4.0,10.0,100.0]:
    pts=[]
    for a in np.linspace(0.01,0.50,50):
        for b in branch_roots(a,R):
            d=well_data(a,b,R)
            pts.append((a,b,d))
    if not pts:
        print(f"  R={R}: no off-axis branch in a in [0.01,0.5]"); continue
    Ns=np.array([p[2]['N1'] for p in pts]); As=np.array([p[2]['p']['A'] for p in pts]); Bs=np.array([p[2]['p']['B'] for p in pts])
    print(f"  R={R}: {len(pts)} pts; N1 in [{Ns.min():+.3f},{Ns.max():+.3f}], N1>=0: {(Ns>=-1e-9).sum()}")
    print(f"       A in [{As.min():.3f},{As.max():.3f}], B in [{Bs.min():.3f},{Bs.max():.3f}], all sign-consistent: {all(p[2]['sg_cons'] for p in pts)}")
