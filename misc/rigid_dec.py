# -*- coding: utf-8 -*-
"""rigid_dec.py v2: rigorous interval arithmetic over Python Decimal with directed rounding.
- pi via Machin with alternating-series bounds
- sin/cos via Taylor series with explicit alternating-series remainder bounds
- atan via alternating series (x<=1) or pi/2 - atan(1/x) (x>1)
- D1 dual numbers (value, derivative) for derivative-sign verification
All endpoints rounded outward (ROUND_FLOOR for lo, ROUND_CEILING for hi)."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING, getcontext

getcontext().prec = 70

def _fl(x):
    with localcontext() as ctx:
        ctx.rounding = ROUND_FLOOR
        return Decimal(x)
def _ce(x):
    with localcontext() as ctx:
        ctx.rounding = ROUND_CEILING
        return Decimal(x)

class I:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi=None):
        if isinstance(lo, I):
            lo, hi = lo.lo, lo.hi
        if hi is None:
            hi = lo
        lo = _fl(lo); hi = _ce(hi)
        if lo > hi:
            lo, hi = hi, lo
        self.lo, self.hi = lo, hi
    @staticmethod
    def _raw(lo, hi):
        o = I.__new__(I)
        o.lo, o.hi = lo, hi
        return o
    def __repr__(self):
        return '[%s, %s]' % (self.lo, self.hi)
    def __add__(self, o):
        if isinstance(o, D1): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR; lo = self.lo + o.lo
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING; hi = self.hi + o.hi
        return I._raw(lo, hi)
    def __radd__(self, o):
        if isinstance(o, D1): return NotImplemented
        return self + o
    def __sub__(self, o):
        if isinstance(o, D1): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR; lo = self.lo - o.hi
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING; hi = self.hi - o.lo
        return I._raw(lo, hi)
    def __rsub__(self, o):
        if isinstance(o, D1): return NotImplemented
        return I(o) - self
    def __mul__(self, o):
        if isinstance(o, D1): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR
            a = self.lo*o.lo; b = self.lo*o.hi; c = self.hi*o.lo; d = self.hi*o.hi
            lo = min(a, b, c, d)
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING
            a = self.lo*o.lo; b = self.lo*o.hi; c = self.hi*o.lo; d = self.hi*o.hi
            hi = max(a, b, c, d)
        return I._raw(lo, hi)
    def __rmul__(self, o):
        if isinstance(o, D1): return NotImplemented
        return self * o
    def __truediv__(self, o):
        if isinstance(o, D1): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError('div by interval containing 0')
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR
            a = self.lo/o.lo; b = self.lo/o.hi; c = self.hi/o.lo; d = self.hi/o.hi
            lo = min(a, b, c, d)
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING
            a = self.lo/o.lo; b = self.lo/o.hi; c = self.hi/o.lo; d = self.hi/o.hi
            hi = max(a, b, c, d)
        return I._raw(lo, hi)
    def __neg__(self):
        return I._raw(-self.hi, -self.lo)
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return I._raw(I(1).lo, I(1).hi)
        if n == 1: return self
        if self.lo >= 0:
            with localcontext() as ctx:
                ctx.rounding = ROUND_FLOOR; lo = self.lo**n
            with localcontext() as ctx:
                ctx.rounding = ROUND_CEILING; hi = self.hi**n
            return I._raw(lo, hi)
        if self.hi <= 0:
            if n % 2 == 0:
                with localcontext() as ctx:
                    ctx.rounding = ROUND_FLOOR; lo = (-self.hi)**n
                with localcontext() as ctx:
                    ctx.rounding = ROUND_CEILING; hi = (-self.lo)**n
                return I._raw(lo, hi)
            with localcontext() as ctx:
                ctx.rounding = ROUND_FLOOR; lo = self.lo**n
            with localcontext() as ctx:
                ctx.rounding = ROUND_CEILING; hi = self.hi**n
            return I._raw(lo, hi)
        if n % 2 == 0:
            with localcontext() as ctx:
                ctx.rounding = ROUND_CEILING; hi = max(self.lo**n, self.hi**n)
            return I._raw(I(0).lo, hi)
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR; lo = self.lo**n
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING; hi = self.hi**n
        return I._raw(lo, hi)
    def contains_zero(self): return self.lo <= 0 <= self.hi
    def is_pos(self): return self.lo > 0
    def is_neg(self): return self.hi < 0
    def width(self): return self.hi - self.lo
    def abs(self):
        if self.lo >= 0: return self
        if self.hi <= 0: return -self
        return I._raw(I(0).lo, max(-self.lo, self.hi))
    def sqrt(self):
        assert self.lo >= 0
        with localcontext() as ctx:
            ctx.rounding = ROUND_FLOOR; lo = self.lo.sqrt()
        with localcontext() as ctx:
            ctx.rounding = ROUND_CEILING; hi = self.hi.sqrt()
        return I._raw(lo, hi)

NS = 40  # sin/cos series terms

def _sc_series(c):
    """sin(c), cos(c) enclosures by alternating Taylor series at center c (Decimal).
    All intermediate products done in interval arithmetic with outward rounding."""
    ci = I(c)
    c2 = ci*ci
    S = I(0)
    p = ci
    fact = I(1)
    for k in range(NS):
        t = p / fact
        S = S + t if k % 2 == 0 else S - t
        p = p * c2
        fact = fact * I((2*k+2)*(2*k+3))
    rem = (p / fact).abs().hi
    sinI = I(S.lo - rem, S.hi + rem)
    T = I(1)
    p = c2
    fact = I(2)
    for k in range(1, NS):
        t = p / fact
        T = T - t if k % 2 == 1 else T + t
        p = p * c2
        fact = fact * I((2*k+1)*(2*k+2))
    rem2 = (p / fact).abs().hi
    cosI = I(T.lo - rem2, T.hi + rem2)
    return sinI, cosI

def _sin_cos_u(w):
    """sin(u), cos(u) enclosures for |u| <= w (w Decimal >= 0)."""
    wi = I(w)
    w2 = wi*wi
    S = I(0)
    p = wi
    fact = I(1)
    for k in range(NS):
        t = p / fact
        S = S + t if k % 2 == 0 else S - t
        p = p * w2
        fact = fact * I((2*k+2)*(2*k+3))
    rems = (p / fact).abs().hi
    sw = I(S.lo - rems, S.hi + rems)
    T = I(1)
    p = w2
    fact = I(2)
    for k in range(1, NS):
        t = p / fact
        T = T - t if k % 2 == 1 else T + t
        p = p * w2
        fact = fact * I((2*k+1)*(2*k+2))
    remc = (p / fact).abs().hi
    cw = I(T.lo - remc, T.hi + remc)
    # range over u in [-w, w]: sin odd -> [-sin(w), sin(w)]; cos even, decreasing on [0,w] -> [cos(w), 1]
    sin_u = I(-sw.hi, sw.hi)
    cos_u = I(cw.lo, I(1).lo)
    return sin_u, cos_u

def I_sin(x):
    c = (x.lo + x.hi) / 2
    w = max(c - x.lo, x.hi - c)
    w = _ce(w)
    sc, cc = _sc_series(c)
    sin_u, cos_u = _sin_cos_u(w)
    return sc*cos_u + cc*sin_u

def I_cos(x):
    c = (x.lo + x.hi) / 2
    w = max(c - x.lo, x.hi - c)
    w = _ce(w)
    sc, cc = _sc_series(c)
    sin_u, cos_u = _sin_cos_u(w)
    return cc*cos_u - sc*sin_u

def I_tan(x):
    return I_sin(x) / I_cos(x)

def _atan_series(v, N=NS):
    """atan(v) enclosure for 0 <= v <= 1 by alternating series (interval arithmetic)."""
    vi = I(v)
    v2 = vi*vi
    S = I(0)
    p = vi
    k = 1
    for _ in range(N):
        t = p / I(k)
        S = S + t if ((k-1)//2) % 2 == 0 else S - t
        p = p * v2
        k += 2
    rem = (p / I(k)).abs().hi
    return I(S.lo - rem, S.hi + rem)

def I_atan2(x):
    """atan(x) for x >= 0."""
    assert x.lo >= 0
    if x.hi <= 1:
        lo = _atan_series(x.lo)
        hi = _atan_series(x.hi)
        return I(lo.lo, hi.hi)
    if x.lo >= 1:
        alo = _atan_series(Decimal(1)/x.hi)
        ahi = _atan_series(Decimal(1)/x.lo)
        return I(PI.lo/2 - ahi.hi, PI.hi/2 - alo.lo)
    lo = _atan_series(x.lo)
    ahi = _atan_series(Decimal(1)/x.hi)
    return I(lo.lo, PI.hi/2 - ahi.lo)

def _machin():
    a = _atan_series(Decimal(1)/Decimal(5))
    b = _atan_series(Decimal(1)/Decimal(239))
    return I(16*a.lo - 4*b.hi, 16*a.hi - 4*b.lo)

class D1:
    __slots__ = ('v', 'd')
    def __init__(self, v, d=None):
        self.v = v if isinstance(v, I) else I(v)
        self.d = I(0) if d is None else (d if isinstance(d, I) else I(d))
    def __repr__(self): return '(%s, %s)' % (self.v, self.d)
    def __add__(self, o):
        if not isinstance(o, D1): o = D1(o, I(0))
        return D1(self.v+o.v, self.d+o.d)
    def __radd__(self, o): return self + o
    def __sub__(self, o):
        if not isinstance(o, D1): o = D1(o, I(0))
        return D1(self.v-o.v, self.d-o.d)
    def __rsub__(self, o): return D1(o) - self
    def __mul__(self, o):
        if not isinstance(o, D1): o = D1(o, I(0))
        return D1(self.v*o.v, self.d*o.v + self.v*o.d)
    def __rmul__(self, o): return self * o
    def __truediv__(self, o):
        if not isinstance(o, D1): o = D1(o, I(0))
        return D1(self.v/o.v, (self.d*o.v - self.v*o.d)/(o.v*o.v))
    def __neg__(self): return D1(-self.v, -self.d)
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return D1(I(1), I(0))
        return D1(self.v**n, self.d*(n*self.v**(n-1)))
    def sqrt(self):
        r = self.v.sqrt()
        return D1(r, self.d/(I(2)*r))

def d1_sin(x): return D1(I_sin(x.v), I_cos(x.v)*x.d)
def d1_cos(x): return D1(I_cos(x.v), -I_sin(x.v)*x.d)
def d1_atan(x): return D1(I_atan2(x.v), x.d/(I(1)+x.v*x.v))

def der_sign(fn, a, b, want_pos, min_w=None, max_boxes=2000000, name=''):
    a = a if isinstance(a, Decimal) else Decimal(str(a))
    b = b if isinstance(b, Decimal) else Decimal(str(b))
    span = b - a
    if min_w is None:
        min_w = span / Decimal(2**24)
    boxes = [(a, b)]
    nboxes = 0
    while boxes:
        lo, hi = boxes.pop()
        w = (hi - lo)/2
        piece = I(lo, hi)
        fp = fn(D1(piece, I(1)))
        nboxes += 1
        if want_pos:
            if fp.d.lo > 0: continue
        else:
            if fp.d.hi < 0: continue
        if w <= min_w:
            return False, ('stuck at n=%d piece %s f_piece=%s' % (nboxes, piece, fp.d))
        boxes.append((lo, lo + w)); boxes.append((lo + w, hi))
        if nboxes > max_boxes:
            return False, ('max_boxes exceeded at %s' % (piece,))
    return True, nboxes

def range_pos(fn, a, b, min_w=None, max_boxes=2000000):
    """Verify fn value > 0 on [a,b] by adaptive interval evaluation."""
    a = a if isinstance(a, Decimal) else Decimal(str(a))
    b = b if isinstance(b, Decimal) else Decimal(str(b))
    span = b - a
    if min_w is None:
        min_w = span / Decimal(2**24)
    boxes = [(a, b)]
    nboxes = 0
    while boxes:
        lo, hi = boxes.pop()
        w = (hi - lo)/2
        piece = I(lo, hi)
        v = fn(D1(piece, I(0))).v
        nboxes += 1
        if v.lo > 0: continue
        if w <= min_w:
            return False, ('stuck at n=%d piece %s val=%s' % (nboxes, piece, v))
        boxes.append((lo, lo + w)); boxes.append((lo + w, hi))
        if nboxes > max_boxes:
            return False, ('max_boxes exceeded at %s' % (piece,))
    return True, nboxes

def val_at(fn, x):
    return fn(D1(I(x), I(0))).v

_PI = None

def get_pi():
    global _PI
    if _PI is None:
        _PI = _machin()
    return _PI

PI = get_pi()
