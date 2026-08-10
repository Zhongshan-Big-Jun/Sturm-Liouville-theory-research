# -*- coding: utf-8 -*-
"""H3 v66: comprehensive checks for the ratio-trap route (z-scale).
Fixed points: even e_j = 1+1/(2j), odd e_j = 1+3/(2j).
Check: d_j = rho_j - e_j sign/size, contraction, self-consistent trap,
v positivity, h* minimal solution decay."""
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

def efix(j, par):
    return 1.0 + (1.0 if par=='e' else 3.0)/(2.0*j)

def solve_z(c, par, N, z1, D):
    z=[0.0]*(N+1); z[1]=z1
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs_f(c,j,par)
        src=0.0
        if D!=0.0:
            logsrc=math.log(abs(Tm*D))-2*math.lgamma(j+1)-j*math.log(4.0/c)-2*math.log(c)
            src=math.copysign(math.exp(logsrc),Tm*D) if logsrc>-740 else 0.0
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else 0.0)+src
    return z

print("=== A. ratio deviations d_j = rho_j - e_j (u, homogeneous z1=1) ===")
for par in ('e','o'):
    for c in (1.0,3.0,10.0,100.0):
        N=40000
        u=solve_z(c,par,N,1.0,0.0)
        neg=0; jneg=None; dmin=1e99; dmax=-1e99
        prev=None; mono_ok=True
        # start from j=3 (rho_2 not defined vs e_2 for u? rho_2 = a1(2); compare too)
        rho2=coeffs_f(c,2,par)[0]
        d2=rho2-efix(2,par)
        for j in range(3,N+1):
            rho=u[j]/u[j-1]
            d=rho-efix(j,par)
            if d<dmin: dmin=d
            if d>dmax: dmax=d
            if d<0:
                neg+=1
                if jneg is None: jneg=j
            if prev is not None and d>prev+1e-15: mono_ok=False
            prev=d
        print("  par=%s c=%-5g: d2=%.3e  d_min=%.3e at 40k  d_max=%.3e  neg_count=%d%s  monotone_dec:%s"
              %(par,c,d2,dmin,dmax,neg,"(first at j=%d)"%jneg if jneg else "",mono_ok))

print()
print("=== B. v solutions: positivity and ratio traps ===")
for par in ('e','o'):
    for c in (1.0,3.0,10.0,100.0):
        N=40000
        v=solve_z(c,par,N,0.0,1.0)
        neg=sum(1 for x in v[2:N+1] if x<=0)
        rmin=1e99; rmax=-1e99; rneg=0
        for j in range(3,N+1):
            r=v[j]/v[j-1]
            if r<rmin: rmin=r
            if r>rmax: rmax=r
            if r<efix(j,par): rneg+=1
        print("  par=%s c=%-5g: v<=0 count=%d  ratio range [%.6f,%.6f]  ratio<e_j count=%d"
              %(par,c,neg,rmin,rmax,rneg))
EOF
