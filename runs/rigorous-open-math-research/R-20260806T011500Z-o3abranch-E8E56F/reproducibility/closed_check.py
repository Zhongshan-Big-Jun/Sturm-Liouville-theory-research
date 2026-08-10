# -*- coding: utf-8 -*-
"""closed_check.py: closed-form branch derivatives at R=1500, a=0.57364 (independent of branch-FD)."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at
from scipy.optimize import brentq

def roots2(a, b, R):
    s = np.concatenate([np.linspace(1e-12, 1.2, 10000), np.linspace(1.2, 3*np.pi, 10000)])
    M = sec(s, a, b, R)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    roots = []
    for i in idx[:4]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(80):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        roots.append(0.5*(lo+hi))
    roots = sorted(set(np.round(r, 13) for r in roots))
    return roots[0], roots[1]

def r1(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*(np.sin(s1*a)/s1)**2/n1 - s2*s2*(np.sin(s2*a)/s2)**2/n2
def r2(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1*s1*y_at(s1, a, b, R, b)**2/n1 - s2*s2*y_at(s2, a, b, R, b)**2/n2

def partials(a, b, R, s1, s2, h=1e-6):
    def fd(f, *args, i, h):
        a1 = list(args); a2 = list(args)
        a1[i] += h; a2[i] -= h
        return (f(*a1) - f(*a2))/(2*h)
    sec_a1 = fd(sec, s1, a, b, R, i=1, h=h); sec_b1 = fd(sec, s1, a, b, R, i=2, h=h); sec_s1 = fd(sec, s1, a, b, R, i=0, h=h)
    sec_a2 = fd(sec, s2, a, b, R, i=1, h=h); sec_b2 = fd(sec, s2, a, b, R, i=2, h=h); sec_s2 = fd(sec, s2, a, b, R, i=0, h=h)
    r1_a = fd(r1, a, b, R, s1, s2, i=0, h=h); r1_b = fd(r1, a, b, R, s1, s2, i=1, h=h)
    r1_s1 = fd(r1, a, b, R, s1, s2, i=3, h=h); r1_s2 = fd(r1, a, b, R, s1, s2, i=4, h=h)
    r2_a = fd(r2, a, b, R, s1, s2, i=0, h=h); r2_b = fd(r2, a, b, R, s1, s2, i=1, h=h)
    r2_s1 = fd(r2, a, b, R, s1, s2, i=3, h=h); r2_s2 = fd(r2, a, b, R, s1, s2, i=4, h=h)
    return dict(sec_a1=sec_a1, sec_b1=sec_b1, sec_s1=sec_s1, sec_a2=sec_a2, sec_b2=sec_b2, sec_s2=sec_s2,
                r1_a=r1_a, r1_b=r1_b, r1_s1=r1_s1, r1_s2=r1_s2, r2_a=r2_a, r2_b=r2_b, r2_s1=r2_s1, r2_s2=r2_s2)

def g1p_closed(a, b, R, s1, s2, P):
    num = -P['r1_a'] + P['r1_s1']*P['sec_a1']/P['sec_s1'] + P['r1_s2']*P['sec_a2']/P['sec_s2']
    den = P['r1_b'] - P['r1_s1']*P['sec_b1']/P['sec_s1'] - P['r1_s2']*P['sec_b2']/P['sec_s2']
    return num/den
def g2p_closed(a, b, R, s1, s2, P):
    num = -P['r2_a'] + P['r2_s1']*P['sec_a1']/P['sec_s1'] + P['r2_s2']*P['sec_a2']/P['sec_s2']
    den = P['r2_b'] - P['r2_s1']*P['sec_b1']/P['sec_s1'] - P['r2_s2']*P['sec_b2']/P['sec_s2']
    return num/den

# branch points at R=1500, a=0.57364
a = 0.57364; R = 1500.0
# g1: root of R1(a,b)=0
def R1v(b):
    s1, s2 = roots2(a, b, R); return r1(a, b, R, s1, s2)
def R2v(b):
    s1, s2 = roots2(a, b, R); return r2(a, b, R, s1, s2)
bb = np.linspace(a+1e-5, 1-1e-5, 60)
g1 = None; g2 = None
v1 = [R1v(b) for b in bb]
for i in range(59):
    if v1[i]*v1[i+1] < 0:
        g1 = brentq(R1v, bb[i], bb[i+1], xtol=1e-13); break
v2 = [R2v(b) for b in bb]
for i in range(59):
    if v2[i]*v2[i+1] < 0:
        g2 = brentq(R2v, bb[i], bb[i+1], xtol=1e-13); break
print(f"g1={g1:.8f} g2={g2:.8f} h={g1-g2:+.6e}")
for (b, which) in [(g1, 'g1'), (g2, 'g2')]:
    s1, s2 = roots2(a, b, R)
    P = partials(a, b, R, s1, s2)
    gp = g1p_closed(a, b, R, s1, s2, P) if which=='g1' else g2p_closed(a, b, R, s1, s2, P)
    print(f"  {which}'(a) closed-form = {gp:+.6f}")
