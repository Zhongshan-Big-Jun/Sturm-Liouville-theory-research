# -*- coding: utf-8 -*-
"""c1_lib.py (v5): fast roots2 via coarse scan + bisection."""
import numpy as np

_memo_cfg = {}
def _cfg_key(a, b, R):
    return (round(a, 12), round(b, 12), R)

def sec(s, a, b, R):
    m = np.sqrt(R)
    alpha = s * a; beta = s * (1 - b); theta = s * m * (b - a)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    ct, st = np.cos(theta), np.sin(theta)
    return cb * ct * sa - m * sb * st * sa + (cb * st / m) * ca + sb * ct * ca

def y_at(s, a, b, R, x):
    m = np.sqrt(R)
    alpha = s * a
    if x <= a:
        return np.sin(s * x) / s
    elif x <= b:
        u = x - a
        return (np.sin(alpha) * np.cos(s * m * u) + (np.cos(alpha) / m) * np.sin(s * m * u)) / s
    else:
        v = x - b
        theta = s * m * (b - a)
        yb = (np.sin(alpha) * np.cos(theta) + (np.cos(alpha) / m) * np.sin(theta)) / s
        ypb = -m * np.sin(theta) * np.sin(alpha) + np.cos(theta) * np.cos(alpha)
        return np.cos(s * v) * yb + np.sin(s * v) * ypb / s

def norm_n(s, a, b, R):
    m = np.sqrt(R)
    L = b - a; beta = 1 - b
    alpha = s * a; theta = s * m * L
    I1 = a / 2 - np.sin(2 * alpha) / (4 * s)
    Icc = L / 2 + np.sin(2 * theta) / (4 * s * m)
    Iss = L / 2 - np.sin(2 * theta) / (4 * s * m)
    Ics = np.sin(theta) ** 2 / (2 * s * m)
    sa = np.sin(alpha); ca = np.cos(alpha)
    I2 = sa * sa * Icc + (ca / m) ** 2 * Iss + 2 * sa * (ca / m) * Ics
    yb_scaled = sa * np.cos(theta) + (ca / m) * np.sin(theta)
    ypb = -m * np.sin(theta) * np.sin(alpha) + np.cos(theta) * np.cos(alpha)
    Icc3 = beta / 2 + np.sin(2 * s * beta) / (4 * s)
    Iss3 = beta / 2 - np.sin(2 * s * beta) / (4 * s)
    Ics3 = np.sin(s * beta) ** 2 / (2 * s)
    I3 = (yb_scaled ** 2 * Icc3 + ypb ** 2 * Iss3 + 2 * yb_scaled * ypb * Ics3) / s ** 2
    return (I1 + R * I2) / s ** 2 + I3

def _bisect(f, lo, hi, iters=90):
    flo = f(lo)
    for _ in range(iters):
        md = 0.5 * (lo + hi)
        if np.signbit(f(md)) == np.signbit(flo):
            lo = md
        else:
            hi = md
    return 0.5 * (lo + hi)

def roots2(a, b, R, ns=6001):
    s = np.linspace(1e-9, 2 * np.pi + 1e-3, ns)
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    out = []
    for i in idx:
        out.append(_bisect(lambda t: sec(t, a, b, R), s[i], s[i + 1]))
        if len(out) == 2:
            return out[0], out[1]
    raise RuntimeError(f"roots2: fewer than 2 roots for (a,b,R)=({a},{b},{R})")

def cfg(a, b, R):
    key = _cfg_key(a, b, R)
    if key in _memo_cfg:
        return _memo_cfg[key]
    s1, s2 = roots2(a, b, R)
    out = (s1, s2, norm_n(s1, a, b, R), norm_n(s2, a, b, R))
    _memo_cfg[key] = out
    return out

def residual(a, b, R, at='a'):
    s1, s2, n1, n2 = cfg(a, b, R)
    if at == 'a':
        return s1 ** 2 * (np.sin(s1 * a) / s1) ** 2 / n1 - s2 ** 2 * (np.sin(s2 * a) / s2) ** 2 / n2
    else:
        return s1 ** 2 * y_at(s1, a, b, R, b) ** 2 / n1 - s2 ** 2 * y_at(s2, a, b, R, b) ** 2 / n2

def residual_both(a, b, R):
    s1, s2, n1, n2 = cfg(a, b, R)
    y1a = np.sin(s1 * a) / s1; y2a = np.sin(s2 * a) / s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    R1 = s1 ** 2 * y1a ** 2 / n1 - s2 ** 2 * y2a ** 2 / n2
    R2 = s1 ** 2 * y1b ** 2 / n1 - s2 ** 2 * y2b ** 2 / n2
    return R1, R2

def v_at(a, b, R, x):
    s1, s2 = roots2(a, b, R)
    return y_at(s2, a, b, R, x) / y_at(s1, a, b, R, x)

def partials(a, b, R, h=1e-6):
    s1, s2 = roots2(a, b, R)
    def dsec(s, var):
        if var == 's': return (sec(s + h, a, b, R) - sec(s - h, a, b, R)) / (2 * h)
        if var == 'a': return (sec(s, a + h, b, R) - sec(s, a - h, b, R)) / (2 * h)
        return (sec(s, a, b + h, R) - sec(s, a, b - h, R)) / (2 * h)
    def dr1(var):
        def r1(s1, s2, a, b, R):
            n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
            return s1 ** 2 * (np.sin(s1 * a) / s1) ** 2 / n1 - s2 ** 2 * (np.sin(s2 * a) / s2) ** 2 / n2
        if var == 'a': return (r1(s1, s2, a + h, b, R) - r1(s1, s2, a - h, b, R)) / (2 * h)
        if var == 'b': return (r1(s1, s2, a, b + h, R) - r1(s1, s2, a, b - h, R)) / (2 * h)
        if var == 's1': return (r1(s1 + h, s2, a, b, R) - r1(s1 - h, s2, a, b, R)) / (2 * h)
        return (r1(s1, s2 + h, a, b, R) - r1(s1, s2 - h, a, b, R)) / (2 * h)
    def dr2(var):
        def r2(s1, s2, a, b, R):
            n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
            return s1 ** 2 * y_at(s1, a, b, R, b) ** 2 / n1 - s2 ** 2 * y_at(s2, a, b, R, b) ** 2 / n2
        if var == 'a': return (r2(s1, s2, a + h, b, R) - r2(s1, s2, a - h, b, R)) / (2 * h)
        if var == 'b': return (r2(s1, s2, a, b + h, R) - r2(s1, s2, a, b - h, R)) / (2 * h)
        if var == 's1': return (r2(s1 + h, s2, a, b, R) - r2(s1 - h, s2, a, b, R)) / (2 * h)
        return (r2(s1, s2 + h, a, b, R) - r2(s1, s2 - h, a, b, R)) / (2 * h)
    ds1_a = -dsec(s1, 'a') / dsec(s1, 's'); ds1_b = -dsec(s1, 'b') / dsec(s1, 's')
    ds2_a = -dsec(s2, 'a') / dsec(s2, 's'); ds2_b = -dsec(s2, 'b') / dsec(s2, 's')
    R1a = dr1('a') + dr1('s1') * ds1_a + dr1('s2') * ds2_a
    R1b = dr1('b') + dr1('s1') * ds1_b + dr1('s2') * ds2_b
    R2a = dr2('a') + dr2('s1') * ds1_a + dr2('s2') * ds2_a
    R2b = dr2('b') + dr2('s1') * ds1_b + dr2('s2') * ds2_b
    return dict(A=R1a, B=R2a, C=R2b, D=R1b, s1=s1, s2=s2)

def a_fp(R, lo=0.40, hi=0.5):
    def f(u):
        return residual(u, 1 - u, R, at='a')
    fl = f(lo)
    for _ in range(90):
        m = 0.5 * (lo + hi)
        if np.signbit(f(m)) == np.signbit(fl):
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)
