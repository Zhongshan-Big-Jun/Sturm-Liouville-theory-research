# -*- coding: utf-8 -*-
"""Session 54p: Q_k = n_k sin^2(A_k) along off-axis E=0 branches and near good root.
Also Phi(x) structure and r_tau monotone regions. EVIDENCE."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from _gapb_s54 import well_data

def Phi(x,q):
    return x/np.tan(x)/(1+q*np.cos(x)**2)

# Phi structure for several q
print("Phi structure (increasing/decreasing regions):")
for q in [0.5,1,3,9,30,99]:
    xs=np.linspace(1e-4,np.pi-1e-4,20000)
    Ph=Phi(xs,q)
    d=np.diff(Ph)
    # count sign changes of derivative
    sc=0; regions=[]
    prev=np.sign(d[0])
    for i in range(1,len(d)):
        s=np.sign(d[i])
        if s!=prev:
            regions.append((xs[i],prev)); prev=s
    print(f"  q={q}: Phi range [{Ph.min():.3f},{Ph.max():.3f}], deriv sign changes at x={[round(r[0],3) for r in regions]}")

# Q structure on off-axis branch R=4
def Q(a,b,R):
    d=well_data(a,b,R); p=d['p']
    return d['n2']*np.sin(p['tau']*p['A'])**2 - d['n1']*np.sin(p['A'])**2
print()
print("Q2-Q1 = n2 sin^2(tauA) - n1 sin^2 A along R=4 off-axis branch:")
for a in [0.02,0.06,0.10,0.14]:
    bs=np.linspace(a+0.005,0.98,600)
    Es=np.array([well_data(a,bb,4.0)['E'] for bb in bs])
    for i in range(len(bs)-1):
        if Es[i]*Es[i+1]<0:
            b0=brentq(lambda bb: well_data(a,bb,4.0)['E'],bs[i],bs[i+1],xtol=1e-12)
            if abs(a+b0-1)>2e-3 and abs(a-b0)>2e-3:
                d=well_data(a,b0,4.0); p=d['p']
                print(f"  a={a:.3f} b={b0:.4f}: Q2-Q1={Q(a,b0,4.0):+.4f} N1={d['N1']:+.4f} A={p['A']:.4f} B={p['B']:.4f} tau={p['tau']:.4f}")
