"""Unmodified function excerpts from current misc/rigid1d.py and misc/e1_certgen.py.
Not a complete-file restoration. Imports and a minimal D/D2 initializer are added
only to support evaluation of scalar interval and constant-callback examples.
"""
from fractions import Fraction as F
import math
class D: pass
class D2:
    def __init__(self,v,d1=None,d2=None):
        self.v=v if isinstance(v,I) else I(v)
        self.d1=I(0) if d1 is None else (d1 if isinstance(d1,I) else I(d1))
        self.d2=I(0) if d2 is None else (d2 if isinstance(d2,I) else I(d2))
def _asF(x): return x if isinstance(x, F) else F(x)
class I:
    __slots__ = ('lo','hi')
    def __init__(self, lo, hi=None):
        if isinstance(lo, I): lo, hi = lo.lo, lo.hi
        if hi is None: hi = lo
        lo, hi = _asF(lo), _asF(hi)
        if lo > hi: lo, hi = hi, lo
        self.lo, self.hi = lo, hi
    def __repr__(self): return '[%s, %s]' % (self.lo, self.hi)
    def __add__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        o = o if isinstance(o, I) else I(o); return I(self.lo+o.lo, self.hi+o.hi)
    def __radd__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        return self + o
    def __sub__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        o = o if isinstance(o, I) else I(o); return I(self.lo-o.hi, self.hi-o.lo)
    def __rsub__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        return I(o) - self
    def __mul__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        a,b,c,d = self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi
        return I(min(a,b,c,d), max(a,b,c,d))
    def __rmul__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        return self * o
    def __truediv__(self, o):
        if isinstance(o, (D, D2)): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        if o.lo <= 0 <= o.hi: raise ZeroDivisionError('div by interval containing 0')
        a,b,c,d = self.lo/o.lo, self.lo/o.hi, self.hi/o.lo, self.hi/o.hi
        return I(min(a,b,c,d), max(a,b,c,d))
    def __neg__(self): return I(-self.hi, -self.lo)
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return I(1)
        if n == 1: return self
        if self.lo >= 0: return I(self.lo**n, self.hi**n)
        if self.hi <= 0:
            if n % 2 == 0: return I((-self.hi)**n, (-self.lo)**n)
            return I(self.lo**n, self.hi**n)
        return I(0, max(self.lo**n, self.hi**n)) if n%2==0 else I(self.lo**n, self.hi**n)
    def contains_zero(self): return self.lo <= 0 <= self.hi
    def is_pos(self): return self.lo > 0
    def is_neg(self): return self.hi < 0
    def width(self): return self.hi - self.lo
    def abs(self): return self if self.lo >= 0 else (-self if self.hi <= 0 else I(0, max(-self.lo, self.hi)))
    def sqrt(self):
        assert self.lo >= 0
        l = F(math.isqrt(self.lo.numerator*self.lo.denominator), self.lo.denominator)
        h = F(math.isqrt(self.hi.numerator*self.hi.denominator) + 1, self.hi.denominator)
        return I(l, h)
NS = 12

def _sc_series(c):
    s = F(0); sign = 1; p = c; fact = F(1)
    for k in range(NS):
        s = s + sign * p / fact
        sign = -sign
        p = p * c * c
        fact = fact * F((2*k+2)*(2*k+3))
    rem = abs(c)**(2*NS+1) / F(math.factorial(2*NS+1))
    sI = I(s - rem, s + rem)
    t = F(1); sign = -1; p = c*c; fact = F(2)
    for k in range(1, NS):
        t = t + sign * p / fact
        sign = -sign
        p = p * c * c
        fact = fact * F((2*k+1)*(2*k+2))
    rem2 = abs(c)**(2*NS) / F(math.factorial(2*NS))
    return sI, I(t - rem2, t + rem2)

def _sc_u(w):
    su = F(0); sign = 1; p = w; fact = F(1)
    for k in range(NS):
        su = su + sign * p / fact
        sign = -sign
        p = p * w * w
        fact = fact * F((2*k+2)*(2*k+3))
    rem = w**(2*NS+1) / F(math.factorial(2*NS+1))
    cu = F(1); sign = -1; p = w*w; fact = F(2)
    for k in range(1, NS):
        cu = cu + sign * p / fact
        sign = -sign
        p = p * w * w
        fact = fact * F((2*k+1)*(2*k+2))
    rem2 = w**(2*NS) / F(math.factorial(2*NS))
    return I(-(su+rem), su+rem), I(cu-rem2, cu+rem2)

def I_sin(x):
    c = (x.lo + x.hi)/2
    w = (x.hi - x.lo)/2
    sc, cc = _sc_series(c)
    sin_u, cos_u = _sc_u(w)
    return sc*cos_u + cc*sin_u

def I_cos(x):
    c = (x.lo + x.hi)/2
    w = (x.hi - x.lo)/2
    sc, cc = _sc_series(c)
    sin_u, cos_u = _sc_u(w)
    return cc*cos_u - sc*sin_u

def _atan1_series(v, N=22):
    s = F(0); sign = 1; p = v; k = 1
    for _ in range(N):
        s = s + sign * p / F(k)
        sign = -sign
        p = p * v * v
        k += 2
    rem = v**(2*N+1) / F(2*N+1)
    return s - rem, s + rem

def certified_pi():
    lo5, hi5 = _atan1_series(F(1,5))
    lo239, hi239 = _atan1_series(F(1,239))
    lo = 16*lo5 - 4*hi239
    hi = 16*hi5 - 4*lo239
    assert lo < F(22,7) and hi > F(157,50) and hi - lo < F(1,10**9)
    return I(lo, hi)
PI=certified_pi()

def I_atan(x):
    assert x.lo >= 0
    if x.hi <= 1:
        lo = _atan1_series(x.lo)[0]; hi = _atan1_series(x.hi)[1]
        return I(lo, hi)
    inv = I(F(1))/x
    a = I_atan(inv)
    return I(PI.lo/2 - a.hi, PI.hi/2 - a.lo)

# Exact source functions from e1_certgen.py below:
def fmtF(x):
    return '%d/%d' % (x.numerator, x.denominator)

def dec(x, nd=12):
    """outward-rounded decimal representation (for readable output only)."""
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
    d = Decimal(x.numerator) / Decimal(x.denominator)
    lo = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_FLOOR)
    hi = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_CEILING)
    return str(lo), str(hi)

def ds(x):
    """single outward-rounded decimal string (12 sig figs)."""
    lo, hi = dec(x)
    # choose the endpoint farther from zero to keep it a valid one-sided display
    return hi if x >= 0 else lo

def taylor_value(fn, a, b, want_pos, n):
    """n-piece Taylor model for values: f(g) in f(c) + f'(piece)*[-w,w].
    Returns (ok, pieces)."""
    span = b - a
    w = span / (2*n)
    pieces = []
    all_ok = True
    for i in range(n):
        lo = a + span*F(i)/n
        hi = a + span*F(i+1)/n
        c = (lo + hi) / 2
        piece = I(lo, hi)
        fp = fn(D2(piece, I(1), I(0)))
        fc = fn(D2(I(c, c), I(1), I(0)))
        M = max(fp.d1.abs().hi, fc.d1.abs().hi)
        corr = M * w
        lo_v = fc.v.lo - corr
        hi_v = fc.v.hi + corr
        ok = (lo_v > 0) if want_pos else (hi_v < 0)
        pieces.append(dict(cell=[fmtF(lo), fmtF(hi)], c=fmtF(c),
                           fvc=[ds(fc.v.lo), ds(fc.v.hi)],
                           M=ds(M), corr=ds(corr),
                           bound=[ds(lo_v), ds(hi_v)],
                           margin=ds(lo_v if want_pos else -hi_v),
                           ok=bool(ok)))
        all_ok = all_ok and ok
    return all_ok, pieces
