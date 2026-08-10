import numpy as np
from scipy.optimize import brentq
from _well_rigid_verify import well_secular_vec
def Fsec(s,a,b,R):
    m=np.sqrt(R)
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    return (np.cos(psi)*np.sin(A)+m*np.sin(psi)*np.cos(A))*np.cos(B) \
         + (-np.sin(psi)*np.sin(A)/m+np.cos(psi)*np.cos(A))*np.sin(B)
a,b,R=0.382598,0.617402,4.0
m=2.0
sp=np.linspace(1e-6, 20, 6000)
d=Fsec(sp,a,b,R)
sg=np.signbit(d[1:])!=np.signbit(d[:-1])
idx=np.nonzero(sg)[0]
s1=brentq(lambda z:Fsec(z,a,b,R),sp[idx[0]],sp[idx[1]],xtol=1e-14)
s2=brentq(lambda z:Fsec(z,a,b,R),sp[idx[2]],sp[idx[3]],xtol=1e-14)
tau=s2/s1
print("s1,s2,tau:",s1,s2,tau)
A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
print("A,B,psi:",A,B,psi," tauA:",tau*A," tauB:",tau*B)
# solution on middle interval (slope normalized, mode 1)
def y1(x):
    if x<=a:
        return np.sin(m*s1*x)/(m*s1)
    y0=np.sin(m*s1*a)/(m*s1); yp0=np.cos(m*s1*a)
    return y0*np.cos(s1*(x-a)) + (yp0/s1)*np.sin(s1*(x-a))
def yp1(x):
    if x<=a:
        return np.cos(m*s1*x)
    y0=np.sin(m*s1*a)/(m*s1); yp0=np.cos(m*s1*a)
    return -y0*s1*np.sin(s1*(x-a)) + yp0*np.cos(s1*(x-a))
print("y(b)=",y1(b)," yp(b)=",yp1(b)," ratio yp/y =",yp1(b)/y1(b))
print("s*cot(psi+alpha)?  -ms cotB =", -m*s1/np.tan(B))
# alpha via direct: alpha = arctan2(sinA/m, cosA)
al=np.arctan2(np.sin(A)/m, np.cos(A))
print("alpha(A)=",al," psi+alpha=",psi+al," s*cot(psi+alpha)=",s1/np.tan(psi+al))
# middle solution formula check
W=np.sin(A)**2+m*m*np.cos(A)**2
print("sqrtW/(ms)*sin(psi+alpha)=", np.sqrt(W)/(m*s1)*np.sin(psi+al), " vs y(b)=", y1(b))
