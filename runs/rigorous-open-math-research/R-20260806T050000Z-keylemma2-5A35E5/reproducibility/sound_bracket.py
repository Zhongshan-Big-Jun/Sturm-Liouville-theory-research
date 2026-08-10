# -*- coding: utf-8 -*-
"""sound_bracket.py -- sound bracketing of alpha1(c,q), alpha2(c,q) at points.
Monotone coordinates: x* = pi/2 - alpha1 solves f1e(x) = atan(tan x / q) -
c(pi/2 - x) = 0, strictly increasing in x.  gamma = pi - alpha2 solves
fO(g) = atan(q tan g) - c(pi - g) = 0, strictly increasing in g.
Bisection with interval evaluations; on a sign-indefinite evaluation the
precision is increased; if still indefinite the current bracket is returned
(the interval width is then below the working tolerance in practice).
"""
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import riarith as R

HALF_PI_IV = R.HALF_PI

def f1e_iv(x, c, q):
    qq = q if isinstance(q, R.Iv) else R.Iv.pt(q)
    cc = c if isinstance(c, R.Iv) else R.Iv.pt(c)
    return R.iv_sub(R.iv_atan(R.iv_div(R.iv_tan(x), qq)),
                    R.iv_mul(cc, R.iv_sub(HALF_PI_IV, x)))

def fO_iv(g, c, q):
    qq = q if isinstance(q, R.Iv) else R.Iv.pt(q)
    cc = c if isinstance(c, R.Iv) else R.Iv.pt(c)
    return R.iv_sub(R.iv_atan(R.iv_mul(qq, R.iv_tan(g))),
                    R.iv_mul(cc, R.iv_sub(R.PI, g)))

def bisect_iv(f, lo, hi, tol=Decimal('1e-38'), maxit=800, prec0=60):
    """f strictly increasing with f(lo)<0<f(hi).  Returns Iv(lo,hi) containing root."""
    lo = Decimal(lo); hi = Decimal(hi)
    prec = prec0
    for _ in range(maxit):
        mid = (lo + hi)/2
        with localcontext() as c:
            c.prec = prec
            fm = f(R.Iv.pt(mid))
        if fm.lo > 0:
            hi = mid
        elif fm.hi < 0:
            lo = mid
        else:
            prec *= 2
            if prec > 1000:
                return R.Iv(lo, hi)
            continue
        if hi - lo < tol:
            break
    return R.Iv(lo, hi)

def bracket_x1(c, q, tol=Decimal('1e-38')):
    return bisect_iv(lambda x: f1e_iv(x, c, q), Decimal(0), HALF_PI_IV.hi, tol)

def bracket_gamma(c, q, tol=Decimal('1e-38')):
    # gamma in (0, pi/3); use hi just below pi/2
    return bisect_iv(lambda g: fO_iv(g, c, q), Decimal(0), Decimal('1.57079632679489661923'), tol)

def alpha1_box(qlo, qhi, clo, chi, tol=Decimal('1e-36')):
    """alpha1 decreasing in c and in q: min at (chi, qhi), max at (clo, qlo)."""
    xhi = bracket_x1(chi, qhi, tol)   # x* = pi/2 - alpha1 increasing in c, q
    xlo = bracket_x1(clo, qlo, tol)
    a1lo = R.iv_sub(HALF_PI_IV, xhi)
    a1hi = R.iv_sub(HALF_PI_IV, xlo)
    return R.Iv(a1lo.lo, a1hi.hi)

def alpha2_box(qlo, qhi, clo, chi, tol=Decimal('1e-36')):
    """alpha2 decreasing in c, increasing in q: min at (chi, qlo), max at (clo, qhi)."""
    glo = bracket_gamma(chi, qlo, tol)   # gamma = pi - alpha2: max at (chi, qlo)
    ghi = bracket_gamma(clo, qhi, tol)   # gamma min at (clo, qhi)
    a2lo = R.iv_sub(R.PI, glo)
    a2hi = R.iv_sub(R.PI, ghi)
    return R.Iv(a2lo.lo, a2hi.hi)
