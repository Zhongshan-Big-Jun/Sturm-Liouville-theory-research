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
sp=np.linspace(1e-6, 2+2*np.pi*m+4, 3000)
d=Fsec(sp,a,b,R)
sg=np.signbit(d[1:])!=np.signbit(d[:-1])
idx=np.nonzero(sg)[0]
print("sign changes at sp indices:", idx[:6], "values:", d[idx][:6])
roots=[]
for i in idx[:4]:
    lo,hi=sp[i],sp[i+1]
    r=brentq(lambda z:Fsec(z,a,b,R),lo,hi,xtol=1e-14)
    roots.append(r)
    print(f"root s={r:.10f}  F(s)={Fsec(r,a,b,R):+.3e}")
s1,s2=roots[0],roots[1]
print("lambda1,lambda2 =", s1*s1, s2*s2, " tau=", s2/s1)
A=m*s1*a; B=m*s1*(1-b); psi=s1*(b-a)
print("A,B,psi =",A,B,psi)
