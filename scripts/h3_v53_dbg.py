# -*- coding: utf-8 -*-
"""Debug v53: compare cleared expression CL(j) vs direct R(j) at j=5, c=3."""
from fractions import Fraction as F

c=F(3); j=5
def Pmul(a,b):
    r=[F(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            r[i+j]+=ai*bj
    return r
def Padd(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0))
    return r
def Psub(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))-(b[i] if i<len(b) else F(0))
    return r
def Pscal(a,s):
    return [s*x for x in a]
def pv(p,n): return sum(p[k]*F(n)**k for k in range(len(p)))

lam=F(4)/c
# direct alpha coefficients
P_e = F(8)*c*j*j - F(4)*c*j + c*c*F(j,j-1)
Q_e = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
R_e = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
a1 = P_e/(c*c*j*j*lam)
a2 = -Q_e/(c*c*j*j*(j-1)*(j-1)*lam*lam)
a3 = R_e/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
sjm1 = F(1)/(F(2)*(j-1)); sjm2=F(1)/(F(2)*(j-2)); sj=F(1)/(F(2)*j)
R = a1 + a2/(F(1)+sjm1) + a3/((F(1)+sjm1)*(F(1)+sjm2)) - (F(1)+sj)
print("R(j=5,c=3) direct =", R)

# cleared expression (multiply R by c^2 j^2 lam)
CL = R*c*c*j*j*lam
print("CL = R*c^2 j^2 lam =", CL)
# term by term of CL:
t1 = P_e
t2 = -Q_e*F(2)*lam/((j-1)*(2*j-1))
t3 = R_e*F(4)/(lam*lam*(j-1)*(j-2)*(2*j-1)*(2*j-3))
t4 = -c*c*j*lam*(2*j+1)/F(2)
print("  t1=",t1," t2=",t2," t3=",t3," t4=",t4," sum=",t1+t2+t3+t4)
