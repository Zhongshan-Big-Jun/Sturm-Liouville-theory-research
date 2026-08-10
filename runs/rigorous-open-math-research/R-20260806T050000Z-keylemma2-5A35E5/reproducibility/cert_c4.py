# -*- coding: utf-8 -*-
"""cert_c4.py (v3) -- pre-subdivide [2pi/7, 2pi/5-1e-3] into uniform small boxes."""
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext
import riarith as R
import mpmath as mp
mp.mp.dps = 60

def K_iv(v):
    u = R.iv_tan(v)
    w = R.iv_sub(R.PI, R.iv_mul(R.Iv.pt(Decimal('2.5')), v))
    q = R.iv_div(R.iv_mul(R.iv_sin(v), R.iv_cos(w)), R.iv_mul(R.iv_cos(v), R.iv_sin(w)))
    q2 = R.iv_sqr(q); u2 = R.iv_sqr(u)
    P = R.iv_add(R.iv_add(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal(5)), v), q),
                          R.iv_mul(R.Iv.pt(-3), u)),
                 R.iv_mul(R.Iv.pt(Decimal(2)), v))
    t1 = R.iv_mul(R.iv_add(q2, u2), P)
    t2 = R.iv_mul(R.iv_mul(R.iv_mul(R.Iv.pt(Decimal('1.2')), u), q), R.iv_add(R.Iv.pt(1), u2))
    return R.iv_sub(t1, t2)

v_lo = Decimal('0.8975979010256552109893266809370008240563341141071730917071270263736618')
v_hi = Decimal('1.255637061435917295385057353311801153678867759750042328389977836923127')

def prove_uniform(N, maxboxes=2000000, tol=Decimal('1e-6')):
    width = (v_hi - v_lo)/N
    accepted = []
    violated = []
    done = 0
    for i in range(N):
        a = v_lo + i*width
        b = a + width
        stack = [(a, b)]
        while stack and done < maxboxes:
            x, y = stack.pop()
            iv = K_iv(R.Iv(x, y))
            done += 1
            if iv.lo > 0:
                accepted.append((str(x), str(y), str(iv.lo), str(iv.hi)))
                continue
            if (y - x) < tol:
                violated.append((str(x), str(y), str(iv.lo), str(iv.hi)))
                continue
            m = (x + y)/2
            stack.append((x, m)); stack.append((m, y))
    return done, accepted, violated

for N in [200, 400, 1000]:
    with localcontext() as c:
        c.prec = 60
        done, accepted, violated = prove_uniform(N)
    worst_lo = min(Decimal(a[2]) for a in accepted)
    print('N=%d: boxes=%d accepted=%d violated=%d worst_lo=%s' % (N, done, len(accepted), len(violated), worst_lo))
    if not violated:
        cert = {'interval': ['2pi/7', '2pi/5 - 1e-3'], 'n_boxes': len(accepted),
                'worst_lower_bound': str(worst_lo), 'uniform_N': N, 'boxes': accepted}
        with open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\cert_c4_boxes.json", "w") as f:
            json.dump(cert, f, indent=1)
        print('  certificate written with N =', N)
        break

