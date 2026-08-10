# -*- coding: utf-8 -*-
"""#13(i): definitive K(1) via backward iteration N=30000."""
import mpmath as mp
mp.mp.dps = 500
c_ = mp.mpf(1)
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

N = 30000
mu = [mp.mpf(0)]*(N+4)
mu[N+1] = mp.mpf(1)
for j in range(N+1, 2, -1):
    mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
s = mu[0]; mu = [m/s for m in mu]

js = list(range(15000, 29000, 1000))
print("j        mu_j*j^3")
for j in js:
    print(f"{j}: {mp.nstr(mu[j]*j**3, 25)}")
# fit log(mu_j j^3) = b0 + b1/j + ... + b5/j^5
import mpmath
J = list(range(15000, 29000))
A = mp.matrix(len(J), 6); y = mp.matrix(len(J), 1)
for i, j in enumerate(J):
    for k in range(6):
        A[i,k] = mp.mpf(1)/j**k
    y[i] = mp.log(mu[j]*j**3)
b = mp.lu_solve(A.T*A, A.T*y)
K = mp.e**b[0]
print("K(1) fitted =", mp.nstr(K, 30))
print("e/4         =", mp.nstr(mp.e/4, 30))
print("K - e/4     =", mp.nstr(K - mp.e/4, 10))
print("coeffs:", [mp.nstr(x, 6) for x in b])
