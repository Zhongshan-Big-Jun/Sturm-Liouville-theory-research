# -*- coding: utf-8 -*-
"""#13(i): try to guess a closed form / lower-order recurrence for the minimal solution mu*_j."""
import mpmath as mp
mp.mp.dps = 150

def minimal_mu(cval, N=800, M=40):
    c_ = mp.mpf(cval)
    def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
    def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
    def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    s = mu[0]; mu = [m/s for m in mu]
    return mu[:M]

for cv in (1, 3):
    mu = minimal_mu(cv)
    print(f"===== c={cv}: mu*_0..mu*_8 =====")
    for j in range(9):
        print(f"  mu*_{j} = {mp.nstr(mu[j], 25)}")
    # try ratios mu_{j+1}/mu_j and j^2 * ratio etc.
    print("  ratios mu_{j+1}/mu_j:")
    for j in range(2, 9):
        print(f"    j={j}: {mp.nstr(mu[j+1]/mu[j], 12)}   j^2*ratio={mp.nstr(j*j*mu[j+1]/mu[j], 8)}")
