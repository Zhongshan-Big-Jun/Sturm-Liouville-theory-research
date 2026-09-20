# -*- coding: utf-8 -*-
"""#12: sparse huge jumps - log-space computation.
eps_{2^{2^j}} = exp(2^{2^j}) = exp(k);  log(1+eps) = k + log1p(exp(-k)) ~ k.
sum min(eps,1) = #jumps ~ log_2 log_2 m = o(log m);  S ~ (largest 2^{2^j} <= m) ~ m^{1/2}..m = omega(log m).
"""
import mpmath as mp
import math
mp.mp.dps = 60

def is_sparse(k):
    x = k; j = 0
    while x > 1 and x % 2 == 0:
        x //= 2; j += 1
    return (x == 1 and j % 2 == 0)

def lu(N):
    """log u_m = sum_{k=2}^m log(1+eps_k), eps_k = exp(k) at sparse k, else 0."""
    lu = [mp.mpf(0)]*(N+1)
    cnt = 0
    for m in range(2, N+1):
        lu[m] = lu[m-1]
        if is_sparse(m):
            cnt += 1
            lu[m] += mp.mpf(m) + mp.log1p(mp.e**(-m))   # log(1+e^m)
    return lu, cnt

N = 4000
lu, cnt = lu(N)
print("sparse exp-jumps: count up to", N, "=", cnt, " (o(log m):  log N =", mp.nstr(mp.log(N),6), ")")
print("log u_4000 =", mp.nstr(lu[N], 10), " vs log(4000) =", mp.nstr(mp.log(4000), 8),
      "  ratio =", mp.nstr(lu[N]/mp.log(N), 8), " -> superpoly")
print("largest jump =", 256, " ~ m^{1/2}..m so S = omega(log m):  sqrt(4000) =", mp.nstr(mp.sqrt(4000),6))
# ratio vs every polynomial power
for beta in (0.5, 1.0, 2.0, 3.0):
    print(f"   log(u_4000) - {beta} log(4000) = {mp.nstr(lu[N]-beta*mp.log(N), 8)}  (>0 -> u_4000 > m^beta)")
