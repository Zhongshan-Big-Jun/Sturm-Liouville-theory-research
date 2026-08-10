# -*- coding: utf-8 -*-
"""e04_check_violation.py: high-precision check of the R=100 violation point."""
import mpmath as mp, sys
mp.mp.dps = 60
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T200000Z-o3a-c1b-7F3A9B\reproducibility")
import c1_lib
import numpy as np

a, b, R = 0.7793, 0.8032, 100.0

# high-precision sec / y_at / norm_n reimplemented with mpmath
def sec_mp(s, a, b, R):
    m = mp.sqrt(R)
    alpha = s*a; beta = s*(1-b); theta = s*m*(b-a)
    ca, sa = mp.cos(alpha), mp.sin(alpha)
    cb, sb = mp.cos(beta), mp.sin(beta)
    ct, st = mp.cos(theta), mp.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def roots2_mp(a, b, R, lo=1e-9, hi=2*mp.pi+1e-3, n=20001):
    ss = [lo + (hi-lo)*i/(n-1) for i in range(n)]
    Ms = [sec_mp(s, a, b, R) for s in ss]
    out = []
    for i in range(n-1):
        if (Ms[i] < 0) != (Ms[i+1] < 0):
            l, h = ss[i], ss[i+1]
            fl = sec_mp(l, a, b, R)
            for _ in range(200):
                md = (l+h)/2
                if (sec_mp(md, a, b, R) < 0) == (fl < 0):
                    l = md
                else:
                    h = md
            out.append((l+h)/2)
            if len(out) == 2:
                break
    return out

def y_at_mp(s, a, b, R, x):
    m = mp.sqrt(R)
    alpha = s*a
    if x <= a:
        return mp.sin(s*x)/s
    elif x <= b:
        u = x - a
        return (mp.sin(alpha)*mp.cos(s*m*u) + (mp.cos(alpha)/m)*mp.sin(s*m*u))/s
    else:
        vv = x - b
        theta = s*m*(b-a)
        yb = (mp.sin(alpha)*mp.cos(theta) + (mp.cos(alpha)/m)*mp.sin(theta))/s
        ypb = -m*mp.sin(theta)*mp.sin(alpha) + mp.cos(theta)*mp.cos(alpha)
        return mp.cos(s*vv)*yb + mp.sin(s*vv)*ypb/s

def norm_n_mp(s, a, b, R):
    m = mp.sqrt(R); L = b-a; beta = 1-b
    alpha = s*a; theta = s*m*L
    I1 = a/2 - mp.sin(2*alpha)/(4*s)
    Icc = L/2 + mp.sin(2*theta)/(4*s*m)
    Iss = L/2 - mp.sin(2*theta)/(4*s*m)
    Ics = mp.sin(theta)**2/(2*s*m)
    sa = mp.sin(alpha); ca = mp.cos(alpha)
    I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb_scaled = sa*mp.cos(theta) + (ca/m)*mp.sin(theta)
    ypb = -m*mp.sin(theta)*mp.sin(alpha) + mp.cos(theta)*mp.cos(alpha)
    Icc3 = beta/2 + mp.sin(2*s*beta)/(4*s)
    Iss3 = beta/2 - mp.sin(2*s*beta)/(4*s)
    Ics3 = mp.sin(s*beta)**2/(2*s)
    I3 = (yb_scaled**2*Icc3 + ypb**2*Iss3 + 2*yb_scaled*ypb*Ics3)/s**2
    return (I1 + R*I2)/s**2 + I3

s1, s2 = roots2_mp(a, b, R)
n1, n2 = norm_n_mp(s1, a, b, R), norm_n_mp(s2, a, b, R)
q = mp.sqrt((s1**2/n1)/(s2**2/n2))
print("s1 =", mp.nstr(s1, 20), " s2 =", mp.nstr(s2, 20))
print("q  =", mp.nstr(q, 20))

def v_mp(x):
    return y_at_mp(s2, a, b, R, x)/y_at_mp(s1, a, b, R, x)

# crossings
def cross(target):
    lo, hi = mp.mpf('1e-12'), mp.mpf('1') - mp.mpf('1e-12')
    gl = v_mp(lo) - target; gh = v_mp(hi) - target
    if (gl > 0) == (gh > 0):
        return None
    for _ in range(300):
        md = (lo+hi)/2
        if (v_mp(md) - target > 0) == (gl > 0):
            lo = md
        else:
            hi = md
    return (lo+hi)/2

xm = cross(q); xp = cross(-q)
print("xm =", mp.nstr(xm, 20))
print("xp =", mp.nstr(xp, 20))
print("v(xp)+q =", mp.nstr(v_mp(xp)+q, 10), " v(1-) =", mp.nstr(v_mp(1-mp.mpf('1e-30')), 20))
print("M =", mp.nstr((xm+xp)/2 - (a+b)/2, 20))