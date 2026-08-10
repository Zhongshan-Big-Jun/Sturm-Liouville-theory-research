# -*- coding: utf-8 -*-
"""Session 54l: good-root phases vs right branch and r_tau non-monotone region. EVIDENCE."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def Psi(x,q):
    W=1+q*np.cos(x)**2
    return x/np.tan(x)+q*x*np.sin(x)*np.cos(x)/W

good={1.05:(0.4175,None),1.1:(0.4154,None),1.2:(0.4115,None),1.5:(0.408798,1.891551),1.52:None,
      1.6:(0.407075,1.8759),2.0:(0.401037,1.8247),2.5:(0.395007,1.7781),3.0:(0.390127,1.7433),
      4.0:(0.382598,1.6941),10.0:(0.361313,1.5778),100.0:(0.334804,1.4667),400.0:(0.33135,None)}

from _gapb_s54 import well_data
print("R | a(v*) | A=B | pi/(tau+1) | on right? | r_tau' violations on [A, pi/tau]")
for R,(a,tau0) in sorted(good.items()):
    if tau0 is None: continue
    b=1-a
    d=well_data(a,b,R); p=d['p']
    tau,A = p['tau'], p['A']
    xmid=np.pi/(tau+1)
    q=R-1
    xs=np.linspace(max(A,1e-6)+1e-6, np.pi/tau-1e-6, 4000)
    if len(xs)<3: 
        print(f"{R:7.2f} | A={A:.4f} xmid={xmid:.4f} | on-right={A>=xmid} | (tiny interval)"); continue
    dg=np.array([Psi(tau*x,q)-Psi(x,q) for x in xs])
    viol=int((dg>0).sum())
    print(f"{R:7.2f} | A={A:.4f} | xmid={xmid:.4f} | {A>=xmid} | viol={viol}/{len(dg)}")
