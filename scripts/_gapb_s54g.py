# -*- coding: utf-8 -*-
"""Session 54g: phase-space structure. For grid (A,B), solve tau from P-sum,
compute E (r_tau equality) and R1 (norm identity). Find zero curves & intersections.
EVIDENCE only."""
import numpy as np
from scipy.optimize import brentq, root_scalar
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def alpha(x,m): return np.arctan2(np.sin(x)/m, np.cos(x))
def alinv(X,m):
    # solve alpha(x)=X: tan X = tan x/m -> tan x = m tan X (branch: x in (0,pi))
    return np.arctan2(m*np.sin(X), np.cos(X))  # x in (0,pi): tan x = m tan X
def Ptau(x,tau,m): return alpha(tau*x,m)-tau*alpha(x,m)
def P_sum_tau(A,B,m):  # solve tau in (1,2) s.t. P(A)+P(B)=(2-tau)pi  (assume exists)
    f=lambda t: alpha(t*A,m)-t*alpha(A,m)+alpha(t*B,m)-t*alpha(B,m)-(2-t)*np.pi
    return f
def W(x,m): return np.sin(x)**2+m*m*np.cos(x)**2
def J(x,m): return np.sin(x)**2/W(x,m)

def surface_tau(A,B,m,lo=1.001,hi=2.0):
    f=P_sum_tau(A,B,m)
    if f(lo)*f(hi)>0: return None
    try:
        return brentq(f,lo,hi,xtol=1e-12)
    except Exception:
        return None

def R1_norm(A,B,tau,m):
    # n2/n1 - sin^2(tau A)/sin^2 A with n from closed form; need psi = pi-alpha(A)-alpha(B), s1=(A+m*psi+B)/m
    psi=np.pi-alpha(A,m)-alpha(B,m)
    if psi<=0: return np.nan
    s1=(A+m*psi+B)/m
    def n(s):
        AA=m*s*(A/(m*s)); # phases re-derived from s: a=A/(m s), etc. -> phases are A,psi,B again
        X0=np.sin(A)/m; Y0=np.cos(A)
        nL=(A/(m*s))/(2*s**2)-np.sin(2*A)/(4*m*s**3)
        nM=(1/s**3)*(W(A,m)*psi/(2*m**2)+(X0**2-Y0**2)*np.sin(2*psi)/4+X0*Y0*np.sin(psi)**2)
        C2=W(A,m)/W(B,m)
        nR=C2*((B/(m*s))/(2*s**2)-np.sin(2*B)/(4*m*s**3))
        return nL+nM+nR
    n1=n(s1); n2=n(tau*s1)
    return n2/n1-np.sin(tau*A)**2/np.sin(A)**2

def E_val(A,B,tau,m):
    return np.log(J(tau*A,m)/J(A,m))-np.log(J(tau*B,m)/J(B,m))

R=4.0; m=np.sqrt(R)
# grid in A,B with tau from surface
ng=120
vals=[]
for i,A in enumerate(np.linspace(0.02,1.70,ng)):
    for j,B in enumerate(np.linspace(0.02,1.70,ng)):
        tau=surface_tau(A,B,m)
        if tau is None: continue
        if A+m*(np.pi-alpha(A,m)-alpha(B,m))+B <= 0: continue
        E=E_val(A,B,tau,m); R1=R1_norm(A,B,tau,m)
        vals.append((A,B,tau,E,R1))
vals=np.array(vals)
print("R=4 grid points with tau:",len(vals))
# zero-curve points
E0=vals[np.abs(vals[:,3])<0.02]
R10=vals[np.abs(vals[:,4])<0.02]
print("E~0 points:",len(E0)," R1~0 points:",len(R10))
if len(E0)>0:
    print("  E0: A in [%.3f,%.3f] B in [%.3f,%.3f]"%(E0[:,0].min(),E0[:,0].max(),E0[:,1].min(),E0[:,1].max()))
if len(R10)>0:
    print("  R10: A in [%.3f,%.3f] B in [%.3f,%.3f]"%(R10[:,0].min(),R10[:,0].max(),R10[:,1].min(),R10[:,1].max()))
# where both near zero
both=vals[(np.abs(vals[:,3])<0.02)&(np.abs(vals[:,4])<0.02)]
print("both near zero:",len(both))
for r in both[:20]:
    print("   A=%.4f B=%.4f tau=%.4f E=%.4f R1=%.4f"%(r[0],r[1],r[2],r[3],r[4]))
