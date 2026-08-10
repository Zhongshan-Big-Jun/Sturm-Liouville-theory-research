# -*- coding: utf-8 -*-
"""zz_verify_e1_dec.py: rigorous certification of every 1D fact used by the E1 proof
of J2_2d < 0 on [0.655,1.0472]x[1,2] (W = T1+...+T8 decomposition chain).
Engine: rigid_dec - Decimal directed-rounding interval arithmetic (E1-grade).
Output: JSON ledger of certified facts + box counts + G1 margin at the corner."""
import sys, time, json
sys.path.insert(0, 'misc')
from decimal import Decimal as D, getcontext
from fractions import Fraction
from rigid_dec import I, PI, D1, d1_sin, d1_cos, d1_atan, der_sign, range_pos, val_at

getcontext().prec = 70
GLO, GHI = D('0.655'), D('1.0472')
MC = D(3164)/D(10000)

def comps(g):
    """All quantities as D1 (value, derivative) intervals at phase g."""
    A = PI - g
    sg = d1_sin(g); cg = d1_cos(g)
    D2 = I(1) + 3*sg*sg
    Ds = D2.sqrt()
    B1 = A*cg - 2*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    tan = sg/cg
    tmax = d1_atan(D(2)*tan)
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2*D2)
    TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2*D2)
    TB = 2*A**3*sg*sg*tmax*cg**5/(D2*D2*Ds)
    TC = MC*G5*A*sg*cg*cg
    z = cg*cg/D2
    Qlo = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    Qhi = 4*A*A*cg**4 - A*B7*cg*cg + 6*cg*cg*sg*sg
    Fv = tmax*tmax*cg*sg*sg
    h_g = g*sg*cg                      # h(gamma) = (gamma/2) sin(2 gamma)
    h_t = 2*tmax*sg*cg/D2              # h(tmax)  = tmax sin(tmax) cos(tmax)
    return dict(A=A, sg=sg, cg=cg, D2=D2, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7,
                G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TB=TB, TC=TC, Qlo=Qlo,
                Qhi=Qhi, Fv=Fv, h_g=h_g, h_t=h_t)

def frac_of(d):
    n, d0 = d.as_integer_ratio()
    return Fraction(n, d0)

def rat(s):
    return Fraction(s)

def lb(fn, x, lo_b):
    v = val_at(fn, D(str(x)))
    return frac_of(v.lo) >= rat(lo_b), v

def ub(fn, x, hi_b):
    v = val_at(fn, D(str(x)))
    return frac_of(v.hi) <= rat(hi_b), v

results = []
def add(name, ok, info=''):
    results.append((name, bool(ok), str(info)))
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', info), flush=True)

t0 = time.time()

# ---------- bracket signs / structure ----------
ok, v = lb(lambda g: comps(g)['B1'], D('0.85'), '1/200');       add('B1(0.85) >= 1/200', ok)
ok, v = ub(lambda g: comps(g)['B1'], D('0.86'), '-1/50');       add('B1(0.86) <= -1/50', ok)
ok, n = der_sign(lambda g: comps(g)['B1'], GLO, GHI, False);    add('B1 decreasing', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['B2']*(-1), GLO, GHI);     add('B2 < 0', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['M']*(-1), GLO, GHI);      add('M < 0', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['B4'], GLO, GHI);          add('B4 > 0', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['G5'], GLO, GHI);          add('G5 > 0', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['Qhi']*(-1), GLO, GHI);    add('Qhi < 0', ok, 'boxes=%d' % n)

# ---------- Qlo / F ----------
ok, v = ub(lambda g: comps(g)['Qlo'], D('1.0014'), '-1/10000'); add('Qlo(1.0014) <= -1/10000', ok)
ok, v = ub(lambda g: comps(g)['Qlo'], GHI, '33/200');           add('Qlo(1.0472) <= 33/200', ok)
ok, n = der_sign(lambda g: comps(g)['Qlo'], GLO, GHI, True);    add('Qlo increasing', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['Fv'], D('1.0014'), GHI, True); add('F increasing [1.0014,1.0472]', ok, 'boxes=%d' % n)
ok, v = ub(lambda g: comps(g)['Fv'], GHI, '63/100');            add('F(1.0472) <= 63/100', ok)

# ---------- m-facts: (t/2) sin(2t) >= 3164/10000 on the track ----------
ok, n = range_pos(lambda g: comps(g)['h_g'] - MC, GLO, GHI);    add('h(gamma) >= 0.3164', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['h_t'] - MC, GLO, GHI);    add('h(tmax)  >= 0.3164', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda t: t*d1_sin(t)*d1_cos(t) - MC, GLO, D('1.30')); add('h(t) >= 0.3164 on [0.655,1.30]', ok, 'boxes=%d' % n)
ok, v = ub(lambda g: comps(g)['tmax'], GHI, '13/10');           add('tau(1.0472) < 13/10', ok)

# ---------- TA monotonicity segments ----------
ok, n = der_sign(lambda g: comps(g)['TA_B2'], GLO, D('0.72'), True);   add('TA(B2) inc [0.655,0.72]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_B2'], D('0.72'), D('0.723'), True); add('TA(B2) inc [0.72,0.723]', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['TA_B2'] - D('27')/D(10), D('0.723'), D('0.724')); add('TA(B2) >= 27/10 on [0.723,0.724]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_B2'], D('0.724'), D('0.73'), False); add('TA(B2) dec [0.724,0.73]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_B2'], D('0.73'), D('0.85'), False);  add('TA(B2) dec [0.73,0.85]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_B2'], D('0.85'), D('0.86'), False);  add('TA(B2) dec [0.85,0.86]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_M'], D('0.85'), D('0.86'), False);   add('TA(M) dec [0.85,0.86]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TA_M'], D('0.86'), GHI, False);         add('TA(M) dec [0.86,1.0472]', ok, 'boxes=%d' % n)

# ---------- TB, TC ----------
ok, n = der_sign(lambda g: comps(g)['TB'], GLO, GHI, False);    add('TB decreasing', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TC'], GLO, D('0.82'), True); add('TC inc [0.655,0.82]', ok, 'boxes=%d' % n)
ok, n = range_pos(lambda g: comps(g)['TC'] - D('19')/D(10), D('0.82'), D('0.83')); add('TC >= 19/10 on [0.82,0.83]', ok, 'boxes=%d' % n)
ok, n = der_sign(lambda g: comps(g)['TC'], D('0.83'), GHI, False); add('TC dec [0.83,1.0472]', ok, 'boxes=%d' % n)

# ---------- endpoint value bounds (E table) ----------
E = [
  ('TA_B2(0.655) >= 11/5',  'TA_B2', '0.655', '11/5', 'lb'),
  ('TA_B2(0.72) >= 13/5',   'TA_B2', '0.72',  '13/5', 'lb'),
  ('TA_B2(0.73) >= 13/5',   'TA_B2', '0.73',  '13/5', 'lb'),
  ('TA_B2(0.82) >= 2',      'TA_B2', '0.82',  '2',    'lb'),
  ('TA_B2(0.83) >= 2',      'TA_B2', '0.83',  '2',    'lb'),
  ('TA_B2(0.85) >= 19/10',  'TA_B2', '0.85',  '19/10','lb'),
  ('TA_B2(0.86) >= 47/25',  'TA_B2', '0.86',  '47/25','lb'),
  ('TA_M(0.86) >= 9/5',     'TA_M',  '0.86',  '9/5',  'lb'),
  ('TA_M(1.0014) >= 3/5',   'TA_M',  '1.0014','3/5',  'lb'),
  ('TA_M(1.0472) >= 3/8',   'TA_M',  GHI,     '3/8',  'lb'),
  ('TB(0.72) >= 3/10',      'TB', '0.72',  '3/10', 'lb'),
  ('TB(0.73) >= 3/10',      'TB', '0.73',  '3/10', 'lb'),
  ('TB(0.82) >= 3/20',      'TB', '0.82',  '3/20', 'lb'),
  ('TB(0.83) >= 3/20',      'TB', '0.83',  '3/20', 'lb'),
  ('TB(0.85) >= 1/10',      'TB', '0.85',  '1/10', 'lb'),
  ('TB(0.86) >= 1/10',      'TB', '0.86',  '1/10', 'lb'),
  ('TB(1.0014) >= 1/25',    'TB', '1.0014','1/25', 'lb'),
  ('TB(1.0472) >= 1/40',    'TB', GHI,     '1/40', 'lb'),
  ('TC(0.655) >= 57/50',    'TC', '0.655', '57/50','lb'),
  ('TC(0.72) >= 3/2',       'TC', '0.72',  '3/2',  'lb'),
  ('TC(0.73) >= 3/2',       'TC', '0.73',  '3/2',  'lb'),
  ('TC(0.85) >= 19/10',     'TC', '0.85',  '19/10','lb'),
  ('TC(0.86) >= 19/10',     'TC', '0.86',  '19/10','lb'),
  ('TC(1.0014) >= 4/3',     'TC', '1.0014','4/3',  'lb'),
  ('TC(1.0472) >= 11/10',   'TC', GHI,     '11/10','lb'),
  ('B4(1.0472) >= 9/25',    'B4',  GHI,     '9/25', 'lb'),
]
for name, key, x, b, kind in E:
    if kind == 'lb':
        ok, v = lb(lambda g, k=key: comps(g)[k], D(x), b)
    else:
        ok, v = ub(lambda g, k=key: comps(g)[k], D(x), b)
    add(name, ok)

# ---------- assembled margin at the corner ----------
F1 = Fraction(3,8) + Fraction(1,40) + Fraction(11,10) - Fraction(63,100)*Fraction(33,200)
print('exact corner margin = %s = %.6f >= 139/100 ? %s' % (F1, float(F1), F1 >= Fraction(139,100)))
print('elapsed %.1fs' % (time.time()-t0))

with open('misc/e1_facts_ledger.json', 'w', encoding='utf-8') as fh:
    json.dump({'facts': results, 'corner_margin': str(F1)}, fh, ensure_ascii=False, indent=1)
print('ledger written: misc/e1_facts_ledger.json')
