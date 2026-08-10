# -*- coding: utf-8 -*-
"""H3 v64: exact small-j structure of r_j = u_j/v_j and w_j = u_j - 2 v_j (c=3, even)."""
from fractions import Fraction as F
import math
c=F(3); par='e'; N=30; lam=F(4)/c
z=[F(0)]*(N+1); z[1]=F(1)
v=[F(0)]*(N+1)
for j in range(2,N+1):
    Pm=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1); Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5); Tm=F(4)*j*(4*j-5)
    a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
    src=Tm/(c*c*F(math.factorial(j))**2*lam**j)
    z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else F(0))
    v[j]=a1*v[j-1]+a2*v[j-2]+(a3*v[j-3] if j>=3 else F(0))+src
w=[z[j]-2*v[j] for j in range(N+1)]
print("j :  u_j            v_j            w_j            r_j-2")
for j in range(2,14):
    print("%2d: %14s %14s %14s  %s"%(j,str(z[j]),str(v[j]),str(w[j]),str(z[j]/v[j]-2)))
print()
print("w_j values (exact):")
for j in range(1,10): print("  w[%d]=%s"%(j,w[j]))
