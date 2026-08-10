# -*- coding: utf-8 -*-
"""test_rigorous.py -- verify rigorous bracketing and interval evaluations."""
import sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import rigorous as R
import kl2_lib as L
import mpmath as mp
from decimal import Decimal
mp.mp.dps = 50

def d(x): return Decimal(str(x))

print('=== alpha brackets vs mpmath ===')
ok = True
for (c, q) in [('0.4', '1.05'), ('0.5', '2.0'), ('0.1', '2.0'), ('0.49', '1.5')]:
    c_d, q_d = Decimal(c), Decimal(q)
    xb = R.bracket_x1(c_d, q_d)
    gb = R.bracket_gamma(c_d, q_d)
    a1_true = L.alpha1(mp.mpf(c), mp.mpf(q))
    a2_true = L.alpha2(mp.mpf(c), mp.mpf(q))
    a1_iv = R.iv_sub(R.HALF_PI_IV, xb)
    a2_iv = R.iv_sub(R.PI, gb)
    ok1 = a1_iv.lo <= d(a1_true) <= a1_iv.hi
    ok2 = a2_iv.lo <= d(a2_true) <= a2_iv.hi
    ok &= ok1 and ok2
    print('  c=%s q=%s: a1 in [%s, %s] ok=%s ; a2 in [%s, %s] ok=%s' %
          (c, q, a1_iv.lo, a1_iv.hi, ok1, a2_iv.lo, a2_iv.hi, ok2))

print()
print('=== G, dGdc, J point enclosures vs mpmath ===')
for (c, q) in [('0.4', '1.05'), ('0.5', '2.0')]:
    c_d, q_d = Decimal(c), Decimal(q)
    a1b = R.bracket_x1(c_d, q_d); gb = R.bracket_gamma(c_d, q_d)
    a1_iv = R.iv_sub(R.HALF_PI_IV, a1b)
    a2_iv = R.iv_sub(R.PI, gb)
    a1 = L.alpha1(mp.mpf(c), mp.mpf(q)); a2 = L.alpha2(mp.mpf(c), mp.mpf(q))
    ci, qi = R.Iv.pt(c_d), R.Iv.pt(q_d)
    G1iv = R.iv_G(R.Iv.pt(Decimal(str(a1))), ci, qi)
    G2iv = R.iv_G(R.Iv.pt(Decimal(str(a2))), ci, qi)
    G1t = L.Gfun(a1, mp.mpf(c), mp.mpf(q)); G2t = L.Gfun(a2, mp.mpf(c), mp.mpf(q))
    ok1 = G1iv.lo <= d(G1t) <= G1iv.hi; ok2 = G2iv.lo <= d(G2t) <= G2iv.hi
    d1iv = R.iv_dGdc(R.Iv.pt(Decimal(str(a1))), ci, qi)
    d2iv = R.iv_dGdc(R.Iv.pt(Decimal(str(a2))), ci, qi)
    d1t = L.dGdc(a1, mp.mpf(c), mp.mpf(q)); d2t = L.dGdc(a2, mp.mpf(c), mp.mpf(q))
    ok3 = d1iv.lo <= d(d1t) <= d1iv.hi; ok4 = d2iv.lo <= d(d2t) <= d2iv.hi
    print('  c=%s q=%s: G1 ok=%s G2 ok=%s dG1dc ok=%s dG2dc ok=%s' % (c, q, ok1, ok2, ok3, ok4))
    if not (ok1 and ok2 and ok3 and ok4):
        print('    G1 [%s, %s] vs %s' % (G1iv.lo, G1iv.hi, d(G1t)))
        print('    G2 [%s, %s] vs %s' % (G2iv.lo, G2iv.hi, d(G2t)))
        print('    dG1dc [%s, %s] vs %s' % (d1iv.lo, d1iv.hi, d(d1t)))
        print('    dG2dc [%s, %s] vs %s' % (d2iv.lo, d2iv.hi, d(d2t)))
    ok &= ok1 and ok2 and ok3 and ok4

print()
print('=== box enclosure test: G2 over box q in [1.05,1.06], c in [0.49,0.50] ===')
qlo, qhi, clo, chi = Decimal('1.05'), Decimal('1.06'), Decimal('0.49'), Decimal('0.50')
qi_lo = R.Iv.pt(qlo); qi_hi = R.Iv.pt(qhi); ci_lo = R.Iv.pt(clo); ci_hi = R.Iv.pt(chi)
a2b = R.alpha2_box(qlo, qhi, clo, chi)
a1b = R.alpha1_box(qlo, qhi, clo, chi)
# G2 over box: G(alpha2_box, c_box, q_box)
qc = R.Iv(clo, chi); qq = R.Iv(qlo, qhi)
G2_box = R.iv_G(a2b, qc, qq)
print('  alpha1 box:', a1b)
print('  alpha2 box:', a2b)
print('  G2 over box:', G2_box)
# compare with point values
G2_true_max = -mp.inf; G2_true_min = mp.inf
for qi2 in range(5):
    q2 = mp.mpf(qlo) + (mp.mpf(qhi)-mp.mpf(qlo))*qi2/4
    for ci2 in range(5):
        c2 = mp.mpf(clo) + (mp.mpf(chi)-mp.mpf(clo))*ci2/4
        v = L.G2(c2, q2)
        G2_true_max = max(G2_true_max, v); G2_true_min = min(G2_true_min, v)
print('  true G2 range over box corners: [%s, %s]' % (mp.nstr(G2_true_min, 8), mp.nstr(G2_true_max, 8)))
print('  enclosure ok:', G2_box.lo <= d(G2_true_min) and d(G2_true_max) <= G2_box.hi)
