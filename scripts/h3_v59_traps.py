# -*- coding: utf-8 -*-
"""H3 v59: precise ratio-trap verification for u, v, w (both parities, c in 1,3,10).
rho_j = r_j * c/(4 j^2) where r_j = nu_j/nu_{j-1} (nu in moment scale).
Also u/v monotone, positivity, and v ratio."""
import math

def coeffs_f(c, j, par):
    lam = 4.0/c
    if par=='e':
        Pm=8.0*c*j*j-4.0*c*j+c*c*j/(j-1)
        Qm=4.0*j*(j-1)*(2*j-1)*(2*j-3)+4.0*c*j*(2*j-3)
        Rm=4.0*j*(j-2)*(2*j-3)*(2*j-5)
        Tm=4.0*j*(4*j-5)
    else:
        Pm=8.0*c*j*j+4.0*c*j+c*c*j/(j-1)
        Qm=4.0*j*(j-1)*(2*j-1)*(2*j+1)+4.0*c*j*(2*j-1)
        Rm=4.0*j*(j-2)*(2*j-1)*(2*j-3)
        Tm=4.0*j*(4*j-3)
    a1=Pm/(c*c*j*j*lam)
    a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else 0.0
    return a1,a2,a3,lam,Tm

def solve_z_f(c,par,N,z1,D):
    z=[0.0]*(N+1); z[1]=z1
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
        if D==0.0:
            src=0.0
        else:
            logsrc=math.log(abs(Tm*D))-2*math.lgamma(j+1)-j*math.log(lam)-2*math.log(c)
            src=math.copysign(math.exp(logsrc),Tm*D) if logsrc>-740 else 0.0
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else 0.0)+src
    return z

def nu_of_z(z, c, N):
    lam=4.0/c
    return [z[j]*math.factorial(j)**2*lam**j for j in range(N+1)]

N=60000; j0=20
for par in ('e','o'):
    for c in (1.0,3.0,10.0):
        u=solve_z_f(c,par,N,1.0,0.0)
        v=solve_z_f(c,par,N,0.0,1.0)
        w=[u[j]-2.0*v[j] for j in range(N+1)]
        nu_u=nu_of_z(u,c,N); nu_v=nu_of_z(v,c,N); nu_w=nu_of_z(w,c,N)
        # rho traps over [j0, N]
        def rho_stats(nu):
            lo=min(nu[j]*c/(4.0*j*j*nu[j-1]) for j in range(j0,N+1))
            hi=max(nu[j]*c/(4.0*j*j*nu[j-1]) for j in range(j0,N+1))
            return lo,hi
        ru=rho_stats(nu_u); rv=rho_stats(nu_v); rw=rho_stats(nu_w)
        # u/v monotone decreasing?
        mono=True
        prev=nu_u[j0]/nu_v[j0]
        for j in range(j0+1,N+1):
            cur=nu_u[j]/nu_v[j]
            if cur>=prev: mono=False; break
            prev=cur
        # positivity
        up=all(x>0 for x in nu_u[j0:N]); vp=all(x>0 for x in nu_v[j0:N]); wp=all(x>0 for x in nu_w[j0:N])
        print("par=%s c=%-4g: rho_u in [%.6f,%.6f]  rho_v in [%.6f,%.6f]  rho_w in [%.6f,%.6f]  u/v mono dec:%s  u>0:%s v>0:%s w>0:%s  u/v(N)=%.6f"
              %(par,c,ru[0],ru[1],rv[0],rv[1],rw[0],rw[1],mono,up,vp,wp,nu_u[N]/nu_v[N]))
