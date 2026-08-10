# -*- coding: utf-8 -*-
# audit_certificates.py -- independent re-verification of the five KEY LEMMA certificates
# with the audit engine (audit_iv.py + audit_functions.py).  Run:
# R-20260806T140000Z-keylemmaaudit-2F83B1   (patched v2: exact-rational tiling,
#   1-D reeval via Iv(a,b), sliver-bridge check, certified-PI coverage check)
#
# Checks per certificate:
#   (1) tiling: leaves inside the declared region, pairwise interior-disjoint,
#       and (for 2-D) exact coverage of the region by consecutive leaves
#       (exact Fraction arithmetic, no rounding);
#   (2) sign condition re-evaluated with the audit engine on every leaf
#       (the certificate-validity criterion);
#   (3) overlap of the stored enclosure and the audit enclosure (consistency);
#   (4) high-precision point values at leaf corners and centres lie inside the
#       stored enclosure;
#   (5) worst (closest to zero) audit bound.
import sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-keylemmaaudit-2F83B1\reproducibility")
from audit_iv import Iv, PI
import audit_functions as AF
from decimal import Decimal
from fractions import Fraction
import mpmath as mp

PRED = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility"
CERT_MAIN = PRED + r"\cert_dM2dq_boxes.json"
CERT_C4 = PRED + r"\cert_c4_boxes.json"
CERT_L4 = PRED + r"\cert_L4box_boxes.json"
CERT_L5 = PRED + r"\cert_L5box_boxes.json"
CERT_STRIP = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T070000Z-keylemma2b-0A6D8F\reproducibility\cert_dM2dq_strip_boxes.json"

def load(name):
    with open(name, encoding="utf-8") as f:
        return json.load(f)

def F(x):
    return Fraction(Decimal(x))

def check_tiling2d(boxes, x0, x1, y0, y1):
    """Exact coverage check: leaves inside [x0,x1]x[y0,y1], pairwise
    interior-disjoint, and total area equals the region area (exact rational
    arithmetic).  For a finite union of closed boxes inside a closed box, area
    equality + containment + interior-disjointness implies the union covers the
    region: the uncovered part is relatively open and has measure zero, hence
    empty.  (No row-alignment assumption: the certificate leaves are not a
    tensor-product partition.)"""
    n = len(boxes)
    X0, X1, Y0, Y1 = F(x0), F(x1), F(y0), F(y1)
    rects = []
    for i in range(n):
        a, b, c, d = F(boxes[i][0]), F(boxes[i][1]), F(boxes[i][2]), F(boxes[i][3])
        if not (X0 <= a < b <= X1 and Y0 <= c < d <= Y1):
            return False, 'leaf %d outside region' % i
        rects.append((a, b, c, d, i))
    for i in range(n):
        for j in range(i + 1, n):
            a, b, c, d, _ = rects[i]
            a2, b2, c2, d2, _ = rects[j]
            if a < b2 and a2 < b and c < d2 and c2 < d:
                return False, 'leaves %d,%d overlap' % (i, j)
    total = sum((b - a) * (d - c) for a, b, c, d, _ in rects)
    target = (X1 - X0) * (Y1 - Y0)
    if total != target:
        return False, 'area mismatch: total=%s target=%s' % (total, target)
    return True, 'exact area tiling of [%s,%s]x[%s,%s] (area %s)' % (x0, x1, y0, y1, target)

def check_tiling1d(boxes, x0, x1):
    X0, X1 = F(x0), F(x1)
    leaves = sorted((F(b[0]), F(b[1])) for b in boxes)
    gaps = []
    cur = X0
    for (a, b) in leaves:
        if not (X0 <= a < b <= X1):
            return False, 'leaf outside region', gaps
        if a > cur:
            gaps.append(a - cur)
        cur = max(cur, b)
    if cur > X1:
        return False, 'leaf beyond region end', gaps
    return True, 'leaves inside [%s,%s]; trailing gap=%s' % (x0, x1, X1 - cur), gaps

mp.mp.dps = 80

def p_alpha1(c, q):
    def f1(x): return mp.atan(mp.tan(x)/q) - c*(mp.pi/2 - x)
    xr = mp.findroot(f1, (mp.mpf('1e-12'), mp.mpf('1.5707')), tol=mp.mpf('1e-60'))
    return mp.pi/2 - xr

def p_alpha2(c, q):
    def fO(g): return mp.atan(q*mp.tan(g)) - c*(mp.pi - g)
    gr = mp.findroot(fO, (mp.mpf('1e-12'), mp.mpf('1.5707')), tol=mp.mpf('1e-60'))
    return mp.pi - gr

def p_Phi(a, q): return mp.cos(a)**2 + q*q*mp.sin(a)**2
def p_W(a): return 3 + 2*a/mp.tan(a)

def p_G(a, c, q):
    Ph = p_Phi(a, q); D = q + c*Ph
    return -Ph*p_W(a)/D + 2*c*a*Ph*(q*q-1)*mp.sin(a)*mp.cos(a)/D**2

def p_dGdc(a, c, q):
    Ph = p_Phi(a, q); D = q + c*Ph
    s, co = mp.sin(a), mp.cos(a); sc = s*co
    W = p_W(a); K = q*q - 1
    Gc = Ph*Ph*W/D**2 + (2*a*Ph*K*sc)*(D - 2*c*Ph)/D**3
    Pha = 2*K*sc
    Wp = 2*(sc - a)/s**2
    d1 = -(Pha*W + Ph*Wp)/D + Ph*W*c*Pha/D**2
    dsc = co*co - s*s
    d2a = 2*c*K*(Ph*a*dsc + Ph*sc + a*Pha*sc)/D**2
    d2b = -4*c*c*a*Ph*K*sc*Pha/D**3
    Ga = d1 + d2a + d2b
    return Ga*(-a*Ph/D) + Gc

def p_Mtilde(a, c, q):
    return a*a*mp.sin(a)**2/(q + c*p_Phi(a, q))

def p_dM2dq(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u); S = q*q + u*u
    return (4*A*A*u + 8*A*u*u*q/S - 7*q*q*u/S - 14*A*q - 9*u**3/S
            + 2*u/(1+u*u) + 4*A*q/(1+u*u) + t*(4*u*u/S - 5 - 9*u*u))

def p_K(v):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u)

def p_Hp(q, c):
    a1 = p_alpha1(c, q); a2 = p_alpha2(c, q)
    return p_dGdc(a2, c, q) - p_dGdc(a1, c, q)

def p_Fpp(q, c):
    a1 = p_alpha1(c, q); a2 = p_alpha2(c, q)
    M1 = p_Mtilde(a1, c, q); M2 = p_Mtilde(a2, c, q)
    J1 = p_dGdc(a1, c, q) + p_G(a1, c, q)**2
    J2 = p_dGdc(a2, c, q) + p_G(a2, c, q)**2
    return M1*J1 - M2*J2

def run2d(name, reeval, peval, x0, x1, y0, y1, want_neg):
    cert = load(name)
    boxes = cert['boxes']
    t0 = time.time()
    ok, msg = check_tiling2d(boxes, x0, x1, y0, y1)
    print('[%s] leaves=%d tiling=%s (%s)' % (name.split('\\')[-1], len(boxes), ok, msg))
    bad = 0; overlap = 0; ptfail = 0
    worst = None
    for bx in boxes:
        qlo, qhi, ulo, uhi = Decimal(bx[0]), Decimal(bx[1]), Decimal(bx[2]), Decimal(bx[3])
        ivv = reeval(qlo, qhi, ulo, uhi)
        stored = (Decimal(bx[4]), Decimal(bx[5]))
        if want_neg:
            if not (ivv.hi < 0):
                bad += 1
                print('  SIGN FAIL leaf', bx[:4], mp.nstr(mp.mpf(str(ivv.lo)),12), mp.nstr(mp.mpf(str(ivv.hi)),12))
            w = ivv.hi
            worst = w if worst is None else max(worst, w)
        else:
            if not (ivv.lo > 0):
                bad += 1
                print('  SIGN FAIL leaf', bx[:4], mp.nstr(mp.mpf(str(ivv.lo)),12), mp.nstr(mp.mpf(str(ivv.hi)),12))
            w = ivv.lo
            worst = w if worst is None else min(worst, w)
        if not (stored[0] <= ivv.hi and ivv.lo <= stored[1]):
            overlap += 1
        qm = (qlo + qhi)/2; cm = (ulo + uhi)/2
        pts = [(qlo, ulo), (qlo, uhi), (qhi, ulo), (qhi, uhi), (qm, cm)]
        for (qq, cc) in pts:
            val = peval(mp.mpf(str(qq)), mp.mpf(str(cc)))
            if not (stored[0] <= Decimal(str(val)) <= stored[1]):
                ptfail += 1
    print('  audit worst bound: %s  sign failures: %d  overlap failures: %d  point failures: %d  time %.1fs'
          % (mp.nstr(mp.mpf(str(worst)), 16), bad, overlap, ptfail, time.time()-t0))
    return ok and bad == 0 and ptfail == 0

def run1d(name, reeval, peval, x0, x1, want_pos, eps=None):
    cert = load(name)
    boxes = cert['boxes']
    t0 = time.time()
    ok, msg, gaps = check_tiling1d(boxes, x0, x1)
    print('[%s] leaves=%d tiling=%s (%s)' % (name.split('\\')[-1], len(boxes), ok, msg))
    print('  internal gaps: count=%d total=%s max=%s' % (len(gaps), sum(gaps, Fraction(0)), max(gaps) if gaps else Fraction(0)))
    bad = 0; overlap = 0; ptfail = 0
    worst = None
    for bx in boxes:
        a, b = Decimal(bx[0]), Decimal(bx[1])
        if eps is None:
            ivv = reeval(Iv(a, b))
        else:
            ivv = reeval(Iv(a - eps, b + eps))
        stored = (Decimal(bx[2]), Decimal(bx[3]))
        if want_pos:
            if not (ivv.lo > 0):
                bad += 1
                print('  SIGN FAIL leaf', bx[:2], mp.nstr(mp.mpf(str(ivv.lo)),12), mp.nstr(mp.mpf(str(ivv.hi)),12))
            w = ivv.lo
            worst = w if worst is None else min(worst, w)
        else:
            if not (ivv.hi < 0):
                bad += 1
                print('  SIGN FAIL leaf', bx[:2], mp.nstr(mp.mpf(str(ivv.lo)),12), mp.nstr(mp.mpf(str(ivv.hi)),12))
            w = ivv.hi
            worst = w if worst is None else max(worst, w)
        if not (stored[0] <= ivv.hi and ivv.lo <= stored[1]):
            overlap += 1
        vm = (a + b)/2
        for vv in [a, b, vm]:
            val = peval(mp.mpf(str(vv)))
            if not (stored[0] <= Decimal(str(val)) <= stored[1]):
                ptfail += 1
    print('  audit worst bound: %s  sign failures: %d  overlap failures: %d  point failures: %d  time %.1fs'
          % (mp.nstr(mp.mpf(str(worst)), 16), bad, overlap, ptfail, time.time()-t0))
    return ok and bad == 0 and ptfail == 0

if __name__ == '__main__':
    SQRT41 = '6.403124237432848686488217674621813264520'
    SQRT41_HI = '6.403124237432848686488217674622813264520'
    allok = True
    allok &= run2d(CERT_MAIN, AF.iv_dM2dq, p_dM2dq, 1, 20, 0, SQRT41, True)
    allok &= run2d(CERT_STRIP, AF.iv_dM2dq, p_dM2dq, 1, 20, SQRT41, SQRT41_HI, True)
    # strip: exact squaring certificate (y1+1e-30)^2 > 41
    y1p = Fraction(Decimal(SQRT41_HI))
    print('[strip] (y1+1e-30)^2 = %s > 41 : %s' % (y1p**2, y1p**2 > 41))
    allok &= (y1p**2 > 41)
    # C4: leaf union [first_lo, last_hi]; coverage of [2pi/7, 2pi/5-1e-3] via certified PI
    c4 = load(CERT_C4)
    c4_first = c4['boxes'][0][0]
    c4_last = c4['boxes'][-1][1]
    allok &= run1d(CERT_C4, AF.iv_K, p_K, c4_first, c4_last, True, eps=Decimal('1e-58'))
    two_pi_7_lo = AF.iv_div(AF.iv_mul_d(PI, 2), Iv.pt(7)).lo
    two_pi_5_m1em3_hi = AF.iv_sub(AF.iv_mul_d(PI, Decimal('0.4')), Iv.pt(Decimal('0.001'))).hi
    print('[c4 coverage] iv(2pi/7).lo = %s >= first_lo %s : %s' % (two_pi_7_lo, c4_first, two_pi_7_lo >= Decimal(c4_first)))
    print('[c4 coverage] iv(2pi/5-1e-3).hi = %s <= last_hi %s : %s' % (two_pi_5_m1em3_hi, c4_last, two_pi_5_m1em3_hi <= Decimal(c4_last)))
    allok &= (two_pi_7_lo >= Decimal(c4_first)) and (two_pi_5_m1em3_hi <= Decimal(c4_last))
    # sliver bridge: consecutive leaves must satisfy a_{i+1}-b_i < 2*eps so that
    # the eps-inflated boxes overlap and the union covers [first-eps, last+eps].
    leaves = sorted((F(b[0]), F(b[1])) for b in c4['boxes'])
    maxgap = Fraction(0)
    for i in range(1, len(leaves)):
        g = leaves[i][0] - leaves[i-1][1]
        if g > maxgap:
            maxgap = g
    eps = Fraction(1, 10**58)
    print('[c4 sliver bridge] max gap = %s < 2*eps = %s : %s' % (maxgap, 2*eps, maxgap < 2*eps))
    allok &= (maxgap < 2*eps)
    allok &= run2d(CERT_L4, AF.iv_Hp_box, p_Hp, 1, 2, '0.4', '0.5', True)
    allok &= run2d(CERT_L5, AF.iv_Fpp_box, p_Fpp, 1, 2, '0.4', '0.5', False)
    print('ALL FIVE CERTIFICATES INDEPENDENTLY RE-VERIFIED (audit engine)' if allok else 'AUDIT RE-VERIFICATION FAILED')
