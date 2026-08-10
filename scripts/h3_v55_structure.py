# -*- coding: utf-8 -*-
"""H3 v55: (1) signs of h* z_j and sigma_j = r_j - r_{j-1};
(2) proportionality of s^u, s^v, s^w;
(3) exact small-j values of h* moments."""
from fractions import Fraction as F
import math

C=F(3)
lam=F(4)/C

def solve_even(cF, nu1, D, N):
    c=cF; nu=[F(0)]*(N+1); nu[1]=F(nu1)
    for j in range(2,N+1):
        Pe=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
        Qe=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
        Re=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Te=F(4)*j*(4*j-5)
        rhs=Pe*nu[j-1]-Qe*nu[j-2]+(Re*nu[j-3] if j>=3 else F(0))+Te*D
        nu[j]=rhs/(c*c)
    return nu

N=120
u=solve_even(C,F(1),F(0),N)
v=solve_even(C,F(0),F(1),N)
w=[u[j]-F(3,2)*v[j] for j in range(N+1)]

# z-scale
def zof(nu,N):
    return [nu[j]/F(math.factorial(j))**2/lam**j for j in range(N+1)]
zu=zof(u,N); zv=zof(v,N); zw=zof(w,N)
# z^E
zE=[F(1)]*(N+1)
for j in range(1,N+1):
    zE[j]=zE[j-1]*(F(1)+F(1)/(F(2)*j))
ru=[zu[j]/zE[j] for j in range(N+1)]
rv=[zv[j]/zE[j] for j in range(N+1)]
rw=[zw[j]/zE[j] for j in range(N+1)]
su=[ru[j]-ru[j-1] for j in range(1,N+1)]
sv=[rv[j]-rv[j-1] for j in range(1,N+1)]
sw=[rw[j]-rw[j-1] for j in range(1,N+1)]
# proportionality su vs sw vs sv (for j>=4)
print("s^u/s^w for j=5,10,20,50:", [float(su[j]/sw[j]) for j in (5,10,20,50)])
print("s^v/s^w for j=5,10,20,50:", [float(sv[j]/sw[j]) for j in (5,10,20,50)])

# h* via backward (use known z1/z0, z2/z0)
z1z0=F(6477471192126609,10**17)  # approx
z2z0=F(32734357146203905,10**19) # approx
print()
print("h* forward (z0=1), c=3:")
zh=[F(0)]*(N+1); zh[0]=F(1); zh[1]=z1z0; zh[2]=z2z0
for j in range(3,N+1):
    P=F(8)*C*j*j-F(4)*C*j+C*C*F(j,j-1)
    Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*C*j*(2*j-3)
    R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    zh[j]=(P/(C*C*j*j*lam))*zh[j-1]+(-Q/(C*C*j*j*(j-1)*(j-1)*lam*lam))*zh[j-2]+(R/(C*C*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3))*zh[j-3]
rh=[zh[j]/zE[j] for j in range(N+1)]
sh=[rh[j]-rh[j-1] for j in range(1,N+1)]
print("  signs of zh[0..40]:", [ (1 if x>0 else -1 if x<0 else 0) for x in zh[:41]])
print("  signs of sh[1..40]:", [ (1 if x>0 else -1 if x<0 else 0) for x in sh[1:41]])
print("  sum sh[1..120] =", sum(sh[1:]))
print("  (should be -z0(h*) = -1 if r->0)")
# moments nu_j(h*) = zh_j (j!)^2 lam^j
nu_h=[zh[j]*F(math.factorial(j))**2*lam**j for j in range(13)]
print("  nu_j(h*) for j=0..12:", [float(x) for x in nu_h])
