# -*- coding: utf-8 -*-
"""Session 54d: verify (M'') with corrected alpha. EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec
from _gapb_s54 import well_data

def alpha(x,m):
    return np.arctan2(np.sin(x)/m, np.cos(x))   # tan alpha = tan x / m, alpha in (0,pi)

def ufun(x,m):
    # u in (0,pi), cot u = -m cot x  (sin u > 0)
    return np.arctan2(1.0, -m/np.tan(x))

def Mpp(a,b,R):
    d=well_data(a,b,R); p=d['p']
    tau,A,B,psi,m=p['tau'],p['A'],p['B'],p['psi'],p['m']
    return alpha(tau*A,m)-tau*alpha(A,m)-(ufun(tau*B,m)-tau*ufun(B,m))-np.pi

def check(R,pts,label):
    for (a,b) in pts:
        d=well_data(a,b,R); p=d['p']
        print(f"  {label} (a,b)=({a},{b}) R={R}: M''={Mpp(a,b,R):+.3e} tau={p['tau']:.4f} A={p['A']:.4f} B={p['B']:.4f} E={d['E']:+.2e}")

check(4.0, [(0.382598,0.617402),(0.2,0.8),(0.1,0.8690044018112135)], "sym/branch")
check(1.6, [(0.407075,0.592925)], "sym")
check(10.0, [(0.361313,0.638687)], "sym")
# find off-axis branch for R=4 at several a
def E_of(a,b,R): return well_data(a,b,R)['E']
for a0 in [0.02,0.06,0.10,0.14]:
    bs=np.linspace(a0+0.005,0.98,800)
    Es=np.array([E_of(a0,bb,4.0) for bb in bs])
    for i in range(len(bs)-1):
        if Es[i]*Es[i+1]<0:
            b0=brentq(lambda bb: E_of(a0,bb,4.0),bs[i],bs[i+1],xtol=1e-13)
            if abs(a0+b0-1)>2e-3 and abs(a0-b0)>2e-3:
                check(4.0,[(a0,b0)],f"off-axis a={a0}")
                break
