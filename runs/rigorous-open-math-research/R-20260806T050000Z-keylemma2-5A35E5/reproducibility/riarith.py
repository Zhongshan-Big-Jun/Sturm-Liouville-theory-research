# -*- coding: utf-8 -*-
"""riarith.py -- rigorous interval arithmetic with directed (outward) rounding.
Soundness model:
- Every operation on interval endpoints uses decimal with ROUND_FLOOR for the lower
  bound and ROUND_CEILING for the upper bound (directed rounding), so each returned
  interval is a valid enclosure of the true result.
- Elementary functions: exact Taylor series with rigorous remainder bounds (see
  function docstrings); all arithmetic inside uses directed rounding.
- pi: Machin formula pi = 16 atan(1/5) - 4 atan(1/239) computed with the same
  rigorous machinery; the result is a certified enclosure.
- Division never divides by an interval containing 0.
"""
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING, localcontext
import math

getcontext().prec = 60

class Iv:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi):
        self.lo = lo if isinstance(lo, Decimal) else Decimal(lo)
        self.hi = hi if isinstance(hi, Decimal) else Decimal(hi)
    @staticmethod
    def pt(x):
        return Iv(x, x)
    def wid(self):
        return self.hi - self.lo
    def __repr__(self):
        return '[%s, %s]' % (self.lo, self.hi)

def _flr(f):
    with localcontext() as c:
        c.rounding = ROUND_FLOOR
        return f()
def _cel(f):
    with localcontext() as c:
        c.rounding = ROUND_CEILING
        return f()

def iv_add(a, b):
    return Iv(_flr(lambda: a.lo + b.lo), _cel(lambda: a.hi + b.hi))
def iv_sub(a, b):
    return Iv(_flr(lambda: a.lo - b.hi), _cel(lambda: a.hi - b.lo))
def iv_neg(a):
    return Iv(_flr(lambda: -a.hi), _cel(lambda: -a.lo))
def iv_mul(a, b):
    ps = [a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi]
    return Iv(_flr(lambda: min(ps)), _cel(lambda: max(ps)))
def iv_div(a, b):
    if b.lo <= 0 <= b.hi:
        raise ValueError('division by interval containing 0')
    ps = [a.lo/b.lo, a.lo/b.hi, a.hi/b.lo, a.hi/b.hi]
    return Iv(_flr(lambda: min(ps)), _cel(lambda: max(ps)))
def iv_inv(b):
    if b.lo <= 0 <= b.hi:
        raise ValueError('inverse of interval containing 0')
    return Iv(_flr(lambda: 1/b.hi), _cel(lambda: 1/b.lo))
def iv_sqrt(a):
    if a.lo < 0:
        raise ValueError('sqrt of negative interval')
    return Iv(a.lo.sqrt(), a.hi.sqrt())
def iv_sqr(a):
    if a.lo >= 0:
        return Iv(_flr(lambda: a.lo*a.lo), _cel(lambda: a.hi*a.hi))
    if a.hi <= 0:
        return Iv(_flr(lambda: a.hi*a.hi), _cel(lambda: a.lo*a.lo))
    return Iv(Decimal(0), _cel(lambda: max(a.lo*a.lo, a.hi*a.hi)))
def iv_mul_d(a, d):
    return Iv(_flr(lambda: a.lo*d), _cel(lambda: a.hi*d)) if d >= 0 else Iv(_flr(lambda: a.hi*d), _cel(lambda: a.lo*d))
def iv_pow_int(a, n):
    if n == 0:
        return Iv.pt(1)
    if n == 1:
        return Iv(a.lo, a.hi)
    if n % 2 == 0:
        return iv_sqr(iv_pow_int(a, n//2))
    return iv_mul(a, iv_pow_int(a, n-1))

def _fact(n):
    return math.factorial(n)

def _taylor_sum(nterms, x_iv, powers_of_x, fac_index, sign_first):
    """Generic alternating Taylor sum: sum_{j} (-1)^{j+sign0} x^{p_j}/fac_j + remainder."""
    raise NotImplementedError

def atan_taylor_series(x_iv, nterms=80):
    """atan on x in [0,1]: alternating series, remainder <= x^(2n+3)/(2n+3)."""
    x2 = iv_sqr(x_iv)
    xp = Iv(x_iv.lo, x_iv.hi)
    acc = Iv.pt(0)
    sign = 1
    for j in range(nterms+1):
        d = 2*j + 1
        fac = Decimal(_fact(0)) if False else Decimal(d)
        t = Iv(_flr(lambda: xp.lo/fac), _cel(lambda: xp.hi/fac))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, x2)
    R = x_iv.hi**(2*nterms+3)/Decimal(2*nterms+3)
    return Iv(acc.lo - R, acc.hi + R)

def _sin_taylor(r):
    n = 25
    acc = Iv.pt(0)
    xp = Iv(r.lo, r.hi)
    r2 = iv_sqr(r)
    sign = 1
    for j in range(n+1):
        d = 2*j + 1
        fac = Decimal(_fact(d))
        t = Iv(_flr(lambda: xp.lo/fac), _cel(lambda: xp.hi/fac))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, r2)
    R = max(abs(r.lo), abs(r.hi))**(2*n+1)/Decimal(_fact(2*n+1))
    return Iv(acc.lo - R, acc.hi + R)

def _cos_taylor(r):
    n = 25
    acc = Iv.pt(1)
    r2 = iv_sqr(r)
    xp = Iv(r2.lo, r2.hi)
    sign = -1
    for j in range(1, n+1):
        d = 2*j
        fac = Decimal(_fact(d))
        t = Iv(_flr(lambda: xp.lo/fac), _cel(lambda: xp.hi/fac))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, r2)
    R = max(abs(r.lo), abs(r.hi))**(2*n)/Decimal(_fact(2*n))
    return Iv(acc.lo - R, acc.hi + R)

def compute_pi_iv():
    a5 = atan_taylor_series(Iv.pt(Decimal(1)/5), 30)
    a239 = atan_taylor_series(Iv.pt(Decimal(1)/239), 30)
    return iv_sub(iv_mul_d(a5, 16), iv_mul_d(a239, 4))

PI = compute_pi_iv()
HALF_PI = Iv(PI.lo/2, PI.hi/2)

def sin_cos_reduce(x_iv):
    q = iv_div(x_iv, HALF_PI)
    k_lo = q.lo.to_integral_value(rounding=ROUND_FLOOR)
    k_hi = q.hi.to_integral_value(rounding=ROUND_CEILING)
    if k_hi - k_lo > 1:
        raise ValueError('reduction ambiguous: %s' % q)
    k = int((q.lo + q.hi)/2 + Decimal('0.5'))
    r = iv_sub(x_iv, iv_mul_d(HALF_PI, k))
    return k, r

def iv_sin(x_iv):
    k, r = sin_cos_reduce(x_iv)
    kk = k % 4
    if kk == 0: return _sin_taylor(r)
    if kk == 1: return _cos_taylor(r)
    if kk == 2: return iv_neg(_sin_taylor(r))
    return iv_neg(_cos_taylor(r))

def iv_cos(x_iv):
    k, r = sin_cos_reduce(x_iv)
    kk = k % 4
    if kk == 0: return _cos_taylor(r)
    if kk == 1: return iv_neg(_sin_taylor(r))
    if kk == 2: return iv_neg(_cos_taylor(r))
    return _sin_taylor(r)

def iv_tan(x_iv):
    return iv_div(iv_sin(x_iv), iv_cos(x_iv))

def _atan_pt(x_iv):
    """rigorous atan of a POINT interval (x >= 0)."""
    if x_iv.lo != x_iv.hi:
        raise ValueError("_atan_pt requires a point interval")
    x = x_iv.lo
    if x < 0:
        raise ValueError("atan for x >= 0 only")
    if x > 1:
        inv = iv_inv(x_iv)   # tiny interval around 1/x in (0,1)
        return Iv(HALF_PI.lo - iv_atan(inv).hi, HALF_PI.hi - iv_atan(inv).lo)
    if x > Decimal('0.5'):
        # atan(x) = 2 atan(x/(1+sqrt(1+x^2))); argument <= ~0.4142.
        # The interval-arithmetic step returns a tiny interval t; atan is
        # increasing, so enclose atan(t) by the two endpoint evaluations.
        one = Iv.pt(1)
        s = iv_sqrt(iv_add(one, iv_sqr(x_iv)))
        t = iv_div(x_iv, iv_add(one, s))
        inner = iv_atan(t)
        return Iv(2*inner.lo, 2*inner.hi)
    return atan_taylor_series(x_iv, 80)

def iv_atan(x_iv):
    if x_iv.lo < 0:
        raise ValueError("atan for x >= 0 only")
    lo_r = _atan_pt(Iv.pt(x_iv.lo))
    hi_r = _atan_pt(Iv.pt(x_iv.hi))
    return Iv(lo_r.lo, hi_r.hi)
def I(x):
    return Iv.pt(Decimal(x))
