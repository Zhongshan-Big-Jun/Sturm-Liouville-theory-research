# -*- coding: utf-8 -*-
"""cert_dM2dq_full.py -- produce JSON certificate for dM2/dq < 0 on [1,20]x[0,sqrt(41)].
Outputs: cert_dM2dq_boxes.json with all accepted boxes and their interval bounds,
plus the worst (closest-to-zero) upper bound and count of boxes.
"""
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext
import riarith as R
import mpmath as mp
mp.mp.dps = 60

D0 = Decimal(0); D1 = Decimal(1); D2 = Decimal(2); D4 = Decimal(4)
D5 = Decimal(5); D8 = Decimal(8); D9 = Decimal(9)

def dM2dq_iv(q, u):
    A = R.iv_sub(R.PI, R.iv_atan(R.iv_div(u, q)))
    t = R.iv_atan(u)
    S = R.iv_add(R.iv_sqr(q), R.iv_sqr(u))
    q2 = R.iv_sqr(q); u2 = R.iv_sqr(u)
    one_iv = R.Iv.pt(D1)
    term1 = R.iv_mul(R.iv_mul(R.Iv.pt(D4), R.iv_sqr(A)), u)
    term2 = R.iv_div(R.iv_mul(R.Iv.pt(D8), R.iv_mul(A, R.iv_mul(u2, q))), S)
    term3 = R.iv_div(R.iv_mul(R.Iv.pt(-7), R.iv_mul(q2, u)), S)
    term4 = R.iv_mul(R.Iv.pt(-14), R.iv_mul(A, q))
    term5 = R.iv_div(R.iv_mul(R.Iv.pt(-9), R.iv_mul(u2, u)), S)
    term6 = R.iv_div(R.iv_mul(R.Iv.pt(D2), u), R.iv_add(one_iv, u2))
    term7 = R.iv_div(R.iv_mul(R.Iv.pt(D4), R.iv_mul(A, q)), R.iv_add(one_iv, u2))
    br = R.iv_sub(R.iv_sub(R.iv_div(R.iv_mul(R.Iv.pt(D4), u2), S), R.Iv.pt(D5)), R.iv_mul(R.Iv.pt(D9), u2))
    term8 = R.iv_mul(t, br)
    acc = R.iv_add(term1, term2); acc = R.iv_add(acc, term3); acc = R.iv_add(acc, term4)
    acc = R.iv_add(acc, term5); acc = R.iv_add(acc, term6); acc = R.iv_add(acc, term7)
    return R.iv_add(acc, term8)

SQRT41 = Decimal('6.403124237432848686488217674621813264520')
def prove_rect(qlo, qhi, ulo, uhi, maxboxes=2000000, tol=Decimal('1e-4')):
    stack = [(Decimal(qlo), Decimal(qhi), Decimal(ulo), Decimal(uhi))]
    done = 0
    accepted = []
    violated = []
    while stack and done < maxboxes:
        ql, qh, ul, uh = stack.pop()
        iv = dM2dq_iv(R.Iv(ql, qh), R.Iv(ul, uh))
        done += 1
        if iv.hi < 0:
            accepted.append((str(ql), str(qh), str(ul), str(uh), str(iv.lo), str(iv.hi)))
            continue
        if (qh - ql) < tol and (uh - ul) < tol:
            violated.append((str(ql), str(qh), str(ul), str(uh), str(iv.lo), str(iv.hi)))
            continue
        if (qh - ql) >= (uh - ul):
            m = (ql + qh)/2
            stack.append((ql, m, ul, uh)); stack.append((m, qh, ul, uh))
        else:
            m = (ul + uh)/2
            stack.append((ql, qh, ul, m)); stack.append((ql, qh, m, uh))
    return done, accepted, violated

with localcontext() as c:
    c.prec = 60
    done, accepted, violated = prove_rect(1, 20, 0, SQRT41)
worst = max(Decimal(a[5]) for a in accepted)
print('boxes:', done, 'accepted:', len(accepted), 'violated:', len(violated))
print('worst (max) upper bound over accepted boxes:', worst)
cert = {'region': {'q': ['1', '20'], 'u': ['0', '6.403124237432848686488217674621813264520']},
        'n_boxes': len(accepted),
        'worst_upper_bound': str(worst),
        'formula': 'dM2dq = 4A^2u + 8Au^2q/S - 7q^2u/S - 14Aq - 9u^3/S + 2u/(1+u^2) + 4Aq/(1+u^2) + t(4u^2/S - 5 - 9u^2), S=q^2+u^2, A=pi-atan(u/q), t=atan(u)',
        'boxes': accepted}
with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\cert_dM2dq_boxes.json", "w") as f:
    json.dump(cert, f, indent=1)
print('certificate written')
