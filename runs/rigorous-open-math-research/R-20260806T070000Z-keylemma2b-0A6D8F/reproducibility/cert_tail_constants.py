# -*- coding: utf-8 -*-
"""cert_tail_constants.py -- rigorous (outward-rounded) enclosure of the C4 tail
constants and the C4 certificate coverage, using the riarith engine.

Checks, all with Decimal directed rounding (ROUND_FLOOR / ROUND_CEILING):
  A. PI recomputed by Machin at prec 90 (nterms 80), certified enclosure.
  B. Coverage: certificate leaves (closed boxes) contain [2pi/7, 2pi/5 - 1e-3]:
       iv(2pi/7).lo >= cert_v_lo and iv(2pi/5 - 1e-3).hi <= cert_v_hi.
  C. Sliver bridge: the stored 1-D leaf endpoints are not exactly contiguous at
     the printed 60-digit precision (gaps <= 1e-59, total 6.25e-58); every leaf
     is re-evaluated on the epsilon-inflated box [a-eps, b+eps], eps = 1e-58,
     and K > 0 must hold on the inflated box, so the slivers are covered too.
  D. Tail constants on [2pi/5 - 1e-3, 2pi/5):
       v >= 1.25,  u = tan(v) in (3.06, 3.08),  T = tan(pi - 2.5v) <= 2.50002e-3,
       all certified by iv_tan on rigorous enclosures of the endpoints.
  E. Exact rational lower bound for T^3 K > 0 (Fractions, no rounding).
"""
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, getcontext, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import riarith as R

getcontext().prec = 90
CERT = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\cert_c4_boxes.json"

def iv_floor(x):  # x: Decimal
    with localcontext() as c:
        c.rounding = ROUND_FLOOR
        return x
def iv_ceil(x):
    with localcontext() as c:
        c.rounding = ROUND_CEILING
        return x

def pi_iv_high(nterms=80):
    a5 = R.atan_taylor_series(R.Iv.pt(Decimal(1)/5), nterms)
    a239 = R.atan_taylor_series(R.Iv.pt(Decimal(1)/239), nterms)
    return R.iv_sub(R.iv_mul_d(a5, 16), R.iv_mul_d(a239, 4))

ok_all = True
def report(name, ok, detail=''):
    global ok_all
    ok_all = ok_all and ok
    print('[%s] %s  %s' % ('PASS' if ok else 'FAIL', name, detail))

print('=== A. certified pi (Machin, prec 90, nterms 80) ===')
PI = pi_iv_high(80)
# sanity: pi in (3.1415926535897932384626, 3.1415926535897932384627)
report('PI enclosure sanity', Decimal('3.1415926535897932384626') < PI.lo and PI.hi < Decimal('3.1415926535897932384627'),
       'PI.lo=%s PI.hi=%s' % (PI.lo, PI.hi))

print('=== B. C4 certificate covers [2pi/7, 2pi/5 - 1e-3] ===')
with open(CERT) as f:
    cert = json.load(f)
boxes = cert['boxes']
cert_v_lo = Decimal(boxes[0][0])
cert_v_hi = Decimal(boxes[-1][1])
two_pi_7 = R.iv_div(R.iv_mul_d(PI, 2), R.Iv.pt(7))
two_pi_5_m1em3 = R.iv_sub(R.iv_mul_d(PI, Decimal('0.4')), R.Iv.pt(Decimal('0.001')))
report('iv(2pi/7).lo >= cert_v_lo', two_pi_7.lo >= cert_v_lo,
       'iv(2pi/7) = [%s, %s], cert_v_lo = %s' % (two_pi_7.lo, two_pi_7.hi, cert_v_lo))
report('iv(2pi/5-1e-3).hi <= cert_v_hi', two_pi_5_m1em3.hi <= cert_v_hi,
       'iv(2pi/5-1e-3) = [%s, %s], cert_v_hi = %s' % (two_pi_5_m1em3.lo, two_pi_5_m1em3.hi, cert_v_hi))

print('=== C. sliver bridge: epsilon-inflated re-evaluation of K on every leaf ===')
def K_iv(v):
    u = R.iv_tan(v)
    w = R.iv_sub(R.PI, R.iv_mul(R.Iv.pt(Decimal('2.5')), v))
    q = R.iv_div(R.iv_mul(R.iv_sin(v), R.iv_cos(w)), R.iv_mul(R.iv_cos(v), R.iv_sin(w)))
    q2 = R.iv_sqr(q); u2 = R.iv_sqr(u)
    P = R.iv_add(R.iv_add(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal(5)), v), q),
                          R.iv_mul(R.Iv.pt(-3), u)),
                 R.iv_mul(R.Iv.pt(Decimal(2)), v))
    t1 = R.iv_mul(R.iv_add(q2, u2), P)
    t2 = R.iv_mul(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal('1.2')), u), q), R.iv_add(R.Iv.pt(1), u2))
    return R.iv_sub(t1, t2)
EPS = Decimal('1e-58')
max_gap = Decimal(0)
total_gap = Decimal(0)
with localcontext() as c:
    c.prec = 60
    leaves = sorted((Decimal(b[0]), Decimal(b[1])) for b in boxes)
    for i in range(1, len(leaves)):
        g = leaves[i][0] - leaves[i-1][1]
        if g > 0:
            max_gap = max(max_gap, g)
            total_gap += g
print('  max gap %.1e  total gap %.2e  (EPS = 1e-58 >= max gap: %s)' % (max_gap, total_gap, EPS >= max_gap))
bad = 0
worst_lo = None
for (a, b) in leaves:
    iv = K_iv(R.Iv(a - EPS, b + EPS))
    if not (iv.lo > 0):
        bad += 1
        print('  INFLATED SIGN FAIL on [%s, %s]: [%s, %s]' % (a, b, iv.lo, iv.hi))
    worst_lo = iv.lo if worst_lo is None else min(worst_lo, iv.lo)
report('K > 0 on all eps-inflated leaves', bad == 0,
       'inflated worst lower bound = %s' % worst_lo)

print('=== D. tail constants ===')
vmin_iv = R.iv_sub(R.iv_mul_d(PI, Decimal('0.4')), R.Iv.pt(Decimal('0.001')))   # 2pi/5 - 1e-3
vmax_iv = R.iv_mul_d(PI, Decimal('0.4'))                                # 2pi/5
u_at_vmin = R.iv_tan(vmin_iv)
u_at_vmax = R.iv_tan(vmax_iv)
T_at_wmax = R.iv_tan(R.Iv.pt(Decimal('2.5e-3')))
report('v >= 1.25 on tail (2pi/5-1e-3 > 1.25)', vmin_iv.lo > Decimal('1.25'),
       'vmin iv = [%s, %s]' % (vmin_iv.lo, vmin_iv.hi))
report('tan(2pi/5-1e-3) > 3.06', u_at_vmin.lo > Decimal('3.06'),
       'tan(vmin) iv = [%s, %s]' % (u_at_vmin.lo, u_at_vmin.hi))
report('tan(2pi/5) < 3.08', u_at_vmax.hi < Decimal('3.08'),
       'tan(vmax) iv = [%s, %s]' % (u_at_vmax.lo, u_at_vmax.hi))
report('tan(2.5e-3) <= 2.50002e-3', T_at_wmax.hi <= Decimal('2.50002e-3'),
       'tan(2.5e-3) iv = [%s, %s]' % (T_at_wmax.lo, T_at_wmax.hi))

print('=== E. exact rational lower bound for T^3 K on the tail ===')
# T^3 K = 5 v u^3 (1+T^2) - 3 u^3 T (1+T^2) + 2 v u^2 T (1+T^2) - 1.2 u^2 (1+u^2) T^2
# >= 5 (5/4) (153/50)^3 - 3 (77/25)^3 Tmax (1+Tmax^2) - (6/5) (77/25)^2 (1+(77/25)^2) Tmax^2
v0 = Fraction(5, 4)
umin = Fraction(153, 50)
umax = Fraction(77, 25)
Tmax = Fraction(125001, 50000000)
term1 = 5 * v0 * umin**3
term2 = 3 * umax**3 * Tmax * (1 + Tmax**2)
term4 = Fraction(6, 5) * umax**2 * (1 + umax**2) * Tmax**2
LB = term1 - term2 - term4
report('exact rational LB(T^3 K) > 0', LB > 0,
       'LB = %s = %s' % (LB, float(LB)))
print('  term1 = %s, term2 = %s, term4 = %s' % (float(term1), float(term2), float(term4)))
print('ALL TAIL/CONSTANT CHECKS PASS' if ok_all else 'TAIL/CONSTANT CHECKS FAILED')
