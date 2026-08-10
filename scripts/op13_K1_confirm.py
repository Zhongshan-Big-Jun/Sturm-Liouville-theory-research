# -*- coding: utf-8 -*-
"""#13(i): confirm K(1) = e/4 to high precision."""
import mpmath as mp
mp.mp.dps = 400
c_ = mp.mpf(1)
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

N = 6000
mu = [mp.mpf(0)]*(N+4)
mu[N+1] = mp.mpf(1)
for j in range(N+1, 2, -1):
    mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
s = mu[0]; mu = [m/s for m in mu]

print("j        mu_j * j^3")
for j in (1000, 2000, 3000, 4000, 5000, 5800):
    print(f"{j}: {mp.nstr(mu[j]*j**3, 30)}")
print("e/4 =", mp.nstr(mp.e/4, 30))
# Richardson extrapolation on mu_j j^3 with 1/j, 1/j^2 corrections using j=3000..5800
js = [3000, 4000, 5000, 5800]
vals = [mu[j]*j**3 for j in js]
# fit log form? use direct polynomial in 1/j
import mpmath
n = len(js)
A = mp.matrix(n, 3); yv = mp.matrix(n, 1)
for i, j in enumerate(js):
    A[i,0]=1; A[i,1]=mp.mpf(1)/j; A[i,2]=mp.mpf(1)/j**2
    yv[i] = vals[i]
b = mp.lu_solve(A.T*A, A.T*yv)
print("extrapolated K =", mp.nstr(b[0], 30))
print("K - e/4 =", mp.nstr(b[0] - mp.e/4, 8))
