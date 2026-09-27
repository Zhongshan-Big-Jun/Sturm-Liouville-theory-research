# -*- coding: utf-8 -*-
"""audit_o3a_cert_replay.py: independent E1 replay of the O3a J2_2d<0 certificate.

Engine independence: the generator (misc/e1_certgen.py on misc/rigid1d.py) uses
exact-rational (fractions.Fraction) interval arithmetic.  This replay uses a
DIFFERENT engine: decimal.Decimal with directed rounding (ROUND_FLOOR for lower
endpoints, ROUND_CEILING for upper), 80 significant digits.  sin/cos/atan/pi
are certified via alternating Taylor series and Machin's formula with rigorous
remainder bounds computed under the same directed rounding.

Scope: the 57 facts in misc/e1_cert_ledger.json plus the 11 primitive rows.
Output: PASS/FAIL per fact, margin-compatibility against the ledger, and a JSON
summary (misc/audit_o3a_cert_replay.json).  This is a REPLAY, not a new proof;
it is E1 (strict interval) evidence.
"""
import sys
import json
import time
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING

PREC = 80
SIN_N = 60
ATAN_N = 80
TOL = Decimal('1e-8')


def _fl(fn):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_FLOOR
        return fn()


def _ce(fn):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_CEILING
        return fn()


def D(x):
    if isinstance(x, Decimal):
        return x
    if isinstance(x, F):
        return _fl(lambda: Decimal(x.numerator) / Decimal(x.denominator))
    return Decimal(str(x))


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


FACT = [_fact(i) for i in range(2 * SIN_N + 2)]


def qnum(s):
    a, b = s.split('/')
    return F(int(a), int(b))


def _parse_iv(field):
    return IV(D(field[0]), D(field[1]))


def _iv_contains(cert, disp, tol=TOL):
    """cert and disp are IV; disp is the ledger display (outward-rounded).
    Check that the two over-approximations agree within tolerance."""
    return (cert.lo - disp.lo <= tol and disp.hi - cert.hi <= tol
            and disp.lo - cert.lo <= tol and cert.hi - disp.hi <= tol)


class IV:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        if isinstance(lo, IV):
            lo, hi = lo.lo, lo.hi
        if hi is None:
            hi = lo
        self.lo = D(lo)
        self.hi = D(hi)
        if self.lo > self.hi:
            self.lo, self.hi = self.hi, self.lo

    def __repr__(self):
        return '[%s, %s]' % (self.lo, self.hi)

    def _as_iv(self, o):
        return o if isinstance(o, IV) else IV(o)

    def __add__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        o = self._as_iv(o)
        return IV(_fl(lambda: self.lo + o.lo), _ce(lambda: self.hi + o.hi))

    def __radd__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        return self + o

    def __sub__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        o = self._as_iv(o)
        return IV(_fl(lambda: self.lo - o.hi), _ce(lambda: self.hi - o.lo))

    def __rsub__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        return IV(o) - self

    def __mul__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        o = self._as_iv(o)
        lo = min(_fl(lambda: self.lo * o.lo), _fl(lambda: self.lo * o.hi),
                 _fl(lambda: self.hi * o.lo), _fl(lambda: self.hi * o.hi))
        hi = max(_ce(lambda: self.lo * o.lo), _ce(lambda: self.lo * o.hi),
                 _ce(lambda: self.hi * o.lo), _ce(lambda: self.hi * o.hi))
        return IV(lo, hi)

    def __rmul__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        return self * o

    def __truediv__(self, o):
        if isinstance(o, D2):
            return NotImplemented
        o = self._as_iv(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError('division by interval containing 0')
        lo = min(_fl(lambda: self.lo / o.lo), _fl(lambda: self.lo / o.hi),
                 _fl(lambda: self.hi / o.lo), _fl(lambda: self.hi / o.hi))
        hi = max(_ce(lambda: self.lo / o.lo), _ce(lambda: self.lo / o.hi),
                 _ce(lambda: self.hi / o.lo), _ce(lambda: self.hi / o.hi))
        return IV(lo, hi)

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0:
            return IV(1)
        if n == 1:
            return self
        if self.lo >= 0:
            return IV(_fl(lambda: self.lo ** n), _ce(lambda: self.hi ** n))
        if self.hi <= 0:
            if n % 2 == 0:
                return IV(_fl(lambda: (-self.hi) ** n), _ce(lambda: (-self.lo) ** n))
            return IV(_fl(lambda: self.lo ** n), _ce(lambda: self.hi ** n))
        if n % 2 == 0:
            return IV(0, _ce(lambda: max(self.lo ** n, self.hi ** n)))
        return IV(_fl(lambda: self.lo ** n), _ce(lambda: self.hi ** n))

    def sqrt(self):
        assert self.lo >= 0
        return IV(_fl(lambda: self.lo.sqrt()), _ce(lambda: self.hi.sqrt()))

    def abs(self):
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return IV(0, max(-self.lo, self.hi))

    @property
    def width(self):
        return self.hi - self.lo

    def is_pos(self):
        return self.lo > 0

    def is_neg(self):
        return self.hi < 0


def _partials(x):
    out = {}
    for tag, rounding in (('lo', ROUND_FLOOR), ('hi', ROUND_CEILING)):
        with localcontext() as ctx:
            ctx.prec = PREC
            ctx.rounding = rounding
            s = Decimal(0)
            p = x
            for k in range(SIN_N):
                if k % 2 == 1:
                    s = s - p / FACT[2 * k + 1]
                else:
                    s = s + p / FACT[2 * k + 1]
                p = p * x * x
            out['sin_' + tag] = s
            out['sin_tail_' + tag] = p / FACT[2 * SIN_N + 1]
            c = Decimal(1)
            p = x * x
            for k in range(1, SIN_N):
                if k % 2 == 1:
                    c = c - p / FACT[2 * k]
                else:
                    c = c + p / FACT[2 * k]
                p = p * x * x
            out['cos_' + tag] = c
            out['cos_tail_' + tag] = p / FACT[2 * SIN_N]
    return out


def sc_pt(x):
    """Rigorous (sin x, cos x) intervals for x in [0, pi/2]."""
    r = _partials(x)
    st = r['sin_tail_hi']
    ct = r['cos_tail_hi']
    return (IV(_fl(lambda: r['sin_lo'] - st), _ce(lambda: r['sin_hi'] + st)),
            IV(_fl(lambda: r['cos_lo'] - ct), _ce(lambda: r['cos_hi'] + ct)))


def sin_iv(x):
    assert x.lo >= 0 and x.hi <= D('1.571')
    s_lo, _ = sc_pt(x.lo)
    s_hi, _ = sc_pt(x.hi)
    return IV(s_lo.lo, s_hi.hi)


def cos_iv(x):
    assert x.lo >= 0 and x.hi <= D('1.571')
    _, c_lo = sc_pt(x.hi)
    _, c_hi = sc_pt(x.lo)
    return IV(c_lo.lo, c_hi.hi)


def _atan_partial(x, rounding):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = rounding
        s = Decimal(0)
        p = x
        kk = 1
        for k in range(ATAN_N):
            if k % 2 == 1:
                s = s - p / kk
            else:
                s = s + p / kk
            p = p * x * x
            kk += 2
        tail = p / kk
        return s, tail


def atan_pt(x):
    """Rigorous atan(x) for x in [0, 1] (point)."""
    slo, _ = _atan_partial(x, ROUND_FLOOR)
    shi, _ = _atan_partial(x, ROUND_CEILING)
    _, thi = _atan_partial(x, ROUND_CEILING)
    return IV(_fl(lambda: slo - thi), _ce(lambda: shi + thi))


def certified_pi():
    a5 = atan_iv(IV(_fl(lambda: Decimal(1) / 5), _ce(lambda: Decimal(1) / 5)))
    a239 = atan_iv(IV(_fl(lambda: Decimal(1) / 239), _ce(lambda: Decimal(1) / 239)))
    lo = _fl(lambda: 16 * a5.lo - 4 * a239.hi)
    hi = _ce(lambda: 16 * a5.hi - 4 * a239.lo)
    pi_iv = IV(lo, hi)
    assert pi_iv.lo > D('3.14159') and pi_iv.hi < D('3.1416'), 'pi sanity'
    return pi_iv


def atan_iv(x):
    assert x.lo >= 0
    if x.hi <= 1:
        return IV(atan_pt(x.lo).lo, atan_pt(x.hi).hi)
    if x.lo >= 1:
        inv = IV(1) / x
        a = atan_iv(inv)
        return IV(_fl(lambda: PI.lo / 2 - a.hi), _ce(lambda: PI.hi / 2 - a.lo))
    return IV(atan_pt(x.lo).lo, atan_iv(IV(x.hi, x.hi)).hi)


PI = certified_pi()
PI_HALF = IV(PI.lo / 2, PI.hi / 2)


class D2:
    __slots__ = ('v', 'd1', 'd2')

    def __init__(self, v, d1=None, d2=None):
        self.v = v if isinstance(v, IV) else IV(v)
        self.d1 = IV(0) if d1 is None else (d1 if isinstance(d1, IV) else IV(d1))
        self.d2 = IV(0) if d2 is None else (d2 if isinstance(d2, IV) else IV(d2))

    def __repr__(self):
        return '(%s, %s, %s)' % (self.v, self.d1, self.d2)

    def __add__(self, o):
        if not isinstance(o, D2):
            o = D2(o, IV(0), IV(0))
        return D2(self.v + o.v, self.d1 + o.d1, self.d2 + o.d2)

    def __radd__(self, o):
        return self + o

    def __sub__(self, o):
        if not isinstance(o, D2):
            o = D2(o, IV(0), IV(0))
        return D2(self.v - o.v, self.d1 - o.d1, self.d2 - o.d2)

    def __rsub__(self, o):
        return D2(o) - self

    def __mul__(self, o):
        if not isinstance(o, D2):
            o = D2(o, IV(0), IV(0))
        return D2(self.v * o.v, self.d1 * o.v + self.v * o.d1,
                  self.d2 * o.v + 2 * self.d1 * o.d1 + self.v * o.d2)

    def __rmul__(self, o):
        return self * o

    def __truediv__(self, o):
        if not isinstance(o, D2):
            o = D2(o, IV(0), IV(0))
        u, w = self, o
        w2 = w.v * w.v
        return D2(u.v / w.v,
                  (u.d1 * w.v - u.v * w.d1) / w2,
                  (u.d2 * w.v - u.v * w.d2) / w2 - 2 * w.d1 * (u.d1 * w.v - u.v * w.d1) / (w2 * w.v))

    def __neg__(self):
        return D2(-self.v, -self.d1, -self.d2)

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0:
            return D2(IV(1), IV(0), IV(0))
        if n == 1:
            return self
        return D2(self.v ** n, self.d1 * (n * self.v ** (n - 1)),
                  self.d2 * (n * self.v ** (n - 1)) + self.d1 * self.d1 * (n * (n - 1) * self.v ** (n - 2)))

    def sqrt(self):
        r = self.v.sqrt()
        return D2(r, self.d1 / (IV(2) * r),
                  self.d2 / (IV(2) * r) - self.d1 * self.d1 / (IV(4) * r * r * r))


def d2_sin(x):
    return D2(sin_iv(x.v), cos_iv(x.v) * x.d1, -sin_iv(x.v) * x.d1 * x.d1 + cos_iv(x.v) * x.d2)


def d2_cos(x):
    return D2(cos_iv(x.v), -sin_iv(x.v) * x.d1, -cos_iv(x.v) * x.d1 * x.d1 - sin_iv(x.v) * x.d2)


def d2_atan(x):
    g = IV(1) + x.v * x.v
    return D2(atan_iv(x.v), x.d1 / g, x.d2 / g - 2 * x.v * x.d1 * x.d1 / (g * g))


GLO = F(131, 200)
GHI = F(1309, 1250)
MCONST = F(791, 2500)


def comps2(g):
    A = PI - g
    sg = d2_sin(g)
    cg = d2_cos(g)
    D2v = IV(1) + 3 * sg * sg
    B1 = A * cg - 2 * sg
    B2 = 4 * A * A * cg * cg - A * A - 12 * A * cg * sg + 6 * sg * sg
    M = 2 * A * A * cg * cg - A * A - 8 * A * cg * sg + 6 * sg * sg
    B4 = 7 * A * cg * cg - A * sg * sg - 4 * cg * sg
    B5 = A * A * cg * cg - A * A * sg * sg + 2 * A * A + 12 * A * cg * sg - 12 * sg * sg
    B7 = 3 * A * cg * cg + A * sg * sg + 8 * cg * sg
    G5 = B5 - A * B4
    tan = sg / cg
    tmax = d2_atan(2 * tan)
    TA_B2 = 4 * (-B2) * A * A * sg * sg * cg ** 4 / (D2v * D2v)
    TA_M = 4 * (-M) * A * A * sg * sg * cg ** 4 / (D2v * D2v)
    TC = MCONST * G5 * A * sg * cg * cg
    TB = 2 * A ** 3 * sg * sg * tmax * cg ** 5 / (D2v * D2v * D2v.sqrt())
    z = cg * cg / D2v
    Qlo = 4 * A * A * z * z - A * B7 * z + 6 * cg * cg * sg * sg
    Qhi = 4 * A * A * cg ** 4 - A * B7 * cg * cg + 6 * cg * cg * sg * sg
    Fv = tmax * tmax * cg * sg * sg
    return dict(A=A, sg=sg, cg=cg, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7,
                G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TC=TC, TB=TB,
                Qlo=Qlo, Qhi=Qhi, Fv=Fv)


def point_value(key, x):
    g = D2(IV(D(x), D(x)), IV(1), IV(0))
    c = comps2(g)
    if key == 'h':
        return g.v * c['sg'].v * c['cg'].v
    return c[key].v


def taylor_fact(key, a, b, want_pos, n, kind):
    """Independent Taylor-model certificate.  kind in ('value', 'deriv')."""
    span = b - a
    w = span / (2 * n)
    pieces = []
    for i in range(n):
        lo = a + span * F(i) / n
        hi = a + span * F(i + 1) / n
        c = (lo + hi) / 2
        g_piece = D2(IV(D(lo), D(hi)), IV(1), IV(0))
        g_center = D2(IV(D(c), D(c)), IV(1), IV(0))
        fp = comps2(g_piece)[key]
        fc = comps2(g_center)[key]
        if kind == 'value':
            M = max(fp.d1.abs().hi, fc.d1.abs().hi)
            b_lo = _fl(lambda: fc.v.lo - M * D(w))
            b_hi = _ce(lambda: fc.v.hi + M * D(w))
            center = fc.v
            dM = fp.d1
        else:
            M = max(fp.d2.abs().hi, fc.d2.abs().hi)
            b_lo = _fl(lambda: fc.d1.lo - M * D(w))
            b_hi = _ce(lambda: fc.d1.hi + M * D(w))
            center = fc.d1
            dM = fp.d2
        ok = (b_lo > 0) if want_pos else (b_hi < 0)
        margin = b_lo if want_pos else -b_hi
        pieces.append(dict(lo=lo, hi=hi, c=c, center=center, M=M,
                           corr=M * D(w), bound=IV(b_lo, b_hi),
                           margin=margin, ok=ok, dM=dM))
    return all(p['ok'] for p in pieces), pieces


def h_concavity():
    """Rigorous enclosure of h'' = 2(cos 2g - g sin 2g) on [0.655, 13/10]."""
    lo_g = D('0.655')
    hi_g = D('1.3')
    u = _fl(lambda: PI.lo - D('2.6'))
    v = _ce(lambda: PI.hi - D('2.6'))
    c131 = cos_pt(D('1.31'))
    cuv = cos_iv(IV(u, v))
    cos26_lo = _fl(lambda: -cuv.hi)
    cos2g = IV(cos26_lo, c131.hi)
    s131 = sin_pt(D('1.31'))
    suv = sin_iv(IV(u, v))
    sin2g = IV(min(s131.lo, suv.lo), D(1))
    gs = IV(lo_g, hi_g) * sin2g
    half = cos2g - gs
    return 2 * half


def sin_pt(x):
    r = _partials(x)
    st = r['sin_tail_hi']
    return IV(_fl(lambda: r['sin_lo'] - st), _ce(lambda: r['sin_hi'] + st))


def cos_pt(x):
    r = _partials(x)
    ct = r['cos_tail_hi']
    return IV(_fl(lambda: r['cos_lo'] - ct), _ce(lambda: r['cos_hi'] + ct))


RANGE_SPECS = [
    ('B2 < 0', 'B2', GLO, GHI, False, 4, 'value'),
    ('M < 0', 'M', GLO, GHI, False, 2, 'value'),
    ('B4 > 0', 'B4', GLO, GHI, True, 8, 'value'),
    ('G5 > 0', 'G5', GLO, GHI, True, 8, 'value'),
    ('Qhi < 0', 'Qhi', GLO, GHI, False, 8, 'value'),
    ('TA_B2 >= 27/10 on [0.723,0.724]', 'TA_B2', F(723, 1000), F(724, 1000), True, 4, 'value'),
    ('TC >= 19/10 on [0.82,0.83]', 'TC', F(82, 100), F(83, 100), True, 4, 'value'),
    ('Qlo increasing', 'Qlo', GLO, GHI, True, 4, 'deriv'),
    ('F increasing [1.0014,1.0472]', 'Fv', F(10014, 10000), GHI, True, 2, 'deriv'),
    ('TA_B2 inc [0.655,0.72]', 'TA_B2', GLO, F(72, 100), True, 8, 'deriv'),
    ('TA_B2 inc [0.72,0.723]', 'TA_B2', F(72, 100), F(723, 1000), True, 2, 'deriv'),
    ('TA_B2 dec [0.724,0.73]', 'TA_B2', F(724, 1000), F(73, 100), False, 2, 'deriv'),
    ('TA_B2 dec [0.73,0.85]', 'TA_B2', F(73, 100), F(85, 100), False, 8, 'deriv'),
    ('TA_B2 dec [0.85,0.86]', 'TA_B2', F(85, 100), F(86, 100), False, 2, 'deriv'),
    ('TA_M dec [0.85,0.86]', 'TA_M', F(85, 100), F(86, 100), False, 2, 'deriv'),
    ('TA_M dec [0.86,1.0472]', 'TA_M', F(86, 100), GHI, False, 4, 'deriv'),
    ('TB decreasing', 'TB', GLO, GHI, False, 8, 'deriv'),
    ('TC inc [0.655,0.82]', 'TC', GLO, F(82, 100), True, 16, 'deriv'),
    ('TC dec [0.83,1.0472]', 'TC', F(83, 100), GHI, False, 8, 'deriv'),
]


def key_of_point_name(name):
    for k in ('TA_B2', 'TA_M', 'TC', 'TB', 'Qlo', 'Qhi', 'B4', 'B1', 'Fv', 'tmax', 'h'):
        if name.startswith(k):
            return k
    if name.startswith('F('):
        return 'Fv'
    if name.startswith('tau'):
        return 'tmax'
    if name.startswith('h('):
        return 'h'
    return None


def fmt_frac(x):
    return '%d/%d' % (x.numerator, x.denominator)


def main():
    t0 = time.time()
    ledger = json.load(open('misc/e1_cert_ledger.json', encoding='utf-8'))
    facts = ledger['facts']
    by_name = dict((f['name'], f) for f in facts)

    rows = []
    failures = 0
    max_margin_diff = Decimal(0)
    min_margin = Decimal('inf')

    def record(name, kind, ok, margin=None, detail=''):
        nonlocal failures, max_margin_diff, min_margin
        if margin is not None:
            if margin < min_margin:
                min_margin = margin
        status = 'PASS' if ok else 'FAIL'
        if not ok:
            failures += 1
        rows.append(dict(name=name, kind=kind, status=status, margin=str(margin), detail=detail))
        print('%-44s %-6s %-16s %s' % (name[:44], status, kind, detail[:70]))

    # ---- meta and counts ----
    meta_ok = (ledger['meta']['GLO'] == fmt_frac(GLO) and ledger['meta']['GHI'] == fmt_frac(GHI)
               and ledger['meta']['m'] == fmt_frac(MCONST))
    record('meta GLO/GHI/m', 'structural', meta_ok, detail='meta consistency')

    kind_counts = {}
    for f in facts:
        kind_counts[f['kind']] = kind_counts.get(f['kind'], 0) + 1
    counts_ok = (kind_counts == {'analytic': 1, 'point': 34, 'value-taylor': 7,
                                 'deriv-taylor': 12, 'concavity-reduction': 3})
    record('fact-kind counts', 'structural', counts_ok, detail=str(kind_counts))
    record('ledger summary', 'structural', ledger['summary'] == {'total': 57, 'pass': 57, 'fail': 0},
           detail='total=57 pass=57')

    # ---- analytic fact: B1 decreasing on [GLO,GHI] ----
    g = D2(IV(D(GLO), D(GHI)), IV(1), IV(0))
    B1p = comps2(g)['B1'].d1
    analytic_ok = B1p.is_neg()
    margin = -B1p.hi
    record('B1 decreasing [0.655,1.0472]', 'analytic', analytic_ok, margin,
           'B1p.hi=%s' % B1p.hi)

    # ---- point facts ----
    for f in facts:
        if f['kind'] != 'point':
            continue
        d = f['detail']
        x = qnum(d['point'])
        target = qnum(d['target'])
        key = key_of_point_name(f['name'])
        v = point_value(key, x)
        tiv = IV(_fl(lambda: D(target)), _ce(lambda: D(target)))
        if d['cmp'] == 'ge':
            ok = v.lo >= tiv.hi
            margin = _fl(lambda: v.lo - tiv.hi)
        else:
            ok = v.hi <= tiv.lo
            margin = _fl(lambda: tiv.lo - v.hi)
        led_margin = D(d['margin'])
        diff = abs(margin - led_margin)
        if diff > max_margin_diff:
            max_margin_diff = diff
        compat = diff <= TOL
        disp_ok = _iv_contains(v, _parse_iv(d['val']))
        ok_all = ok and compat and disp_ok and f['ok']
        record(f['name'], 'point', ok_all, margin,
               'margin=%s led=%s d=%s' % (margin, d['margin'], diff))

    # ---- range facts (value-taylor / deriv-taylor) ----
    for name, key, a, b, want_pos, n, kind in RANGE_SPECS:
        led = by_name.get(name)
        if led is None:
            record(name, kind, False, detail='NOT IN LEDGER')
            continue
        ok, pieces = taylor_fact(key, a, b, want_pos, n, kind)
        led_kind = 'value-taylor' if kind == 'value' else 'deriv-taylor'
        led_pieces = led['detail']['pieces']
        struct_ok = (len(led_pieces) == n and led['detail']['n'] == n and led['kind'] == led_kind)
        worst_diff = Decimal(0)
        all_compat = True
        if struct_ok:
            for i, p in enumerate(pieces):
                lp = led_pieces[i]
                cell_ok = (fmt_frac(p['lo']) == lp['cell'][0] and fmt_frac(p['hi']) == lp['cell'][1]
                           and fmt_frac(p['c']) == lp['c'])
                field = 'fvc' if kind == 'value' else 'fpc'
                center_ok = _iv_contains(p['center'], _parse_iv(lp[field]))
                M_diff = abs(p['M'] - D(lp['M']))
                corr_diff = abs(p['corr'] - D(lp['corr']))
                bound_ok = _iv_contains(p['bound'], _parse_iv(lp['bound']))
                margin_diff = abs(p['margin'] - D(lp['margin']))
                if margin_diff > worst_diff:
                    worst_diff = margin_diff
                piece_ok = (cell_ok and center_ok and bound_ok and margin_diff <= TOL
                            and M_diff <= TOL and corr_diff <= TOL and lp['ok'] == p['ok'])
                if not piece_ok:
                    all_compat = False
                    break
        else:
            all_compat = False
        if worst_diff > max_margin_diff:
            max_margin_diff = worst_diff
        ok_all = ok and struct_ok and all_compat and led['ok']
        record(name, led_kind, ok_all, None,
               'n=%d pieces=%d worst_mdiff=%s' % (n, len(pieces), worst_diff))

    # ---- concavity-reduction facts ----
    hpp = h_concavity()
    conc_ok = hpp.is_neg()
    if -hpp.hi < min_margin:
        min_margin = -hpp.hi
    # h(0.655) >= m and h(13/10) >= m are point facts (replayed above)
    t_lo = point_value('h', GLO)
    t_hi = point_value('h', F(13, 10))
    miv = IV(D(MCONST), D(MCONST))
    ep_ok = t_lo.lo >= miv.hi and t_hi.lo >= miv.hi
    # tau(0.655) > pi/4 > 0.655 and tau(1.0472) < 13/10
    tau_lo = point_value('tmax', GLO)
    tau_hi = point_value('tmax', GHI)
    p4 = IV(PI.lo / 4, PI.hi / 4)
    tau_ok = (tau_lo.lo > p4.hi and p4.lo > D('0.655') and tau_hi.hi < D('13') / 10)
    subset_ok = GHI <= F(13, 10)
    for f in facts:
        if f['kind'] != 'concavity-reduction':
            continue
        name = f['name']
        if name == 'h(gamma) >= m':
            ok = conc_ok and subset_ok and ep_ok
        elif name == 'h(tau) >= m':
            ok = conc_ok and subset_ok and tau_ok and ep_ok
        else:
            ok = conc_ok and subset_ok and ep_ok
        record(name, 'concavity-reduction', ok and f['ok'],
               -hpp.hi if ok else None, 'hpp.hi=%s ep=%s tau=%s' % (hpp.hi, ep_ok, tau_ok))

    # ---- primitives (11 rows) ----
    prim_fail = 0
    for r in ledger['primitives']:
        x = qnum(r['point'])
        g = D2(IV(D(x), D(x)), IV(1), IV(0))
        c = comps2(g)
        sg = c['sg'].v
        cg = c['cg'].v
        tau = c['tmax'].v
        A = c['A'].v
        Dv = (IV(1) + 3 * sg * sg).sqrt()
        fields = [('sg', sg, r['sg']), ('cg', cg, r['cg']), ('tau', tau, r['tau']),
                  ('A', A, r['A']), ('D', Dv, r['D'])]
        all_ok = True
        for fname, iv, disp in fields:
            if not _iv_contains(iv, _parse_iv(disp)):
                all_ok = False
        if not all_ok:
            prim_fail += 1
        record('prim ' + r['point'], 'primitive', all_ok, None, '')

    print()
    print('summary: %d facts, %d failures' % (len(rows), failures))
    print('min independent margin: %s' % min_margin)
    print('max |margin - ledger margin|: %s (tol %s)' % (max_margin_diff, TOL))
    print('primitives failures: %d / %d' % (prim_fail, len(ledger['primitives'])))
    print('elapsed %.1f s' % (time.time() - t0))

    out = dict(meta=dict(prec=PREC, engine='decimal.Decimal directed rounding',
                         sin_terms=SIN_N, atan_terms=ATAN_N, tol=str(TOL)),
               failures=failures, prim_failures=prim_fail,
               min_margin=str(min_margin), max_margin_diff=str(max_margin_diff),
               rows=rows)
    with open('misc/audit_o3a_cert_replay.json', 'w', encoding='utf-8') as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
    print('written misc/audit_o3a_cert_replay.json')
    sys.exit(0 if failures == 0 and prim_fail == 0 else 1)


if __name__ == '__main__':
    main()
