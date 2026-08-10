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

def data(a,b,R):
    lam1,lam2=eigs_fast(a,b,R)
    s1=np.sqrt(lam1); s2=np.sqrt(lam2); tau=s2/s1
    m=np.sqrt(R)
    A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
    n1=norm_closed(a,b,R,s1); n2=norm_closed(a,b,R,s2)
    J=lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    E=np.log(J(tau*A)/J(A))-np.log(J(tau*B)/J(B))
    N1=n2/n1 - np.sin(tau*A)**2/np.sin(A)**2
    # sign-consistency: y2(a)/y1(a) = sin(tau A)/(tau sin A) >0 always; y2(b)/y1(b)= (C2/C1) sin(tau B)/(tau sin B)
    Xb1 = np.cos(psi)*np.sin(A)/m + np.sin(psi)*np.cos(A)
    Xb2 = np.cos(tau*psi)*np.sin(tau*A)/m + np.sin(tau*psi)*np.cos(tau*A)
    C1 = Xb1/np.sin(B)   # C1 = m X_b1 / sin B times m... sign only
    C2v = Xb2/np.sin(tau*B)
    y2b_y1b = (C2v/C1)*np.sin(tau*B)/(tau*np.sin(B))
    y2a_y1a = np.sin(tau*A)/(tau*np.sin(A))
    return dict(tau=tau,A=A,B=B,psi=psi,E=E,N1=N1,y2b_y1b=y2b_y1b,y2a_y1a=y2a_y1a)

R=4.0
print("R=4 branch trace: a, b, a+b, A, B, tau, N1, sign(y2b/y1b), sign(y2a/y1a)")
prev=None
for a in np.linspace(1e-5, 0.45, 120):
    bs=np.linspace(a+0.005, 0.999, 900)
    Es=np.array([data(a,bb,R)['E'] for bb in bs])
    for i in range(len(bs)-1):
        if Es[i]*Es[i+1]<0:
            b0=brentq(lambda bb: data(a,bb,R)['E'], bs[i], bs[i+1], xtol=1e-12)
            d=data(a,b0,R)
            if abs(a+b0-1)>1e-3:
                print(f"  a={a:.5f} b={b0:.5f} a+b={a+b0:.5f} A={d['A']:.4f} B={d['B']:.4f} tau={d['tau']:.4f} N1={d['N1']:+.4f} sg2b={np.sign(d['y2b_y1b']):+.0f} sg2a={np.sign(d['y2a_y1a']):+.0f}")
