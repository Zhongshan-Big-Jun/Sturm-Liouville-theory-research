# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 200
cval = 1
c_ = mp.mpf(cval)
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

def backward(N):
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    return mu

for N in (50, 100, 200, 400):
    mu = backward(N)
    # mu-scale ratio at j=40 (well below N)
    r40 = mu[40]/mu[39]
    z40 = mu[40]*(c_/4)**40/mp.factorial(40)**2
    z39 = mu[39]*(c_/4)**39/mp.factorial(39)**2
    print(f"N={N}: mu[1]={mp.nstr(mu[1],6)} mu[2]={mp.nstr(mu[2],6)} mu_40/mu_39={mp.nstr(r40,8)} z_40/z_39={mp.nstr(z40/z39,8)}")
    if N==200:
        # check forward recurrence at j=40
        lhs = c_*c_*mu[40]; rhs = P(40)*mu[39]-Q(40)*mu[38]+R(40)*mu[37]
        print("   forward res at j=40:", mp.nstr(abs(lhs-rhs),5))
        print("   h*_j ~ K(c/4)^j j^-3/(j!)^2 prediction: mu_40/mu_39 ~ (c/4)*(j/(j+1))^3*1/40^2 =", mp.nstr((c_/4)*(40/41)**3/mp.mpf(40)**2, 8))
