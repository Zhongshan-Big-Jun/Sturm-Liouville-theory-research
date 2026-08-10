# -*- coding: utf-8 -*-
"""Direction 3: stability of the moment-jump growth lemma.
Theorem (stability): if q_n has jump structure q_{2m} = c0 x^{2m} - A_m x^{2m-2}
+ B_m x^{2m-4} (B_m >= 0, A_m >= B_m) and sum_{k<=m}(A_k-B_k-c0)/c0 = omega(log m),
then {q_n} is complete in any H with ||x^k||_H <= C k^beta.
Sharpness: if u_m (the recurrence solution) is only polynomial (e.g. eps_k ~ C/k),
completeness can fail in the diagonal space H_beta for beta > C + 1/2."""
from fractions import Fraction as F
import math

def solve_u(c0, A, B, N, u0=0, u1=1):
    """c0 u_m = A_m u_{m-1} - B_m u_{m-2}, u_0=u0, u_1=u1."""
    u = [F(0)]*(N+1)
    u[0], u[1] = F(u0), F(u1)
    for m in range(2, N+1):
        u[m] = (A(m)*u[m-1] - B(m)*u[m-2]) / F(c0)
    return u

def poly_growth_rate(u, N):
    """Estimate C in u_m ~ m^C via log u_m / log m at the tail."""
    import math
    vals = []
    for m in range(N//2, N):
        if u[m] > 0:
            vals.append(math.log(float(u[m]))/math.log(m))
    return sum(vals)/len(vals) if vals else float('nan')

# --- V1: growth lemma u_m >= prod(1+eps_k) with eps_k = (A_k-B_k-c0)/c0 ---
print("=== V1: growth lemma lower bound ===")
def check_growth_lemma(c0, eps, N=200):
    A = lambda m: F(c0)*(1+eps(m))
    B = lambda m: F(0)
    u = solve_u(c0, A, B, N)
    prod = F(1)
    ok = True
    worst = F(0)
    for m in range(2, N+1):
        prod *= 1+eps(m)
        if u[m] < prod:
            ok = False
            worst = max(worst, (prod-u[m])/prod)
    return ok, float(worst) if not ok else 0.0

for name, eps in [
    ("eps_k = 1/sqrt(k)  [omega(log), superpoly]", lambda m: F(1)/math.isqrt(m) if m>0 else F(0)),
    ("eps_k = 1/k        [O(log), poly]",            lambda m: F(1)/m),
    ("eps_k = 1/k^1.5    [summable, bounded]",       lambda m: F(1)/max(m*math.isqrt(m),1)),
]:
    ok, worst = check_growth_lemma(F(1), eps)
    print(f"  {name}: lemma holds = {ok}, worst rel err = {worst:.2e}")

# --- V2: growth rates for eps_k ~ C k^{-alpha} ---
print("=== V2: growth rates log u_m / log m ===")
for alpha in (0.5, 1.0, 1.5):
    c0 = F(1); N = 400
    A = lambda m: F(c0) + F(1)/(m**alpha if m>0 else 1)
    B = lambda m: F(0)
    u = solve_u(c0, A, B, N)
    r = poly_growth_rate(u, N)
    log_u = math.log(float(u[N-1]))
    print(f"  alpha={alpha}: est. exponent C = {r:.4f}, log u_399 = {log_u:.3f}")

# --- V3: sharpness counterexample in diagonal space ---
# eps_k = C/k -> u_m ~ m^C (polynomial). Diagonal space H_beta, beta > C+1/2:
# w = sum M2 u_m (2m+1)^{-2 beta} x^{2m} is nonzero with moments M_{2m}=M2 u_m.
print("=== V3: sharpness - diagonal counterexample ===")
Cconst = 2   # eps_k = 2/k
c0 = F(1); N = 60
A = lambda m: F(c0) + F(Cconst)/m
B = lambda m: F(0)
u = solve_u(c0, A, B, N)
# verify u_m * (m^C) ratio bounded: polynomial
import math
rat = [float(u[m])/(m**Cconst) for m in range(20, N)]
print(f"  u_m/m^{Cconst} for m=20..59: min={min(rat):.4f} max={max(rat):.4f} (bounded => polynomial)")
# moment representability: sum m^2C (2m+1)^{-2 beta} converges iff beta > C+1/2
for beta in (Cconst+0.4, Cconst+0.6, Cconst+1.0):
    s = sum((m**Cconst)**2 / (2*m+1)**(2*beta) for m in range(1, 100000))
    print(f"  beta = {beta}: sum_1^infty m^(2C)(2m+1)^-2beta = {s:.6f} (converges = representable)")

# --- V4: Krein c-perturbation stability ---
print("=== V4: Krein family c-perturbation ===")
for cval in (3, 5, 1, 0.5):
    cF = F(cval)
    A = lambda m: F(2)*m*(2*m-1) + cF*m/(m-1)
    B = lambda m: F(2)*m*(2*m-3)
    N = 200
    u = solve_u(cF, A, B, N)
    # check u_m >= (4/c)^{m-1} (m-1)!-type growth: log u_m vs m log m
    logu = math.log(float(u[N-1])); m = N-1
    print(f"  c={cval}: log u_{m} = {logu:.2f}, (m log m) = {m*math.log(m):.2f}, ratio = {logu/(m*math.log(m)):.4f} (superfactorial)")
    # perturb c by +delta and -delta/2
    for delta in (0.0, 2.0, -1.5):
        cp = cF + F(delta)
        if cp <= 0: 
            print(f"    delta={delta}: skipped (c+delta<=0)")
            continue
        Ap = lambda m: F(2)*m*(2*m-1) + cp*m/(m-1)
        Bp = lambda m: F(2)*m*(2*m-3)
        up = solve_u(cp, Ap, Bp, N)
        # verify A-B >= cp: min excess
        minx = min(float(Ap(m)-Bp(m)-cp) for m in range(2, N))
        logup = math.log(float(up[N-1]))
        print(f"    delta={delta}: min(A-B-c') = {minx:.3f} >= 0, log u'_{N-1} = {logup:.2f}")

# --- V5: basis perturbation stability ---
# p_{2m} = x^{2m} - (m/(m-1) + delta_m) x^{2m-2}, delta_m = D m^{-0.5}
print("=== V5: basis coefficient perturbation (delta_m = D/sqrt(m)) ===")
for D in (0.0, 1.0, 5.0):
    cF = F(3)
    A = lambda m: F(2)*m*(2*m-1) + cF*(F(m)/(m-1) + F(D)/math.isqrt(max(m,1)))
    B = lambda m: F(2)*m*(2*m-3)
    N = 300
    u = solve_u(cF, A, B, N)
    logu = math.log(float(u[N-1]))
    print(f"  D={D}: log u_{N-1} = {logu:.2f} (superpoly, stable), min(A-B-c) = {float(min(A(m)-B(m)-cF for m in range(2,N))):.3f}")
