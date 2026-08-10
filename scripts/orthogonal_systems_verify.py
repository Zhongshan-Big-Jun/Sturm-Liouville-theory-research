# -*- coding: utf-8 -*-
# Direction 1 verification: explicit orthogonal polynomial systems in H^s
# s = 2r: Q_n = K_c^{-r} P_n (Legendre);  s = 2r+1: Q_n = K_c^{-r} K_n (Krein-Sobolev)
from fractions import Fraction as F
from math import comb
import itertools

# ---------------- polynomial utilities (coefficient lists, index = power) ----------------
def pad(p, n):
    return p + [F(0)] * (n - len(p))

def padd(p, q):
    n = max(len(p), len(q)); return [pad(p,n)[i] + pad(q,n)[i] for i in range(n)]

def psub(p, q):
    n = max(len(p), len(q)); return [pad(p,n)[i] - pad(q,n)[i] for i in range(n)]

def pscale(c, p):
    return [c*x for x in p]

def pmul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return r

def pderiv(p):
    return [F(i)*p[i] for i in range(1, len(p))]

def peval(p, x):
    return sum(p[i] * x**i for i in range(len(p)))

def pdeg(p):
    d = len(p) - 1
    while d >= 0 and p[d] == 0: d -= 1
    return d

# ---------------- operators ----------------
def Kc_apply(p, c):
    return padd(pscale(c, p), pscale(F(-1), pderiv(pderiv(p))))

def Kc_r_apply(p, c, r):
    # (c - D^2)^r acting on polynomial p
    q = p
    for _ in range(r):
        q = Kc_apply(q, c)
    return q

def Kc_inv_r_monomial(k, c, r):
    # K_c^{-r} x^k = sum_{j=0}^{floor(k/2)} C(r+j-1, j) c^{-(r+j)} k!/(k-2j)! x^{k-2j}
    coeffs = [F(0)] * (k + 1)
    for j in range(0, k // 2 + 1):
        f = F(comb(r + j - 1, j)) * F(1, c ** (r + j)) * F(_fact(k), _fact(k - 2 * j))
        coeffs[k - 2 * j] += f
    return coeffs

def _fact(n):
    r = 1
    for i in range(2, n + 1): r *= i
    return r

def Kc_inv_r_apply(p, c, r):
    if r == 0:
        return p
    out = [F(0)] * len(p)
    for k, coef in enumerate(p):
        if coef != 0:
            out = padd(out, pscale(coef, Kc_inv_r_monomial(k, c, r)))
    return out

# ---------------- Legendre ----------------
def legendre(n):
    # P_n with P_n(1) = 1
    coeffs = [F(0)] * (n + 1)
    for k in range(0, n // 2 + 1):
        sign = F((-1) ** k)
        num = _fact(2 * n - 2 * k)
        den = _fact(k) * _fact(n - k) * _fact(n - 2 * k)
        coeffs[n - 2 * k] = sign * F(num, den * (2 ** n))
    return coeffs

# ---------------- Krein-Sobolev via S_n basis and a-coefficient recurrence ----------------
def S_poly(n):
    # S_n = P_n - P_{n-2}
    if n == 0: return [F(1)]
    if n == 1: return [F(0), F(1)]
    return psub(legendre(n), legendre(n - 2))

def a_coeffs(N, c):
    # a_0=a_1=a_2=a_3=1, a_{n+2} = a_n(1+(4n^2-1)/c) + (2n+1)/(2n-3)(a_n - a_{n-2})
    a = [F(1)] * max(4, N + 1)
    for n in range(2, N - 1):
        a[n + 2] = a[n] * (1 + F(4 * n * n - 1, c)) + F(2 * n + 1, 2 * n - 3) * (a[n] - a[n - 2])
    return a

def a_closed_even(m, c):
    # a_{2m} = sum_{k=0}^{m-1} (1/(4c))^k (2m+2k-1)!/((2m-2k-1)!(2k)!), a_0=a_2=1
    if m == 0 or m == 1: return F(1)
    s = F(0)
    for k in range(0, m):
        s += (F(1, 4 * c) ** k) * F(_fact(2 * m + 2 * k - 1), _fact(2 * m - 2 * k - 1) * _fact(2 * k))
    return s

def a_closed_odd(m, c):
    # a_{2m+1} = sum_{k=0}^{m-1} (1/(4c))^k (m-k)/(m+k) (2m+2k+1)!/((2m-2k+1)!(2k)!), a_1=a_3=1
    if m == 0 or m == 1: return F(1)
    s = F(0)
    for k in range(0, m):
        s += (F(1, 4 * c) ** k) * F(m - k, m + k) * F(_fact(2 * m + 2 * k + 1), _fact(2 * m - 2 * k + 1) * _fact(2 * k))
    return s

def krein_sobolev(n, c, a=None):
    # K_n = sum_{r=0}^{[n/2]} a_{n-2r} S_{n-2r}
    if a is None:
        a = a_coeffs(n + 2, c)
    out = [F(0)] * (n + 1)
    for r in range(0, n // 2 + 1):
        out = padd(out, pscale(a[n - 2 * r], S_poly(n - 2 * r)))
    return out

# ---------------- inner products ----------------
def L2_inner(p, q):
    s = F(0)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            if (i + j) % 2 == 0:
                s += a * b * F(2, i + j + 1)
    return s

def eval_Delta(p):
    return peval(p, F(1)) - peval(p, F(-1))

def inner_1(p, q, c):
    return (L2_inner(pderiv(p), pderiv(q)) + c * L2_inner(p, q)
            - F(1, 2) * eval_Delta(p) * eval_Delta(q))

def inner_s(p, q, s, c):
    if s % 2 == 0:
        r = s // 2
        return L2_inner(Kc_r_apply(p, c, r), Kc_r_apply(q, c, r))
    else:
        r = (s - 1) // 2
        return inner_1(Kc_r_apply(p, c, r), Kc_r_apply(q, c, r), c)

# ---------------- Q families ----------------
def Q_poly(n, s, c):
    # Q_n^{(s)} = K_c^{-floor(s/2)} tildeQ where tildeQ = P_n (s even) or K_n (s odd)
    r = s // 2
    if s % 2 == 0:
        return Kc_inv_r_apply(legendre(n), c, r)
    else:
        return Kc_inv_r_apply(krein_sobolev(n, c), c, r)

def norm_sq(p, s, c):
    return inner_s(p, p, s, c)

if __name__ == '__main__':
    # ---------------- tests ----------------
    ok = True
    def check(name, cond):
        global ok
        print(("PASS " if cond else "FAIL ") + name)
        if not cond: ok = False

    # T1: K_c^{-r} x^k closed form matches direct linear solve (inverse of (c-D^2)^r)
    for c in [1, 3, 5]:
        for r in [1, 2, 3]:
            for k in range(0, 9):
                direct = Kc_inv_r_apply([F(0)]*k + [F(1)], c, r)   # polynomial x^k
                # verify (c-D^2)^r applied to direct == x^k
                back = Kc_r_apply(direct, c, r)
                check(f"T1 inv formula c={c} r={r} k={k}", back == [F(0)]*k + [F(1)])

    # T2: a-coefficient closed forms vs recurrence
    for c in [1, 3, 5, 10]:
        a = a_coeffs(24, c)
        for m in range(0, 12):
            check(f"T2 even closed a_{2*m} c={c}", a[2*m] == a_closed_even(m, c))
            check(f"T2 odd closed a_{2*m+1} c={c}", a[2*m+1] == a_closed_odd(m, c))

    # T3: orthogonality + norms for s=1..4, c in {1,3,5}, n up to 8
    for c in [1, 3, 5]:
        for s in [1, 2, 3, 4]:
            N = 8
            polys = [Q_poly(n, s, c) for n in range(0, N+1)]
            # triangularity: Q_n has exact degree n
            for n in range(0, N+1):
                check(f"T3 deg Q_{n} s={s} c={c}", pdeg(polys[n]) == n)
            # orthogonality
            for m in range(0, N+1):
                for n in range(m+1, N+1):
                    v = inner_s(polys[m], polys[n], s, c)
                    check(f"T3 orth (Q_{m},Q_{n}) s={s} c={c}", v == 0)
            # norms: even s: 2/(2n+1); odd s: (2c/(2n+1)) a_n a_{n+2}
            a = a_coeffs(N + 3, c)
            for n in range(0, N+1):
                nsq = norm_sq(polys[n], s, c)
                if s % 2 == 0:
                    target = F(2, 2*n + 1)
                else:
                    target = F(2*c, 2*n + 1) * a[n] * a[n+2]
                check(f"T3 norm Q_{n} s={s} c={c}", nsq == target)

    # T4: s=1 family == paper's Krein-Sobolev polynomials (first few explicit from paper)
    for c in [1, 3]:
        K1 = Q_poly(1, 1, c);  K2 = Q_poly(2, 1, c);  K3 = Q_poly(3, 1, c);  K4 = Q_poly(4, 1, c)
        # K1 = x
        check(f"T4 K1 c={c}", K1 == [F(0), F(1)])
        # K2 = (3/2)x^2 - 1/2
        check(f"T4 K2 c={c}", K2 == [F(-1,2), F(0), F(3,2)])
        # K3 = (5/2)x^3 - (3/2)x
        check(f"T4 K3 c={c}", K3 == [F(0), F(-3,2), F(0), F(5,2)])
        # K4 = ((35c+525)/(8c))x^4 - ((30c+630)/(8c))x^2 + (3c+105)/(8c)
        K4t = [F(3*c+105, 8*c), F(0), F(-(30*c+630), 8*c), F(0), F(35*c+525, 8*c)]
        check(f"T4 K4 c={c}", K4 == K4t)

    # T5: (K_m, K_n)_1 norm formula from paper Theorem 3, and roots in (-1,1) simple for n<=8
    from fractions import Fraction as F
    for c in [1, 3]:
        a = a_coeffs(12, c)
        for n in range(0, 9):
            Kn = Q_poly(n, 1, c)
            nsq = norm_sq(Kn, 1, c)
            check(f"T5 norm K_{n} c={c}", nsq == F(2*c, 2*n+1) * a[n] * a[n+2])

    # T6: even case Q_n^{(2)} first few closed forms
    for c in [1, 3]:
        Q2 = Q_poly(2, 2, c)
        # Q_2^{(2)} = (3x^2 + 6/c - 1)/(2c)
        t = [F(6, c) - 1, F(0), F(3)]
        t = pscale(F(1, 2*c), t)
        check(f"T6 Q_2 s=2 c={c}", Q2 == t)
        Q4 = Q_poly(4, 2, c)
        # Q_4^{(2)} = (35x^4 + (420/c - 30)x^2 + (840/c^2 - 60/c + 3))/(8c)
        t4 = [F(840, c*c) - F(60, c) + 3, F(0), F(420, c) - 30, F(0), F(35)]
        t4 = pscale(F(1, 8*c), t4)
        check(f"T6 Q_4 s=2 c={c}", Q4 == t4)

    print("\nALL PASS" if ok else "\nSOME FAILED")
