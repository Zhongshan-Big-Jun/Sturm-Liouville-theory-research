# -*- coding: utf-8 -*-
"""Session 54j: is r_tau monotone on the region where P_tau(A)+P_tau(B)=(2-tau)pi?
Test: for R in list, find (A,B) solutions of P-sum with tau; check r_tau monotonicity on their range.
EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def alpha(x,m): return np.arctan2(np.sin(x)/m, np.cos(x))
def Ptau(x,tau,m): return alpha(tau*x,m)-tau*alpha(x,m)
def J(x,m): return np.sin(x)**2/(np.sin(x)**2+m*m*np.cos(x)**2)

def surface_tau(A,B,m):
    f=lambda t: Ptau(A,t,m)+Ptau(B,t,m)-(2-t)*np.pi
    if f(1.0001)*f(1.999)>0: return None
    return brentq(f,1.0001,1.999,xtol=1e-12)

for R in [1.52,1.6,2.0,3.0,4.0,10.0,100.0]:
    m=np.sqrt(R)
    # find diagonal solution A=B=A*(tau) for various tau in valid range
    taus=np.linspace(1.05,1.99,60)
    diag=[]
    for tau in taus:
        # solve 2P(A)=(2-tau)pi
        f=lambda A: 2*Ptau(A,tau,m)-(2-tau)*np.pi
        # A in (0,pi/tau)
        ok=False
        for lo in np.linspace(1e-4, np.pi/tau-1e-4, 30):
            pass
        try:
            # find a root by scanning
            xs=np.linspace(1e-4,np.pi/tau-1e-4,2000)
            fs=f(xs)
            for i in range(len(xs)-1):
                if fs[i]*fs[i+1]<0:
                    A0=brentq(f,xs[i],xs[i+1],xtol=1e-12)
                    diag.append((tau,A0)); break
        except Exception:
            pass
    if not diag: continue
    # For the good root tau value: check monotonicity of r_tau on (pi/(tau+1), pi/tau) and (0,pi/(tau+1))
    # find tau at good root from data: use known good roots
    good={1.6:(0.407075,0.592925),2.0:(0.401037,0.598963),3.0:(0.390127,0.609873),4.0:(0.382598,0.617402),10.0:(0.361313,0.638687),100.0:(0.334804,0.665196)}
    if R not in good: continue
    a,b=good[R]
    from _gapb_s54 import well_data
    tau=well_data(a,b,R)['p']['tau']
    xmid=np.pi/(tau+1)
    for name,(lo,hi) in [("left",(1e-5,xmid)),("right",(xmid+1e-5,np.pi/tau-1e-5))]:
        xs=np.linspace(lo,hi,2000)
        rr=np.array([np.log(J(tau*x,m)/J(x,m)) for x in xs])
        d=np.diff(rr)
        inc=(d>1e-12).sum(); dec=(d<-1e-12).sum()
        print(f"R={R} tau={tau:.4f} {name} branch ({lo:.3f},{hi:.3f}): increasing steps={inc} decreasing={dec}")
