# -*- coding: utf-8 -*-
"""E1 structural exploration v3 (evidence only, vectorized)."""
import numpy as np

def sec(s, a, b, R):
    m = np.sqrt(R); alpha = s*a; beta = s*(1-b); theta = s*m*(b-a)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    ct, st = np.cos(theta), np.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def _bisect(f, lo, hi, iters=80):
    flo = f(lo)
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(f(md)) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def roots2(a, b, R, ns=8001):
    for cap in (2*np.pi+1e-3, 4*np.pi, 6*np.pi):
        s = np.linspace(1e-9, cap, ns)
        M = sec(s, a, b, R)
        ch = np.signbit(M[1:]) != np.signbit(M[:-1])
        idx = np.nonzero(ch)[0]
        out = []
        for i in idx:
            out.append(_bisect(lambda t: sec(t, a, b, R), s[i], s[i+1]))
            if len(out) == 2: return out[0], out[1]
    raise RuntimeError("roots2 failed")

_cfg = {}
def cfg(a, b, R):
    k = (round(a,12), round(b,12), R)
    if k not in _cfg:
        _cfg[k] = roots2(a, b, R)
    return _cfg[k]

def yv(s, a, b, R, x):
    """vectorized y(x) on array x"""
    m = np.sqrt(R); alpha = s*a
    out = np.empty_like(x)
    m1 = x <= a
    m2 = (x > a) & (x <= b)
    m3 = x > b
    out[m1] = np.sin(s*x[m1])/s
    u = x[m2]-a
    out[m2] = (np.sin(alpha)*np.cos(s*m*u) + (np.cos(alpha)/m)*np.sin(s*m*u))/s
    v = x[m3]-b; theta = s*m*(b-a)
    yb = (np.sin(alpha)*np.cos(theta) + (np.cos(alpha)/m)*np.sin(theta))/s
    ypb = -m*np.sin(theta)*np.sin(alpha) + np.cos(theta)*np.cos(alpha)
    out[m3] = np.cos(s*v)*yb + np.sin(s*v)*ypb/s
    return out

def norm_n(s, a, b, R):
    m = np.sqrt(R); L = b-a; beta = 1-b
    alpha = s*a; theta = s*m*L
    I1 = a/2 - np.sin(2*alpha)/(4*s)
    Icc = L/2 + np.sin(2*theta)/(4*s*m)
    Iss = L/2 - np.sin(2*theta)/(4*s*m)
    Ics = np.sin(theta)**2/(2*s*m)
    sa = np.sin(alpha); ca = np.cos(alpha)
    I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb_scaled = sa*np.cos(theta) + (ca/m)*np.sin(theta)
    ypb = -m*np.sin(theta)*np.sin(alpha) + np.cos(theta)*np.cos(alpha)
    Icc3 = beta/2 + np.sin(2*s*beta)/(4*s)
    Iss3 = beta/2 - np.sin(2*s*beta)/(4*s)
    Ics3 = np.sin(s*beta)**2/(2*s)
    I3 = (yb_scaled**2*Icc3 + ypb**2*Iss3 + 2*yb_scaled*ypb*Ics3)/s**2
    return (I1 + R*I2)/s**2 + I3

def residual_both(a, b, R):
    s1, s2 = cfg(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = yv(s1, a, b, R, np.array([b]))[0]; y2b = yv(s2, a, b, R, np.array([b]))[0]
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    return R1, R2

def band(a, b, R, ns=20000):
    s1, s2 = cfg(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    q = (s1/s2)*np.sqrt(n2/n1)
    xs = np.linspace(1e-9, 1-1e-9, ns)
    y1 = yv(s1, a, b, R, xs); y2 = yv(s2, a, b, R, xs)
    v = y2/y1
    m1 = np.nonzero(np.signbit(v[1:]-q) != np.signbit(v[:-1]-q))[0]
    m2 = np.nonzero(np.signbit(v[1:]+q) != np.signbit(v[:-1]+q))[0]
    if len(m1)==0 or len(m2)==0: return np.nan, np.nan
    return xs[m1[0]], xs[m2[-1]]

a0 = np.arccos(0.25)/np.pi; b0 = 1-a0
print("=== symmetric family band endpoints, R=4 (a<1/2) ===")
for a in [0.30, 0.38, 0.42, 0.45, 0.4515, 0.48]:
    b = 1-a
    xm, xp = band(a, b, 4.0)
    print(f"  a={a:.4f}: x-={xm:.6f} x+={xp:.6f}  d-={xm-a:+.6f} d+={xp-b:+.6f}")

print("\n=== E1: g1(b0)-b0 vs R (coarse scan + refine) ===")
def g1b0(R):
    aa = np.linspace(a0+5e-4, 0.985, 400)
    best = None; best_r = 1e9
    for a in aa:
        R1, R2 = residual_both(a, b0, R)
        xm, xp = band(a, b0, R)
        if xm != xm: continue
        if abs(a-xm) < 2e-3 and b0 <= xp + 1e-9 and abs(R1) < best_r:
            best_r = abs(R1); best = a
    return best, best_r
for R in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1e4]:
    best, r = g1b0(R)
    print(f"  R={R:g}: g1(b0)={best:.6f}  h(b0)={best-b0:+.6f}  min|R1|={r:.1e}")

print("\n=== band endpoint monotonicity, R=4 around fp ===")
def fp(R, lo=0.40, hi=0.5):
    for _ in range(80):
        m = 0.5*(lo+hi)
        R1,_ = residual_both(m, 1-m, R)
        R1l,_ = residual_both(lo, 1-lo, R)
        if np.signbit(R1) == np.signbit(R1l): lo = m
        else: hi = m
    return 0.5*(lo+hi)
af = fp(4.0); bf = 1-af
print(f"  fp={af:.6f}")
xm0, xp0 = band(af, bf, 4.0)
for (da, db) in [(0.03,0),(-0.03,0),(0,0.03),(0,-0.03),(0.02,0.02),(-0.02,-0.02),(0.02,-0.02),(-0.02,0.02)]:
    a = af+da; b = bf+db
    if not (0 < a < b < 1): continue
    xm, xp = band(a, b, 4.0)
    print(f"  (da,db)=({da:+.2f},{db:+.2f}): dx-={xm-xm0:+.6f} dx+={xp-xp0:+.6f}")