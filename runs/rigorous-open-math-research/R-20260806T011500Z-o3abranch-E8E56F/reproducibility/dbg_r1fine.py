import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at

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

def R1f(a, b, R):
    rs = roots2(a, b, R)
    s1, s2 = rs[0], rs[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*(np.sin(s1*a)/s1)**2/n1 - s2*s2*(np.sin(s2*a)/s2)**2/n2

a, R = 0.57364, 1500.0
print("R1 over [0.5825, 0.5845] (step 5e-5):")
prev = None
for b in np.arange(0.5825, 0.58451, 5e-5):
    v = R1f(a, b, R)
    s = 1 if v > 0 else (-1 if v < 0 else 0)
    if prev is not None and s != prev:
        print(f"  SIGN CHANGE between b={b-5e-5:.5f} (R1={prevv:+.3e}) and b={b:.5f} (R1={v:+.3e})")
    prev, prevv = s, v
print(f"R1(0.5830)={R1f(a,0.5830,R):+.6e}  R1(0.5836)={R1f(a,0.5836,R):+.6e}")
