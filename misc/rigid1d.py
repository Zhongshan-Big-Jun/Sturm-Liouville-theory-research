# -*- coding: utf-8 -*-
"""rigid1d.py v3: fast exact-rational interval arithmetic + 2nd-order Taylor sign verifier.
- Tight pi certified via Machin series.
- sin/cos: 10-term alternating series at center + interval for u.
- atan: 20-term series (x<=1) or pi/2 - atan(1/x).
- D: dual (value, derivative);  sign verification via Taylor model f'(x) in f'(c) + f''(piece)*[-w,w]."""
from fractions import Fraction as F
import math

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

NS = 12  # sin/cos series terms at center

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

# Machin: pi = 16 atan(1/5) - 4 atan(1/239), certified via alternating series
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

PI = certified_pi()

def I_atan(x):
    assert x.lo >= 0
    if x.hi <= 1:
        lo = _atan1_series(x.lo)[0]; hi = _atan1_series(x.hi)[1]
        return I(lo, hi)
    inv = I(F(1))/x
    a = I_atan(inv)
    return I(PI.lo/2 - a.hi, PI.hi/2 - a.lo)

class D:
    __slots__ = ('v','d')
    def __init__(self, v, d=None):
        self.v = v if isinstance(v, I) else I(v)
        self.d = I(0) if d is None else (d if isinstance(d, I) else I(d))
    def __repr__(self): return '(%s, %s)' % (self.v, self.d)
    def __add__(self, o):
        if not isinstance(o, D): o = D(o, I(0))
        return D(self.v+o.v, self.d+o.d)
    def __radd__(self, o): return self + o
    def __sub__(self, o):
        if not isinstance(o, D): o = D(o, I(0))
        return D(self.v-o.v, self.d-o.d)
    def __rsub__(self, o): return D(o) - self
    def __mul__(self, o):
        if not isinstance(o, D): o = D(o, I(0))
        return D(self.v*o.v, self.d*o.v + self.v*o.d)
    def __rmul__(self, o): return self * o
    def __truediv__(self, o):
        if not isinstance(o, D): o = D(o, I(0))
        return D(self.v/o.v, (self.d*o.v - self.v*o.d)/(o.v*o.v))
    def __neg__(self): return D(-self.v, -self.d)
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return D(I(1), I(0))
        return D(self.v**n, self.d*(n*self.v**(n-1)))
    def sqrt(self):
        r = self.v.sqrt()
        return D(r, self.d/(I(2)*r))

def d_sin(x): return D(I_sin(x.v), I_cos(x.v)*x.d)
def d_cos(x): return D(I_cos(x.v), -I_sin(x.v)*x.d)
def d_atan(x): return D(I_atan(x.v), x.d/(I(1)+x.v*x.v))

# ---- second-order sign verifier ----

class D2:
    """(v, d1, d2): value, first, second derivative (interval parts)."""
    __slots__ = ('v','d1','d2')
    def __init__(self, v, d1=None, d2=None):
        self.v = v if isinstance(v, I) else I(v)
        self.d1 = I(0) if d1 is None else (d1 if isinstance(d1, I) else I(d1))
        self.d2 = I(0) if d2 is None else (d2 if isinstance(d2, I) else I(d2))
    def __repr__(self): return '(%s, %s, %s)' % (self.v, self.d1, self.d2)
    def __add__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        return D2(self.v+o.v, self.d1+o.d1, self.d2+o.d2)
    def __radd__(self, o): return self + o
    def __sub__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        return D2(self.v-o.v, self.d1-o.d1, self.d2-o.d2)
    def __rsub__(self, o): return D2(o) - self
    def __mul__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        return D2(self.v*o.v, self.d1*o.v + self.v*o.d1,
                  self.d2*o.v + 2*self.d1*o.d1 + self.v*o.d2)
    def __rmul__(self, o): return self * o
    def __truediv__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        u, w = self, o
        w2 = w.v*w.v
        return D2(u.v/w.v,
                  (u.d1*w.v - u.v*w.d1)/w2,
                  (u.d2*w.v - u.v*w.d2)/w2 - 2*w.d1*(u.d1*w.v - u.v*w.d1)/(w2*w.v))
    def __neg__(self): return D2(-self.v, -self.d1, -self.d2)
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return D2(I(1), I(0), I(0))
        if n == 1: return self
        return D2(self.v**n, self.d1*(n*self.v**(n-1)),
                  self.d2*(n*self.v**(n-1)) + self.d1*self.d1*(n*(n-1)*self.v**(n-2)))
    def sqrt(self):
        r = self.v.sqrt()
        return D2(r, self.d1/(I(2)*r), self.d2/(I(2)*r) - self.d1*self.d1/(4*r*r*r))
    def inv(self):
        # 1/v
        return D2(I(1))/self

def d2_sin(x):
    return D2(I_sin(x.v), I_cos(x.v)*x.d1,
              -I_sin(x.v)*x.d1*x.d1 + I_cos(x.v)*x.d2)
def d2_cos(x):
    return D2(I_cos(x.v), -I_sin(x.v)*x.d1,
              -I_cos(x.v)*x.d1*x.d1 - I_sin(x.v)*x.d2)
def d2_atan(x):
    g = I(1) + x.v*x.v
    return D2(I_atan(x.v), x.d1/g,
              x.d2/g - 2*x.v*x.d1*x.d1/(g*g))

def der_sign2(fn, a, b, want_pos, base_n=64, max_n=65536, name=''):
    """Verify d/dg fn has constant sign on [a,b] via Taylor model:
    f'(x) in f'(c) + f''(piece)*[-w,w], where f''(piece) is the D2 interval evaluation (superset)."""
    span = b - a
    n = base_n
    while n <= max_n:
        w = span / (2*n)
        all_ok = True
        bad = None
        for i in range(n):
            c = a + span*F(2*i+1, 2*n)
            piece = I(c - w, c + w)
            fp = fn(D2(piece, I(1), I(0)))      # f'' over piece (superset)
            fc = fn(D2(I(c, c), I(1), I(0)))    # sharp at center
            M = max(fp.d2.abs().hi, fc.d2.abs().hi)
            corr = M * w
            lo = fc.d1.lo - corr
            hi = fc.d1.hi + corr
            if want_pos:
                if not (lo > 0):
                    all_ok = False; bad = (i, c, lo, hi, M); break
            else:
                if not (hi < 0):
                    all_ok = False; bad = (i, c, lo, hi, M); break
        if all_ok:
            return True, n
        n *= 2
    return False, ('failed at n=%d piece %s' % (n, bad))



def der_sign_adaptive(fn, a, b, want_pos, min_w=None, max_boxes=200000, name=''):
    """Adaptive Taylor-model sign verification of f' on [a,b].
    Splits only pieces whose sign is not certified. Returns (True, nboxes) or (False, info)."""
    span = b - a
    if min_w is None: min_w = span / (2**20)
    boxes = [(a, b)]
    nboxes = 0
    while boxes:
        lo, hi = boxes.pop()
        w = (hi - lo) / 2
        c = (lo + hi) / 2
        piece = I(c - w, c + w)
        fp = fn(D2(piece, I(1), I(0)))
        fc = fn(D2(I(c, c), I(1), I(0)))
        M = max(fp.d2.abs().hi, fc.d2.abs().hi)
        corr = M * w
        lo_d = fc.d1.lo - corr
        hi_d = fc.d1.hi + corr
        nboxes += 1
        if want_pos:
            if lo_d > 0: continue
        else:
            if hi_d < 0: continue
        if w <= min_w:
            return False, ('stuck at n=%d piece [%s,%s] f=[%s,%s] M=%s' % (nboxes, lo, hi, lo_d, hi_d, M))
        boxes.append((lo, c)); boxes.append((c, hi))
        if nboxes > max_boxes:
            return False, ('max_boxes exceeded at [%s,%s]' % (lo, hi))
    return True, nboxes
