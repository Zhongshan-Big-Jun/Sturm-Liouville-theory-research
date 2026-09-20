# -*- coding: utf-8 -*-
"""#12: verify the refined dichotomy (fixed version).
Sufficiency: S(m)=sum log(1+eps_k)=omega(log m)  ->  u_m super-poly  ->  complete.
Diagonal-space exactness: complete in H_beta  <->  sum u_m^2 (2m+1)^{-2beta} = inf.
Threshold line eps_k = C/(k log k): u_m ~ (log m)^C -> complete <-> beta <= 1/2.
Sharpness eps_k = C/k: u_m ~ m^C/Gamma(1+C) -> complete <-> beta <= C+1/2.
Sparse huge jumps (gain of S over sum min): eps_{2^{2^j}} = exp(2^{2^j}).
  sum min(eps,1) = #jumps = o(log m);  S ~ m^{1/2}..m = omega(log m) -> complete.
"""
import mpmath as mp
import math
mp.mp.dps = 60

def u_sequence(eps, N):
    u = [mp.mpf(1)]*(N+1)
    for m in range(2, N+1):
        u[m] = u[m-1]*(1+eps(m))
    return u

def diag_series(u, N, beta):
    # sum_{m=1..N} u[m]^2 (2m+1)^(-2 beta), plain loop (no mp.nsum on list)
    s = mp.mpf(0)
    for m in range(1, N+1):
        s += u[m]**2 * (2*m+1)**(-2*beta)
    return s

# ---- (1) eps_k = k^{-0.5}: S ~ 2 sqrt(m) = omega(log m), super-poly, complete
u = u_sequence(lambda k: 1.0/math.sqrt(k), 4000)
print("(1) eps=k^-0.5: log(u_4000)/log(4000) =", mp.nstr(mp.log(u[4000])/mp.log(4000), 8), "-> superpoly (S ~ 2 sqrt m)")

# ---- (2) threshold line eps_k = 1/(k log k): S ~ log log m, u_m ~ log m
u = u_sequence(lambda k: 1.0/(k*math.log(k+1)), 200000)
print("(2) eps=1/(k log k): u_200000 =", mp.nstr(u[200000], 8), " log u =", mp.nstr(mp.log(u[200000]), 6),
      " loglog m =", mp.nstr(mp.log(mp.log(200000)), 6))
print("    u_m/m^0.1 ->", mp.nstr(u[200000]/200000**0.1, 6), "(->0, polynomial)")
for beta in (0.5, 0.6, 1.0):
    s = diag_series(u, 200000, beta)
    print(f"    beta={beta}: partial sum u_m^2 (2m+1)^-2beta = {mp.nstr(s,8)}  (converges iff beta>1/2)")

# ---- (3) sparse huge jumps: eps = exp(k) at k = 2^{2^j};  sum min = o(log m), S = omega(log m)
def eps_sparse(k):
    x = k; j = 0
    while x > 1 and x % 2 == 0:
        x //= 2; j += 1
    return math.exp(k) if (x == 1 and j % 2 == 0) else 0.0
u = u_sequence(eps_sparse, 4000)
jumps = [k for k in range(2,4001) if eps_sparse(k) > 0]
print("(3) sparse exp-jumps at k =", jumps, "-> sum min(eps,1) =", len(jumps), "= o(log 4000)")
print("    log u_4000 =", mp.nstr(mp.log(u[4000]), 8), " vs log(4000)=", mp.nstr(mp.log(4000), 6),
      " ratio =", mp.nstr(mp.log(u[4000])/mp.log(4000), 6), "-> superpoly -> complete")

# ---- (4) eps_k = C/k: u_m ~ m^C/Gamma(1+C); complete <-> beta <= C+1/2
C = 2.0
u = u_sequence(lambda k: C/k, 5000)
print("(4) eps=2/k: u_m/m^2 at m=5000 =", mp.nstr(u[5000]/5000**2, 8), " (-> 1/Gamma(3) = 1/2)")
for beta in (2.4, 2.6, 2.5):
    s = diag_series(u, 5000, beta)
    print(f"    beta={beta}: partial sum = {mp.nstr(s,8)}  (threshold beta>C+1/2=2.5)")

# ---- (5) threshold line with constant C: eps = C/(k log k), u_m ~ (log m)^C
for Cv in (1.0, 2.0):
    u = u_sequence(lambda k: Cv/(k*math.log(k+1)), 200000)
    r = mp.log(u[200000])/mp.log(mp.log(200000))
    print(f"(5) eps={Cv}/(k log k): log u / loglog m = {mp.nstr(r,8)} (-> C={Cv})")
