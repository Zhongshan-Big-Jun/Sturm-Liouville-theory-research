# -*- coding: utf-8 -*-
"""cert_dM2dq.py (fixed) -- certified dM2/dq < 0 on [1,20]x[0,sqrt(41)]."""
import sys
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

def dM2dq_pt(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u); S = q*q + u*u
    return (4*A*A*u + 8*A*u*u*q/S - 7*q*q*u/S - 14*A*q - 9*u**3/S
            + 2*u/(1+u*u) + 4*A*q/(1+u*u) + t*(4*u*u/S - 5 - 9*u*u))

print('=== point-box verification vs mpmath (60 digits) ===')
ok = True
for qv in ['1.01','1.05','2','5','10','19.9']:
    for uv in ['0.01','0.5','0.87','2','5','6.4']:
        if float(uv) >= float(mp.sqrt(2*mp.mpf(qv)+1)): continue
        qd, ud = Decimal(qv), Decimal(uv)
        iv = dM2dq_iv(R.Iv.pt(qd), R.Iv.pt(ud))
        tv = dM2dq_pt(mp.mpf(qv), mp.mpf(uv))
        good = iv.lo <= Decimal(str(tv)) <= iv.hi
        ok &= good
        if not good:
            print('  FAIL q=%s u=%s: [%s,%s] vs %s' % (qv, uv, iv.lo, iv.hi, tv))
print('  point enclosures all ok:', ok)

print('=== adaptive subdivision of [1,20] x [0, sqrt(41)] ===')
SQRT41 = Decimal('6.403124237432848686488217674621813264520')
def prove_rect(qlo, qhi, ulo, uhi, maxboxes=2000000, tol=Decimal('1e-4')):
    stack = [(Decimal(qlo), Decimal(qhi), Decimal(ulo), Decimal(uhi))]
    done = 0
    violated = []
    while stack and done < maxboxes:
        ql, qh, ul, uh = stack.pop()
        iv = dM2dq_iv(R.Iv(ql, qh), R.Iv(ul, uh))
        done += 1
        if iv.hi < 0:
            continue
        if (qh - ql) < tol and (uh - ul) < tol:
            violated.append((ql, qh, ul, uh, iv.lo, iv.hi))
            continue
        if (qh - ql) >= (uh - ul):
            m = (ql + qh)/2
            stack.append((ql, m, ul, uh)); stack.append((m, qh, ul, uh))
        else:
            m = (ul + uh)/2
            stack.append((ql, qh, ul, m)); stack.append((ql, qh, m, uh))
    return done, violated, len(stack)

with localcontext() as c:
    c.prec = 60
    done, violated, rem = prove_rect(1, 20, 0, SQRT41)
print('  boxes evaluated:', done, ' remaining:', rem, ' violated:', len(violated))
for v in violated[:5]:
    print('    VIOLATED box q=[%s,%s] u=[%s,%s] range=[%s,%s]' % v)
