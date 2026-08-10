# -*- coding: utf-8 -*-
"""cert_dM2dq_strip.py -- closes the uncovered corner strip of the dM2/dq certificate.

The certificate cert_dM2dq_boxes.json tiles [1,20] x [0, y1] with
  y1 = 6.403124237432848686488217674621813264520,
which is 4.2e-40 BELOW sqrt(41) (y1 is a 40-digit truncation of sqrt(41)).  The
M2 proof needs dM2/dq < 0 on [1,20] x [0, sqrt(41)] (superset of D intersect
{q <= 20}).  This script certifies dM2/dq < 0 on the remaining strip
  [1,20] x [y1, y1 + 1e-30]  (superset of [1,20] x [y1, sqrt(41)]
since sqrt(41) < y1 + 1e-30, verified below by exact squaring), using the same
riarith outward-rounded engine, with a modest q-subdivision.
"""
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext, getcontext
import riarith as R

getcontext().prec = 60
Y1 = Decimal('6.403124237432848686488217674621813264520')
EPS = Decimal('1e-30')
Y2 = Y1 + EPS   # strip upper endpoint

def dM2dq_iv(qlo, qhi, ulo, uhi):
    q = R.Iv(qlo, qhi); u = R.Iv(ulo, uhi)
    A = R.iv_sub(R.PI, R.iv_atan(R.iv_div(u, q)))
    t = R.iv_atan(u)
    S = R.iv_add(R.iv_sqr(q), R.iv_sqr(u))
    q2 = R.iv_sqr(q); u2 = R.iv_sqr(u)
    one = R.Iv.pt(Decimal(1))
    term1 = R.iv_mul(R.iv_mul(R.Iv.pt(Decimal(4)), R.iv_sqr(A)), u)
    term2 = R.iv_div(R.iv_mul(R.Iv.pt(Decimal(8)), R.iv_mul(A, R.iv_mul(u2, q))), S)
    term3 = R.iv_div(R.iv_mul(R.Iv.pt(Decimal(-7)), R.iv_mul(q2, u)), S)
    term4 = R.iv_mul(R.Iv.pt(Decimal(-14)), R.iv_mul(A, q))
    term5 = R.iv_div(R.iv_mul(R.Iv.pt(Decimal(-9)), R.iv_mul(u2, u)), S)
    term6 = R.iv_div(R.iv_mul(R.Iv.pt(Decimal(2)), u), R.iv_add(one, u2))
    term7 = R.iv_div(R.iv_mul(R.Iv.pt(Decimal(4)), R.iv_mul(A, q)), R.iv_add(one, u2))
    br = R.iv_sub(R.iv_sub(R.iv_div(R.iv_mul(R.Iv.pt(Decimal(4)), u2), S), R.Iv.pt(Decimal(5))), R.iv_mul(R.Iv.pt(Decimal(9)), u2))
    acc = R.iv_add(term1, term2); acc = R.iv_add(acc, term3); acc = R.iv_add(acc, term4)
    acc = R.iv_add(acc, term5); acc = R.iv_add(acc, term6); acc = R.iv_add(acc, term7)
    return R.iv_add(acc, R.iv_mul(t, br))

print('=== exact check: sqrt(41) < y1 + 1e-30 ===')
# exact: (y1 + 1e-30)^2 > 41  with 80-digit Decimal arithmetic
with localcontext() as c:
    c.prec = 80
    sq = Y2 * Y2
    print('  (y1+1e-30)^2 =', sq)
    print('  (y1+1e-30)^2 > 41:', sq > 41)

print('=== certified dM2/dq < 0 on [1,20] x [y1, y1+1e-30] ===')
edges = [Decimal(1), Decimal(2), Decimal(3), Decimal(5), Decimal(8), Decimal(12), Decimal(16), Decimal(18), Decimal(19.5), Decimal(19.9), Decimal(20)]
worst_hi = None
boxes = []
with localcontext() as c:
    c.prec = 60
    for i in range(len(edges) - 1):
        iv = dM2dq_iv(edges[i], edges[i+1], Y1, Y2)
        ok = iv.hi < 0
        print('  q in [%s, %s]: [%s, %s]  hi<0: %s' % (edges[i], edges[i+1], iv.lo, iv.hi, ok))
        if not ok:
            raise SystemExit('STRIP CERTIFICATE FAILED')
        boxes.append((str(edges[i]), str(edges[i+1]), str(Y1), str(Y2), str(iv.lo), str(iv.hi)))
        worst_hi = iv.hi if worst_hi is None else max(worst_hi, iv.hi)
print('worst upper bound on the strip:', worst_hi)
json.dump({'region': {'q': ['1', '20'], 'u': [str(Y1), str(Y2)]},
           'n_boxes': len(boxes), 'worst_upper_bound': str(worst_hi), 'boxes': boxes},
          open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T070000Z-keylemma2b-0A6D8F\reproducibility\cert_dM2dq_strip_boxes.json", "w"), indent=1)
print('STRIP CERTIFICATE WRITTEN')
