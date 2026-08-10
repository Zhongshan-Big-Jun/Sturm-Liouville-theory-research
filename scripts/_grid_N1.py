import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec

def eigs_fast(a,b,R,k=2,N=600):
    m=np.sqrt(R); smax=2+k*np.pi*m+4
    sp_=np.linspace(1e-9,smax,N)
    d=well_secular_vec(sp_,a,b,R)
    sg=np.signbit(d[1:])!=np.signbit(d[:-1])
    idx=np.nonzero(sg)[0]
    out=[]
    for i in idx[:k]:
        lo,hi=sp_[i],sp_[i+1]
        out.append(brentq(lambda z: well_secular_vec(z,a,b,R),lo,hi,xtol=1e-13,rtol=1e-13)**2)
    return np.sort(out)[:k]

def norm_closed(a,b,R,s):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    W=lambda t: np.sin(t)**2 + m*m*np.cos(t)**2
    X0=np.sin(A)/m; Y0=np.cos(A)
    nL=a/(2*s*s) - np.sin(2*A)/(4*m*s**3)
    nM=(1/s**3)*(W(A)*psi/(2*m*m) + (X0**2-Y0**2)*np.sin(2*psi)/4 + X0*Y0*np.sin(psi)**2)
    C2=W(A)/W(B)
    nR=C2*((1-b)/(2*s*s) - np.sin(2*B)/(4*m*s**3))
    return nL+nM+nR

def N1_of(a,b,R):
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    return n2/n1 - np.sin(tau*A)**2/np.sin(A)**2

R=4.0
bad=0; tot=0
for a in np.linspace(0.001,0.98,40):
    for b in np.linspace(a+0.002,0.998,40):
        N=N1_of(a,b,R)
        # symmetric line within tolerance
        if abs(a+b-1)<0.01: continue
        tot+=1
        if not (N < 0):
            bad+=1
            if bad<=6: print(f"  N1>=0 at (a,b)=({a:.3f},{b:.3f}) N1={N:+.4f}")
print(f"R=4 grid: {bad} violations of N1<0 out of {tot} points (excluding symmetric band)")
