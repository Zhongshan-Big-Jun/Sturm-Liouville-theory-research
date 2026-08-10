# -*- coding: utf-8 -*-
"""Session 54h: phase-space structure (fixed norm). EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def alpha(x,m): return np.arctan2(np.sin(x)/m, np.cos(x))
def Ptau(x,tau,m): return alpha(tau*x,m)-tau*alpha(x,m)
def W(x,m): return np.sin(x)**2+m*m*np.cos(x)**2
def J(x,m): return np.sin(x)**2/W(x,m)

def surface_tau(A,B,m):
    f=lambda t: Ptau(A,t,m)+Ptau(B,t,m)-(2-t)*np.pi
    if f(1.0001)*f(1.999)>0: return None
    try: return brentq(f,1.0001,1.999,xtol=1e-12)
    except Exception: return None

def norm_phases(AA,psi,BB,m,s):
    X0=np.sin(AA)/m; Y0=np.cos(AA)
    nL=(AA/(m*s))/(2*s**2)-np.sin(2*AA)/(4*m*s**3)
    nM=(1/s**3)*(W(AA,m)*psi/(2*m**2)+(X0**2-Y0**2)*np.sin(2*psi)/4+X0*Y0*np.sin(psi)**2)
    C2=W(AA,m)/W(BB,m)
    nR=C2*((BB/(m*s))/(2*s**2)-np.sin(2*BB)/(4*m*s**3))
    return nL+nM+nR

def data(A,B,tau,m):
    psi=np.pi-alpha(A,m)-alpha(B,m)
    s1=(A+m*psi+B)/m
    n1=norm_phases(A,psi,B,m,s1)
    n2=norm_phases(tau*A,tau*psi,tau*B,m,tau*s1)
    R1=n2/n1-np.sin(tau*A)**2/np.sin(A)**2
    E=np.log(J(tau*A,m)/J(A,m))-np.log(J(tau*B,m)/J(B,m))
    return dict(psi=psi,s1=s1,n1=n1,n2=n2,R1=R1,E=E)

def scan(R, amax=1.75, ng=140, tolE=0.015, tolR=0.015):
    m=np.sqrt(R)
    rows=[]
    for A in np.linspace(0.02,amax,ng):
        for B in np.linspace(0.02,amax,ng):
            tau=surface_tau(A,B,m)
            if tau is None: continue
            d=data(A,B,tau,m)
            if d['psi']<=0: continue
            rows.append((A,B,tau,d['E'],d['R1']))
    arr=np.array(rows)
    E0=arr[np.abs(arr[:,3])<tolE]; R10=arr[np.abs(arr[:,4])<tolR]
    both=arr[(np.abs(arr[:,3])<tolE)&(np.abs(arr[:,4])<tolR)]
    print(f"R={R}: pts={len(arr)} E~0={len(E0)} R1~0={len(R10)} both~0={len(both)}")
    # cluster both points
    if len(both):
        for r in both[:12]:
            print(f"    A={r[0]:.4f} B={r[1]:.4f} tau={r[2]:.4f} E={r[3]:+.4f} R1={r[4]:+.4f}  a+b? A vs B: {abs(r[0]-r[1]):.4f}")
    return arr

for R in [1.6,2.0,3.0,4.0,10.0]:
    scan(R)
