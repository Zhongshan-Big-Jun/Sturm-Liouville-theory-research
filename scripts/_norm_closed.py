import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec, norm2_well, y_well

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

# verify closed form vs trapezoid
for (a,b,R) in [(0.38258,0.61742,4.0),(0.10,0.70,4.0),(0.3,0.6,1.5),(0.05,0.9,10.0)]:
    lam=eigs_fast(a,b,R)
    s1=np.sqrt(lam[0]); s2=np.sqrt(lam[1])
    nc1=norm_closed(a,b,R,s1); nc2=norm_closed(a,b,R,s2)
    nt1=norm2_well(a,b,R,s1,n=4000); nt2=norm2_well(a,b,R,s2,n=4000)
    print(f"(a,b,R)=({a},{b},{R}): closed n1,n2={nc1:.6f},{nc2:.6f} trapz={nt1:.6f},{nt2:.6f} rel={abs(nc1-nt1)/nt1:.2e},{abs(nc2-nt2)/nt2:.2e}")
