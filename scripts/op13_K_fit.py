# -*- coding: utf-8 -*-
"""#13(i): accurate K(c) via LSQ fit of log(mu_j * j^3) = log K + A/j + B/j^2 + C/j^3."""
import mpmath as mp
mp.mp.dps = 300

def K_fit(cval, N=3000, jlo=1000, jhi=2800):
    c_ = mp.mpf(cval)
    def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
    def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
    def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    s = mu[0]; mu = [m/s for m in mu]
    # fit y_j = log(mu_j j^3) = b0 + b1/j + b2/j^2 + b3/j^3  (LSQ)
    js = list(range(jlo, jhi))
    import mpmath
    A = mp.matrix(len(js), 4)
    y = mp.matrix(len(js), 1)
    for i, j in enumerate(js):
        A[i,0] = 1; A[i,1] = mp.mpf(1)/j; A[i,2] = mp.mpf(1)/j**2; A[i,3] = mp.mpf(1)/j**3
        y[i] = mp.log(mu[j] * j**3)
    AtA = A.T*A; Atb = A.T*y
    b = mp.lu_solve(AtA, b=Atb)
    K = mp.e**b[0]
    # residual check
    r = [mp.log(mu[j]*j**3) - (b[0]+b[1]/j+b[2]/j**2+b[3]/j**3) for j in js[-200:]]
    maxr = max(abs(x) for x in r)
    return K, b, maxr

print("c       K(c)                    max-resid")
results = {}
for cval in (0.25, 0.5, 1, 2, 3, 4, 5, 10, 20, 100):
    K, b, r = K_fit(cval)
    results[cval] = K
    print(f"{cval:>6}  {mp.nstr(K, 20)}   {mp.nstr(r,3)}")

print()
print("=== functional-form exploration ===")
cvals = list(results.keys())
Kv = [results[c] for c in cvals]
# test K(c) ~ A/(c+1): compute K*(c+1)
for c in cvals:
    print(f"c={c}: K*(c+1)={mp.nstr(results[c]*(c+1),8)}  K*(c+1)^2={mp.nstr(results[c]*(c+1)**2,8)}  K*exp(c/4)={mp.nstr(results[c]*mp.e**(c/4),8)}")
