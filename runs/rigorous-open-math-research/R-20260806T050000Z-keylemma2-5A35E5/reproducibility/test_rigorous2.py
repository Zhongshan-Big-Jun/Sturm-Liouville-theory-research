# -*- coding: utf-8 -*-
"""test_rigorous2.py -- rerun dGdc point checks + box enclosure."""
import sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import rigorous as R
import kl2_lib as L
import mpmath as mp
from decimal import Decimal
mp.mp.dps = 50
def d(x): return Decimal(str(x))

ok = True
for (c, q) in [('0.4', '1.05'), ('0.5', '2.0'), ('0.45', '1.5'), ('0.41', '1.9')]:
    c_d, q_d = Decimal(c), Decimal(q)
    ci, qi = R.Iv.pt(c_d), R.Iv.pt(q_d)
    for a in [L.alpha1(mp.mpf(c), mp.mpf(q)), L.alpha2(mp.mpf(c), mp.mpf(q))]:
        iv = R.iv_dGdc(R.Iv.pt(Decimal(str(a))), ci, qi)
        tv = L.dGdc(a, mp.mpf(c), mp.mpf(q))
        good = iv.lo <= d(tv) <= iv.hi
        ok &= good
        if not good:
            print('FAIL c=%s q=%s a=%s: [%s, %s] vs %s' % (c, q, mp.nstr(a,8), iv.lo, iv.hi, d(tv)))
print('dGdc point enclosures all ok:', ok)

print()
print('=== box enclosure: G2 over box q=[1.05,1.06], c=[0.49,0.50] ===')
qlo, qhi, clo, chi = Decimal('1.05'), Decimal('1.06'), Decimal('0.49'), Decimal('0.50')
a2b = R.alpha2_box(qlo, qhi, clo, chi)
a1b = R.alpha1_box(qlo, qhi, clo, chi)
qc = R.Iv(clo, chi); qq = R.Iv(qlo, qhi)
G2_box = R.iv_G(a2b, qc, qq)
print('  G2 box:', G2_box)
G2mn = mp.inf; G2mx = -mp.inf
for i in range(6):
    q2 = mp.mpf(str(qlo)) + (mp.mpf(str(qhi))-mp.mpf(str(qlo)))*i/5
    for j in range(6):
        c2 = mp.mpf(str(clo)) + (mp.mpf(str(chi))-mp.mpf(str(clo)))*j/5
        v = L.G2(c2, q2)
        G2mn = min(G2mn, v); G2mx = max(G2mx, v)
print('  true corner range: [%s, %s]' % (mp.nstr(G2mn,10), mp.nstr(G2mx,10)))
print('  enclosure ok:', G2_box.lo <= d(G2mn) and d(G2mx) <= G2_box.hi)
