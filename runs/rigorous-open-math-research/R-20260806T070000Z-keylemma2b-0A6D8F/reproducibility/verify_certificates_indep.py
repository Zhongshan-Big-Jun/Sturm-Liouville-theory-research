# -*- coding: utf-8 -*-
"""verify_certificates_indep.py -- INDEPENDENT verification of the four box certificates.  v2.

Engine: mpmath.iv (libmp outward-rounded interval arithmetic) + own rigorous atan
(alternating Taylor series on [0,1] with explicit remainder, reduction atan(x) =
pi/2 - atan(1/x) for x > 1) + own sign-safe bisection bracketing of the secular roots.

Checks per certificate:
  (1) tiling: leaves inside declared region, pairwise interior-disjoint, total area
      within 1e-28 of the region area (sliver quantified and reported);
  (2) re-evaluation: every leaf evaluated with the independent engine; the sign
      condition with the stated polarity must hold with margin (this is the rigorous
      certificate-validity criterion, engine-independent);
  (3) consistency: stored enclosure and independent enclosure must overlap (both
      enclose the true value) -- reported, not required to nest;
  (4) point cross-check: exact function values at leaf corners and centre by
      80-digit mpmath (root solves by monotone bisection) must lie inside the
      stored enclosure.

C4 domain constants corrected to the certificate's own region
[2pi/7, 2pi/5 - 1e-3] (the predecessor verify script used a stale upper endpoint).
"""
import json, time
import mpmath as mp
iv = mp.iv

iv.dps = 50
mp.mp.dps = 80

CERTDIR = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility"
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

def _atan_sanity():
    ok = True
    for t in ['0', '0.1', '0.5', '0.9', '1', '2', '5', '100', '1e5']:
        tv = mp.mpf(t)
        r = iv_atan(iv.mpf([tv, tv]))
        exact = mp.atan(tv)
        if not (r.a <= exact <= r.b):
            ok = False
            print('  atan fail t=%s: [%s,%s] vs %s' % (t, r.a, r.b, mp.nstr(exact, 30)))
    # interval sanity
    for (t0, t1) in [('0.2', '0.5'), ('1', '3'), ('0', '10')]:
        r = iv_atan(iv.mpf([mp.mpf(t0), mp.mpf(t1)]))
        e0, e1 = mp.atan(mp.mpf(t0)), mp.atan(mp.mpf(t1))
        if not (r.a <= e0 and e1 <= r.b):
            ok = False
            print('  atan interval fail [%s,%s]: [%s,%s] vs [%s,%s]' % (t0, t1, r.a, r.b, mp.nstr(e0,25), mp.nstr(e1,25)))
    return ok

def load(name):
    with open(CERTDIR + '\\' + name) as f:
        return json.load(f)

def check_tiling(boxes, x0, x1, y0, y1):
    n = len(boxes)
    total = mp.mpf(0)
    for i in range(n):
        a, b, c, d = mp.mpf(boxes[i][0]), mp.mpf(boxes[i][1]), mp.mpf(boxes[i][2]), mp.mpf(boxes[i][3])
        if not (mp.mpf(x0) <= a < b <= mp.mpf(x1) and mp.mpf(y0) <= c < d <= mp.mpf(y1)):
            return False, total, 'leaf %d outside region' % i
        total += (b - a) * (d - c)
        for j in range(i + 1, n):
            a2, b2, c2, d2 = mp.mpf(boxes[j][0]), mp.mpf(boxes[j][1]), mp.mpf(boxes[j][2]), mp.mpf(boxes[j][3])
            if a < b2 and a2 < b and c < d2 and c2 < d:
                return False, total, 'leaves %d,%d overlap' % (i, j)
    target = (mp.mpf(x1) - mp.mpf(x0)) * (mp.mpf(y1) - mp.mpf(y0))
    return abs(total - target) < mp.mpf('1e-28'), total, 'target=%s gap=%s' % (mp.nstr(target, 20), mp.nstr(target - total, 3))

def check_tiling1d(boxes, x0, x1):
    n = len(boxes)
    total = mp.mpf(0)
    for i in range(n):
        a, b = mp.mpf(boxes[i][0]), mp.mpf(boxes[i][1])
        if not (mp.mpf(x0) <= a < b <= mp.mpf(x1)):
            return False, total, 'leaf %d outside region' % i
        total += b - a
        for j in range(i + 1, n):
            a2, b2 = mp.mpf(boxes[j][0]), mp.mpf(boxes[j][1])
            if a < b2 and a2 < b:
                return False, total, 'leaves %d,%d overlap' % (i, j)
    target = mp.mpf(x1) - mp.mpf(x0)
    return abs(total - target) < mp.mpf('1e-28'), total, 'target=%s gap=%s' % (mp.nstr(target, 20), mp.nstr(target - total, 3))

# ---------------- interval re-evaluators ----------------
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

def reeval_c4(vlo, vhi):
    v = iv.mpf([vlo, vhi])
    u = iv.tan(v)
    w = PI_IV - 2.5 * v
    q = iv.sin(v) * iv.cos(w) / (iv.cos(v) * iv.sin(w))
    q2 = q * q; u2 = u * u
    P = 5 * v * q - 3 * u + 2 * v
    t1 = (q2 + u2) * P
    t2 = 1.2 * u * q * (1 + u2)
    return t1 - t2

def f1e_iv(x, c, q):
    return iv_atan(iv.tan(x) / q) - c * (PI_IV / 2 - x)

def fO_iv(g, c, q):
    return iv_atan(q * iv.tan(g)) - c * (PI_IV - g)

def bisect_iv(f, lo, hi, tol, maxit=4000):
    lo = mp.mpf(lo); hi = mp.mpf(hi)
    for _ in range(maxit):
        mid = (lo + hi) / 2
        fm = f(iv.mpf([mid, mid]))
        if fm.a > 0:
            hi = mid
        elif fm.b < 0:
            lo = mid
        else:
            iv.dps = min(iv.dps * 2, 200)
            continue
        if hi - lo < tol:
            break
    return iv.mpf([lo, hi])

def alpha1_box_iv(qlo, qhi, clo, chi, tol=mp.mpf('1e-28')):
    xhi = bisect_iv(lambda x: f1e_iv(x, iv.mpf([chi, chi]), iv.mpf([qhi, qhi])), mp.mpf(0), mp.mpf('1.570796326794896619231321691639751442'), tol)
    xlo = bisect_iv(lambda x: f1e_iv(x, iv.mpf([clo, clo]), iv.mpf([qlo, qlo])), mp.mpf(0), mp.mpf('1.570796326794896619231321691639751442'), tol)
    a1lo = PI_IV / 2 - xhi
    a1hi = PI_IV / 2 - xlo
    return iv.mpf([a1lo.a, a1hi.b])

def alpha2_box_iv(qlo, qhi, clo, chi, tol=mp.mpf('1e-28')):
    glo = bisect_iv(lambda g: fO_iv(g, iv.mpf([chi, chi]), iv.mpf([qlo, qlo])), mp.mpf(0), mp.mpf('1.57079632679489661923'), tol)
    ghi = bisect_iv(lambda g: fO_iv(g, iv.mpf([clo, clo]), iv.mpf([qhi, qhi])), mp.mpf(0), mp.mpf('1.57079632679489661923'), tol)
    a2lo = PI_IV - glo
    a2hi = PI_IV - ghi
    return iv.mpf([a2lo.a, a2hi.b])

def iv_Phi(a, q):
    return iv.cos(a) ** 2 + q * q * iv.sin(a) ** 2

def iv_cot(a):
    return iv.cos(a) / iv.sin(a)

def iv_W(a):
    return 3 + 2 * a * iv_cot(a)

def iv_Wp(a):
    return 2 * (iv.sin(a) * iv.cos(a) - a) / iv.sin(a) ** 2

def iv_Mtilde(a, c, q):
    s = iv.sin(a)
    return a * a * s * s / (q + c * iv_Phi(a, q))

def iv_G(a, c, q):
    Ph = iv_Phi(a, q); W = iv_W(a); D = q + c * Ph
    sc = iv.sin(a) * iv.cos(a)
    K = q * q - 1
    return -Ph * W / D + 2 * c * a * Ph * K * sc / (D * D)

def iv_dGdc(a, c, q):
    Ph = iv_Phi(a, q)
    sc = iv.sin(a) * iv.cos(a)
    K = q * q - 1
    D = q + c * Ph
    W = iv_W(a)
    term1 = Ph * Ph * W / (D * D)
    num2 = 2 * a * Ph * K * sc
    term2 = num2 * (D - 2 * c * Ph) / (D * D * D)
    Gc = term1 + term2
    Pha = 2 * K * sc
    Wp = iv_Wp(a)
    dsc = iv.cos(a) ** 2 - iv.sin(a) ** 2
    d1 = -(Pha * W + Ph * Wp) / D + Ph * W * c * Pha / (D * D)
    N = 2 * c * a * Ph * K * sc
    dN = 2 * c * K * (Ph * a * dsc + Ph * sc + a * Pha * sc)
    d2 = dN / (D * D) - 4 * c * c * a * Ph * K * sc * Pha / (D * D * D)
    Ga = d1 + d2
    ap = -a * Ph / D
    return Ga * ap + Gc

def iv_J(a, c, q):
    return iv_G(a, c, q) ** 2 + iv_dGdc(a, c, q)

def reeval_l4(qlo, qhi, clo, chi):
    a1b = alpha1_box_iv(qlo, qhi, clo, chi)
    a2b = alpha2_box_iv(qlo, qhi, clo, chi)
    c = iv.mpf([clo, chi]); q = iv.mpf([qlo, qhi])
    return iv_dGdc(a2b, c, q) - iv_dGdc(a1b, c, q)

def reeval_l5(qlo, qhi, clo, chi):
    a1b = alpha1_box_iv(qlo, qhi, clo, chi)
    a2b = alpha2_box_iv(qlo, qhi, clo, chi)
    c = iv.mpf([clo, chi]); q = iv.mpf([qlo, qhi])
    M1 = iv_Mtilde(a1b, c, q); M2 = iv_Mtilde(a2b, c, q)
    J1 = iv_J(a1b, c, q); J2 = iv_J(a2b, c, q)
    return M1 * J1 - M2 * J2

# ---------------- exact point evaluators (80-digit mpmath) ----------------
def p_alpha1(c, q):
    lo, hi = mp.mpf('1e-80'), mp.pi / 2
    for _ in range(400):
        mid = (lo + hi) / 2
        fv = mp.atan(1 / (q * mp.tan(mid))) - c * mid
        if fv > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def p_alpha2(c, q):
    lo, hi = mp.mpf('1e-80'), mp.pi
    for _ in range(400):
        mid = (lo + hi) / 2
        if mid == mp.pi / 2:
            ov = mp.pi / 2
        elif mid < mp.pi / 2:
            ov = mp.pi - mp.atan(q * mp.tan(mid))
        else:
            ov = mp.atan(-q * mp.tan(mid))
        fv = ov - c * mid
        if fv > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def p_dM2dq(q, u):
    A = mp.pi - mp.atan(u / q); t = mp.atan(u); S = q * q + u * u
    return (4 * A * A * u + 8 * A * u * u * q / S - 7 * q * q * u / S - 14 * A * q
            - 9 * u ** 3 / S + 2 * u / (1 + u * u) + 4 * A * q / (1 + u * u)
            + t * (4 * u * u / S - 5 - 9 * u * u))

def p_c4(v):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5') * v
    q = mp.sin(v) * mp.cos(w) / (mp.cos(v) * mp.sin(w))
    return (q * q + u * u) * (5 * v * q - 3 * u + 2 * v) - mp.mpf('1.2') * u * q * (1 + u * u)

def p_G(a, c, q):
    Ph = mp.cos(a) ** 2 + q * q * mp.sin(a) ** 2
    D = q + c * Ph
    W = 3 + 2 * a / mp.tan(a)
    return -Ph * W / D + 2 * c * a * Ph * (q * q - 1) * mp.sin(a) * mp.cos(a) / D ** 2

def p_dGdc(a, c, q):
    # total derivative along the curve, 80-digit; same formula as kl2_lib.dGdc
    Ph = mp.cos(a) ** 2 + q * q * mp.sin(a) ** 2
    D = q + c * Ph
    s, co = mp.sin(a), mp.cos(a)
    sc = s * co
    W = 3 + 2 * a / mp.tan(a)
    Gc = Ph * W * Ph / D ** 2 + (2 * a * Ph * (q * q - 1) * s * co) * (D - 2 * c * Ph) / D ** 3
    Pha = 2 * (q * q - 1) * s * co
    Wp = 2 * (s * co - a) / s ** 2
    d1 = -(Pha * W + Ph * Wp) / D + Ph * W * c * Pha / D ** 2
    dsc = co * co - s * s
    d2a = 2 * c * (q * q - 1) * (Ph * a * dsc + Ph * sc + a * Pha * sc) / D ** 2
    d2b = -4 * c * c * a * Ph * (q * q - 1) * sc * Pha / D ** 3
    Ga = d1 + d2a + d2b
    return Ga * (-a * Ph / D) + Gc

def p_Mtilde(a, c, q):
    return a * a * mp.sin(a) ** 2 / (q + c * (mp.cos(a) ** 2 + q * q * mp.sin(a) ** 2))

def p_l4(q, c):
    a1 = p_alpha1(c, q); a2 = p_alpha2(c, q)
    return p_dGdc(a2, c, q) - p_dGdc(a1, c, q)

def p_l5(q, c):
    a1 = p_alpha1(c, q); a2 = p_alpha2(c, q)
    M1 = p_Mtilde(a1, c, q); M2 = p_Mtilde(a2, c, q)
    J1 = p_dGdc(a1, c, q) + p_G(a1, c, q) ** 2
    J2 = p_dGdc(a2, c, q) + p_G(a2, c, q) ** 2
    return M1 * J1 - M2 * J2

# ---------------- runner ----------------
def run(name, reeval, peval, x0, x1, y0, y1, want_neg, dim2=True):
    cert = load(name)
    boxes = cert['boxes']
    t0 = time.time()
    ok, total, msg = check_tiling(boxes, x0, x1, y0, y1) if dim2 else check_tiling1d(boxes, x0, x1)
    print('[%s] leaves=%d tiling_ok=%s (%s)' % (name, len(boxes), ok, msg))
    bad = 0
    worst = None
    overlap_fail = 0
    pt_fail = 0
    for bx in boxes:
        if dim2:
            ivv = reeval(mp.mpf(bx[0]), mp.mpf(bx[1]), mp.mpf(bx[2]), mp.mpf(bx[3]))
            stored = (mp.mpf(bx[4]), mp.mpf(bx[5]))
        else:
            ivv = reeval(mp.mpf(bx[0]), mp.mpf(bx[1]))
            stored = (mp.mpf(bx[2]), mp.mpf(bx[3]))
        # sign condition from the independent engine
        if want_neg:
            if not (ivv.b < 0):
                bad += 1
                print('  SIGN FAIL (need <0) leaf %s: [%s,%s]' % (bx[:4], mp.nstr(ivv.a, 12), mp.nstr(ivv.b, 12)))
            w = ivv.b
            worst = w if worst is None else max(worst, w)
        else:
            if not (ivv.a > 0):
                bad += 1
                print('  SIGN FAIL (need >0) leaf %s: [%s,%s]' % (bx[:4], mp.nstr(ivv.a, 12), mp.nstr(ivv.b, 12)))
            w = ivv.a
            worst = w if worst is None else min(worst, w)
        # overlap of stored and independent enclosures
        if not (stored[0] <= ivv.b and ivv.a <= stored[1]):
            overlap_fail += 1
        # point cross-check: corners and centre
        pts = []
        if dim2:
            qm = (mp.mpf(bx[0]) + mp.mpf(bx[1])) / 2
            cm = (mp.mpf(bx[2]) + mp.mpf(bx[3])) / 2
            pts = [(mp.mpf(bx[0]), mp.mpf(bx[2])), (mp.mpf(bx[0]), mp.mpf(bx[3])),
                   (mp.mpf(bx[1]), mp.mpf(bx[2])), (mp.mpf(bx[1]), mp.mpf(bx[3])), (qm, cm)]
        else:
            vm = (mp.mpf(bx[0]) + mp.mpf(bx[1])) / 2
            pts = [(mp.mpf(bx[0]),), (mp.mpf(bx[1]),), (vm,)]
        for pt in pts:
            val = peval(*pt) if dim2 else peval(pt[0])
            if not (stored[0] <= val <= stored[1]):
                pt_fail += 1
                if pt_fail <= 3:
                    print('  POINT FAIL leaf %s pt=%s: value %s outside stored [%s,%s]' % (bx[:4], pt, mp.nstr(val, 14), mp.nstr(stored[0], 14), mp.nstr(stored[1], 14)))
    print('  independent worst bound: %s  sign failures: %d  overlap failures: %d  point failures: %d  time %.1fs'
          % (mp.nstr(worst, 14), bad, overlap_fail, pt_fail, time.time() - t0))
    return ok and bad == 0 and pt_fail == 0

if __name__ == '__main__':
    print('atan sanity:', _atan_sanity())
    SQRT41 = mp.sqrt(41)
    allok = True
    allok &= run('cert_dM2dq_boxes.json', reeval_dM2dq, p_dM2dq, 1, 20, 0, SQRT41, True)
    allok &= run('cert_c4_boxes.json', reeval_c4, p_c4,
                 mp.mpf('0.897597901025655210989326680937000824056334114107173091707127'),
                 mp.mpf('1.25563706143591729538505735331180115367886775975004232838998'),
                 0, 0, False, dim2=False)
    allok &= run('cert_L4box_boxes.json', reeval_l4, p_l4, 1, 2, '0.4', '0.5', True)
    allok &= run('cert_L5box_boxes.json', reeval_l5, p_l5, 1, 2, '0.4', '0.5', False)
    print('ALL CERTIFICATES INDEPENDENTLY VERIFIED' if allok else 'INDEPENDENT VERIFICATION FAILED')


