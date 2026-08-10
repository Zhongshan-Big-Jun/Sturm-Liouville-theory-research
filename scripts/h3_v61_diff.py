# -*- coding: utf-8 -*-
"""H3 v61: measure d_j = rho^u_j - rho^v_j, r_j - 2, w/v at large j (both parities, c=3)."""
import math
def coeffs_f(c, j, par):
    lam = 4.0/c
    if par=='e':
        Pm=8.0*c*j*j-4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j-3)+4.0*c*j*(2*j-3)
        Rm=4.0*j*(j-2)*(2*j-3)*(2*j-5); Tm=4.0*j*(4*j-5)
    else:
        Pm=8.0*c*j*j+4.0*c*j+c*c*j/(j-1); Qm=4.0*j*(j-1)*(2*j-1)*(2*j+1)+4.0*c*j*(2*j-1)
        Rm=4.0*j*(j-2)*(2*j-1)*(2*j-3); Tm=4.0*j*(4*j-3)
    a1=Pm/(c*c*j*j*lam); a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else 0.0
    return a1,a2,a3,lam,Tm
def solve_z_f(c,par,N,z1,D):
    z=[0.0]*(N+1); z[1]=z1
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
        if D==0.0: src=0.0
        else:
            logsrc=math.log(abs(Tm*D))-2*math.lgamma(j+1)-j*math.log(lam)-2*math.log(c)
            src=math.copysign(math.exp(logsrc),Tm*D) if logsrc>-740 else 0.0
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else 0.0)+src
    return z
N=400000
for par in ('e','o'):
    c=3.0
    u=solve_z_f(c,par,N,1.0,0.0); v=solve_z_f(c,par,N,0.0,1.0)
    w=[u[j]-2.0*v[j] for j in range(N+1)]
    ru=[0.0,0.0]+[0.0]*(N-1)+[u[j]/u[j-1] for j in range(3,N+1)]
    rv=[0.0,0.0]+[0.0]*(N-1)+[v[j]/v[j-1] for j in range(3,N+1)]
    r=[0.0,0.0]+[0.0]*(N-1)+[u[j]/v[j] for j in range(2,N+1)]
    print("par=%s c=3:"%par)
    for jj in (100, 1000, 10000, 100000, 400000):
        print("   j=%7d: rho_u-rho_v=%.3e  1/j^2=%.2e  r_j-2=%.3e  w/v=%.3e"
              %(jj, ru[jj]-rv[jj], 1.0/jj**2, r[jj]-2.0, w[jj]/v[jj]))
