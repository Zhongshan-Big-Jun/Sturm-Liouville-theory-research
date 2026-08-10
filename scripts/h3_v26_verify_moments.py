# -*- coding: utf-8 -*-
"""H3 v26: independent re-derivation check of the even/odd moment systems.
Direct exact computation of (w, K_c p_{2m})_1 and (w, K_c p_{2m+1})_1 for
polynomial test functions w, vs the closed-form moment recurrences in
h3_moment_system.py.  Also checks mu_0 = mu_1 = 0.
"""
from fractions import Fraction as F

def ev(p, x):
    return sum(a*x**k for k, a in enumerate(p))

def deriv(p):
    return [F(k)*p[k] for k in range(1, len(p))]

def l2(p, q):
    n = max(len(p), len(q))
    P = list(p) + [F(0)]*(n-len(p))
    Q = list(q) + [F(0)]*(n-len(q))
    return sum(P[j]*Q[k]*F(2, j+k+1) for j in range(n) for k in range(n) if (j+k) % 2 == 0)

def h1(p, q, c):
    # (p,q)_1 = -1/2 * Delta p * Delta q + int (p' q' + c p q)
    Dp = ev(p, F(1)) - ev(p, F(-1))
    Dq = ev(q, F(1)) - ev(q, F(-1))
    return -F(1,2)*Dp*Dq + l2(deriv(p), deriv(q)) + c*l2(p, q)

def kc(p, c):
    # K_c p = -p'' + c p as polynomial list
    n = len(p) - 1
    out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n:
            out[j] -= F((j+1)*(j+2))*p[j+2]
    return out

def P_e(j, c): return F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
def Q_e(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
def R_e(j, c): return F(4)*j*(j-2)*(2*j-3)*(2*j-5)
def T_e(j, c): return F(4)*j*(4*j-5)
def P_o(j, c): return F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
def Q_o(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
def R_o(j, c): return F(4)*j*(j-2)*(2*j-1)*(2*j-3)
def T_o(j, c): return F(4)*j*(4*j-3)

c = F(3)
print("=== c = 3: check mu_0 = mu_1 = 0 from (w, Kp_0)_1, (w, Kp_1)_1 ===")
for wname, w in (("x^2", [F(0),F(0),F(1)]), ("x", [F(0),F(1)]), ("x^2+x", [F(0),F(1),F(1)])):
    h01 = h1(w, kc([F(1)], c), c)      # (w, K p_0)_1 = c^2 mu_0
    h11 = h1(w, kc([F(0),F(1)], c), c) # (w, K p_1)_1 = c^2 mu_1
    mu0 = l2(w, [F(1)])
    mu1 = l2(w, [F(0),F(1)])
    print(f"  w={wname}: (w,Kp0)_1={h01} (c^2 mu0={c*c*mu0}) ; (w,Kp1)_1={h11} (c^2 mu1={c*c*mu1})")

print()
print("=== even: (w, Kc p_{2m})_1 vs recurrence formula for w = x^2 (and w = x^4) ===")
for wname, w in (("x^2", [F(0),F(0),F(1)]), ("x^4", [F(0),F(0),F(0),F(0),F(1)])):
    # moments
    def moments(w, N):
        mu = [F(0)]*(N+1)
        for k in range(N+1):
            pk = [F(0)]*(k+1); pk[k] = F(1)
            mu[k] = l2(w, pk)
        return mu
    mu = moments(w, 30)
    D = ev(w, F(1)) + ev(w, F(-1))
    ok = True
    for m in range(2, 8):
        # p_{2m} = x^{2m} - m/(m-1) x^{2m-2}
        pm = [F(0)]*(2*m+1); pm[2*m] = F(1); pm[2*m-2] = -F(m, m-1)
        lhs = h1(w, kc(pm, c), c)
        rhs = c*c*mu[2*m] - P_e(m,c)*mu[2*m-2] + Q_e(m,c)*mu[2*m-4] - R_e(m,c)*(mu[2*m-6] if 2*m-6 >= 0 else F(0)) - T_e(m,c)*D
        if lhs != rhs:
            ok = False
            print(f"  MISMATCH m={m}: lhs={lhs} rhs={rhs}")
    print(f"  w={wname}: even system OK = {ok}")

print()
print("=== odd: (w, Kc p_{2m+1})_1 vs recurrence formula for w = x (and w = x^3) ===")
for wname, w in (("x", [F(0),F(1)]), ("x^3", [F(0),F(0),F(0),F(1)])):
    def moments(w, N):
        mu = [F(0)]*(N+1)
        for k in range(N+1):
            pk = [F(0)]*(k+1); pk[k] = F(1)
            mu[k] = l2(w, pk)
        return mu
    mu = moments(w, 30)
    S = ev(w, F(1)) - ev(w, F(-1))
    ok = True
    for m in range(2, 8):
        pm = [F(0)]*(2*m+2); pm[2*m+1] = F(1); pm[2*m-1] = -F(m, m-1)
        lhs = h1(w, kc(pm, c), c)
        rhs = c*c*mu[2*m+1] - P_o(m,c)*mu[2*m-1] + Q_o(m,c)*mu[2*m-3] - R_o(m,c)*(mu[2*m-5] if 2*m-5 >= 0 else F(0)) - T_o(m,c)*S
        if lhs != rhs:
            ok = False
            print(f"  MISMATCH m={m}: lhs={lhs} rhs={rhs}")
    print(f"  w={wname}: odd system OK = {ok}")
