# -*- coding: utf-8 -*-
"""#13(i): compute minimal-solution asymptotic constant K(c).
z-scale minimal: z*_j ~ K(c/4)^j j^{-3}/(j!)^2, normalized z*_0 = 1.
mu-scale: mu_j = z*_j (j!)^2 (4/c)^j ~ K j^{-3}."""
import mpmath as mp
mp.mp.dps = 250

def K_estimate(cval, N=1200, jstart=400, jend=1000):
    c_ = mp.mpf(cval)
    def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
    def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
    def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    # normalize mu_0 = 1
    s = mu[0]
    mu = [m/s for m in mu]
    # K estimate: K_j = mu_j * j^3  (mu_j ~ K j^{-3})
    Ks = [mu[j]*j**3 for j in range(jstart, jend)]
    # Richardson-style extrapolation: K_j = K + A/j + B/j^2
    # use last three values to extrapolate
    K1, K2, K3 = Ks[-1], Ks[-2], Ks[-3]
    # solve K + A/j + B/j^2 for j = n-2, n-1, n
    n = jend-1
    Knum = (mp.mpf(1),)
    # linear system
    import mpmath
    M = mp.matrix([[mp.mpf(1), mp.mpf(1)/n, mp.mpf(1)/n**2],
                   [mp.mpf(1), mp.mpf(1)/(n-1), mp.mpf(1)/(n-1)**2],
                   [mp.mpf(1), mp.mpf(1)/(n-2), mp.mpf(1)/(n-2)**2]])
    bvec = mp.matrix([mu[n]*n**3, mu[n-1]*(n-1)**3, mu[n-2]*(n-2)**3])
    sol = mp.lu_solve(M, bvec)
    return sol[0], mu

print("c      K(c) (extrapolated)      K_j at j=500,1000 (ratio check)")
for cval in (1, 2, 3, 4, 5, 10, 100):
    K, mu = K_estimate(cval, N=1400, jstart=600, jend=1200)
    # consistency: mu_j*j^3 at j=600,1200
    print(f"{cval:>4}  {mp.nstr(K, 18)}   {mp.nstr(mu[600]*600**3,8)} / {mp.nstr(mu[1200]*1200**3,8)}")
