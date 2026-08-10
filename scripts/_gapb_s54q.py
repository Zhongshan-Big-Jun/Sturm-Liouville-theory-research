# -*- coding: utf-8 -*-
"""Session 54q: N1 sign on left-branch region; good-root phase ranges over many R.
EVIDENCE."""
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from _gapb_s54 import well_data

print("good-root phases (A=B) vs pi/2 and pi/(tau+1):")
Rs=[1.05,1.1,1.2,1.3,1.4,1.5,1.6,1.8,2,2.5,3,4,5,7,10,20,50,100,200,400]
for R in Rs:
    # find symmetric good root by 1D search on v=a (solve R1(v,1-v)=0)
    vs=np.linspace(0.05,0.49,300)
    R1s=[well_data(v,1-v,R)['R1'] for v in vs]
    vstar=None
    for i in range(len(vs)-1):
        if R1s[i]*R1s[i+1]<0:
            from scipy.optimize import brentq
            vstar=brentq(lambda v: well_data(v,1-v,R)['R1'], vs[i], vs[i+1], xtol=1e-12)
            break
    if vstar is None: continue
    d=well_data(vstar,1-vstar,R); p=d['p']
    print(f"  R={R:6.2f}: v*={vstar:.5f} A={p['A']:.4f} (<pi/2? {p['A']<np.pi/2}) tau={p['tau']:.4f} pi/(tau+1)={np.pi/(p['tau']+1):.4f} (A>xmid? {p['A']>np.pi/(p['tau']+1)})")
