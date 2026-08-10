# -*- coding: utf-8 -*-
"""#13(i): accurate K(c) on fine grid."""
import mpmath as mp
mp.mp.dps = 200

def K_fit(cval, N=12000, jlo=5000, jhi=11000):
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

cs = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100]
res = {}
for cv in cs:
    K = K_fit(cv)
    res[cv] = K
    print(f"K({cv}) = {mp.nstr(K, 16)}")
mp.save(res, 'misc/op13_K_table.pkl')
print("saved")
