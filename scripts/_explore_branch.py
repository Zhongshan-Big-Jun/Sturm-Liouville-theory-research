import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec, y_well, norm2_well

def eigs_fast(a,b,R,k=2,N=500):
    m=np.sqrt(R)
    smax=2+k*np.pi*m+4
    sp_=np.linspace(1e-9,smax,N)
    d=well_secular_vec(sp_,a,b,R)
    sg=np.signbit(d[1:])!=np.signbit(d[:-1])
    idx=np.nonzero(sg)[0]
    out=[]
    for i in idx[:k]:
        lo,hi=sp_[i],sp_[i+1]
        out.append(brentq(lambda z: well_secular_vec(z,a,b,R),lo,hi,xtol=1e-12,rtol=1e-12)**2)
    return np.sort(out)[:k]

def data(a,b,R,n=1200):
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
    n1=norm2_well(a,b,R,s1,n); n2=norm2_well(a,b,R,s2,n)
    J=lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    E=np.log(J(tau*A)/J(A))-np.log(J(tau*B)/J(B))
    N1=n2/n1 - np.sin(tau*A)**2/np.sin(A)**2
    return dict(lam1=lam1,lam2=lam2,s1=s1,tau=tau,A=A,B=B,psi=psi,n1=n1,n2=n2,E=E,N1=N1)

def offaxis_branch(R, amax=0.35, na=80, nb=400):
    branch=[]
    for a in np.linspace(1e-4, amax, na):
        bs=np.linspace(a+0.05, 0.999, nb)
        Es=np.array([data(a,bb,R)['E'] for bb in bs])
        for i in range(len(bs)-1):
            if Es[i]*Es[i+1]<0:
                b0=brentq(lambda bb: data(a,bb,R)['E'], bs[i], bs[i+1], xtol=1e-11)
                d=data(a,b0,R)
                if abs(a+b0-1)>1e-3:
                    branch.append((a,b0,d))
    return branch

for R in [1.6,2.0,3.0,4.0,10.0,100.0]:
    br=offaxis_branch(R)
    if not br:
        print(f"R={R}: no off-axis branch in scan"); continue
    aa=[x[0] for x in br]; 
    Ns=[x[2]['N1'] for x in br]; As=[x[2]['A'] for x in br]; Bs=[x[2]['B'] for x in br]
    tau=[x[2]['tau'] for x in br]
    print(f"R={R}: npts={len(br)} a in [{min(aa):.4f},{max(aa):.4f}]")
    print(f"    A in [{min(As):.4f},{max(As):.4f}] B in [{min(Bs):.4f},{max(Bs):.4f}] pi/tau min={min(np.pi/t for t in tau):.4f}")
    print(f"    N1 in [{min(Ns):+.4f},{max(Ns):+.4f}]")
