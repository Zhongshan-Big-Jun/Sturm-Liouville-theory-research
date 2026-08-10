# -*- coding: utf-8 -*-
"""Direction 3 (part 2): Krein-family stability in log-space.
A_m - B_m = 4m + c m/(m-1) >= 4m -> u_m >= prod(1+4k/c) ~ (4/c)^{m-1} (m-1)! superfactorial."""
import math

def solve_u_log(A, B, c0, N):
    """u_0=0, u_1=1, c0 u_m = A_m u_{m-1} - B_m u_{m-2}. Return log u_m."""
    logu = [None]*(N+1)
    logu[0] = -math.inf
    logu[1] = 0.0
    for m in range(2, N+1):
        Am, Bm = A(m), B(m)
        ratio = math.exp(logu[m-1] - logu[m-2])   # u_{m-1}/u_{m-2} >= 1
        arg = 1.0 - (Bm/Am)/ratio
        logu[m] = math.log(Am) + logu[m-1] + math.log(arg)
    return logu

def lfact(n):
    return math.lgamma(n+1)

print("=== V4: Krein family c-perturbation (log-space) ===")
for cval in (3.0, 5.0, 1.0, 0.5):
    N = 300
    A = lambda m: 2*m*(2*m-1) + cval*m/(m-1)
    B = lambda m: 2*m*(2*m-3)
    logu = solve_u_log(A, B, cval, N)
    m = N-1
    lower = (m-1)*math.log(4.0/cval) + lfact(m-1)
    print(f"  c={cval}: log u_{m} = {logu[m]:.1f}, lower bound (4/c)^(m-1)(m-1)! = {lower:.1f}, margin = {logu[m]-lower:+.1f} (>=0 means lemma holds)")

print()
print("=== V4b: perturbed c (delta = +2, -1.5) ===")
for delta in (2.0, -1.5):
    cval = 3.0 + delta
    if cval <= 0: continue
    N = 300
    A = lambda m: 2*m*(2*m-1) + cval*m/(m-1)
    B = lambda m: 2*m*(2*m-3)
    logu = solve_u_log(A, B, cval, N)
    m = N-1
    lower = (m-1)*math.log(4.0/cval) + lfact(m-1)
    print(f"  c={cval}: log u_{m} = {logu[m]:.1f}, lower = {lower:.1f}, margin = {logu[m]-lower:+.1f}")
    # min excess A-B-c
    print(f"    min_{2<=m<300} (A-B-c') = {min(2*m*(2*m-1) + cval*m/(m-1) - 2*m*(2*m-3) - cval for m in range(2,N)):.4f}")

print()
print("=== V5: basis coefficient perturbation delta_m = D/sqrt(m) ===")
for D in (0.0, 1.0, 5.0, 20.0):
    cval = 3.0; N = 300
    A = lambda m: 2*m*(2*m-1) + cval*(m/(m-1) + D/math.sqrt(m))
    B = lambda m: 2*m*(2*m-3)
    logu = solve_u_log(A, B, cval, N)
    m = N-1
    lower = (m-1)*math.log(4.0/cval) + lfact(m-1)
    minsum = min(A(m)-B(m)-cval for m in range(2, N))
    print(f"  D={D}: log u_{m} = {logu[m]:.1f}, lower = {lower:.1f}, margin = {logu[m]-lower:+.1f}, min(A-B-c) = {minsum:.3f}")

print()
print("=== V6: marginal cases - eps_k = 1/log^p(k) ===")
# eps_k = 1/log(k): sum ~ m/log m = omega(log m) -> superpoly; verify
import math
for p in (1.0,):
    c0 = 1.0; N = 2000
    A = lambda m: c0*(1.0 + 1.0/math.log(max(m,2))**p)
    B = lambda m: 0.0
    logu = solve_u_log(A, B, c0, N)
    # log u_m - 8 log m should -> +inf
    print(f"  eps=1/log^p k, p={p}: log u_1999 = {logu[N-1]:.2f}, 8 log 1999 = {8*math.log(N-1):.2f}")
    for m in (200, 800, 1999):
        print(f"    m={m}: log u - 8 log m = {logu[m] - 8*math.log(m):.3f}")
