# -*- coding: utf-8 -*-
"""verify_hp.py: high-precision check of h' near right end at R=1e4 (Lemma A possible violation)."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def cfg(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 14000), np.linspace(1.2, 3*np.pi, 14000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(100):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    if len(roots) < 2: return None
    s1, s2 = roots[0], roots[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return dict(s1=s1, s2=s2, R1=s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2,
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2, va=y2a/y1a, vb=y2b/y1b)

R = 1e4
a0v = np.arccos(0.25)/np.pi; b0v = np.arccos(-0.25)/np.pi
a = 0.57364
# find branches precisely
bb = np.linspace(a+1e-5, 1-1e-5, 60)
# g1
vals1 = [cfg(a, b, R)['R1'] for b in bb]
g1 = None
for i in range(59):
    if vals1[i]*vals1[i+1] < 0:
        g1 = brentq(lambda b: cfg(a, b, R)['R1'], bb[i], bb[i+1], xtol=1e-14)
        break
vals2 = [cfg(a, b, R)['R2'] for b in bb]
g2 = None
for i in range(59):
    if vals2[i]*vals2[i+1] < 0:
        g2 = brentq(lambda b: cfg(a, b, R)['R2'], bb[i], bb[i+1], xtol=1e-14)
        break
print(f"a={a}: g1={g1:.10f} g2={g2:.10f} h={g1-g2:+.6e}")
c1 = cfg(a, g1, R); c2 = cfg(a, g2, R)
print(f"  R1(g1)={c1['R1']:.3e} va={c1['va']:.4f} | R2(g2)={c2['R2']:.3e} vb={c2['vb']:.4f}")
# h at nearby a-values: direct monotonicity test
for aa in [0.57300, 0.57330, 0.57364, 0.57400, 0.57440]:
    gg1 = brentq(lambda b: cfg(aa, b, R)['R1'], aa+1e-5, 1-1e-5)
    gg2 = brentq(lambda b: cfg(aa, b, R)['R2'], aa+1e-5, 1-1e-5)
    print(f"  a={aa:.5f}: g1={gg1:.8f} g2={gg2:.8f} h={gg1-gg2:+.6e}")
# FD h' with several h (central)
hvals = [1e-4, 3e-5, 1e-5, 3e-6, 1e-6]
print("h' via FD of h(a) = g1(a)-g2(a):")
for h in hvals:
    def gg(aa, which):
        lo, hi = aa+1e-5, 1-1e-5
        f = (lambda b: cfg(aa, b, R)['R1']) if which=='g1' else (lambda b: cfg(aa, b, R)['R2'])
        return brentq(f, lo, hi, xtol=1e-13)
    hp = ( (gg(a+h,'g1')-gg(a-h,'g1')) - (gg(a+h,'g2')-gg(a-h,'g2')) )/(2*h)
    print(f"  h={h:.0e}: h'={hp:+.6f}")
