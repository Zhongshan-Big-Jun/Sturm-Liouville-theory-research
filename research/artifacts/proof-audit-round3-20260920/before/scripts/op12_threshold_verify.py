# -*- coding: utf-8 -*-
"""#12: exact diagonal-space threshold - partial sums at growing N.
complete in H_beta  <->  sum u_m^2 (2m+1)^{-2beta} = inf.
Threshold line eps=1/(k log k): u_m ~ log m -> boundary at beta=1/2.
"""
import mpmath as mp
import math
mp.mp.dps = 60

def u_sequence(eps, N):
    u = [mp.mpf(1)]*(N+1)
    for m in range(2, N+1):
        u[m] = u[m-1]*(1+eps(m))
    return u

def diag_partial(u, beta, Ns):
    s = mp.mpf(0); out = []
    for N in range(1, Ns+1):
        s += u[N]**2 * (2*N+1)**(-2*beta)
        if N in (Ns//8, Ns//4, Ns//2, Ns):
            out.append((N, mp.nstr(s, 6)))
    return out

# threshold line
for Ns in (50000, 100000):
    u = u_sequence(lambda k: 1.0/(k*math.log(k+1)), Ns)
    print("eps=1/(k log k), N=", Ns)
    for beta in (0.5, 0.6):
        print(f"   beta={beta}:", diag_partial(u, beta, Ns), "(beta=0.5 diverges slowly, 0.6 converges)")

# sharpness C/k
Ns = 50000
C = 2.0
u = u_sequence(lambda k: C/k, Ns)
print("eps=2/k: u_m/m^2 ->", mp.nstr(u[Ns]/Ns**2, 10), "(=1/Gamma(3)=0.5 expected)")
for beta in (2.4, 2.5, 2.6):
    print(f"   beta={beta}:", diag_partial(u, beta, Ns), "(boundary beta=2.5)")
