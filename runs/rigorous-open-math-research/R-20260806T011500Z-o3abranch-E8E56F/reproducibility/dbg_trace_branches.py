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
                R2=s1*s1*y1b*y1b/n1 - s2*s2*y2b*y2b/n2, va=y2a/y1a, vb=y2b/y1b)

def root_in(f, lo, hi):
    if f(lo)*f(hi) > 0: return None
    try: return brentq(f, lo, hi, xtol=1e-14)
    except Exception: return None

a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
R = 1500.0
# trace Gamma_2 downward from (b0, b0), adaptive bracket
b_prev = b0
found2 = None
for a in np.arange(b0, 0.5734, -1e-4):
    f = lambda bb: cfg(a, bb, R)['R2']
    # search progressively wider brackets around previous root
    b_new = None
    for w in [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2]:
        lo, hi = max(a+1e-5, b_prev-w), min(1-1e-6, b_prev+w)
        b_new = root_in(f, lo, hi)
        if b_new is not None:
            c = cfg(a, b_new, R)
            if c['vb'] < 0:
                break
            b_new = None
    if b_new is None:
        print(f"  Gamma_2 trace FAILS at a={a:.5f} (prev b={b_prev:.6f})")
        break
    b_prev = b_new
    if abs(a - 0.57364) < 1e-4:
        found2 = (a, b_new)
print(f"Gamma_2 main sheet at a={found2[0]:.5f}: g2={found2[1]:.9f} (checkpoint: 0.57600536)")
c = cfg(*found2, R); print(f"  vb={c['vb']:+.6f} va={c['va']:+.6f}")
# trace Gamma_1 upward from (a0, a0)
b_prev = a0
found1 = None
for a in np.arange(a0, 0.5740, 1e-4):
    f = lambda bb: cfg(a, bb, R)['R1']
    b_new = None
    for w in [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2]:
        lo, hi = max(a+1e-5, b_prev-w), min(1-1e-6, b_prev+w)
        b_new = root_in(f, lo, hi)
        if b_new is not None:
            c = cfg(a, b_new, R)
            if c['va'] > 0:
                break
            b_new = None
    if b_new is None:
        print(f"  Gamma_1 trace FAILS at a={a:.5f} (prev b={b_prev:.6f})")
        break
    b_prev = b_new
    if abs(a - 0.57364) < 1e-4:
        found1 = (a, b_new)
print(f"Gamma_1 main sheet at a={found1[0]:.5f}: g1={found1[1]:.9f} (checkpoint: 0.58327448)")
c = cfg(*found1, R); print(f"  va={c['va']:+.6f} vb={c['vb']:+.6f}")
