# -*- coding: utf-8 -*-
"""#13(i): small-c asymptotics of K(c)."""
import mpmath as mp
mp.mp.dps = 250

def K_fit(cval, N=20000, jlo=8000, jhi=19000):
    c_ = mp.mpf(cval)
    def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
    def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
    def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    s = mu[0]; mu = [m/s for m in mu]
    import mpmath
    J = list(range(jlo, jhi))
    A = mp.matrix(len(J), 5); y = mp.matrix(len(J), 1)
    for i, j in enumerate(J):
        for k in range(5):
            A[i,k] = mp.mpf(1)/j**k
        y[i] = mp.log(mu[j]*j**3)
    b = mp.lu_solve(A.T*A, A.T*y)
    return mp.e**b[0]

Kvals = {}
for cv in (0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1):
    Kvals[cv] = K_fit(cv)
    print(f"K({cv}) = {mp.nstr(Kvals[cv], 20)}")

# fit log K = log K0 + a*c + b*c^2 on c in {0.001..0.05}
cs = sorted(Kvals)
import mpmath
# use small cs up to 0.02 for clean quadratic fit
sel = [c for c in cs if c <= 0.02]
A = mp.matrix(len(sel), 3); y = mp.matrix(len(sel), 1)
for i, c in enumerate(sel):
    A[i,0]=1; A[i,1]=c; A[i,2]=c*c
    y[i] = mp.log(Kvals[c])
b = mp.lu_solve(A.T*A, A.T*y)
print("fit log K = logK0 + a c + b c^2  on c<=0.02:")
print("  K0 =", mp.nstr(mp.e**b[0], 20))
print("  a  =", mp.nstr(b[1], 20))
print("  b  =", mp.nstr(b[2], 12))
print("  3/4 =", mp.mpf(3)/4)
print("  a candidates: -0.1:", mp.nstr(b[1]+mp.mpf(1)/10, 6))
print("  predicted K(1) from fit: K0*exp(a+b) =", mp.nstr(mp.e**b[0]*mp.e**(b[1]+b[2]), 10))
print("  e/4 =", mp.nstr(mp.e/4, 10))
