# audit_functions.py -- independent interval evaluations for the KEY LEMMA audit.
# Run: R-20260806T140000Z-keylemmaaudit-2F83B1
#
# Everything is re-derived from the primary definitions:
#   alpha_1, alpha_2: unique roots of the even/odd secular equations;
#   G, dG/dc (total along the curve), J, Mtilde, Hp = dG2/dc - dG1/dc,
#   Fpp = M1*J1 - M2*J2, dM2/dq, K (C4), IN, M2.
# The formulas for G, dGdc, M2, dM2dq, IN were symbolically verified against
# the definitions in audit_symbolic.py (diff = 0).
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-keylemmaaudit-2F83B1\reproducibility")
from audit_iv import (Iv, iv_add, iv_sub, iv_mul, iv_div, iv_neg, iv_sqr, iv_sqrt,
                      iv_sin, iv_cos, iv_tan, iv_cot, iv_atan, iv_inv, iv_mul_d,
                      iv_pow_int, PI, HALF_PI, _flr, _cel)
from decimal import Decimal

def iv_Phi(a, q):
    s = iv_sin(a); c = iv_cos(a)
    return iv_add(iv_sqr(c), iv_mul(iv_sqr(q), iv_sqr(s)))

def iv_W(a):
    return iv_add(Iv.pt(3), iv_mul_d(iv_mul(a, iv_cot(a)), 2))

def iv_Wp(a):
    s = iv_sin(a); c = iv_cos(a)
    return iv_mul_d(iv_div(iv_sub(iv_mul(s, c), a), iv_sqr(s)), 2)

def iv_Mtilde(a, c, q):
    s = iv_sin(a)
    num = iv_mul(iv_sqr(a), iv_sqr(s))
    D = iv_add(q, iv_mul(c, iv_Phi(a, q)))
    return iv_div(num, D)

def iv_G(a, c, q):
    Ph = iv_Phi(a, q); W = iv_W(a); D = iv_add(q, iv_mul(c, Ph))
    s = iv_sin(a); co = iv_cos(a); sc = iv_mul(s, co)
    K = iv_sub(iv_sqr(q), Iv.pt(1))
    t1 = iv_neg(iv_div(iv_mul(Ph, W), D))
    num = iv_mul_d(iv_mul(iv_mul(iv_mul(c, a), Ph), iv_mul(K, sc)), 2)
    return iv_add(t1, iv_div(num, iv_sqr(D)))

def iv_dGdc(a, c, q):
    """total derivative dG/dc along either curve (G_a * a'(c) + G_c)."""
    Ph = iv_Phi(a, q)
    s = iv_sin(a); co = iv_cos(a); sc = iv_mul(s, co)
    K = iv_sub(iv_sqr(q), Iv.pt(1))
    D = iv_add(q, iv_mul(c, Ph))
    W = iv_W(a)
    # Gc
    term1 = iv_div(iv_mul(iv_sqr(Ph), W), iv_sqr(D))
    num2 = iv_mul_d(iv_mul(iv_mul(a, Ph), iv_mul(K, sc)), 2)
    br = iv_sub(D, iv_mul_d(iv_mul(c, Ph), 2))
    term2 = iv_div(iv_mul(num2, br), iv_pow_int(D, 3))
    Gc = iv_add(term1, term2)
    # Ga
    Pha = iv_mul_d(iv_mul(K, sc), 2)
    Wp = iv_Wp(a)
    dsc = iv_sub(iv_sqr(co), iv_sqr(s))
    d1 = iv_add(iv_neg(iv_div(iv_add(iv_mul(Pha, W), iv_mul(Ph, Wp)), D)),
                iv_div(iv_mul(iv_mul(Ph, W), iv_mul(c, Pha)), iv_sqr(D)))
    N = iv_mul_d(iv_mul(iv_mul(c, a), iv_mul(Ph, iv_mul(K, sc))), 2)
    dN = iv_mul_d(iv_mul(iv_mul(c, K),
                         iv_add(iv_add(iv_mul(Ph, iv_mul(a, dsc)), iv_mul(Ph, sc)),
                                iv_mul(a, iv_mul(Pha, sc)))), 2)
    d2 = iv_sub(iv_div(dN, iv_sqr(D)),
                iv_div(iv_mul_d(iv_mul(N, iv_mul(c, Pha)), 2), iv_pow_int(D, 3)))
    Ga = iv_add(d1, d2)
    ap = iv_neg(iv_div(iv_mul(a, Ph), D))
    return iv_add(iv_mul(Ga, ap), Gc)

def iv_J(a, c, q):
    return iv_add(iv_sqr(iv_G(a, c, q)), iv_dGdc(a, c, q))

# ---------------- secular equations in monotone coordinates ----------------
def f1e_iv(x, c, q):
    qq = q if isinstance(q, Iv) else Iv.pt(q)
    cc = c if isinstance(c, Iv) else Iv.pt(c)
    return iv_sub(iv_atan(iv_div(iv_tan(x), qq)), iv_mul(cc, iv_sub(HALF_PI, x)))

def fO_iv(g, c, q):
    qq = q if isinstance(q, Iv) else Iv.pt(q)
    cc = c if isinstance(c, Iv) else Iv.pt(c)
    return iv_sub(iv_atan(iv_mul(qq, iv_tan(g))), iv_mul(cc, iv_sub(PI, g)))

def _bisect_sound(f, f_float, lo_pt, hi_pt, tol):
    """Sound bracketing of the unique root of the strictly increasing f.

    Two-phase: (1) fast float bisection (mpmath, 90 digits, f_float) locates the
    root to ~1e-70; (2) the bracket is inflated and certified by sign-definite
    INTERVAL evaluations f(lo).hi < 0 < f(hi).lo.  The interval phase is the
    certificate: strictly monotone continuous f with a rigorous sign change on
    [lo, hi] forces the root into (lo, hi).  The float phase is only a fast root
    locator; nothing is claimed from it."""
    import mpmath as mp
    mp.mp.dps = 90
    lo = mp.mpf(str(lo_pt)); hi = mp.mpf(str(hi_pt))
    for _ in range(400):
        mid = (lo + hi) / 2
        if f_float(mid) > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < mp.mpf('1e-70'):
            break
    infl = mp.mpf('1e-40')
    for _ in range(60):
        clo = lo - infl
        chi = hi + infl
        f_lo = f(Iv.pt(clo)); f_hi = f(Iv.pt(chi))
        if f_lo.hi < 0 and f_hi.lo > 0:
            return Iv(clo, chi)
        infl *= 10
    raise ValueError('could not certify bracket: f(lo)=%s f(hi)=%s' % (f_lo, f_hi))

def bracket_x1(c, q, tol=Decimal('1e-38')):
    import mpmath as mp
    mp.mp.dps = 90
    cv, qv = mp.mpf(str(c)), mp.mpf(str(q))
    def f1e_float(x):
        return mp.atan(mp.tan(x)/qv) - cv*(mp.pi/2 - x)
    return _bisect_sound(lambda x: f1e_iv(x, c, q), f1e_float,
                         Decimal(0), Decimal('1.57079632679489661923'), tol)

def bracket_gamma(c, q, tol=Decimal('1e-38')):
    import mpmath as mp
    mp.mp.dps = 90
    cv, qv = mp.mpf(str(c)), mp.mpf(str(q))
    def fO_float(g):
        return mp.atan(qv*mp.tan(g)) - cv*(mp.pi - g)
    return _bisect_sound(lambda g: fO_iv(g, c, q), fO_float,
                         Decimal(0), Decimal('1.5707'), tol)

def alpha1_box(qlo, qhi, clo, chi, tol=Decimal('1e-36')):
    """alpha_1 strictly decreasing in c and in q:
       min at (chi, qhi), max at (clo, qlo).  x* = pi/2 - alpha_1."""
    xhi = bracket_x1(chi, qhi, tol)
    xlo = bracket_x1(clo, qlo, tol)
    a1lo = iv_sub(HALF_PI, Iv(xhi.hi, xhi.hi)).lo
    a1hi = iv_sub(HALF_PI, Iv(xlo.lo, xlo.lo)).hi
    # widen by the interval arithmetic of the subtraction:
    A1 = iv_sub(HALF_PI, Iv(xhi.lo, xhi.hi))
    A2 = iv_sub(HALF_PI, Iv(xlo.lo, xlo.hi))
    return Iv(A1.lo, A2.hi)

def alpha2_box(qlo, qhi, clo, chi, tol=Decimal('1e-36')):
    """alpha_2 strictly decreasing in c, strictly increasing in q:
       min at (chi, qlo), max at (clo, qhi).  gamma = pi - alpha_2."""
    glo = bracket_gamma(chi, qlo, tol)
    ghi = bracket_gamma(clo, qhi, tol)
    A1 = iv_sub(PI, Iv(glo.lo, glo.hi))
    A2 = iv_sub(PI, Iv(ghi.lo, ghi.hi))
    return Iv(A1.lo, A2.hi)

# ---------------- composite quantities ----------------
def iv_Hp_box(qlo, qhi, clo, chi, tol=Decimal('1e-34')):
    a1b = alpha1_box(qlo, qhi, clo, chi, tol)
    a2b = alpha2_box(qlo, qhi, clo, chi, tol)
    c = Iv(clo, chi); q = Iv(qlo, qhi)
    return iv_sub(iv_dGdc(a2b, c, q), iv_dGdc(a1b, c, q))

def iv_Fpp_box(qlo, qhi, clo, chi, tol=Decimal('1e-34')):
    a1b = alpha1_box(qlo, qhi, clo, chi, tol)
    a2b = alpha2_box(qlo, qhi, clo, chi, tol)
    c = Iv(clo, chi); q = Iv(qlo, qhi)
    M1 = iv_Mtilde(a1b, c, q); M2 = iv_Mtilde(a2b, c, q)
    J1 = iv_J(a1b, c, q); J2 = iv_J(a2b, c, q)
    return iv_sub(iv_mul(M1, J1), iv_mul(M2, J2))

def iv_dM2dq(qlo, qhi, ulo, uhi):
    q = Iv(qlo, qhi); u = Iv(ulo, uhi)
    A = iv_sub(PI, iv_atan(iv_div(u, q)))
    t = iv_atan(u)
    S = iv_add(iv_sqr(q), iv_sqr(u))
    q2 = iv_sqr(q); u2 = iv_sqr(u)
    one = Iv.pt(1)
    term1 = iv_mul(iv_mul(Iv.pt(4), iv_sqr(A)), u)
    term2 = iv_div(iv_mul(Iv.pt(8), iv_mul(A, iv_mul(u2, q))), S)
    term3 = iv_div(iv_mul(Iv.pt(-7), iv_mul(q2, u)), S)
    term4 = iv_mul(Iv.pt(-14), iv_mul(A, q))
    term5 = iv_div(iv_mul(Iv.pt(-9), iv_mul(u2, u)), S)
    term6 = iv_div(iv_mul(Iv.pt(2), u), iv_add(one, u2))
    term7 = iv_div(iv_mul(Iv.pt(4), iv_mul(A, q)), iv_add(one, u2))
    br = iv_sub(iv_sub(iv_div(iv_mul(Iv.pt(4), u2), S), Iv.pt(5)), iv_mul(Iv.pt(9), u2))
    acc = iv_add(term1, term2); acc = iv_add(acc, term3); acc = iv_add(acc, term4)
    acc = iv_add(acc, term5); acc = iv_add(acc, term6); acc = iv_add(acc, term7)
    return iv_add(acc, iv_mul(t, br))

def iv_K(v):
    u = iv_tan(v)
    w = iv_sub(PI, iv_mul(Iv.pt(Decimal('2.5')), v))
    q = iv_div(iv_mul(iv_sin(v), iv_cos(w)), iv_mul(iv_cos(v), iv_sin(w)))
    q2 = iv_sqr(q); u2 = iv_sqr(u)
    P = iv_add(iv_add(iv_mul(iv_mul(Iv.pt(5), v), q), iv_mul(Iv.pt(-3), u)),
               iv_mul(Iv.pt(2), v))
    t1 = iv_mul(iv_add(q2, u2), P)
    t2 = iv_mul(iv_mul(iv_mul(Iv.pt(Decimal('1.2')), u), q), iv_add(Iv.pt(1), u2))
    return iv_sub(t1, t2)

def iv_IN(q, u):
    A = iv_sub(PI, iv_atan(iv_div(u, q)))
    t = iv_atan(u)
    q2 = iv_sqr(q); u2 = iv_sqr(u)
    return iv_sub(iv_mul(iv_mul(iv_add(q2, u2), A),
                         iv_add(iv_add(iv_mul_d(iv_mul(A, q), 2), iv_mul(Iv.pt(-3), u)),
                                iv_mul(Iv.pt(2), t))),
                  iv_mul_d(iv_mul(iv_mul(iv_mul(t, u), q), iv_add(Iv.pt(1), u2)), 3))

def iv_M2(q, u):
    A = iv_sub(PI, iv_atan(iv_div(u, q)))
    t = iv_atan(u)
    q2 = iv_sqr(q); u2 = iv_sqr(u)
    term1 = iv_mul_d(iv_mul(iv_mul(iv_sqr(A), u), q), 4)
    term2 = iv_mul(Iv.pt(-7), iv_mul(A, q2))
    term3 = iv_mul(Iv.pt(-9), iv_mul(A, u2))
    term4 = iv_mul_d(iv_mul(A, iv_div(iv_add(q2, u2), iv_add(Iv.pt(1), u2))), 2)
    br = iv_sub(iv_sub(iv_mul_d(iv_mul(A, u), 4), iv_mul(Iv.pt(5), q)), iv_mul(Iv.pt(9), iv_mul(q, u2)))
    return iv_add(iv_add(iv_add(iv_add(term1, term2), term3), term4), iv_mul(t, br))

if __name__ == '__main__':
    import mpmath as mp
    mp.mp.dps = 60
    # point sanity: alpha bracketing at points contains the true root
    ok = True
    for (c, q) in [('0.4','1.0'), ('0.5','2.0'), ('0.45','1.5'), ('0.1','5.0'), ('0.49','1.01')]:
        cv, qv = mp.mpf(c), mp.mpf(q)
        a1 = alpha1_box(Decimal(q), Decimal(q), Decimal(c), Decimal(c))
        a2 = alpha2_box(Decimal(q), Decimal(q), Decimal(c), Decimal(c))
        # true roots by high precision bisection on the gamma/x coordinates
        def f1(x): return mp.atan(mp.tan(x)/qv) - cv*(mp.pi/2 - x)
        def fO(g): return mp.atan(qv*mp.tan(g)) - cv*(mp.pi - g)
        xr = mp.findroot(f1, (mp.mpf('1e-10'), mp.mpf('1.5707')), tol=1e-50)
        gr = mp.findroot(fO, (mp.mpf('1e-10'), mp.mpf('1.5707')), tol=1e-50)
        a1t = mp.pi/2 - xr
        a2t = mp.pi - gr
        if not (mp.mpf(str(a1.lo)) <= a1t <= mp.mpf(str(a1.hi))):
            ok = False; print('a1 FAIL', c, q, a1, mp.nstr(a1t, 30))
        if not (mp.mpf(str(a2.lo)) <= a2t <= mp.mpf(str(a2.hi))):
            ok = False; print('a2 FAIL', c, q, a2, mp.nstr(a2t, 30))
    print('alpha bracketing point sanity ok:', ok)
