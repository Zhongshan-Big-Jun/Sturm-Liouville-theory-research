import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec, norm2_well, y_well, fval

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

for (a,b) in [(1e-5,0.84651),(1e-3,0.8466),(0.01,0.8470),(0.1,0.8703)]:
    R=4.0
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=2.0; A=m*s1*a; B=m*s1*(1-b)
    n1c=norm_closed(a,b,R,s1); n2c=norm_closed(a,b,R,s2)
    n1t=norm2_well(a,b,R,s1,n=8000); n2t=norm2_well(a,b,R,s2,n=8000)
    N1c=n2c/n1c - np.sin(tau*A)**2/np.sin(A)**2
    N1t=n2t/n1t - np.sin(tau*A)**2/np.sin(A)**2
    fv=fval(a,b,R,a)
    print(f"a={a:.5f} b={b:.5f}: N1_closed={N1c:+.6f} N1_trapz={N1t:+.6f} fval(a)={fv:+.3e}")
    print(f"   n1c={n1c:.8f} n1t={n1t:.8f} n2c={n2c:.8f} n2t={n2t:.8f} sin2(tauA)/sin2A={np.sin(tau*A)**2/np.sin(A)**2:.6f}")
