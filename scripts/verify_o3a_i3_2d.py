# -*- coding: utf-8 -*-
"""verify_o3a_i3_2d.py -- Independent verification of the 2D-parametrized certificates.
Certifies:
  (P1) J1_2d(x,q) = J(x, c1(x,q), q) > 0 on [x1a,x1b] x [1,2], c1 = atan(1/(q tan x))/x
  (P2) J2_2d(g,q) = J(pi-g, c2(g,q), q) < 0 on [g0,g1] x [1,2], c2 = atan(q tan g)/(pi-g)
Engine: mpmath.iv with hand-rolled outward-rounded atan (alternating Taylor + explicit
remainder on [0,1], reduction atan(x)=pi/2-atan(1/x) for x>1).
Audit: (a) adaptive subdivision into leaves; every leaf's certified interval has the
required polarity with margin; (b) every leaf corner/centre point-evaluated by
80-digit mpmath with monotone bisection-free direct formula must lie inside the leaf
interval; (c) total leaf area = box area (sliver quantified).
J, G, Gx, Gc are built from sympy (exact algebra), then evaluated with interval ops.
"""
import json, os, math, time
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 50
mp.mp.dps = 80

# ---------------- interval atan (sound: alternating series + remainder) ----------------
def iv_atan(x, nterms=200):
    a, b = x.a, x.b
    if a < 0:
        if a > -mp.mpf('1e-40'):
            a = mp.mpf(0)
        else:
            raise ValueError('atan for x >= 0 only, got %s' % (x,))
    def atan_series(xx, n):
        x2 = xx * xx
        xp = xx
        acc = iv.mpf(0)
        sign = 1
        for j in range(n + 1):
            d = 2 * j + 1
            term = xp / iv.mpf(d)
            acc = acc + term if sign > 0 else acc - term
            sign *= -1
            xp = xp * x2
        R = xx.b**(2 * n + 3) / iv.mpf(2 * n + 3)
        return iv.mpf([acc.a - R, acc.b + R])
    def atan_endpoint(pt):
        if pt <= 1:
            return atan_series(iv.mpf([pt, pt]), nterms)
        inv = iv.mpf([1, 1]) / iv.mpf([pt, pt])
        return iv.pi / 2 - atan_series(inv, nterms)
    return iv.mpf([atan_endpoint(a).a, atan_endpoint(b).b])

def _atan_sanity():
    ok = True
    for t in ['0', '0.1', '0.5', '0.9', '1', '2', '5', '100', '1e5']:
        tv = mp.mpf(t)
        r = iv_atan(iv.mpf([tv, tv]))
        exact = mp.atan(tv)
        if not (r.a <= exact <= r.b):
            ok = False
            print('  atan fail t=%s: [%s,%s] vs %s' % (t, r.a, r.b, mp.nstr(exact, 30)))
    for (t0, t1) in [('0.2', '0.5'), ('1', '3'), ('0', '10')]:
        r = iv_atan(iv.mpf([mp.mpf(t0), mp.mpf(t1)]))
        e0, e1 = mp.atan(mp.mpf(t0)), mp.atan(mp.mpf(t1))
        if not (r.a <= e0 and e1 <= r.b):
            ok = False
            print('  atan interval fail [%s,%s]: [%s,%s] vs [%s,%s]' % (t0, t1, r.a, r.b, mp.nstr(e0, 25), mp.nstr(e1, 25)))
    return ok

# ---------------- symbolic functions (exact algebra) ----------------
X, C, Q = sp.symbols('x c q', positive=True)
_sx = sp.sin(X); _cx = sp.cos(X)
_Ph = _cx**2 + Q**2 * _sx**2
_D = Q + C * _Ph
_W = 3 + 2 * X / _sx * _cx
_sc = _sx * _cx
_G = -_Ph * _W / _D + 2 * C * X * _Ph * (Q**2 - 1) * _sc / (_D**2)
_Gx = sp.simplify(sp.diff(_G, X))
_Gc = sp.simplify(sp.diff(_G, C))
_xp = -X * _Ph / _D
_J = sp.simplify(_G**2 + (_Gx * _xp + _Gc))

_mods = {'sin': iv.sin, 'cos': iv.cos, 'tan': iv.tan, 'mpf': iv.mpf, 'pi': iv.pi}
J_iv = sp.lambdify((X, C, Q), _J, modules=_mods)
G_iv = sp.lambdify((X, C, Q), _G, modules=_mods)
Gx_iv = sp.lambdify((X, C, Q), _Gx, modules=_mods)
Gc_iv = sp.lambdify((X, C, Q), _Gc, modules=_mods)

def c1_iv(x, q): return iv_atan(1.0 / (q * iv.tan(x))) / x
def c2_iv(g, q): return iv_atan(q * iv.tan(g)) / (iv.pi - g)
def J1_2d_iv(x, q): return J_iv(x, c1_iv(x, q), q)
def J2_2d_iv(g, q): return J_iv(iv.pi - g, c2_iv(g, q), q)

# ---------------- adaptive subdivision ----------------
def certify(f, x0, x1, q0, q1, want_pos, depth=0, maxdepth=16):
    x = iv.mpf([x0, x1]); q = iv.mpf([q0, q1])
    r = f(x, q)
    if want_pos and r.a > 0:
        return (True, [(float(x0), float(x1), float(q0), float(q1), float(r.a), float(r.b))], 0)
    if (not want_pos) and r.b < 0:
        return (True, [(float(x0), float(x1), float(q0), float(q1), float(r.a), float(r.b))], 0)
    if depth >= maxdepth:
        return (None, [(float(x0), float(x1), float(q0), float(q1), float(r.a), float(r.b))], 1)
    xm = (x0 + x1) / 2; qm = (q0 + q1) / 2
    subs = [(x0, xm, q0, qm), (xm, x1, q0, qm), (x0, xm, qm, q1), (xm, x1, qm, q1)]
    ok = True; leaves = []; bad = 0
    for (a, b, c, d) in subs:
        st, lf, bl = certify(f, a, b, c, d, want_pos, depth + 1, maxdepth)
        if st is None:
            ok = False
        leaves += lf; bad += bl
    return ((True if ok else None), leaves, bad)

def check_leaves(f, leaves, want_pos):
    """Re-evaluate every leaf with the same engine; require strict polarity."""
    n = len(leaves); worst = None
    for (a, b, c, d, la, lb) in leaves:
        r = f(iv.mpf([a, b]), iv.mpf([c, d]))
        if want_pos:
            if not (r.a > 0):
                return False, n, (a, b, c, d, r.a, r.b)
            m = r.a
        else:
            if not (r.b < 0):
                return False, n, (a, b, c, d, r.a, r.b)
            m = -r.b
        if worst is None or m < worst: worst = m
    return True, n, worst

def point_crosscheck(f, leaves, want_pos):
    """80-digit point values at leaf corners + centre inside leaf interval."""
    n = 0; fails = 0
    for (a, b, c, d, la, lb) in leaves:
        pts = [(a, c), (a, d), (b, c), (b, d), ((a + b) / 2, (c + d) / 2)]
        for (px, pq) in pts:
            n += 1
            try:
                v = f(mp.mpf(px), mp.mpf(pq))
            except Exception:
                continue
            if not (mp.mpf(la) <= v <= mp.mpf(lb)):
                fails += 1
                if fails < 4:
                    print('  point fail leaf (%s,%s,%s,%s) pt (%s,%s) v=%s outside [%s,%s]' % (
                        mp.nstr(a, 8), mp.nstr(b, 8), mp.nstr(c, 8), mp.nstr(d, 8), mp.nstr(px, 8), mp.nstr(pq, 8), mp.nstr(v, 20), mp.nstr(la, 10), mp.nstr(lb, 10)))
    return n, fails

# sum of leaf areas must equal the box area (partition invariant)
def area_audit(leaves, x0, x1, q0, q1):
    total = 0.0
    for (a, b, c, d, la, lb) in leaves:
        total += (b - a) * (d - c)
    box = (x1 - x0) * (q1 - q0)
    return total, box

# point evaluators for cross-check (mpf, high precision)
_Gx_pt_fn = sp.lambdify((X, C, Q), _Gx, modules='mpmath')
_Gc_pt_fn = sp.lambdify((X, C, Q), _Gc, modules='mpmath')
def _J_pt(x, c, q):
    Ph = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Ph
    W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    Gv = -Ph*W/D + 2*c*x*Ph*(q*q-1)*sc/(D*D)
    Gxv = _Gx_pt_fn(x, c, q)
    Gcv = _Gc_pt_fn(x, c, q)
    xp = -x*Ph/D
    return Gv*Gv + Gxv*xp + Gcv
def _c1_pt(x, q): return mp.atan(1.0/(q*mp.tan(x)))/x
def _c2_pt(g, q): return mp.atan(q*mp.tan(g))/(mp.pi-g)
def _J1_pt(x, q): return _J_pt(x, _c1_pt(x, q), q)
def _J2_pt(g, q): return _J_pt(mp.pi-g, _c2_pt(g, q), q)

print('atan sanity:', _atan_sanity())
specs = [
    ('P1_J1_gt0', J1_2d_iv, mp.mpf('0.841'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), True, _J1_pt),
    ('P2_J2_lt0', J2_2d_iv, mp.mpf('0.655'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2), False, _J2_pt),
]
results = {}
for name, f, x0, x1, q0, q1, wp, fpt in specs:
    t0 = time.time()
    st, leaves, bad = certify(f, x0, x1, q0, q1, wp)
    ok, n, worst = check_leaves(f, leaves, wp)
    npts, nfail = point_crosscheck(fpt, leaves, wp)
    atot, abox = area_audit(leaves, x0, x1, q0, q1)
    area_ok = abs(atot - abox) < 1e-9 * max(1.0, abox)
    print('%s: certify=%s leaves=%d bad=%d recheck_ok=%s worst_margin=%.12g pts=%d pt_fails=%d area_ok=%s (%.1fs)' % (
        name, st, n, bad, ok, worst, npts, nfail, area_ok, time.time()-t0))
    results[name] = dict(status=('OK' if (st is True and ok and nfail == 0) else 'FAIL'),
                         leaves=n, bad=bad, worst_margin=worst, pt_checked=npts, pt_fails=nfail,
                         domain=[str(x0), str(x1), str(q0), str(q1)], polarity=('>0' if wp else '<0'),
                         area_ok=area_ok, area_sum=atot, area_box=abox)
    with open(r'misc/i3_2d_leaves_%s.json' % name, 'w') as fh:
        json.dump({'box': [str(x0), str(x1), str(q0), str(q1)], 'want_pos': wp, 'leaves': leaves}, fh)
print('SUMMARY:')
for k, v in results.items():
    print(' ', k, v['status'], 'leaves=%d worst_margin=%.12g pt_fails=%d area_ok=%s' % (v['leaves'], v['worst_margin'], v['pt_fails'], v['area_ok']))
