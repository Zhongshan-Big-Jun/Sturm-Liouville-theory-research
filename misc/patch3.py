# -*- coding: utf-8 -*-
"""Add D2 (value, f, f'') and Taylor sign verifier to rigid1d."""
src = open('misc/rigid1d.py', encoding='utf-8').read()
addition = '''
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
        inv = D2(I(1))/o
        return self * inv
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
'''
src = src.replace('''def der_sign2(fn, a, b, want_pos, base_n=64, max_n=16384, name=''):
    """Verify d/dg fn has constant sign on [a,b]. Taylor model per piece: 
    f'(x) in f'(c) + f''(piece)*[-w,w].  Subdivide until sign decided or max_n."""
    span = b - a
    n = base_n
    while n <= max_n:
        ok_all = True
        w = span / (2*n)
        for i in range(n):
            c = a + span*F(2*i+1, 2*n)
            piece = I(c - w, c + w)
            g = D(piece, I(1))
            dfull = fn(g)              # interval AD: value and derivative bounds over piece
            fc = fn(D(I(c, c), I(1)))  # sharp point value/derivative at center
            # Taylor: f'(x) in fc.d + dfull.d-derivative-correction; use f'' bound via dfull of d? 
            # Instead: f'(x) - f'(c) in f''(piece)*[-w,w]; approximate f''(piece) by AD on the derivative expr
            # We get f'' bound by differentiating fn(g).d with respect to g: use AD of the derivative.
            # Implement: second derivative via D-of-D is complex; instead use crude: 
            # f''(piece) bounded by AD interval of (fn(g+h)-fn(g))/h? no.
            # Simpler robust: use fc.d + (derivative of fn's d via finite AD). We compute it:
            # g2 = D(piece, I(1)) ; take .d which is f'; differentiate again manually:
            # Instead of full AD2, use: f'(x) in fc.d ± w * |f''|_max where |f''|_max from AD of f' over piece:
            # d_of_fprime = fn(g).d is f'(g) as interval over piece (crude). Use it directly? No — that's the crude f' interval.
            pass
        break
    return False''', addition)
open('misc/rigid1d.py', 'w', encoding='utf-8').write(src)
print('added D2 + der_sign2')
