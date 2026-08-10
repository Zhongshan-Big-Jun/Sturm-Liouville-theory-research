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

def Rvals(a,b,R):
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    J=lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    E=np.log(J(tau*A)/J(A))-np.log(J(tau*B)/J(B))
    N1=n2/n1 - np.sin(tau*A)**2/np.sin(A)**2   # sign = sign(R1)
    # R2: f(b) = (1/m^2)[C2^2 sin^2(tau B)/n2 - C1^2 sin^2 B/n1]
    W=lambda t: np.sin(t)**2+m*m*np.cos(t)**2
    C1sq=W(A)/W(B); C2sq=W(tau*A)/W(tau*B)
    R2=(C2sq*np.sin(tau*B)**2/n2 - C1sq*np.sin(B)**2/n1)/m**2
    return N1,R2,E,tau,A,B

R=4.0
# coarse grid contour sign data
ng=200
aa=np.linspace(0.002,0.498,ng); bb=np.linspace(a+0.004,0.998,ng) if False else np.linspace(0.006,0.998,ng)
N1g=np.zeros((ng,ng)); R2g=np.zeros((ng,ng)); Eg=np.zeros((ng,ng))
for i,a in enumerate(np.linspace(0.002,0.49,ng)):
    for j,b in enumerate(np.linspace(0.006,0.998,ng)):
        if b<=a+1e-4: continue
        N1g[i,j],R2g[i,j],Eg[i,j],_,_,_=Rvals(a,b,R)
# report sign changes along rows/cols -> zero curve segments (E3)
def segments(g, axis, lo, hi):
    out=[]
    if axis==0:
        for j in range(ng):
            col=g[:,j]
            for i in range(ng-1):
                if col[i]*col[i+1]<0: out.append((np.linspace(0.002,0.49,ng)[i]+np.linspace(0.002,0.49,ng)[i+1])/2, np.linspace(0.006,0.998,ng)[j])
    return out
# print structure summary: for R1=0 (N1=0), count crossing segments per column j
print("R=4: N1=0 crossings per b-column (b grid 0.006..0.998):")
cnt=[]
for j in range(ng):
    col=N1g[:,j]; nz=0
    for i in range(ng-1):
        if col[i]*col[i+1]<0: nz+=1
    cnt.append(nz)
print("  nonzero counts:", sorted(set(cnt)))
print("R=4: R2=0 crossings per a-row:")
cnt=[]
for i in range(ng):
    row=R2g[i,:]; nz=0
    for j in range(ng-1):
        if row[j]*row[j+1]<0: nz+=1
    cnt.append(nz)
print("  nonzero counts:", sorted(set(cnt)))
print("R=4: E=0 crossings per b-column:")
cnt=[]
for j in range(ng):
    col=Eg[:,j]; nz=0
    for i in range(ng-1):
        if col[i]*col[i+1]<0: nz+=1
    cnt.append(nz)
print("  nonzero counts:", sorted(set(cnt)))
