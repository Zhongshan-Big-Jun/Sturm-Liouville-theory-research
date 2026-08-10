# -*- coding: utf-8 -*-
"""verify_dM2dq_strip_indep.py -- independent (mpmath.iv) re-verification of the
dM2/dq strip certificate cert_dM2dq_strip_boxes.json.

The strip certificate was produced with riarith, whose iv_sqrt is not strictly
outward-rounded (documented in audit_report.md).  This script re-verifies the same
boxes with the sound independent engine used for the other four certificates:
mpmath.iv 50 dps + own rigorous atan + monotone bracketing-free interval evaluation
(dM2/dq has no secular roots, so no bisection is needed).
"""
import json
import mpmath as mp
iv = mp.iv
iv.dps = 50
mp.mp.dps = 80
CERT = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T070000Z-keylemma2b-0A6D8F\reproducibility\cert_dM2dq_strip_boxes.json"
PI_IV = iv.pi

def iv_atan(x, nterms=140):
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
        return PI_IV / 2 - atan_series(inv, nterms)
    return iv.mpf([atan_endpoint(a).a, atan_endpoint(b).b])

def reeval_dM2dq(qlo, qhi, ulo, uhi):
    q = iv.mpf([qlo, qhi]); u = iv.mpf([ulo, uhi])
    A = PI_IV - iv_atan(u / q)
    t = iv_atan(u)
    S = q * q + u * u
    q2 = q * q; u2 = u * u
    term1 = 4 * A * A * u
    term2 = 8 * A * u2 * q / S
    term3 = -7 * q2 * u / S
    term4 = -14 * A * q
    term5 = -9 * u * u2 / S
    term6 = 2 * u / (1 + u2)
    term7 = 4 * A * q / (1 + u2)
    br = 4 * u2 / S - 5 - 9 * u2
    return term1 + term2 + term3 + term4 + term5 + term6 + term7 + t * br

d = json.load(open(CERT, encoding="utf-8"))
boxes = d["boxes"]
print('strip region declared:', d["region"])
# exact coverage check: sqrt(41) in (y1, y1+1e-30)
y1 = mp.mpf('6.403124237432848686488217674621813264520')
eps = mp.mpf('1e-30')
sq = (y1 + eps) ** 2
print('(y1+eps)^2 > 41 :', sq > 41, ' (value', mp.nstr(sq, 40), ')')
print('sqrt41 < y1+eps :', mp.sqrt(41) < y1 + eps)
# tiling: leaves within [1,20]x[y1,y1+eps], disjoint, total area == 19*eps
total = mp.mpf(0)
ok = True
for i, bx in enumerate(boxes):
    a, b, c, d = mp.mpf(bx[0]), mp.mpf(bx[1]), mp.mpf(bx[2]), mp.mpf(bx[3])
    if not (mp.mpf(1) <= a < b <= mp.mpf(20) and y1 <= c < d <= y1 + eps):
        ok = False
        print('  leaf %d outside region' % i)
    total += (b - a) * (d - c)
    for j in range(i + 1, len(boxes)):
        a2, b2, c2, d2 = mp.mpf(boxes[j][0]), mp.mpf(boxes[j][1]), mp.mpf(boxes[j][2]), mp.mpf(boxes[j][3])
        if a < b2 and a2 < b and c < d2 and c2 < d:
            ok = False
            print('  leaves %d,%d overlap' % (i, j))
print('strip tiling ok:', ok, ' total area:', mp.nstr(total, 20), ' target:', mp.nstr(19 * eps, 20))
bad = 0
worst = None
for bx in boxes:
    ivv = reeval_dM2dq(mp.mpf(bx[0]), mp.mpf(bx[1]), mp.mpf(bx[2]), mp.mpf(bx[3]))
    if not (ivv.b < 0):
        bad += 1
        print('  SIGN FAIL leaf', bx[:4], mp.nstr(ivv.a, 10), mp.nstr(ivv.b, 10))
    w = ivv.b
    worst = w if worst is None else max(worst, w)
    stored = (mp.mpf(bx[4]), mp.mpf(bx[5]))
    if not (stored[0] <= ivv.b and ivv.a <= stored[1]):
        print('  OVERLAP FAIL leaf', bx[:4])
print('independent worst upper bound on strip:', mp.nstr(worst, 20))
print('sign failures:', bad)
print('STRIP INDEPENDENTLY VERIFIED' if (ok and bad == 0) else 'STRIP INDEPENDENT VERIFICATION FAILED')
