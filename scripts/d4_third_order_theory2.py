# -*- coding: utf-8 -*-
"""Direction 4 fix pass."""
from fractions import Fraction as F
import math
from mpmath import mp, mpf, log

# ---------- (A) closed forms, exact Fraction division ----------
print("=== (A) closed forms (fixed) ===")
def fact(n):
    r = F(1)
    for k in range(2, n+1): r *= k
    return r
def check_mu_form(parity, form, cval, N=30):
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

even_form1 = lambda j,cF: fact(2*j+1)/(cF**j)
even_form2 = lambda j,cF: fact(2*j)/(cF**j)
odd_form1  = lambda j,cF: fact(2*j+3)/(F(6)*(j+1)*cF**j)
odd_form2  = lambda j,cF: fact(2*j+1)/(cF**j)
for cval in (1, 3, 5, 10):
    res = []
    for name, form, par in (("even (2j+1)!/c^j", even_form1, 'e'),
                            ("even (2j)!/c^j",   even_form2, 'e'),
                            ("odd (2j+3)!/(6(j+1)c^j)", odd_form1, 'o'),
                            ("odd (2j+1)!/c^j",  odd_form2, 'o')):
        ok, jf = check_mu_form(par, form, cval)
        res.append(f"{name}={ok}" + (f"@j={jf}" if jf else ""))
    print(f"  c={cval}: " + ", ".join(res))

# ---------- (C) debug s-recurrence ----------
print("=== (C) s-recurrence debug ===")
def build_z(parity, cval, zinit, N=80):
    cF = F(cval); lam = F(4)/cF
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
    z = [zinit(k) for k in range(N+1)]
    for j in range(3,N+1):
        z[j] = a1f(j)*z[j-1] + a2f(j)*z[j-2] + a3f(j)*z[j-3]
    return z, E, a2f, a3f

def check_s(parity, cval, z, E, a2f, a3f, N=80):
    r = [z[j]/E[j] for j in range(N+1)]
    s = [None]*(N+1)
    for j in range(1,N+1): s[j] = r[j]-r[j-1]
    for j in range(3,N+1):
        Y = a2f(j)/(E[j]*E[j-1])
        Z = a3f(j)/(E[j]*E[j-1]*E[j-2])
        if s[j] != -(Y+Z)*s[j-1] - Z*s[j-2]:
            return False, j
    return True, None

for parity in ('e','o'):
    for cval in (3,):
        # case 1: random initial data
        z,E,a2f,a3f = build_z(parity, cval, lambda k: F(k+1), 60)
        ok,jf = check_s(parity, cval, z, E, a2f, a3f, 60)
        print(f"  parity={parity} c={cval}: random init s-rec = {ok}" + (f" fail@j={jf}" if jf else ""))
        # case 2: mu_1 = 1 solution (as in h3_v56)
        cF = F(cval)
        def mu_sol(k):
            if k == 0: return F(0)
            if k == 1: return F(1)
            return None
        # build via mu recurrence then z-transform
        N2 = 60
        mu = [F(0)]*(N2+1); mu[1] = F(1)
        for j in range(2,N2+1):
            if parity=='e':
                P,Q,R = (F(8)*cF*j*j - F(4)*cF*j + cF*cF*F(j,j-1),
                         F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3),
                         F(4)*j*(j-2)*(2*j-3)*(2*j-5))
            else:
                P,Q,R = (F(8)*cF*j*j + F(4)*cF*j + cF*cF*F(j,j-1),
                         F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1),
                         F(4)*j*(j-2)*(2*j-1)*(2*j-3))
            mu[j] = (P*mu[j-1] - Q*mu[j-2] + R*mu[j-3])/(cF*cF)
        lam = F(4)/cF
        z2 = [mu[j]/(fact(j)**2 * lam**j) for j in range(N2+1)]
        # rebuild E for this N2
        E2 = [F(1)]*(N2+1)
        beta = 1 if parity=='e' else 3
        for j in range(1,N2+1): E2[j] = E2[j-1]*(F(1)+F(beta)/(F(2)*j))
        def a2b(j):
            if parity=='e': Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3)
            else:           Q = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1)
            return -Q/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
        def a3b(j):
            if parity=='e': R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
            else:           R = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
            return R/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
        ok,jf = check_s(parity, cval, z2, E2, a2b, a3b, N2)
        print(f"  parity={parity} c={cval}: mu_1=1 init  s-rec = {ok}" + (f" fail@j={jf}" if jf else ""))

# ---------- (D) minimal solution with mpmath ----------
print("=== (D) minimal solution (mpmath backward iteration) ===")
mp.dps = 80
def minimal_mp(parity, cval, N=120):
    cf = mpf(cval); lam = mpf(4)/cf
    def a1(j):
        jj = mpf(j)
        if parity=='e': P = 8*cf*jj*jj - 4*cf*jj + cf*cf*jj/(jj-1)
        else:           P = 8*cf*jj*jj + 4*cf*jj + cf*cf*jj/(jj-1)
        return P/(cf*cf*jj*jj*lam)
    def a2(j):
        jj = mpf(j)
        if parity=='e': Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj-3) + 4*cf*jj*(2*jj-3)
        else:           Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj+1) + 4*cf*jj*(2*jj-1)
        return -Q/(cf*cf*jj*jj*(jj-1)*(jj-1)*lam*lam)
    def a3(j):
        jj = mpf(j)
        if parity=='e': R = 4*jj*(jj-2)*(2*jj-3)*(2*jj-5)
        else:           R = 4*jj*(jj-2)*(2*jj-1)*(2*jj-3)
        return R/(cf*cf*jj*jj*(jj-1)*(jj-1)*(jj-2)*(jj-2)*lam**3)
    z = [mpf(0)]*(N+3)
    z[N] = mpf(1)
    for j in range(N-1, -1, -1):
        z[j] = (z[j+3] - a1(j+3)*z[j+2] - a2(j+3)*z[j+1])/a3(j+3)
    h = [z[j]/z[0] for j in range(N+1)]
    return h

for parity in ('e','o'):
    h = minimal_mp(parity, 3)
    print(f"  parity={parity} c=3: h*_1/h*_0 = {mp.nstr(h[1],10)}, h*_2/h*_0 = {mp.nstr(h[2],10)}")
    fwd = [h[1], h[2]/h[1], h[3]/h[2], h[4]/h[3], h[5]/h[4]]
    print(f"    forward ratios h*_j/h*_j-1 (j=1..5): {[mp.nstr(x,8) for x in fwd]}")
    for j in (10, 50, 100):
        print(f"    ratio at j={j}: {mp.nstr(h[j+1]/h[j],8)}")
    # compare with guesses
    print(f"    1/(2j+1) at j=5: {mp.nstr(1/mpf(11),8)}; h*_6/h*_5 = {mp.nstr(h[6]/h[5],8)}")
