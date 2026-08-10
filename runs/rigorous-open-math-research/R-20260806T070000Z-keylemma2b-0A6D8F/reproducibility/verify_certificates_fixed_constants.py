# -*- coding: utf-8 -*-
"""verify_certificates.py -- independent verification of all four box certificates.

For each certificate JSON:
  1. pairwise interior-disjointness of the leaves and total-measure match with the
     declared region (so the leaves tile the region);
  2. independent re-evaluation of every leaf with the riarith engine (sound
     outward-rounded interval arithmetic) and the sign condition;
  3. worst (closest to zero) bound over all leaves.

Notation: each leaf is [a,b,c,d,lo,hi] with (a,b) the first coordinate, (c,d) the
second, and [lo,hi] the stored interval enclosure of the certified quantity.
"""
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext
import riarith as R
import rigorous as RG
import sound_bracket as SB
import mpmath as mp
mp.mp.dps = 60

RUN = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility"
BRACK_TOL = Decimal('1e-12')

def load(name):
    with open(RUN + '\\' + name) as f:
        return json.load(f)

def area1(x0, x1): return Decimal(x1) - Decimal(x0)

def check_tiling(boxes, x0, x1, y0, y1, want_neg):
    """boxes: list of [a,b,c,d,lo,hi].  Returns (ok, total_area, message)."""
    n = len(boxes)
    total = Decimal(0)
    for i in range(n):
        a, b, c, d = Decimal(boxes[i][0]), Decimal(boxes[i][1]), Decimal(boxes[i][2]), Decimal(boxes[i][3])
        if not (Decimal(x0) <= a < b <= Decimal(x1) and Decimal(y0) <= c < d <= Decimal(y1)):
            return False, total, 'leaf %d outside region' % i
        total += (b - a) * (d - c)
        for j in range(i+1, n):
            a2, b2, c2, d2 = Decimal(boxes[j][0]), Decimal(boxes[j][1]), Decimal(boxes[j][2]), Decimal(boxes[j][3])
            if a < b2 and a2 < b and c < d2 and c2 < d:
                return False, total, 'leaves %d,%d overlap' % (i, j)
    target = (Decimal(x1) - Decimal(x0)) * (Decimal(y1) - Decimal(y0))
    return abs(total - target) <= Decimal('1e-30'), total, 'target=%s' % target

def check_tiling1d(boxes, x0, x1):
    n = len(boxes)
    total = Decimal(0)
    for i in range(n):
        a, b = Decimal(boxes[i][0]), Decimal(boxes[i][1])
        if not (Decimal(x0) <= a < b <= Decimal(x1)):
            return False, total, 'leaf %d outside region' % i
        total += b - a
        for j in range(i+1, n):
            a2, b2 = Decimal(boxes[j][0]), Decimal(boxes[j][1])
            if a < b2 and a2 < b:
                return False, total, 'leaves %d,%d overlap' % (i, j)
    target = Decimal(x1) - Decimal(x0)
    return abs(total - target) <= Decimal('1e-30'), total, 'target=%s' % target

def reeval_dM2dq(qlo, qhi, ulo, uhi):
    q = R.Iv(Decimal(qlo), Decimal(qhi)); u = R.Iv(Decimal(ulo), Decimal(uhi))
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

def reeval_c4(vlo, vhi):
    v = R.Iv(Decimal(vlo), Decimal(vhi))
    u = R.iv_tan(v)
    w = R.iv_sub(R.PI, R.iv_mul(R.Iv.pt(Decimal('2.5')), v))
    q = R.iv_div(R.iv_mul(R.iv_sin(v), R.iv_cos(w)), R.iv_mul(R.iv_cos(v), R.iv_sin(w)))
    q2 = R.iv_sqr(q); u2 = R.iv_sqr(u)
    P = R.iv_add(R.iv_add(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal(5)), v), q), R.iv_mul(R.Iv.pt(Decimal(-3)), u)), R.iv_mul(R.Iv.pt(Decimal(2)), v))
    t1 = R.iv_mul(R.iv_add(q2, u2), P)
    t2 = R.iv_mul(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal('1.2')), u), q), R.iv_add(R.Iv.pt(Decimal(1)), u2))
    return R.iv_sub(t1, t2)

def reeval_l4(qlo, qhi, clo, chi):
    a1b = SB.alpha1_box(Decimal(qlo), Decimal(qhi), Decimal(clo), Decimal(chi), BRACK_TOL)
    a2b = SB.alpha2_box(Decimal(qlo), Decimal(qhi), Decimal(clo), Decimal(chi), BRACK_TOL)
    c = R.Iv(Decimal(clo), Decimal(chi)); q = R.Iv(Decimal(qlo), Decimal(qhi))
    return R.iv_sub(RG.iv_dGdc(a2b, c, q), RG.iv_dGdc(a1b, c, q))

def reeval_l5(qlo, qhi, clo, chi):
    a1b = SB.alpha1_box(Decimal(qlo), Decimal(qhi), Decimal(clo), Decimal(chi), BRACK_TOL)
    a2b = SB.alpha2_box(Decimal(qlo), Decimal(qhi), Decimal(clo), Decimal(chi), BRACK_TOL)
    c = R.Iv(Decimal(clo), Decimal(chi)); q = R.Iv(Decimal(qlo), Decimal(qhi))
    M1 = RG.iv_Mtilde(a1b, c, q); M2 = RG.iv_Mtilde(a2b, c, q)
    J1 = RG.iv_J(a1b, c, q); J2 = RG.iv_J(a2b, c, q)
    return R.iv_sub(R.iv_mul(M1, J1), R.iv_mul(M2, J2))

def run(name, reeval, x0, x1, y0, y1, want_neg, dim2=True):
    cert = load(name)
    boxes = cert['boxes']
    ok, total, msg = check_tiling(boxes, x0, x1, y0, y1, want_neg) if dim2 else check_tiling1d(boxes, x0, x1)
    print('[%s] leaves=%d tiling_ok=%s (%s)' % (name, len(boxes), ok, msg))
    worst = None
    bad = 0
    with localcontext() as c:
        c.prec = 60
        for bx in boxes:
            iv = reeval(*bx[:4]) if dim2 else reeval(*bx[:2])
            stored = (Decimal(bx[4]), Decimal(bx[5])) if dim2 else (Decimal(bx[2]), Decimal(bx[3]))
            if not (stored[0] <= iv.lo and iv.hi <= stored[1]):
                bad += 1
                print('  BAD ENCLOSURE on leaf %s: stored [%s,%s] vs reeval [%s,%s]' % (bx[:4], stored[0], stored[1], iv.lo, iv.hi))
            if want_neg:
                if not (iv.hi < 0):
                    bad += 1
                    print('  SIGN FAIL (need <0) on leaf %s: [%s,%s]' % (bx[:4], iv.lo, iv.hi))
                w = iv.hi
                worst = w if worst is None else max(worst, w)
            else:
                if not (iv.lo > 0):
                    bad += 1
                    print('  SIGN FAIL (need >0) on leaf %s: [%s,%s]' % (bx[:4], iv.lo, iv.hi))
                w = iv.lo
                worst = w if worst is None else min(worst, w)
    print('  re-evaluated worst bound:', worst, ' failures:', bad)
    return ok and bad == 0

if __name__ == '__main__':
    allok = True
    allok &= run('cert_dM2dq_boxes.json', reeval_dM2dq, 1, 20, 0, '6.403124237432848686488217674621813264520', True)
    allok &= run('cert_c4_boxes.json', reeval_c4, '0.897597901025655210989326680937000824056334114107173091707127', '1.25563706143591729538505735331180115367886775975004232838998', 0, 0, False, dim2=False)
    allok &= run('cert_L4box_boxes.json', reeval_l4, 1, 2, '0.4', '0.5', True)
    allok &= run('cert_L5box_boxes.json', reeval_l5, 1, 2, '0.4', '0.5', False)
    print('ALL CERTIFICATES VERIFIED' if allok else 'CERTIFICATE VERIFICATION FAILED')






