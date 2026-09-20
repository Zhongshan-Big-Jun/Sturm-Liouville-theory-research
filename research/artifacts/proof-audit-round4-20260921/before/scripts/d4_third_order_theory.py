# -*- coding: utf-8 -*-
"""Direction 4: third-order recurrence general theory (Route A).
(A) closed forms in mu-scale; (B) beta-characterization of product solutions;
(C) exact reduction of order (s-recurrence); (D) minimal solution via backward iteration."""
from fractions import Fraction as F
import math
from sympy import symbols, expand, Poly, Rational, solve, factor, together, simplify

c = symbols('c', positive=True)
b = symbols('beta')

def even_coeffs(j, c):
    P = 8*c*j*j - 4*c*j + c*c*Rational(j, j-1)
    Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3)
    R = 4*j*(j-2)*(2*j-3)*(2*j-5)
    return P, Q, R

def odd_coeffs(j, c):
    P = 8*c*j*j + 4*c*j + c*c*Rational(j, j-1)
    Q = 4*j*(j-1)*(2*j-1)*(2*j+1) + 4*c*j*(2*j-1)
    R = 4*j*(j-2)*(2*j-1)*(2*j-3)
    return P, Q, R

# ---------- (A) closed forms in mu-scale, exact for fixed c ----------
print("=== (A) closed forms mu_j = (2j+1)!/c^j, (2j)!/c^j (even); odd analog ===")
def check_mu_form(parity, form, cval, N=40):
    cF = F(cval)
    for j in range(3, N+1):
        if parity == 'e':
            P,Q,R = (F(8)*cF*j*j - F(4)*cF*j + cF*cF*F(j,j-1),
                     F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3),
                     F(4)*j*(j-2)*(2*j-3)*(2*j-5))
        else:
            P,Q,R = (F(8)*cF*j*j + F(4)*cF*j + cF*cF*F(j,j-1),
                     F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1),
                     F(4)*j*(j-2)*(2*j-1)*(2*j-3))
        mu = lambda k: form(k, cF)
        lhs = cF*cF*mu(j)
        rhs = P*mu(j-1) - Q*mu(j-2) + R*mu(j-3)
        if lhs != rhs:
            return False, j
    return True, None

even_form1 = lambda j,cF: F(math.factorial(2*j+1))//(cF**j)  # (2j+1)!/c^j
def even_form2(j,cF):
    # (2j)!/c^j
    num = 1
    for k in range(1, 2*j+1): num *= k
    return F(num)//(cF**j)
def odd_form1(j,cF):
    # (2j+3)!/(6(j+1)c^j)
    num = 1
    for k in range(1, 2*j+4): num *= k
    return F(num)//(F(6)*(j+1)*(cF**j))
def odd_form2(j,cF):
    # (2j+1)!/c^j
    num = 1
    for k in range(1, 2*j+2): num *= k
    return F(num)//(cF**j)

for cval in (1, 3, 5, 10):
    ok1,_ = check_mu_form('e', even_form1, cval)
    ok2,_ = check_mu_form('e', even_form2, cval)
    ok3,_ = check_mu_form('o', odd_form1, cval)
    ok4,_ = check_mu_form('o', odd_form2, cval)
    print(f"  c={cval}: even (2j+1)!/c^j ok={ok1}, even (2j)!/c^j ok={ok2}, odd (2j+3)!/(6(j+1)c^j) ok={ok3}, odd (2j+1)!/c^j ok={ok4}")

# ---------- (B) beta-characterization: product solution E_j(beta) ----------
print("=== (B) beta-characterization ===")
def z_residual_poly(parity, j):
    """Residual of the ratio fixed-point identity, cleared of denominators.
    identity: 1+b/(2j) = a1 + a2/(1+b/(2(j-1))) + a3/((1+b/(2(j-1)))(1+b/(2(j-2))))"""
    if parity == 'e':
        P,Q,R = even_coeffs(j, c)
    else:
        P,Q,R = odd_coeffs(j, c)
    lam = Rational(4)/c
    a1 = P/(c*c*j*j*lam)
    a2 = -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    e1 = 1 + b/Rational(2*(j-1))
    e2 = 1 + b/Rational(2*(j-2))
    ej = 1 + b/Rational(2*j)
    resid = a1 + a2/e1 + a3/(e1*e2) - ej
    return together(resid)

for parity in ('e','o'):
    print(f"  parity={parity}: solving beta from coefficient conditions ...")
    # Take j = 3, 4, 5: clear denominators and solve each numerator=0 for beta
    sols = None
    eqs = []
    for j in (3,4,5):
        r = z_residual_poly(parity, j)
        num = Poly(factor(together(r).as_numer_denom()[0]), b)
        eqs.append(num.as_expr())
    # solve the system
    sol = solve(eqs, b, dict=True)
    print(f"    equations (j=3,4,5 numerator=0) solved: beta = {sol}")

# ---------- (C) exact reduction of order: s-recurrence ----------
print("=== (C) s-recurrence (exact reduction of order) ===")
def check_s_recurrence(parity, cval, N=80):
    cF = F(cval); lam = F(4)/cF
    # z-scale homogeneous solution from explicit E (dominant)
    E = [F(1)]*(N+1)
    beta = 1 if parity=='e' else 3
    for j in range(1,N+1): E[j] = E[j-1]*(F(1)+F(beta)/(F(2)*j))
    def a1f(j):
        if parity=='e': P = F(8)*cF*j*j - F(4)*cF*j + cF*cF*F(j,j-1)
        else:           P = F(8)*cF*j*j + F(4)*cF*j + cF*cF*F(j,j-1)
        return P/(cF*cF*j*j*lam)
    def a2f(j):
        if parity=='e': Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3)
        else:           Q = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1)
        return -Q/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
    def a3f(j):
        if parity=='e': R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        else:           R = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        return R/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    # take the second product solution E2 (beta2) as the "other" solution, and a third random one
    beta2 = -1 if parity=='e' else 1
    E2 = [F(1)]*(N+1)
    for j in range(1,N+1): E2[j] = E2[j-1]*(F(1)+F(beta2)/(F(2)*j))
    # random third solution: initial data z0=1, z1=2, z2=3
    z = [F(1), F(2), F(3)] + [F(0)]*(N-2)
    for j in range(3,N+1):
        z[j] = a1f(j)*z[j-1] + a2f(j)*z[j-2] + a3f(j)*z[j-3]
    # r_j = z_j/E_j, s_j = r_j - r_{j-1}; check s_j = -(Y+Z)s_{j-1} - Z s_{j-2}
    r = [z[j]/E[j] for j in range(N+1)]
    s = [None]*(N+1)
    for j in range(1,N+1): s[j] = r[j] - r[j-1]
    ok = True
    for j in range(3,N+1):
        Y = a2f(j)/(E[j]*E[j-1])
        Z = a3f(j)/(E[j]*E[j-1]*E[j-2])
        if s[j] != -(Y+Z)*s[j-1] - Z*s[j-2]:
            ok = False; break
    return ok

for parity in ('e','o'):
    for cval in (1,3,10):
        print(f"  parity={parity} c={cval}: s-recurrence exact for z=random initial data: {check_s_recurrence(parity,cval)}")

# ---------- (D) minimal solution via backward iteration ----------
print("=== (D) minimal solution (backward iteration) ===")
def minimal_solution(parity, cval, N=2000, K=12):
    cF = float(cval); lam = 4.0/cF
    def a1(j):
        if parity=='e': P = 8*cF*j*j - 4*cF*j + cF*cF*j/(j-1)
        else:           P = 8*cF*j*j + 4*cF*j + cF*cF*j/(j-1)
        return P/(cF*cF*j*j*lam)
    def a2(j):
        if parity=='e': Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*cF*j*(2*j-3)
        else:           Q = 4*j*(j-1)*(2*j-1)*(2*j+1) + 4*cF*j*(2*j-1)
        return -Q/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
    def a3(j):
        if parity=='e': R = 4*j*(j-2)*(2*j-3)*(2*j-5)
        else:           R = 4*j*(j-2)*(2*j-1)*(2*j-3)
        return R/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    # backward: z_j = (z_{j+3} - a1(j+3) z_{j+2} - a2(j+3) z_{j+1})/a3(j+3)
    z = [0.0]*(N+3)
    z[N] = 1.0
    for j in range(N-1, -1, -1):
        z[j] = (z[j+3] - a1(j+3)*z[j+2] - a2(j+3)*z[j+1])/a3(j+3)
    h = [z[j]/z[0] for j in range(N+1)]
    return h

for parity in ('e','o'):
    h = minimal_solution(parity, 3.0)
    print(f"  parity={parity} c=3: h*_1/h*_0 = {h[1]:.6f}, h*_2/h*_0 = {h[2]:.6f}")
    print(f"    forward ratios: h1/h0={h[1]:.4f} h2/h1={h[2]/h[1]:.4f} h3/h2={h[3]/h[2]:.4f} h4/h3={h[4]/h[3]:.4f}")
    # compare with 1/((j!)^2 (4/c)^j E_j) guess: h_j ~ ?
    # print log h_j vs j
    print(f"    log h_j for j=0,1,2,3,4: {[round(math.log(max(h[j],1e-300)),3) for j in range(5)]}")
    # ratios h_{j+1}/h_j for larger j
    print(f"    ratios at j=10,100,1000: {h[11]/h[10]:.6f}, {h[101]/h[100]:.6f}, {h[1001]/h[1000]:.6f}")
