# -*- coding: utf-8 -*-
"""H3 moment systems of the shifted Krein Laplacian: exact coefficients, fundamental
solutions, growth analysis, minimal-growth direction, balance-lemma asymptotics.

Context: {p_n} analytically complete in H^3  <=>  {K_c p_n} complete in H^1.
For w in H^1 with (w, K_c p_n)_1 = 0 for all admissible n, moments mu_k = <w, x^k>
satisfy (verified identities):
  mu_0 = mu_1 = 0,
  c^2 mu_{2m}   = P_m mu_{2m-2} - Q_m mu_{2m-4} + R_m mu_{2m-6} + T_m D,   D = w(1)+w(-1),
  c^2 mu_{2m+1} = Pp_m mu_{2m-1} - Qp_m mu_{2m-3} + Rp_m mu_{2m-5} + Tp_m S, S = w(1)-w(-1),
with the closed-form coefficients below (R_2 = Rp_2 = 0).

Usage: python h3_moment_system.py
"""
import numpy as np
import math
from fractions import Fraction as F

C = 3  # default shift parameter (c > 0)

def P_e(j, c): return F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
def Q_e(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
def R_e(j, c): return F(4)*j*(j-2)*(2*j-3)*(2*j-5)
def T_e(j, c): return F(4)*j*(4*j-5)
def P_o(j, c): return F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
def Q_o(j, c): return F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
def R_o(j, c): return F(4)*j*(j-2)*(2*j-1)*(2*j-3)
def T_o(j, c): return F(4)*j*(4*j-3)

def solve_even(c, nu1, D, N):
    """mu_{2j} sequence; nu_0 = 0 fixed; free params (nu1 = mu_2, D)."""
    c = F(c); nu = [F(0)]*(N+1); nu[1] = F(nu1)
    for j in range(2, N+1):
        rhs = P_e(j,c)*nu[j-1] - Q_e(j,c)*nu[j-2] + R_e(j,c)*nu[j-3] + T_e(j,c)*D
        nu[j] = rhs/(c*c)
    return nu

def solve_odd(c, w1, S, N):
    """mu_{2j+1} sequence; w_0 = 0 fixed; free params (w1 = mu_3, S)."""
    c = F(c); w = [F(0)]*(N+1); w[1] = F(w1)
    for j in range(2, N+1):
        rhs = P_o(j,c)*w[j-1] - Q_o(j,c)*w[j-2] + R_o(j,c)*w[j-3] + T_o(j,c)*S
        w[j] = rhs/(c*c)
    return w

def scaled_growth(c, parity, N, nu1, src, mode='y'):
    """Scaled (and optionally dominant-mode-normalized) recurrence.
    mode 'y': y_j = nu_j/(j!)^2.  mode 'z': z_j = y_j/(4/c)^j.
    src: D or S (the boundary source)."""
    c = float(c); lam = 4.0/c
    z = np.zeros(N+1); z[1] = nu1
    fac = [1,1,2,6,24,120]
    def a1(j):
        if parity=='e': return (8.0*c*j*j - 4.0*c*j + c*c*j/(j-1.0))/(c*c*j*j)
        else: return (8.0*c*j*j + 4.0*c*j + c*c*j/(j-1.0))/(c*c*j*j)
    def a2(j):
        if parity=='e': Q = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
        else: Q = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
        return -Q/(c*c*j*j*(j-1)*(j-1))
    def a3(j):
        if parity=='e': R = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
        else: R = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
        if j == 2: return 0.0
        return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2))
    def s_scaled(j):
        if parity=='e': T = 4.0*j*(4*j-5)
        else: T = 4.0*j*(4*j-3)
        if j <= 5: return T*src/(c*c*fac[j]**2)/lam**j
        return 0.0
    lam2, lam3 = lam*lam, lam*lam*lam
    for j in range(2, N+1):
        z[j] = (a1(j)/lam)*z[j-1] + (a2(j)/lam2)*z[j-2] + (a3(j)/lam3)*z[j-3] + s_scaled(j)
    if mode == 'y':
        # convert z back to y: y_j = z_j * lam^j  (watch overflow for lam > 1)
        return z
    return z

def log_fact(n): return math.lgamma(n+1)/math.log(10.0)

def main():
    print("=== 1. exact coefficient identities for a concrete w (w = x^2, c = 3) ===")
    # (w, K_c p_{2m})_1 = c^2 mu_{2m} - P_m mu_{2m-2} + Q_m mu_{2m-4} - R_m mu_{2m-6} - T_m D
    c = F(3)
    def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
    def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
    def l2(p, q):
        n = max(len(p), len(q)); P = list(p)+[F(0)]*(n-len(p)); Q = list(q)+[F(0)]*(n-len(q))
        return sum(P[j]*Q[k]*F(2, j+k+1) for j in range(n) for k in range(n) if (j+k)%2==0)
    def h1(p, q):
        return -F(1,2)*(ev(p,F(1))-ev(p,F(-1)))*(ev(q,F(1))-ev(q,F(-1))) + l2(deriv(p),deriv(q)) + c*l2(p,q)
    def kc(p):
        n = len(p)-1; out=[F(0)]*(n+1)
        for j in range(n+1):
            out[j] += c*p[j]
            if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
        return out
    # p_4 = x^4 - 2 x^2
    p4 = [F(0)]*5; p4[4]=F(1); p4[2]=-F(2)
    q4 = kc(p4)
    w = [F(0)]*3; w[2]=F(1)
    lhs = h1(w, q4)
    mu4 = l2(w, [F(0),F(0),F(0),F(0),F(1)])
    mu2 = l2(w, [F(0),F(0),F(1)])
    mu0 = l2(w, [F(1)])
    D = ev(w,F(1))+ev(w,F(-1))
    m = 2
    rhs = c*c*mu4 - P_e(m,c)*mu2 + Q_e(m,c)*mu0 - R_e(m,c)*F(0) - T_e(m,c)*D
    print("  (w,K_c p_4)_1 =", lhs, " ; formula =", rhs, " ; match:", lhs == rhs)

    print("=== 2. fundamental solutions u (nu1=1,D=0) and v (nu1=0,D=1): positivity + ratios ===")
    for cc in (1, 3, 5, 10):
        cF = F(cc); N = 60
        u = solve_even(cF, F(1), F(0), N); v = solve_even(cF, F(0), F(1), N)
        uo = solve_odd(cF, F(1), F(0), N); vo = solve_odd(cF, F(0), F(1), N)
        print(f"  c={cc}: u>0:{all(x>0 for x in u[2:])} v>0:{all(x>0 for x in v[2:])} "
              f"odd u>0:{all(x>0 for x in uo[2:])} odd v>0:{all(x>0 for x in vo[2:])}")
        # scaled ratio -> 4/c
        su = [u[j]/F(math.factorial(j))**2 for j in range(N+1)]
        print("    scaled u ratio at j=60:", float(su[60]/su[59]), " (target 4/c =", float(F(4)/cF), ")")

    print("=== 3. minimal-growth direction in the 2-param family is superfactorial ===")
    for cc in (1.0, 3.0, 10.0):
        N = 800; lam = 4.0/cc
        for name, par in (("even",'e'), ("odd",'o')):
            u = scaled_growth(cc, par, N, 1.0, 0.0)
            v = scaled_growth(cc, par, N, 0.0, 1.0)
            tail = 120
            Wm = np.column_stack([u[-tail:], v[-tail:]])
            _, _, Vt = np.linalg.svd(Wm)
            x = Vt[-1]
            zmin = x[0]*u + x[1]*v
            j = 700
            lognu = 2*log_fact(j) + j*np.log10(lam) + np.log10(abs(zmin[j]))
            bound = np.log10(np.sqrt(2.0/(2*j+1)))
            print(f"  c={cc} {name}: min-growth log10|mu_{2*j}| = {lognu:.1f} vs L2-bound log10 = {bound:.2f}"
                  f"  (params nu1,D = {x[0]:.4f},{x[1]:.4f})")

if __name__ == "__main__":
    main()
