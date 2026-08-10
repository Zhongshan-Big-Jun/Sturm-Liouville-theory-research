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

R=4.0; a=1e-5; b=0.84651
lam1,lam2=eigs_fast(a,b,R)
s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1; m=2.0
A=m*s1*a
print("lam1,lam2,s1,s2,tau,A:",lam1,lam2,s1,s2,tau,A)
print("y2(a), y1(a):", y_well(a,b,R,s2,a), y_well(a,b,R,s1,a))
for nn in [1000, 4000, 8000]:
    n1=norm2_well(a,b,R,s1,n=nn); n2=norm2_well(a,b,R,s2,n=nn)
    fv=lam2*y_well(a,b,R,s2,a)**2/n2 - lam1*y_well(a,b,R,s1,a)**2/n1
    print(f"  n={nn}: n1={n1:.10f} n2={n2:.10f} fval={fv:+.3e} n2/n1={n2/n1:.6f} sin2tauA/sin2A={np.sin(tau*A)**2/np.sin(A)**2:.6f}")
# accurate: refine grid
n1=norm2_well(a,b,R,s1,n=40000); n2=norm2_well(a,b,R,s2,n=40000)
print("n=40000: n1=",n1,"n2=",n2," fval=",lam2*y_well(a,b,R,s2,a)**2/n2 - lam1*y_well(a,b,R,s1,a)**2/n1)
