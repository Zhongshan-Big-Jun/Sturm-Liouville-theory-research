"""Polynomial-only execution excerpts from ec45bf99 misc/rigid1d.py.
I/D2 methods and sign-verifier bodies copied; imports isolated. The D sentinel
only satisfies I's dispatch test; no first-order dual arithmetic is exercised.
This is not a full upstream file, nor a replacement implementation.
"""
from fractions import Fraction as F
import math
class D:
    pass

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
        if not isinstance(n, int): raise TypeError('power requires an integer exponent')
        if n < 0: raise ValueError('power requires a nonnegative exponent')
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
        if not isinstance(n, int): raise TypeError('power requires an integer exponent')
        if n < 0: raise ValueError('power requires a nonnegative exponent')
        if n == 0: return D2(I(1), I(0), I(0))
        if n == 1: return self
        return D2(self.v**n, self.d1*(n*self.v**(n-1)),
                  self.d2*(n*self.v**(n-1)) + self.d1*self.d1*(n*(n-1)*self.v**(n-2)))

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
            fp = fn(D2(piece, I(1), I(0)))
            fc = fn(D2(I(c, c), I(1), I(0)))
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
