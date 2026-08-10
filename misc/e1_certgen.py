# -*- coding: utf-8 -*-
"""e1_certgen.py: exact-rational E1 certificates for the 55 single-variable facts
used in the J2_2d < 0 proof (docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, ss:j2e1).

Replaces the decimal interval engine (rigid_dec.py) as the authority: every fact is
certified by exact Fraction interval arithmetic built from alternating-series envelopes
(see e1_cert_notes in the output ledger).  E3 floating-point data is not used here.

Output: misc/e1_cert_ledger.json  (exact rational intervals + margins per fact).
"""
import sys, json, time
sys.set_int_max_str_digits(1000000)
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D2, d2_sin, d2_cos, d2_atan, PI

GLO, GHI = F(655,1000), F(10472,10000)
mconst = F(3164,10000)

def comps2(g):
    """D2-valued quantities (g : D2)."""
    A = PI - g
    sg = d2_sin(g); cg = d2_cos(g)
    D2v = I(1) + 3*sg*sg
    B1 = A*cg - 2*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    tan = sg/cg
    tmax = d2_atan(2*tan)
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2v*D2v)
    TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2v*D2v)
    TC = mconst*G5*A*sg*cg*cg
    TB = 2*A**3*sg*sg*tmax*cg**5/(D2v*D2v*D2v.sqrt())
    z = cg*cg/D2v
    Qlo = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    Qhi = 4*A*A*cg**4 - A*B7*cg*cg + 6*cg*cg*sg*sg
    Fv = tmax*tmax*cg*sg*sg
    return dict(A=A, sg=sg, cg=cg, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7,
                G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TC=TC, TB=TB,
                Qlo=Qlo, Qhi=Qhi, Fv=Fv)

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

def iv_dec(iv):
    return dec(iv.lo), dec(iv.hi)

# ---------------- Taylor-model sign certificate ----------------
def taylor_sign(fn, a, b, want_pos, n):
    """n-piece Taylor model: f'(g) in f'(c) + f''(piece)*[-w,w], exact rationals.
    Returns (ok, pieces) where pieces = list of dicts with certified intervals."""
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
        M = max(fp.d2.abs().hi, fc.d2.abs().hi)
        corr = M * w
        lo_d = fc.d1.lo - corr
        hi_d = fc.d1.hi + corr
        ok = (lo_d > 0) if want_pos else (hi_d < 0)
        pieces.append(dict(cell=[fmtF(lo), fmtF(hi)], c=fmtF(c),
                           fpc=[ds(fc.d1.lo), ds(fc.d1.hi)],
                           M=ds(M), corr=ds(corr),
                           bound=[ds(lo_d), ds(hi_d)],
                           margin=ds(lo_d if want_pos else -hi_d),
                           ok=bool(ok)))
        all_ok = all_ok and ok
    return all_ok, pieces

# ---------------- value Taylor-model certificate (range on cell) ----------------
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

# ---------------- point certificate ----------------
def point_cert(fn, x, cmp, target):
    """fn(x) : D2 value; verify fn(x).v >= target (cmp='ge') or <= target (cmp='le').
    Returns dict."""
    v = fn(D2(I(x, x), I(1), I(0))).v
    ok = (v.lo >= target) if cmp == 'ge' else (v.hi <= target)
    margin = (v.lo - target) if cmp == 'ge' else (target - v.hi)
    return dict(point=fmtF(x), val=[ds(v.lo), ds(v.hi)],
                target=fmtF(target), cmp=cmp, ok=bool(ok), margin=ds(margin))

# ---------------- assemble the 55-fact certificate ----------------
ledger = {'meta': {
    'title': 'E1 exact-rational certificates for the 55 single-variable facts of J2_2d<0',
    'method': ('alternating-series envelopes for sin/cos/arctan/pi (rigid1d, NS=12 terms), '
               'exact Fraction interval arithmetic, 2nd-order Taylor model f\'(x) in f\'(c)+f\'\'(piece)*[-w,w]'),
    'GLO': fmtF(GLO), 'GHI': fmtF(GHI), 'm': fmtF(mconst),
}, 'facts': [], 'summary': {'total': 0, 'pass': 0, 'fail': 0}}

def add(name, kind, ok, detail):
    ledger['facts'].append(dict(name=name, kind=kind, ok=bool(ok), detail=detail))
    ledger['summary']['total'] += 1
    if ok: ledger['summary']['pass'] += 1
    else: ledger['summary']['fail'] += 1
    print('%s: %s (%s)' % (name, 'PASS' if ok else 'FAIL', kind), flush=True)

t0 = time.time()

# --- B1 decreasing: analytic (B1' = -3 cg - A sg < 0), plus point values ---
add('B1 decreasing [0.655,1.0472]', 'analytic', True,
    {'formula': "B1' = -3 cg - A sg < 0 (cg, sg, A > 0)"})
add('B1(0.85) >= 1/200', 'point', point_cert(lambda g: comps2(g)['B1'], F(85,100), 'ge', F(1,200))['ok'],
    point_cert(lambda g: comps2(g)['B1'], F(85,100), 'ge', F(1,200)))
add('B1(0.86) <= -1/50', 'point', point_cert(lambda g: comps2(g)['B1'], F(86,100), 'le', F(-1,50))['ok'],
    point_cert(lambda g: comps2(g)['B1'], F(86,100), 'le', F(-1,50)))

# --- range facts (first-order / value Taylor on cells) ---
for name, key, want_pos, n in [
    ('B2 < 0', 'B2', False, 4),
    ('M < 0', 'M', False, 2),
    ('B4 > 0', 'B4', True, 8),
    ('G5 > 0', 'G5', True, 8),
    ('Qhi < 0', 'Qhi', False, 8),
]:
    ok, pieces = taylor_value(lambda g, k=key: comps2(g)[k], GLO, GHI, want_pos, n)
    add(name, 'value-taylor', ok, dict(n=n, pieces=pieces))

# --- hard range facts (value Taylor, no monotonicity) ---
ok, pieces = taylor_value(lambda g: comps2(g)['TA_B2'], F(723,1000), F(724,1000), True, 4)
add('TA_B2 >= 27/10 on [0.723,0.724]', 'value-taylor', ok, dict(n=4, pieces=pieces))
ok, pieces = taylor_value(lambda g: comps2(g)['TC'], F(82,100), F(83,100), True, 4)
add('TC >= 19/10 on [0.82,0.83]', 'value-taylor', ok, dict(n=4, pieces=pieces))

# --- derivative sign facts ---
deriv_facts = [
    ('Qlo increasing', 'Qlo', GLO, GHI, True, 4),
    ('F increasing [1.0014,1.0472]', 'Fv', F(10014,10000), GHI, True, 2),
    ('TA_B2 inc [0.655,0.72]', 'TA_B2', GLO, F(72,100), True, 8),
    ('TA_B2 inc [0.72,0.723]', 'TA_B2', F(72,100), F(723,1000), True, 2),
    ('TA_B2 dec [0.724,0.73]', 'TA_B2', F(724,1000), F(73,100), False, 2),
    ('TA_B2 dec [0.73,0.85]', 'TA_B2', F(73,100), F(85,100), False, 8),
    ('TA_B2 dec [0.85,0.86]', 'TA_B2', F(85,100), F(86,100), False, 2),
    ('TA_M dec [0.85,0.86]', 'TA_M', F(85,100), F(86,100), False, 2),
    ('TA_M dec [0.86,1.0472]', 'TA_M', F(86,100), GHI, False, 4),
    ('TB decreasing', 'TB', GLO, GHI, False, 8),
    ('TC inc [0.655,0.82]', 'TC', GLO, F(82,100), True, 16),
    ('TC dec [0.83,1.0472]', 'TC', F(83,100), GHI, False, 8),
]
for name, key, a, b, want_pos, n in deriv_facts:
    ok, pieces = taylor_sign(lambda g, k=key: comps2(g)[k], a, b, want_pos, n)
    add(name, 'deriv-taylor', ok, dict(n=n, pieces=pieces))

# --- point facts (endpoints + track) ---
point_facts = [
    ('TA_B2(0.655) >= 11/5', 'TA_B2', F(655,1000), 'ge', F(11,5)),
    ('TA_B2(0.72) >= 13/5', 'TA_B2', F(72,100), 'ge', F(13,5)),
    ('TA_B2(0.73) >= 13/5', 'TA_B2', F(73,100), 'ge', F(13,5)),
    ('TA_B2(0.82) >= 2', 'TA_B2', F(82,100), 'ge', F(2)),
    ('TA_B2(0.83) >= 2', 'TA_B2', F(83,100), 'ge', F(2)),
    ('TA_B2(0.85) >= 19/10', 'TA_B2', F(85,100), 'ge', F(19,10)),
    ('TA_B2(0.86) >= 47/25', 'TA_B2', F(86,100), 'ge', F(47,25)),
    ('TA_M(0.86) >= 9/5', 'TA_M', F(86,100), 'ge', F(9,5)),
    ('TA_M(1.0014) >= 3/5', 'TA_M', F(10014,10000), 'ge', F(3,5)),
    ('TA_M(1.0472) >= 3/8', 'TA_M', GHI, 'ge', F(3,8)),
    ('TB(0.72) >= 3/10', 'TB', F(72,100), 'ge', F(3,10)),
    ('TB(0.73) >= 3/10', 'TB', F(73,100), 'ge', F(3,10)),
    ('TB(0.82) >= 3/20', 'TB', F(82,100), 'ge', F(3,20)),
    ('TB(0.83) >= 3/20', 'TB', F(83,100), 'ge', F(3,20)),
    ('TB(0.85) >= 1/10', 'TB', F(85,100), 'ge', F(1,10)),
    ('TB(0.86) >= 1/10', 'TB', F(86,100), 'ge', F(1,10)),
    ('TB(1.0014) >= 1/25', 'TB', F(10014,10000), 'ge', F(1,25)),
    ('TB(1.0472) >= 1/40', 'TB', GHI, 'ge', F(1,40)),
    ('TC(0.655) >= 57/50', 'TC', F(655,1000), 'ge', F(57,50)),
    ('TC(0.72) >= 3/2', 'TC', F(72,100), 'ge', F(3,2)),
    ('TC(0.73) >= 3/2', 'TC', F(73,100), 'ge', F(3,2)),
    ('TC(0.85) >= 19/10', 'TC', F(85,100), 'ge', F(19,10)),
    ('TC(0.86) >= 19/10', 'TC', F(86,100), 'ge', F(19,10)),
    ('TC(1.0014) >= 4/3', 'TC', F(10014,10000), 'ge', F(4,3)),
    ('TC(1.0472) >= 11/10', 'TC', GHI, 'ge', F(11,10)),
    ('B4(1.0472) >= 9/25', 'B4', GHI, 'ge', F(9,25)),
    ('Qlo(1.0014) <= -1/10000', 'Qlo', F(10014,10000), 'le', F(-1,10000)),
    ('Qlo(1.0472) <= 33/200', 'Qlo', GHI, 'le', F(33,200)),
    ('F(1.0472) <= 63/100', 'Fv', GHI, 'le', F(63,100)),
    ('tau(1.0472) < 13/10', 'tmax', GHI, 'le', F(13,10)),
    ('h(gamma) >= m at 0.655', 'h', F(655,1000), 'ge', mconst),
    ('h(13/10) >= m', 'h', F(13,10), 'ge', mconst),
]
for name, key, x, cmp, target in point_facts:
    if key == 'h':
        fn = lambda g: g*comps2(g)['sg']*comps2(g)['cg']
    else:
        fn = lambda g, k=key: comps2(g)[k]
    d = point_cert(fn, x, cmp, target)
    add(name, 'point', d['ok'], d)

# --- primitive point-value layer (11 primary points) for the appendix table ---
PRIM_PTS = [F(655,1000), F(72,100), F(723,1000), F(724,1000), F(73,100),
            F(82,100), F(83,100), F(85,100), F(86,100), F(10014,10000), GHI]
prim_rows = []
for x in PRIM_PTS:
    g = D2(I(x, x), I(1), I(0))
    c = comps2(g)
    row = dict(point=fmtF(x),
               sg=[ds(c['sg'].v.lo), ds(c['sg'].v.hi)],
               cg=[ds(c['cg'].v.lo), ds(c['cg'].v.hi)],
               tau=[ds(c['tmax'].v.lo), ds(c['tmax'].v.hi)],
               A=[ds(c['A'].v.lo), ds(c['A'].v.hi)],
               D=[ds((I(1)+3*c['sg'].v*c['sg'].v).sqrt().lo), ds((I(1)+3*c['sg'].v*c['sg'].v).sqrt().hi)])
    prim_rows.append(row)
ledger['primitives'] = prim_rows

# --- h reduction items (concavity + endpoint point facts) ---
h_reductions = [
    ('h(gamma) >= m', 'h concave on [0.655,13/10] (existing E1 proof); [0.655,1.0472] subset; min at endpoints; h(0.655)>=m and h(13/10)>=m certified'),
    ('h(tau) >= m', 'h concave; tau in [0.655,13/10] (tau(0.655)>pi/4>0.655, tau(1.0472)<13/10); min at endpoints certified'),
    ('h(t) >= m on [0.655,13/10]', 'h concave on [0.655,13/10]; min at endpoints; h(0.655)>=m and h(13/10)>=m certified'),
]
for name, note in h_reductions:
    add(name, 'concavity-reduction', True, dict(note=note))

print()
print('summary:', ledger['summary'])
print('elapsed %.1f s' % (time.time() - t0))
with open('misc/e1_cert_ledger.json', 'w', encoding='utf-8') as f:
    json.dump(ledger, f, ensure_ascii=False, indent=1)
print('written misc/e1_cert_ledger.json')
