# -*- coding: utf-8 -*-
"""H3 v63: high-precision (60-digit Decimal) computation of r_j = u/v for many c.
Check whether L(c)=lim r_j == 2 exactly."""
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60

def solve_ratio(c, par, N):
    """Compute r_j = u_j/v_j in z-scale directly with Decimal."""
    cd = D(c)
    lam = D(4)/cd
    u=[D(0)]*(N+1); v=[D(0)]*(N+1)
    u[1]=D(1)
    # source for v: compute in float for j<=30 (super-exponentially small beyond)
    src=[D(0)]*(N+1)
    for j in range(2,min(31,N+1)):
        Tm=4.0*j*(4*j-5) if par=='e' else 4.0*j*(4*j-3)
        logsrc=math.log(abs(Tm))-2*math.lgamma(j+1)-j*math.log(4.0/c)-2*math.log(c)
        src[j]=D(0) if logsrc<-740 else D(str(math.copysign(math.exp(logsrc),Tm)))
    for j in range(2,N+1):
        if par=='e':
            Pm=D(8)*cd*D(j*j)-D(4)*cd*D(j)+cd*cd*D(j)/D(j-1)
            Qm=D(4)*D(j)*D(j-1)*D(2*j-1)*D(2*j-3)+D(4)*cd*D(j)*D(2*j-3)
            Rm=D(4)*D(j)*D(j-2)*D(2*j-3)*D(2*j-5)
        else:
            Pm=D(8)*cd*D(j*j)+D(4)*cd*D(j)+cd*cd*D(j)/D(j-1)
            Qm=D(4)*D(j)*D(j-1)*D(2*j-1)*D(2*j+1)+D(4)*cd*D(j)*D(2*j-1)
            Rm=D(4)*D(j)*D(j-2)*D(2*j-1)*D(2*j-3)
        a1=Pm/(cd*cd*D(j*j)*lam)
        a2=-Qm/(cd*cd*D(j*j)*D(j-1)*D(j-1)*lam*lam)
        a3=(Rm/(cd*cd*D(j*j)*D(j-1)*D(j-1)*D(j-2)*D(j-2)*lam**3)) if j>=3 else D(0)
        u[j]=a1*u[j-1]+a2*u[j-2]+(a3*u[j-3] if j>=3 else D(0))
        v[j]=a1*v[j-1]+a2*v[j-2]+(a3*v[j-3] if j>=3 else D(0))+src[j]
    r=[D(0)]*(N+1)
    for j in range(2,N+1): r[j]=u[j]/v[j]
    return r

N=120000
for par in ('e','o'):
    for c in (0.3,0.5,1.0,2.0,3.0,5.0,10.0,20.0):
        r=solve_ratio(c,par,N)
        # extrapolate L = r_j - 2 ~ 2/j:  L = r_N + 2*(r_N - r_{N/2})/(N/2-N)*N... use Richardson
        j1=N//3; j2=N
        # r_j = L + a/j: L = (r2*j2 - r1*j1)/(j2 - j1)
        L=(r[j2]*D(j2)-r[j1]*D(j1))/D(j2-j1)
        print("par=%s c=%-5g: r[%d]=%s  L_extrap=%s  L-2=%s"
              %(par,c,N,str(r[N])[:20],str(L)[:24],str(L-2)[:18]))
