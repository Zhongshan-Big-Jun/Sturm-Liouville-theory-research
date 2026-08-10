# -*- coding: utf-8 -*-
"""Check: does the backward-iteration minimal solution satisfy the z-recurrence and the ratio identity?"""
import mpmath as mp
mp.mp.dps = 120
cval = 1
c_ = mp.mpf(cval)
lam = mp.mpf(4)/c_
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

N = 600
mu = [mp.mpf(0)]*(N+4)
mu[N+1] = mp.mpf(1)
for j in range(N+1, 2, -1):
    mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
s = mu[0]; mu = [m/s for m in mu]
# z-scale
z = [mu[j]*(c_/4)**j/mp.factorial(j)**2 for j in range(N+1)]
# a-coefficients in z-scale
def af(j):
    a1 = P(j)/(c_*c_*j*j*lam)
    a2 = -Q(j)/(c_*c_*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R(j)/(c_*c_*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

print("j    z_j/z_{j-1}     z-recurrence resid   ratio-identity resid")
for j in (100, 200, 300, 400, 500):
    a1,a2,a3 = af(j)
    rec = z[j] - (a1*z[j-1] + a2*z[j-2] + a3*z[j-3])
    rho_j = z[j]/z[j-1]; rho_1 = z[j-1]/z[j-2]; rho_2 = z[j-2]/z[j-3]
    rid = rho_j - (a1 + a2/rho_1 + a3/(rho_1*rho_2))
    print(f"{j}  {mp.nstr(rho_j,6)}   {mp.nstr(abs(rec),3)}   {mp.nstr(abs(rid),3)}")
