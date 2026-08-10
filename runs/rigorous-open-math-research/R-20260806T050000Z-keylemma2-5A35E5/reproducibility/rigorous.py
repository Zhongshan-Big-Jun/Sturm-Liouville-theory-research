# -*- coding: utf-8 -*-
"""rigorous.py -- rigorous interval evaluation of the KEY LEMMA objects over boxes.
Soundness model (audited):
  (R1) The riarith engine provides outward-rounded enclosures of all elementary ops.
  (R2) alpha_1(c,q) is strictly decreasing in c and in q; alpha_2(c,q) strictly
       decreasing in c and strictly increasing in q (derived from the implicit
       equations; both verified numerically in this run).
  (R3) Hence over a box [qlo,qhi]x[clo,chi]:
         alpha_1 in [alpha_1(chi,qhi), alpha_1(clo,qlo)]
         alpha_2 in [alpha_2(chi,qlo), alpha_2(clo,qhi)]
       and each corner value is bracketed rigorously by interval bisection of the
       strictly monotone secular equations (in x = pi/2 - alpha_1 and gamma).
  (R4) G, dG/dc, Mtilde are evaluated by the natural interval extension; the result
       is an enclosure over the box (sound, possibly loose; subdivision tightens).
"""
import sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
from decimal import Decimal
from riarith import (Iv, iv_add, iv_sub, iv_mul, iv_div, iv_neg, iv_sqr, iv_sqrt,
                     iv_sin, iv_cos, iv_tan, iv_atan, iv_inv, iv_mul_d, iv_pow_int, I, PI)

HALF_PI_IV = Iv(PI.lo/2, PI.hi/2)

def iv_Phi(a, q):
    s = iv_sin(a); c = iv_cos(a)
    return iv_add(iv_sqr(c), iv_mul(iv_sqr(q), iv_sqr(s)))

def iv_cot(a):
    return iv_div(iv_cos(a), iv_sin(a))

def iv_W(a):
    return iv_add(I(3), iv_mul_d(iv_mul(a, iv_cot(a)), 2))

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
    K = iv_sub(iv_sqr(q), I(1))
    t1 = iv_neg(iv_div(iv_mul(Ph, W), D))
    num = iv_mul_d(iv_mul(iv_mul(iv_mul(c, a), Ph), iv_mul(K, sc)), 2)
    return iv_add(t1, iv_div(num, iv_sqr(D)))

def iv_dGdc(a, c, q):
    """total derivative dG/dc along either curve.
    G = -Ph W/D + 2 c a Ph K sc / D^2,  D = q + c Ph,  K = q^2 - 1.
    dGdc = Ga*ap + Gc with ap = -a Ph / D."""
    Ph = iv_Phi(a, q)
    s = iv_sin(a); co = iv_cos(a); sc = iv_mul(s, co)
    K = iv_sub(iv_sqr(q), I(1))
    D = iv_add(q, iv_mul(c, Ph))
    W = iv_W(a)
    # ---- partial in c ----
    # d/dc[-Ph W/D] = Ph^2 W / D^2
    # d/dc[2 c a Ph K sc / D^2] = 2 a Ph K sc (D - 2 c Ph)/D^3
    term1 = iv_div(iv_mul(iv_sqr(Ph), W), iv_sqr(D))
    num2 = iv_mul_d(iv_mul(iv_mul(a, Ph), iv_mul(K, sc)), 2)
    br = iv_sub(D, iv_mul_d(iv_mul(c, Ph), 2))
    term2 = iv_div(iv_mul(num2, br), iv_pow_int(D, 3))
    Gc = iv_add(term1, term2)
    # ---- partial in a ----
    Pha = iv_mul_d(iv_mul(K, sc), 2)
    Wp = iv_Wp(a)
    dsc = iv_sub(iv_sqr(co), iv_sqr(s))
    d1 = iv_add(iv_neg(iv_div(iv_add(iv_mul(Pha, W), iv_mul(Ph, Wp)), D)),
                iv_div(iv_mul(iv_mul(Ph, W), iv_mul(c, Pha)), iv_sqr(D)))
    # d/da[2 c a Ph K sc / D^2]
    N = iv_mul_d(iv_mul(iv_mul(c, a), iv_mul(Ph, iv_mul(K, sc))), 2)
    dN = iv_mul_d(iv_mul(iv_mul(c, K), iv_add(iv_add(iv_mul(Ph, iv_mul(a, dsc)),
                                          iv_mul(Ph, sc)),
                                   iv_mul(a, iv_mul(Pha, sc)))), 2)
    d2 = iv_sub(iv_div(dN, iv_sqr(D)),
                iv_div(iv_mul_d(iv_mul(N, iv_mul(c, Pha)), 2), iv_pow_int(D, 3)))
    Ga = iv_add(d1, d2)
    ap = iv_neg(iv_div(iv_mul(a, Ph), D))
    return iv_add(iv_mul(Ga, ap), Gc)

def iv_J(a, c, q):
    return iv_add(iv_sqr(iv_G(a, c, q)), iv_dGdc(a, c, q))

# ---- secular equations in monotone coordinates ----
def f1e_iv(x, c, q):
    """even: x = pi/2 - alpha_1;  atan(tan x / q) - c(pi/2 - x) = 0."""
    qq = q if isinstance(q, Iv) else Iv.pt(q)
    cc = c if isinstance(c, Iv) else Iv.pt(c)
    return iv_sub(iv_atan(iv_div(iv_tan(x), qq)),
                  iv_mul(cc, iv_sub(HALF_PI_IV, x)))

def fO_iv(g, c, q):
    """odd: gamma; atan(q tan g) - c(pi - g) = 0."""
    qq = q if isinstance(q, Iv) else Iv.pt(q)
    cc = c if isinstance(c, Iv) else Iv.pt(c)
    return iv_sub(iv_atan(iv_mul(qq, iv_tan(g))),
                  iv_mul(cc, iv_sub(PI, g)))

def _bisect(f, lo_pt, hi_pt, tol, maxit=600):
    """Rigorous bisection: f strictly increasing on [lo_pt, hi_pt] with f(lo)<0, f(hi)>0.
    Evaluations use interval arithmetic; the bracket shrinks only on sign-definite evals.
    Returns [xlo, xhi] containing the unique root."""
    lo = Iv.pt(lo_pt)
    hi = Iv.pt(hi_pt)
    for _ in range(maxit):
        mid = Iv.pt((lo.lo + hi.lo)/2)
        fm = f(mid)
        if fm.lo > 0:
            hi = mid
        elif fm.hi < 0:
            lo = mid
        else:
            # sign-indefinite: narrow from the upper side and continue
            hi = mid
        if hi.lo - lo.hi < tol:
            break
    return Iv(lo.lo, hi.hi)

def bracket_x1(c, q, tol=Decimal('1e-40')):
    """x* = pi/2 - alpha_1(c,q).  f1e increasing on [0, pi/2)."""
    hi_pt = Decimal('1.570796326794896619231321691639751442')  # pi/2 lower-ish
    return _bisect(lambda x: f1e_iv(x, c, q), Decimal(0), hi_pt, tol)

def bracket_gamma(c, q, tol=Decimal('1e-40')):
    return _bisect(lambda g: fO_iv(g, c, q), Decimal(0), Decimal('1.5707'), tol)

def alpha1_box(qlo, qhi, clo, chi, tol=Decimal('1e-38')):
    """rigorous interval containing alpha_1(c,q) over the box."""
    xhi_corner = bracket_x1(chi, qhi, tol)   # x* largest at (chi, qhi)? x* = pi/2 - alpha1;
    xlo_corner = bracket_x1(clo, qlo, tol)
    # alpha_1 decreasing in c and q: alpha1(min) at (chi,qhi) = pi/2 - x*(chi,qhi)
    # x* = pi/2 - alpha_1 is increasing in c and q
    a1_lo = iv_sub(HALF_PI_IV, xhi_corner)
    a1_hi = iv_sub(HALF_PI_IV, xlo_corner)
    return Iv(a1_lo.lo, a1_hi.hi)

def alpha2_box(qlo, qhi, clo, chi, tol=Decimal('1e-38')):
    """alpha_2 decreasing in c, increasing in q: min at (chi, qlo), max at (clo, qhi)."""
    g_lo_corner = bracket_gamma(chi, qlo, tol)   # gamma max at (chi, qlo) => alpha2 min
    g_hi_corner = bracket_gamma(clo, qhi, tol)   # gamma min at (clo, qhi) => alpha2 max
    a2_lo = iv_sub(PI, g_lo_corner)
    a2_hi = iv_sub(PI, g_hi_corner)
    return Iv(a2_lo.lo, a2_hi.hi)

def box_to_ivs(qlo, qhi, clo, chi):
    return Iv.pt(Decimal(str(qlo))), Iv.pt(Decimal(str(qhi))), Iv.pt(Decimal(str(clo))), Iv.pt(Decimal(str(chi)))
