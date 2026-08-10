# -*- coding: utf-8 -*-
# audit_iv.py -- independent Decimal interval engine with directed rounding.  (fixed v3)
# Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit of KEY LEMMA certificates)
#
# Soundness model:
#  * Every arithmetic operation uses ROUND_FLOOR for the lower endpoint and
#    ROUND_CEILING for the upper endpoint, with ALL inner arithmetic inside the
#    directed context (a bug in v1 computed products in the ambient 28-digit
#    context, which is unsound and was caught by the sanity harness).
#  * sqrt: directed rounding via Decimal.sqrt with the context rounding set
#    explicitly (Decimal.sqrt ignores the rounding mode in Python 3.10; v2
#    implemented _sqrt_directed with PREC+20 correct rounding + outward 1-ulp
#    inflation, validated on 3000 random cases).
#  * pi: Machin pi = 16*atan(1/5) - 4*atan(1/239) with own rigorous atan.
#  * atan: alternating Taylor series with explicit remainder on [0,1], halving
#    formula for (0.5,1], reduction atan(x)=pi/2-atan(1/x) for x>1.  atan is
#    strictly increasing, so the interval value is the endpoint range.
#  * sin/cos: exact monotone-range computation over the interval (v3): the
#    interval is reduced modulo 2*pi and the exact range is obtained from the
#    point values at the endpoints plus the critical points pi/2, pi, 3pi/2
#    (with sound membership tests against certified intervals for those
#    constants).  The previous Taylor-over-the-whole-interval version suffered
#    from dependency blow-up on wide intervals (width 10x the true range), which
#    made the L4box/L5box leaf re-evaluations useless.
from decimal import Decimal, getcontext, localcontext, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN

PREC = 80

class Iv:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        self.lo = lo if isinstance(lo, Decimal) else Decimal(str(lo))
        self.hi = hi if isinstance(hi, Decimal) else Decimal(str(hi))
    @staticmethod
    def pt(x):
        return Iv(x, x)
    def __repr__(self):
        return '[%s, %s]' % (self.lo, self.hi)

def _flr(f):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_FLOOR
        return f()
def _cel(f):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_CEILING
        return f()

def iv_add(a, b):
    return Iv(_flr(lambda: a.lo + b.lo), _cel(lambda: a.hi + b.hi))
def iv_sub(a, b):
    return Iv(_flr(lambda: a.lo - b.hi), _cel(lambda: a.hi - b.lo))
def iv_neg(a):
    return Iv(_flr(lambda: -a.hi), _cel(lambda: -a.lo))
def iv_mul(a, b):
    p1 = _flr(lambda: a.lo*b.lo); p2 = _flr(lambda: a.lo*b.hi)
    p3 = _flr(lambda: a.hi*b.lo); p4 = _flr(lambda: a.hi*b.hi)
    lo = min(p1, p2, p3, p4)
    q1 = _cel(lambda: a.lo*b.lo); q2 = _cel(lambda: a.lo*b.hi)
    q3 = _cel(lambda: a.hi*b.lo); q4 = _cel(lambda: a.hi*b.hi)
    hi = max(q1, q2, q3, q4)
    return Iv(lo, hi)
def iv_div(a, b):
    if b.lo <= 0 <= b.hi:
        raise ValueError('division by interval containing 0: %s' % b)
    p1 = _flr(lambda: a.lo/b.lo); p2 = _flr(lambda: a.lo/b.hi)
    p3 = _flr(lambda: a.hi/b.lo); p4 = _flr(lambda: a.hi/b.hi)
    lo = min(p1, p2, p3, p4)
    q1 = _cel(lambda: a.lo/b.lo); q2 = _cel(lambda: a.lo/b.hi)
    q3 = _cel(lambda: a.hi/b.lo); q4 = _cel(lambda: a.hi/b.hi)
    hi = max(q1, q2, q3, q4)
    return Iv(lo, hi)
def iv_inv(b):
    if b.lo <= 0 <= b.hi:
        raise ValueError('inverse of interval containing 0')
    return Iv(_flr(lambda: 1/b.hi), _cel(lambda: 1/b.lo))
def _sqrt_directed(x):
    """Directed P-digit sqrt of a nonnegative Decimal x.
    Decimal.sqrt ignores the context rounding mode (Python 3.10 behavior: it
    always rounds to nearest).  Compute s at PREC+20 digits (correctly rounded),
    then round outward with directed rounding plus a 1-ulp inflation.
    |s - sqrt(x)| < 0.5*ulp_{PREC+20} << ulp_P, so the inflation is sound.
    Validated on 3000 random x in [1e-300, 1e300] plus special cases."""
    if x == 0:
        return Decimal(0)
    with localcontext() as ctx:
        ctx.prec = PREC + 20
        ctx.rounding = ROUND_HALF_EVEN
        s = x.sqrt()
    e = s.adjusted()
    shift = PREC - 1 - e
    p10_shift = Decimal(10) ** shift
    with localcontext() as ctx:
        ctx.prec = PREC + 30
        ctx.rounding = ROUND_FLOOR
        lo_i = (s * p10_shift).to_integral_value(rounding=ROUND_FLOOR)
        lo = (lo_i - 1) * (Decimal(10) ** (e - PREC + 1))
        ctx.rounding = ROUND_CEILING
        hi_i = (s * p10_shift).to_integral_value(rounding=ROUND_CEILING)
        hi = (hi_i + 1) * (Decimal(10) ** (e - PREC + 1))
    return lo, hi

def iv_sqrt(a):
    if a.lo < 0:
        raise ValueError('sqrt of negative interval')
    lo = _sqrt_directed(a.lo)[0]
    hi = _sqrt_directed(a.hi)[1]
    return Iv(lo, hi)
def iv_sqr(a):
    if a.lo >= 0:
        return Iv(_flr(lambda: a.lo*a.lo), _cel(lambda: a.hi*a.hi))
    if a.hi <= 0:
        return Iv(_flr(lambda: a.hi*a.hi), _cel(lambda: a.lo*a.lo))
    return Iv(Decimal(0), _cel(lambda: max(a.lo*a.lo, a.hi*a.hi)))
def iv_mul_d(a, d):
    d = Decimal(d)
    if d >= 0:
        return Iv(_flr(lambda: a.lo*d), _cel(lambda: a.hi*d))
    return Iv(_flr(lambda: a.hi*d), _cel(lambda: a.lo*d))
def iv_pow_int(a, n):
    if n == 0:
        return Iv.pt(1)
    if n == 1:
        return Iv(a.lo, a.hi)
    if n % 2 == 0:
        return iv_sqr(iv_pow_int(a, n//2))
    return iv_mul(a, iv_pow_int(a, n-1))

def _fact(n):
    import math
    return math.factorial(n)

def _atan_series(x, n):
    """atan(x) for x in [0,1], alternating series with explicit remainder."""
    x2 = iv_sqr(x)
    xp = Iv(x.lo, x.hi)
    acc = Iv.pt(0)
    sign = 1
    for j in range(n+1):
        d = 2*j+1
        t = Iv(_flr(lambda: xp.lo/Decimal(d)), _cel(lambda: xp.hi/Decimal(d)))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, x2)
    r = max(abs(x.lo), abs(x.hi))
    r_pow = Iv(_flr(lambda: r**(2*n+3)), _cel(lambda: r**(2*n+3)))
    R = Iv(_flr(lambda: r_pow.lo/Decimal(2*n+3)), _cel(lambda: r_pow.hi/Decimal(2*n+3)))
    return Iv(_flr(lambda: acc.lo - R.hi), _cel(lambda: acc.hi + R.hi))

def _atan_pt(x):
    """atan of a point x >= 0."""
    if x < 0:
        raise ValueError('atan for x >= 0 only')
    if x > 1:
        inv = iv_inv(Iv.pt(x))
        inner = _atan_pt(inv.lo)
        inner2 = _atan_pt(inv.hi)
        return Iv(_flr(lambda: HALF_PI.lo - inner2.hi), _cel(lambda: HALF_PI.hi - inner.lo))
    if x > Decimal('0.5'):
        one = Iv.pt(1)
        s = iv_sqrt(iv_add(one, iv_sqr(Iv.pt(x))))
        t = iv_div(Iv.pt(x), iv_add(one, s))
        inner_lo = _atan_pt(t.lo)
        inner_hi = _atan_pt(t.hi)
        return Iv(_flr(lambda: 2*inner_lo.lo), _cel(lambda: 2*inner_hi.hi))
    return _atan_series(Iv.pt(x), 90)

def iv_atan(x):
    if x.lo < 0:
        raise ValueError('atan for x >= 0 only')
    lo_r = _atan_pt(x.lo)
    hi_r = _atan_pt(x.hi)
    return Iv(lo_r.lo, hi_r.hi)

def compute_pi():
    a5 = _atan_series(Iv.pt(_flr(lambda: Decimal(1)/Decimal(5))), 120)
    a239 = _atan_series(Iv.pt(_flr(lambda: Decimal(1)/Decimal(239))), 120)
    return iv_sub(iv_mul_d(a5, 16), iv_mul_d(a239, 4))

PI = compute_pi()
HALF_PI = Iv(_flr(lambda: PI.lo/2), _cel(lambda: PI.hi/2))
TWO_PI = Iv(_flr(lambda: 2*PI.lo), _cel(lambda: 2*PI.hi))
THREE_HALF_PI = Iv(_flr(lambda: Decimal('1.5')*PI.lo), _cel(lambda: Decimal('1.5')*PI.hi))

def _sin_cos_taylor(r):
    n = 55
    r2 = iv_sqr(r)
    acc = Iv.pt(0); xp = Iv(r.lo, r.hi); sign = 1
    for j in range(n+1):
        d = 2*j+1
        fac = Decimal(_fact(d))
        t = Iv(_flr(lambda: xp.lo/fac), _cel(lambda: xp.hi/fac))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, r2)
    Rm = max(abs(r.lo), abs(r.hi))
    Rpow = Iv(_flr(lambda: Rm**(2*n+3)), _cel(lambda: Rm**(2*n+3)))
    R = Iv(_flr(lambda: Rpow.lo/Decimal(_fact(2*n+3))), _cel(lambda: Rpow.hi/Decimal(_fact(2*n+3))))
    s_iv = Iv(_flr(lambda: acc.lo - R.hi), _cel(lambda: acc.hi + R.hi))
    acc = Iv.pt(1); xp = Iv(r2.lo, r2.hi); sign = -1
    for j in range(1, n+1):
        d = 2*j
        fac = Decimal(_fact(d))
        t = Iv(_flr(lambda: xp.lo/fac), _cel(lambda: xp.hi/fac))
        acc = iv_add(acc, t) if sign > 0 else iv_sub(acc, t)
        sign *= -1
        xp = iv_mul(xp, r2)
    Rpow = Iv(_flr(lambda: Rm**(2*n+2)), _cel(lambda: Rm**(2*n+2)))
    R = Iv(_flr(lambda: Rpow.lo/Decimal(_fact(2*n+2))), _cel(lambda: Rpow.hi/Decimal(_fact(2*n+2))))
    c_iv = Iv(_flr(lambda: acc.lo - R.hi), _cel(lambda: acc.hi + R.hi))
    return s_iv, c_iv

def _sin_cos_pt(t):
    """sin(t), cos(t) of a point t (>= 0) with outward rounding.
    Reduction mod 2pi: all uses in this audit have 0 <= t <= pi, but the
    general reduction is kept for safety."""
    if t > TWO_PI.hi:
        # reduce: find k with t - k*2pi in [0, 2pi]
        k = int((t / TWO_PI.lo).to_integral_value(rounding=ROUND_FLOOR))
        # sound: t/2pi < t/TWO_PI.lo, so k = floor(t/2pi) <= floor(t/TWO_PI.lo)
        tt = Iv(_flr(lambda: t - k*TWO_PI.hi), _cel(lambda: t - k*TWO_PI.lo))
    else:
        tt = Iv.pt(t)
    return _sin_cos_taylor(tt)

def _range_sin_cos(lo, hi):
    """Exact range of (sin, cos) over [lo, hi] subset of [0, 2*pi], width < 2*pi.
    Uses the critical points pi/2 (sin max 1), 3pi/2 (sin min -1),
    pi (cos min -1), 0 and 2pi (cos max 1).  Membership is decided with
    certified intervals: if hi < HALF_PI.lo then pi/2 > hi etc.; in ambiguous
    cases the extremal value is included (safe over-approximation)."""
    sl, sh = _sin_cos_pt(lo), _sin_cos_pt(hi)
    # sin
    sin_lo = min(sl[0].lo, sh[0].lo); sin_hi = max(sl[0].hi, sh[0].hi)
    if not (hi < HALF_PI.lo or lo > HALF_PI.hi):
        sin_hi = Decimal(1)
    if not (hi < THREE_HALF_PI.lo or lo > THREE_HALF_PI.hi):
        sin_lo = Decimal(-1)
    # cos: decreasing on [0, pi], increasing on [pi, 2pi]
    cos_lo = min(sl[1].lo, sh[1].lo); cos_hi = max(sl[1].hi, sh[1].hi)
    if not (hi < PI.lo or lo > PI.hi):
        cos_lo = Decimal(-1)
    if lo == 0 or hi == 0 or (lo <= TWO_PI.lo <= hi) or (lo <= TWO_PI.hi <= hi):
        cos_hi = Decimal(1)
    # (2*pi membership is tested only against the certified interval; if 2*pi
    #  lies inside [lo, hi] in the ambiguous band, including +1 is safe.)
    if hi >= TWO_PI.lo and lo <= TWO_PI.hi:
        # possibly contains 2pi -> max 1 possible; but only when the interval
        # actually reaches 2pi.  Safe to include.
        if hi >= TWO_PI.lo:
            cos_hi = Decimal(1)
    return Iv(sin_lo, sin_hi), Iv(cos_lo, cos_hi)

def _reduce_sincos(x):
    """Reduce x (>= 0) to a subset of [0, 2pi] modulo 2pi, or None if the
    interval spans a full period."""
    if x.lo < 0:
        raise ValueError('sin/cos for x >= 0 only in this engine')
    if x.hi - x.lo >= TWO_PI.hi:
        return None
    q = iv_div(x, TWO_PI)
    k_lo = q.lo.to_integral_value(rounding=ROUND_FLOOR)
    k_hi = q.hi.to_integral_value(rounding=ROUND_CEILING)
    if k_hi - k_lo > 1:
        return None
    k = k_lo
    r = iv_sub(x, iv_mul_d(TWO_PI, k))
    return r

def iv_sin(x):
    r = _reduce_sincos(x)
    if r is None:
        return Iv(Decimal(-1), Decimal(1))
    lo, hi = r.lo, r.hi
    if lo < 0 or hi > TWO_PI.hi:
        # wrapped interval: split at the 2pi boundary
        s1, _ = _range_sin_cos(Decimal(0), hi)
        s2, _ = _range_sin_cos(lo, TWO_PI.hi)
        return Iv(min(s1.lo, s2.lo), max(s1.hi, s2.hi))
    s, _ = _range_sin_cos(lo, hi)
    return s

def iv_cos(x):
    r = _reduce_sincos(x)
    if r is None:
        return Iv(Decimal(-1), Decimal(1))
    lo, hi = r.lo, r.hi
    if lo < 0 or hi > TWO_PI.hi:
        c1, _ = _range_sin_cos(Decimal(0), hi)
        c2, _ = _range_sin_cos(lo, TWO_PI.hi)
        return Iv(min(c1.lo, c2.lo), max(c1.hi, c2.hi))
    _, c = _range_sin_cos(lo, hi)
    return c

def iv_tan(x):
    s = iv_sin(x); c = iv_cos(x)
    if c.lo <= 0 <= c.hi:
        raise ValueError('tan: cos interval contains 0: %s' % c)
    return iv_div(s, c)
def iv_cot(x):
    s = iv_sin(x); c = iv_cos(x)
    if s.lo <= 0 <= s.hi:
        raise ValueError('cot: sin interval contains 0: %s' % s)
    return iv_div(c, s)

if __name__ == '__main__':
    import mpmath as mp
    mp.mp.dps = 120
    ok = True
    for t in ['0', '0.1', '0.49', '0.5', '0.7', '0.999', '1', '1.5', '2', '3.06', '3.08', '6.4', '1000']:
        tv = mp.mpf(t)
        for f_iv, f_mp, name in [(iv_atan, mp.atan, 'atan'), (iv_sin, mp.sin, 'sin'), (iv_cos, mp.cos, 'cos')]:
            r = f_iv(Iv.pt(t))
            exact = f_mp(tv)
            if not (mp.mpf(str(r.lo)) <= exact <= mp.mpf(str(r.hi))):
                ok = False
                print('FAIL', name, t, mp.nstr(mp.mpf(str(r.lo)),30), mp.nstr(mp.mpf(str(r.hi)),30), mp.nstr(exact,35))
    # interval sanity: monotone functions evaluated over [a,b]
    for (a, b) in [('0.2', '0.5'), ('1', '3'), ('0', '10'), ('0.5', '6.5'), ('2.39', '2.43')]:
        for f_iv, f_mp, name in [(iv_atan, mp.atan, 'atan'), (iv_sin, mp.sin, 'sin'), (iv_cos, mp.cos, 'cos')]:
            r = f_iv(Iv(a, b))
            # exact range over [a,b] by dense sampling
            xs = [mp.mpf(a) + (mp.mpf(b)-mp.mpf(a))*mp.mpf(i)/mp.mpf(20000) for i in range(20001)]
            vals = [f_mp(x) for x in xs]
            e0, e1 = min(vals), max(vals)
            if not (mp.mpf(str(r.lo)) <= e0 and mp.mpf(str(r.hi)) >= e1):
                ok = False
                print('INTERVAL FAIL', name, (a,b), mp.nstr(mp.mpf(str(r.lo)),30), mp.nstr(mp.mpf(str(r.hi)),30), mp.nstr(e0,20), mp.nstr(e1,20))
    # wide-interval width quality: sin over [2.39, 2.43] must be much narrower than the old Taylor result
    r = iv_sin(Iv('2.3919630965733993919703900258', '2.4275405688916751400460331944'))
    print('sin([2.392,2.4275]) =', r, 'width =', float(r.hi - r.lo))
    print('PI contains true pi:', mp.mpf(str(PI.lo)) <= mp.pi <= mp.mpf(str(PI.hi)))
    print('PI width:', float(PI.hi - PI.lo))
    # Note: the raw Decimal.sqrt rounding-mode check is intentionally NOT part
    # of the harness (Python 3.10 Decimal.sqrt ignores the rounding mode; the
    # engine's _sqrt_directed works around it and was validated separately on
    # 3000 random cases in dbg_iv2.py).
    print('ALL SANITY OK' if ok else 'SANITY FAILED')
