# -*- coding: utf-8 -*-
"""Session 54o: parametric curve (P(x), rho(x)) = (P_tau(x), log r_tau(x)).
Look for structure: is rho a function of P on each branch? monotone?
EVIDENCE."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def alpha(x,m): return np.arctan2(np.sin(x)/m, np.cos(x))
def Ptau(x,tau,m): return alpha(tau*x,m)-tau*alpha(x,m)
def J(x,m): return np.sin(x)**2/(np.sin(x)**2+m*m*np.cos(x)**2)

for R,tau in [(4.0,1.6941),(100.0,1.4667)]:
    m=np.sqrt(R)
    xs=np.linspace(1e-5, np.pi/tau-1e-5, 6000)
    P=np.array([Ptau(x,tau,m) for x in xs])
    rho=np.array([np.log(J(tau*x,m)/J(x,m)) for x in xs])
    xmid=np.pi/(tau+1)
    # split branches
    L=xs< xmid; Rg=xs>xmid
    print(f"R={R} tau={tau}: xmid={xmid:.4f}")
    print(f"  left: P in [{P[L].min():.4f},{P[L].max():.4f}] rho in [{rho[L].min():.4f},{rho[L].max():.4f}]")
    print(f"  right: P in [{P[Rg].min():.4f},{P[Rg].max():.4f}] rho in [{rho[Rg].min():.4f},{rho[Rg].max():.4f}]")
    # is rho monotone in P on each branch? check via sorting
    for nm,mask in [("left",L),("right",Rg)]:
        idx=np.argsort(P[mask])
        rP=rho[mask][idx]; PP=P[mask][idx]
        dd=np.diff(rP)
        inc=(dd>1e-9).sum(); dec=(dd<-1e-9).sum()
        print(f"    {nm}: rho as function of P: inc={inc} dec={dec} (of {len(dd)})")
    # P-sum level (2-tau)pi
    c=(2-tau)*np.pi
    print(f"  (2-tau)pi={c:.4f}")
    # where P(x)=c/2 (diagonal candidate)
    d2=np.abs(P-c/2)
    i=np.argmin(d2)
    print(f"  P=c/2 closest at x={xs[i]:.4f} P={P[i]:.4f} rho={rho[i]:.4f}")
