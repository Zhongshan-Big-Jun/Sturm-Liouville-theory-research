# -*- coding: utf-8 -*-
"""Session 54e: verify secular reduction psi=pi-alpha(A)-alpha(B) and P-sum.
EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq
from _gapb_s54 import well_data

def alpha(x,m): return np.arctan2(np.sin(x)/m, np.cos(x))
def Ptau(x,tau,m): return alpha(tau*x,m)-tau*alpha(x,m)

def check(a,b,R):
    d=well_data(a,b,R); p=d['p']
    tau,A,B,psi,m=p['tau'],p['A'],p['B'],p['psi'],p['m']
    rhs= np.pi - alpha(A,m) - alpha(B,m)
    print(f"  (a,b)=({a},{b}) R={R}: psi={psi:.6f} pi-aA-aB={rhs:.6f} diff={psi-rhs:+.2e}")
    print(f"      P(A)+P(B)={(Ptau(A,tau,m)+Ptau(B,tau,m)):.6f} (2-tau)pi={(2-tau)*np.pi:.6f} diff={Ptau(A,tau,m)+Ptau(B,tau,m)-(2-tau)*np.pi:+.2e}")

check(0.382598,0.617402,4.0)
check(0.407075,0.592925,1.6)
check(0.361313,0.638687,10.0)
check(0.14,0.9184329045602553,4.0)
check(0.02,0.8472454043205739,4.0)

# structure of P_tau for R=4 (m=2): find tau range at good roots ~1.69; off-axis ~1.78-1.8
m=2.0; tau=1.6941
xs=np.linspace(1e-6, np.pi/tau-1e-6, 5000)
P=np.array([Ptau(x,tau,m) for x in xs])
im=np.argmax(P)
print(f"R=4 tau={tau}: max P at x={xs[im]:.4f} (pi/(tau+1)={np.pi/(tau+1):.4f}), Pmax={P[im]:.4f}")
print(f"  P(0+)={P[0]:.4f} P(pi/tau-)={P[-1]:.4f}  (2-tau)pi={(2-tau)*np.pi:.4f}")
# where does P(x)+P(y)=(2-tau)pi have off-diagonal solutions? sample
sol=[]
for x in np.linspace(0.01, np.pi/tau-0.01, 400):
    for y in np.linspace(0.01, np.pi/tau-0.01, 400):
        if abs(Ptau(x,tau,m)+Ptau(y,tau,m)-(2-tau)*np.pi)<0.01:
            sol.append((x,y))
print(f"  sampled P-sum solutions near diagonal: count={len(sol)}; max |x-y| = {max(abs(x-y) for x,y in sol) if sol else 0:.4f}")
