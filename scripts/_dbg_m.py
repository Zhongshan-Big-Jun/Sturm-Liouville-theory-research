import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec
def Fsec(s,a,b,R):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    return (np.cos(psi)*np.sin(A)+m*np.sin(psi)*np.cos(A))*np.cos(B) \
         + (-np.sin(psi)*np.sin(A)/m+np.cos(psi)*np.cos(A))*np.sin(B)
a,b,R=0.3826,0.6174,4.0
m=2.0
def roots_upto(a,b,R,nmax=4):
    sp=np.linspace(1e-6, 2+nmax*np.pi*m+4, 4000)
    d=Fsec(sp,a,b,R)
    sg=np.signbit(d[1:])!=np.signbit(d[:-1])
    idx=np.nonzero(sg)[0]
    out=[]
    for i in idx[:nmax]:
        out.append(brentq(lambda z:Fsec(z,a,b,R),sp[i],sp[i+1],xtol=1e-14))
    return out
rr=roots_upto(a,b,R)
s1,s2=rr[0],rr[1]
tau=s2/s1
A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
print("s1,s2,tau:",s1,s2,tau)
print("A,B,psi:",A,B,psi," tauA,tauB,taupsi:",tau*A,tau*B,tau*psi)
alA=np.arctan2(np.cos(A),np.sin(A)/m)
alA2=np.arctan2(np.cos(tau*A),np.sin(tau*A)/m)
print("alpha(A)=",alA," alpha(tauA)=",alA2)
print("psi+alpha(A)=",psi+alA)
print("cot(psi+alpha(A))=",1/np.tan(psi+alA)," -m cotB=",-m/np.tan(B))
uB=np.arctan2(1.0,-m/np.tan(B))
print("u(B)=",uB," cot u(B)=",1/np.tan(uB))
print("tau psi + alpha(tauA)=",tau*psi+alA2, " +pi+u(tauB)?")
uB2=np.arctan2(1.0,-m/np.tan(tau*B))
print("pi+u(tauB)=",np.pi+uB2," cot=",1/np.tan(np.pi+uB2)," -m cot(tauB)=",-m/np.tan(tau*B))
print("M'' = alpha(tauA)-tau alpha(A) - (u(tauB)-tau u(B)) - pi =", alA2-tau*alA-(uB2-tau*uB)-np.pi)
