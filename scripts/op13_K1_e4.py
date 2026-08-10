# -*- coding: utf-8 -*-
"""#13(i): check K(1) vs e/4 carefully; test for log j/j^3 corrections."""
import mpmath as mp
mp.mp.dps = 300
c_ = mp.mpf(1)
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

N = 4000
mu = [mp.mpf(0)]*(N+4)
mu[N+1] = mp.mpf(1)
for j in range(N+1, 2, -1):
    mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
s = mu[0]; mu = [m/s for m in mu]

# fit log(mu_j j^3) with basis {1, 1/j, 1/j^2, 1/j^3, logj/j^3}
import mpmath
js = list(range(2000, 3900))
A = mp.matrix(len(js), 5); y = mp.matrix(len(js), 1)
for i, j in enumerate(js):
    A[i,0]=1; A[i,1]=mp.mpf(1)/j; A[i,2]=mp.mpf(1)/j**2; A[i,3]=mp.mpf(1)/j**3; A[i,4]=mp.log(j)/j**3
    y[i] = mp.log(mu[j]*j**3)
AtA = A.T*A; Atb = A.T*y
b = mp.lu_solve(AtA, Atb)
print("log K =", mp.nstr(b[0], 25))
print("K     =", mp.nstr(mp.e**b[0], 25))
print("e/4   =", mp.nstr(mp.e/4, 25))
print("log-term coeff =", mp.nstr(b[4], 12))
# also plain fit without log term
A2 = A[:, :4]
b2 = mp.lu_solve(A2.T*A2, A2.T*y)
print("without log: K =", mp.nstr(mp.e**b2[0], 25))
print("K - e/4 =", mp.nstr(mp.e**b2[0] - mp.e/4, 6))
