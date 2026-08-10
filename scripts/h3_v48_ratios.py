# -*- coding: utf-8 -*-
"""H3 v48: precise ratio structure of the u-mode (nu-scale, y-scale, z-scale),
Decimal 60 digits.  c=3."""
from decimal import Decimal as D, getcontext
getcontext().prec = 60
import math

C = D(3)
def solve_even_dec(nu1, Dval, N):
    c=C; nu=[D(0)]*(N+1); nu[1]=D(nu1)
    for j in range(2,N+1):
        jd=D(j)
        Pe = D(8)*c*jd*jd - D(4)*c*jd + c*c*jd/(jd-D(1))
        Qe = D(4)*jd*(jd-D(1))*(D(2)*jd-D(1))*(D(2)*jd-D(3)) + D(4)*c*jd*(D(2)*jd-D(3))
        Re = D(4)*jd*(jd-D(2))*(D(2)*jd-D(3))*(D(2)*jd-D(5))
        Te = D(4)*jd*(D(4)*jd-D(5))
        rhs = Pe*nu[j-1] - Qe*nu[j-2] + (Re*nu[j-3] if j>=3 else D(0)) + Te*Dval
        nu[j] = rhs/(c*c)
    return nu

N=60000
u = solve_even_dec(1,0,N)
lam = D(4)/C
# z-scale: z_j = nu_j/(j!)^2 / lam^j ; use logs to avoid overflow
import math as m
lfac=[m.lgamma(j+1)/m.log(10.0) for j in range(N+1)]
def log10_abs(x):
    if x==0: return None
    return m.log10(abs(x))
def log10z(j):
    return log10_abs(u[j]) - 2*lfac[j] - j*m.log10(float(lam))
# ratios
print("=== nu-scale ratio r_j = nu_j/nu_{j-1} : compare to (4/c)j^2(1+1/(2j)) ===")
for j in (100,1000,10000,60000):
    r = u[j]/u[j-1]
    target = (D(4)/C)*D(j)*D(j)*(D(1)+D(1)/(D(2)*D(j)))
    print("  j=%6d: r_j/((4/c)j^2) = %s" % (j, (r/((D(4)/C)*D(j)*D(j)))))
    print("         (r_j/target - 1) = %s" % ((r/target - D(1))))
print()
print("=== z-scale ratio: z_j/z_{j-1} vs 1+1/(2j) ===")
for j in (100,1000,10000,60000):
    zr = u[j]/u[j-1]/(D(j)*D(j)*lam)
    print("  j=%6d: z_j/z_{j-1} = %s ; 1+1/(2j)=%s ; diff=%s" % (j, zr, D(1)+D(1)/(D(2)*D(j)), zr-(D(1)+D(1)/(D(2)*D(j)))))
print()
print("=== check u_j/u_{j-1} >= 1+1/(2j) in which scale? min over j of each ===")
min_nu=None; min_z=None
for j in range(3,N):
    rn = u[j]/u[j-1]
    if min_nu is None or rn < min_nu: min_nu=rn
    rz = rn/(D(j)*D(j)*lam)
    if min_z is None or rz < min_z: min_z=rz
print("  min nu-ratio:", min_nu)
print("  min z-ratio:", min_z)
print()
print("=== t_j := (u_j-u_{j-1})/u_j in z-scale: t_j*j ===")
for j in (10,100,1000,10000,60000):
    zr = u[j]/u[j-1]/(D(j)*D(j)*lam)
    t = D(1) - D(1)/zr
    print("  j=%6d: t_j*j = %s" % (j, t*D(j)))
