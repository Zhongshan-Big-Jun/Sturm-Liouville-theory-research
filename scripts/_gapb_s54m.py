# -*- coding: utf-8 -*-
"""Session 54m: good-root phases vs right branch (fixed). EVIDENCE."""
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def Psi(x,q):
    W=1+q*np.cos(x)**2
    return x/np.tan(x)+q*x*np.sin(x)*np.cos(x)/W

good={1.5:(0.408798,1.891551),1.6:(0.407075,1.8759),2.0:(0.401037,1.8247),2.5:(0.395007,1.7781),
      3.0:(0.390127,1.7433),4.0:(0.382598,1.6941),10.0:(0.361313,1.5778),100.0:(0.334804,1.4667)}

from _gapb_s54 import well_data
print("R | A=B | pi/(tau+1) | on right? | r_tau' viol on [A,pi/tau] | min Psi-gap")
for R,(a,tau0) in sorted(good.items()):
    b=1-a
    d=well_data(a,b,R); p=d['p']
    tau,A = p['tau'], p['A']
    xmid=np.pi/(tau+1)
    q=R-1
    xs=np.linspace(A+1e-6, np.pi/tau-1e-6, 4000)
    if len(xs)<3:
        print(f"{R:7.2f} | A={A:.4f} | xmid={xmid:.4f} | {A>=xmid} | tiny"); continue
    dg=np.array([Psi(tau*x,q)-Psi(x,q) for x in xs])
    viol=int((dg>0).sum())
    print(f"{R:7.2f} | A={A:.4f} | xmid={xmid:.4f} | {A>=xmid} | viol={viol}/{len(dg)} | maxgap={dg.max():+.3e}")
