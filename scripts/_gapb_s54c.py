# -*- coding: utf-8 -*-
"""Session 54c: verify the (M'') separation identity: P_tau(A) - U_tau(B) = pi
at good roots / E=0 branch points, and explore P_tau, U_tau structure.
EVIDENCE only.
"""
import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec
from _gapb_s54 import well_data, eigs_fast

def alpha(x,m):
    return np.arctan2(np.cos(x), np.sin(x)/m)   # in (0,pi) for x in (0,pi)

def ufun(x,m):
    # u in (0,pi), cot u = -m cot x
    return np.arctan2(np.sin(1.0), 1.0)*0 + np.pi - np.arctan2(1.0, -m/np.tan(x)) if False else None

def ufun2(x,m):
    # cot u = -m cot x, u in (0,pi): u = pi/2 - arctan(-m cot x) adjusted
    # use: u = arctan2(1, -m*cotx) gives angle with cot = -m cotx and sin>0? arctan2(y,x) with y=1: sin>0, cot = x/y = -m cotx.
    return np.arctan2(1.0, -m/np.tan(x))

def check(R, pts):
    m=np.sqrt(R)
    for (a,b) in pts:
        d=well_data(a,b,R)
        p=d['p']; tau=p['tau']; A=p['A']; B=p['B']; psi=p['psi']
        P=alpha(tau*A,m)-tau*alpha(A,m)
        U=ufun2(tau*B,m)-tau*ufun2(B,m)
        M=P-U-np.pi
        # direct secular check
        sec1=np.cos(psi)*np.sin(A)/m+np.sin(psi)*np.cos(A)
        sec1b=(-np.sin(psi)*np.sin(A)/m+np.cos(psi)*np.cos(A))
        F1=sec1*np.cos(B)+sec1b*np.sin(B)
        print(f"  (a,b)=({a},{b}) R={R}: M'' = {M:+.3e}   F1(secular)={F1:+.3e}  tau={tau:.4f} A={A:.4f} B={B:.4f} E={d['E']:+.2e}")

print("M'' at symmetric good roots / off-axis branch points")
check(4.0, [(0.382598,0.617402)])
check(1.6, [(0.407075,0.592925)])
check(10.0, [(0.361313,0.638687)])
# off-axis branch: find one for R=4
def E_of(a,b,R):
    return well_data(a,b,R)['E']
R=4.0
a0=0.10
bs=np.linspace(a0+0.01,0.95,600)
Es=np.array([E_of(a0,bb,R) for bb in bs])
for i in range(len(bs)-1):
    if Es[i]*Es[i+1]<0:
        b0=brentq(lambda bb: E_of(a0,bb,R),bs[i],bs[i+1],xtol=1e-13)
        d=well_data(a0,b0,R)
        if abs(a0+b0-1)>1e-3 and abs(a0-b0)>1e-3:
            print(f"R=4 off-axis branch pt a={a0:.4f} b={b0:.4f}")
            check(4.0,[(a0,b0)])
            break
