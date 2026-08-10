# -*- coding: utf-8 -*-
"""cert_l4l5.py (v2, uniform cells) -- certified L4box (Hp < 0) and L5box (Fpp > 0)
on the box [1,2] x [0.4,0.5].

Strategy: pre-partition the box into uniform cells, evaluate the natural interval
extension of Hp = dG2/dc - dG1/dc (resp. Fpp = M~1*J1 - M~2*J2) on each cell using
sound_bracket.alpha1_box / alpha2_box for the secular roots, and refine only the
sign-indefinite cells.  The accepted leaves tile the whole box, so a negative upper
bound (resp. positive lower bound) on every leaf certifies the sign on the box.

Soundness model: riarith.py provides outward-rounded enclosures (documented in the
file header and in the run audit); alpha1/alpha2 bracketing is by monotone bisection
with interval evaluations (sound_bracket.py); iv_dGdc / iv_Mtilde / iv_J are the
natural interval extensions of the exact formulas (rigorous.py).
"""
import sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext
import riarith as R
import rigorous as RG
import sound_bracket as SB
import mpmath as mp
mp.mp.dps = 40

BRACK_TOL = Decimal('1e-12')
MAXDEPTH = 8

def Hp_iv(qlo, qhi, clo, chi, tol=BRACK_TOL):
    a1b = SB.alpha1_box(qlo, qhi, clo, chi, tol)
    a2b = SB.alpha2_box(qlo, qhi, clo, chi, tol)
    c = R.Iv(clo, chi); q = R.Iv(qlo, qhi)
    return R.iv_sub(RG.iv_dGdc(a2b, c, q), RG.iv_dGdc(a1b, c, q))

def Fpp_iv(qlo, qhi, clo, chi, tol=BRACK_TOL):
    a1b = SB.alpha1_box(qlo, qhi, clo, chi, tol)
    a2b = SB.alpha2_box(qlo, qhi, clo, chi, tol)
    c = R.Iv(clo, chi); q = R.Iv(qlo, qhi)
    M1 = RG.iv_Mtilde(a1b, c, q); M2 = RG.iv_Mtilde(a2b, c, q)
    J1 = RG.iv_J(a1b, c, q); J2 = RG.iv_J(a2b, c, q)
    return R.iv_sub(R.iv_mul(M1, J1), R.iv_mul(M2, J2))

def prove_box(f_iv, qlo, qhi, clo, chi, want_neg, Nq, Nc, maxboxes=400000):
    """uniform Nq x Nc pre-partition; refine sign-indefinite cells to depth MAXDEPTH."""
    QW = (Decimal(qhi) - Decimal(qlo))/Nq
    CW = (Decimal(chi) - Decimal(clo))/Nc
    accepted = []; violated = []; done = 0
    t0 = time.time()
    for i in range(Nq):
        for j in range(Nc):
            stack = [(Decimal(qlo) + i*QW, Decimal(qlo) + (i+1)*QW,
                      Decimal(clo) + j*CW, Decimal(clo) + (j+1)*CW, 0)]
            while stack:
                ql, qh, cl, ch, depth = stack.pop()
                iv = f_iv(ql, qh, cl, ch)
                done += 1
                if (iv.hi < 0) if want_neg else (iv.lo > 0):
                    accepted.append((str(ql), str(qh), str(cl), str(ch), str(iv.lo), str(iv.hi)))
                    continue
                if depth >= MAXDEPTH:
                    violated.append((str(ql), str(qh), str(cl), str(ch), str(iv.lo), str(iv.hi)))
                    continue
                if (qh - ql) >= (ch - cl):
                    m = (ql + qh)/2
                    stack.append((ql, m, cl, ch, depth+1)); stack.append((m, qh, cl, ch, depth+1))
                else:
                    m = (cl + ch)/2
                    stack.append((ql, qh, cl, m, depth+1)); stack.append((ql, qh, m, ch, depth+1))
    return done, accepted, violated, time.time()-t0

if __name__ == '__main__':
    # point sanity vs kl2_lib
    print('=== point sanity vs kl2_lib ===')
    import kl2_lib as L
    for (q, c) in [('1.05', '0.5'), ('2', '0.5'), ('1.5', '0.45')]:
        iv = Hp_iv(Decimal(q), Decimal(q), Decimal(c), Decimal(c))
        tv = L.Hp(mp.mpf(c), mp.mpf(q))
        print('  Hp q=%s c=%s: [%s,%s] encloses %s -> %s' % (q, c, iv.lo, iv.hi, mp.nstr(tv,8), iv.lo <= Decimal(str(tv)) <= iv.hi))
        iv2 = Fpp_iv(Decimal(q), Decimal(q), Decimal(c), Decimal(c))
        tv2 = L.Fpp_t(mp.mpf(c), mp.mpf(q))
        print('  Fpp q=%s c=%s: [%s,%s] encloses %s -> %s' % (q, c, iv2.lo, iv2.hi, mp.nstr(tv2,8), iv2.lo <= Decimal(str(tv2)) <= iv2.hi))

    with localcontext() as c:
        c.prec = 60
        done1, acc1, viol1, t1 = prove_box(Hp_iv, 1, 2, '0.4', '0.5', True, 16, 8)
    print('Hp: evals=%d accepted=%d violated=%d time=%.1fs' % (done1, len(acc1), len(viol1), t1))
    if viol1:
        for v in viol1[:3]: print('  VIOL:', v)
    else:
        worst = max(Decimal(a[5]) for a in acc1)
        print('  worst upper bound:', worst)
        json.dump({'region': {'q': ['1','2'], 'c': ['0.4','0.5']},
                   'n_boxes': len(acc1), 'worst_upper_bound': str(worst), 'boxes': acc1},
                  open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\cert_L4box_boxes.json", "w"), indent=1)

    with localcontext() as c:
        c.prec = 60
        done2, acc2, viol2, t2 = prove_box(Fpp_iv, 1, 2, '0.4', '0.5', False, 16, 8)
    print('Fpp: evals=%d accepted=%d violated=%d time=%.1fs' % (done2, len(acc2), len(viol2), t2))
    if viol2:
        for v in viol2[:3]: print('  VIOL:', v)
    else:
        worst = min(Decimal(a[4]) for a in acc2)
        print('  worst lower bound:', worst)
        json.dump({'region': {'q': ['1','2'], 'c': ['0.4','0.5']},
                   'n_boxes': len(acc2), 'worst_lower_bound': str(worst), 'boxes': acc2},
                  open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\cert_L5box_boxes.json", "w"), indent=1)
