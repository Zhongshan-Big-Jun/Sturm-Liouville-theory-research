import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def roots2(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 12000), np.linspace(1.2, 3*np.pi, 12000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:6]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    return roots

def cfg(a, b, R):
    rs = roots2(a, b, R)
    if len(rs) < 2: return None
    s1, s2 = rs[0], rs[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    return dict(s1=s1, s2=s2, R1=s1*s1*y1a*y1a/n1 - s2*s2*y2a*y2a/n2,
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2, va=y2a/y1a, vb=y2b/y1b, q=None)

a, R = 0.57364, 1500.0
print("=== R2 profile R=1500, a=0.57364 (b from a+1e-5 to 0.60, fine) ===")
bb = np.linspace(a+1e-5, 0.60, 800)
prev = None
crossings = []
for b in bb:
    c = cfg(a, b, R)
    if c is None: continue
    v = c['R2']
    s = np.sign(v)
    if prev is not None and prev != s and prev != 0:
        crossings.append(b)
    prev = s
print("R2 sign-change locations (coarse):", [round(x,6) for x in crossings])
# refine each crossing
def R2v(b):
    c = cfg(a, b, R)
    return c['R2'] if c else None
roots_found = []
for i in range(len(crossings)):
    lo, hi = crossings[i] - 1e-4, crossings[i] + 1e-4
    try:
        r = brentq(R2v, lo, hi, xtol=1e-13)
    except Exception as e:
        print("  brentq fail:", e); continue
    c = cfg(a, r, R)
    roots_found.append((r, c['vb'], c['va']))
print("refined R2 roots (b, v(b), v(a)):")
for r, vb, va in roots_found:
    print(f"  b={r:.9f}  v(b)={vb:+.6f}  v(a)={va:+.6f}  good(b=x_+): {vb < 0}")
# branch-1
print("=== R1 profile ===")
prev = None; crossings1 = []
for b in bb:
    c = cfg(a, b, R)
    if c is None: continue
    v = c['R1']
    s = np.sign(v)
    if prev is not None and prev != s and prev != 0:
        crossings1.append(b)
    prev = s
print("R1 sign-change locations (coarse):", [round(x,6) for x in crossings1])
def R1v(b):
    c = cfg(a, b, R)
    return c['R1'] if c else None
for i in range(len(crossings1)):
    lo, hi = crossings1[i] - 1e-4, crossings1[i] + 1e-4
    try:
        r = brentq(R1v, lo, hi, xtol=1e-13)
    except Exception:
        continue
    c = cfg(a, r, R)
    print(f"  b={r:.9f}  v(a)={c['va']:+.6f}  good(a=x_-): {c['va'] > 0}")
