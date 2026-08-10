# -*- coding: utf-8 -*-
"""agentB_lib.py: fast 3-block barrier solver for O3a (vectorized, cached)."""
import numpy as np

def M01_vec(a, b, R, s):
    s = np.atleast_1d(np.asarray(s, dtype=float))
    def blk(L, c, s):
        w = s*np.sqrt(c); q = np.sqrt(c)
        cw = np.cos(w*L); sw = np.sin(w*L)/q
        return cw, sw, -q*np.sin(w*L), cw
    cw, sw, sw2, cw2 = blk(a, 1.0, s)
    M00, M01, M10, M11 = cw, sw, sw2, cw2
    for (L, c) in [(b-a, R), (1-b, 1.0)]:
        cw, sw, sw2, cw2 = blk(L, c, s)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw2*M10, sw2*M01+cw2*M11
    return M01

def secular_roots(a, b, R, k=2, s_hint=None):
    """First k eigenvalues (as s) of barrier config; s_hint optional refinement window."""
    allr = []
    segs = [(1e-7, np.pi + 1e-3), (np.pi - 1e-3, 2*np.pi + 1e-3)]
    for (lo0, hi0) in segs:
        s = np.linspace(lo0, hi0, 900)
        d = M01_vec(a, b, R, s)
        sg = np.signbit(d[1:]) != np.signbit(d[:-1])
        idx = np.nonzero(sg)[0]
        for i in idx:
            l, h = s[i], s[i+1]
            fl = M01_vec(a, b, R, np.array([l]))[0]
            for _ in range(55):
                m = 0.5*(l+h)
                if np.signbit(M01_vec(a, b, R, np.array([m]))[0]) == np.signbit(fl):
                    l = m
                else:
                    h = m
            allr.append(0.5*(l+h))
    allr = sorted(set(np.round(allr, 13)))
    if len(allr) < k:
        # fallback: finer scan over 4 segments
        allr = []
        for seg in range(4):
            s = np.linspace(seg*np.pi + 1e-10, (seg+1)*np.pi - 1e-10, 3001)
            d = M01_vec(a, b, R, s)
            sg = np.signbit(d[1:]) != np.signbit(d[:-1])
            idx = np.nonzero(sg)[0]
            for i in idx:
                l, h = s[i], s[i+1]
                fl = M01_vec(a, b, R, np.array([l]))[0]
                for _ in range(55):
                    m = 0.5*(l+h)
                    if np.signbit(M01_vec(a, b, R, np.array([m]))[0]) == np.signbit(fl):
                        l = m
                    else:
                        h = m
                allr.append(0.5*(l+h))
        allr = sorted(set(np.round(allr, 13)))
    return np.array(allr[:k])

def _cache(a, b, R):
    key = (round(a,12), round(b,12), R)
    return key

# small memo for (a,b,R) -> (s, n, z0) to speed up repeated configs
_memo = {}
def config(a, b, R):
    key = (round(a,13), round(b,13), R)
    if key in _memo:
        return _memo[key]
    s = secular_roots(a, b, R, 2)
    n = np.array([np.sqrt(norm2_barrier(a, b, R, sk)) for sk in s])
    z0 = z0_of_core(a, b, R, s)
    _memo[key] = (s, n, z0)
    return _memo[key]

def norm2_barrier(a, b, R, s):
    nrm = 0.0
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    xs = [0.0, a, b, 1.0]
    for i in range(3):
        L = xs[i+1]-xs[i]; c = R if i == 1 else 1.0
        w = s*np.sqrt(c)
        y0 = M01/s          # y at block start (state (y,y'/s), init (0,1/s))
        yp0 = M11          # y' at block start = s*(M11/s)
        A = y0; B = yp0/w
        Icc = 0.5*(L + np.sin(2*w*L)/(2*w)); Iss = 0.5*(L - np.sin(2*w*L)/(2*w)); Ics = np.sin(w*L)**2/(2*w)
        nrm += c*(A*A*Icc + B*B*Iss + 2*A*B*Ics)
        cw = np.cos(w*L); sw = np.sin(w*L)/np.sqrt(c); sw2 = -np.sqrt(c)*np.sin(w*L)
        M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
    return nrm

def y_L(a, b, R, s_vals, pts):
    s_vals = np.atleast_1d(np.asarray(s_vals, dtype=float))
    pts = np.atleast_1d(np.asarray(pts, dtype=float))
    xs = [0.0, a, b, 1.0]
    out = np.zeros((len(s_vals), len(pts)))
    for j, p in enumerate(pts):
        bi = max(i for i in range(3) if xs[i] <= p)
        for si, s in enumerate(s_vals):
            M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
            for i in range(bi):
                L = xs[i+1]-xs[i]; c = R if i == 1 else 1.0
                w = s*np.sqrt(c)
                cw = np.cos(w*L); sw = np.sin(w*L)/np.sqrt(c); sw2 = -np.sqrt(c)*np.sin(w*L)
                M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
            L = p - xs[bi]; c = R if bi == 1 else 1.0
            w = s*np.sqrt(c)
            cw = np.cos(w*L); sw = np.sin(w*L)/np.sqrt(c); sw2 = -np.sqrt(c)*np.sin(w*L)
            M00, M01, M10, M11 = cw*M00+sw*M10, cw*M01+sw*M11, sw2*M00+cw*M10, sw2*M01+cw*M11
            out[si, j] = M01/s
    return out

def f_at(a, b, R, x, cfg=None):
    if cfg is None:
        cfg = config(a, b, R)
    s, n, z0 = cfg
    y = y_L(a, b, R, s, np.atleast_1d(np.asarray(x, dtype=float)))
    U = y/n[:,None]
    return s[0]**2*U[0]**2 - s[1]**2*U[1]**2

def z0_of_core(a, b, R, s):
    # v = y2/y1 is strictly decreasing on (0,1), v(0+)=1>0, v(1-)<0; bisect on v.
    s1, s2 = s[0], s[1]
    def v(x):
        y = y_L(a, b, R, [s1, s2], [x])[:,0]
        return float(y[1]/y[0])
    l, h = 1e-9, 1.0-1e-9
    vl = v(l)
    assert vl > 0 and v(h) < 0, f"v signs wrong: {vl}, {v(h)}"
    for _ in range(70):
        m = 0.5*(l+h)
        if v(m) > 0: l = m
        else: h = m
    return 0.5*(l+h)

def z0_of(a, b, R):
    return config(a, b, R)[2]

def zeros_f(a, b, R):
    cfg = config(a, b, R)
    s, n, z0 = cfg
    fa0 = f_at(a, b, R, 1e-12, cfg)
    fz0 = f_at(a, b, R, z0, cfg)
    if not (fa0 < 0 and fz0 > 0):
        return None
    lo, hi = 0.0, z0
    for _ in range(80):
        m = 0.5*(lo+hi)
        if f_at(a, b, R, m, cfg) < 0: lo = m
        else: hi = m
    xm = 0.5*(lo+hi)
    f1m = f_at(a, b, R, 1.0-1e-12, cfg)
    if not (f1m < 0):
        return None
    lo, hi = z0, 1.0
    for _ in range(80):
        m = 0.5*(lo+hi)
        if f_at(a, b, R, m, cfg) > 0: lo = m
        else: hi = m
    xp = 0.5*(lo+hi)
    xx = np.linspace(0, 1, 401)
    ff = f_at(a, b, R, xx, cfg)
    ch = np.signbit(ff[2:-1]) != np.signbit(ff[1:-2])
    if ch.sum() != 2:
        return None
    return (xm, xp)
