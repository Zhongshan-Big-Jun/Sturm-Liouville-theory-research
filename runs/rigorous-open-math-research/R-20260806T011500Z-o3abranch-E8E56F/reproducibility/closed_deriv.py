# -*- coding: utf-8 -*-
"""closed_deriv.py: closed-form g1', g2' via the implicit system (sec equations + residual).
Verifies against finite differences of R1/R2."""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
from clean_lib import sec, norm_n, y_at, roots2, R1_R2

def r1(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1**2*(np.sin(s1*a)/s1)**2/n1 - s2**2*(np.sin(s2*a)/s2)**2/n2

def r2(a, b, R, s1, s2):
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return s1**2*y_at(s1, a, b, R, b)**2/n1 - s2**2*y_at(s2, a, b, R, b)**2/n2

def partials(a, b, R, s1, s2, h=1e-6):
    """All needed partials via central differences of explicit functions."""
    def fd(f, *args, i, h):
        args1 = list(args); args2 = list(args)
        args1[i] += h; args2[i] -= h
        return (f(*args1) - f(*args2))/(2*h)
    sec_a1 = fd(sec, s1, a, b, R, i=1, h=h); sec_b1 = fd(sec, s1, a, b, R, i=2, h=h); sec_s1 = fd(sec, s1, a, b, R, i=0, h=h)
    sec_a2 = fd(sec, s2, a, b, R, i=1, h=h); sec_b2 = fd(sec, s2, a, b, R, i=2, h=h); sec_s2 = fd(sec, s2, a, b, R, i=0, h=h)
    r1_a = fd(r1, a, b, R, s1, s2, i=0, h=h); r1_b = fd(r1, a, b, R, s1, s2, i=1, h=h)
    r1_s1 = fd(r1, a, b, R, s1, s2, i=3, h=h); r1_s2 = fd(r1, a, b, R, s1, s2, i=4, h=h)
    r2_a = fd(r2, a, b, R, s1, s2, i=0, h=h); r2_b = fd(r2, a, b, R, s1, s2, i=1, h=h)
    r2_s1 = fd(r2, a, b, R, s1, s2, i=3, h=h); r2_s2 = fd(r2, a, b, R, s1, s2, i=4, h=h)
    return dict(sec_a1=sec_a1, sec_b1=sec_b1, sec_s1=sec_s1, sec_a2=sec_a2, sec_b2=sec_b2, sec_s2=sec_s2,
                r1_a=r1_a, r1_b=r1_b, r1_s1=r1_s1, r1_s2=r1_s2, r2_a=r2_a, r2_b=r2_b, r2_s1=r2_s1, r2_s2=r2_s2)

def g1p_closed(a, b, R, s1, s2, P=None):
    if P is None: P = partials(a, b, R, s1, s2)
    num = -P['r1_a'] + P['r1_s1']*P['sec_a1']/P['sec_s1'] + P['r1_s2']*P['sec_a2']/P['sec_s2']
    den = P['r1_b'] - P['r1_s1']*P['sec_b1']/P['sec_s1'] - P['r1_s2']*P['sec_b2']/P['sec_s2']
    return num/den

def g2p_closed(a, b, R, s1, s2, P=None):
    if P is None: P = partials(a, b, R, s1, s2)
    num = -P['r2_a'] + P['r2_s1']*P['sec_a1']/P['sec_s1'] + P['r2_s2']*P['sec_a2']/P['sec_s2']
    den = P['r2_b'] - P['r2_s1']*P['sec_b1']/P['sec_s1'] - P['r2_s2']*P['sec_b2']/P['sec_s2']
    return num/den

if __name__ == "__main__":
    # test at the R=4 fp and at a point on each branch
    a0 = np.arccos(0.25)/np.pi; b0 = np.arccos(-0.25)/np.pi
    R = 4.0
    test_pts = [(0.451485465757, 0.548514534243), (0.45, 0.544), (0.50, 0.56), (0.55, 0.58)]
    for (a, b) in test_pts:
        s1, s2 = roots2(a, b, R)
        P = partials(a, b, R, s1, s2)
        # FD check of total derivatives dR1/da (with s implicit) - compare with branch formula consistency:
        # r1_a + r1_b*g1' + r1_s1*s1' + r1_s2*s2' should = 0
        s1a = -(P['sec_a1'] + P['sec_b1']*g1p_closed(a,b,R,s1,s2,P))/P['sec_s1']
        s2a = -(P['sec_a2'] + P['sec_b2']*g1p_closed(a,b,R,s1,s2,P))/P['sec_s2']
        resid = P['r1_a'] + P['r1_b']*g1p_closed(a,b,R,s1,s2,P) + P['r1_s1']*s1a + P['r1_s2']*s2a
        g1p = g1p_closed(a, b, R, s1, s2, P); g2p = g2p_closed(a, b, R, s1, s2, P)
        print(f"({a},{b}): g1'={g1p:.6f} g2'={g2p:.6f} branch-resid={resid:.2e}")
    # verify vs FD of branch at fp
    a, b, R = 0.451485465757, 0.548514534243, 4.0
    # find branch points at a+-h using clean_lib residual root find
    from scipy.optimize import brentq
    def R1sc(a, b, R):
        s1, s2 = roots2(a, b, R)
        return r1(a, b, R, s1, s2)
    h = 1e-5
    for (da, which) in [(0, 'both')]:
        pass
    # g1 at a and a+h
    def g1_at(aa):
        f = lambda bb: R1sc(aa, bb, R)
        return brentq(f, aa+1e-6, 1-1e-6)
    def g2_at(aa):
        s = lambda bb: r2(aa, bb, R, *roots2(aa, bb, R))
        return brentq(s, aa+1e-6, 1-1e-6)
    aa = 0.47
    g1 = g1_at(aa); g2 = g2_at(aa)
    s1, s2 = roots2(aa, g1, R)
    c1 = g1p_closed(aa, g1, R, s1, s2)
    fd1 = (g1_at(aa+h) - g1_at(aa-h))/(2*h)
    s1, s2 = roots2(aa, g2, R)
    c2 = g2p_closed(aa, g2, R, s1, s2)
    fd2 = (g2_at(aa+h) - g2_at(aa-h))/(2*h)
    print(f"a={aa}: g1' closed={c1:.8f} FD={fd1:.8f} diff={abs(c1-fd1):.2e}")
    print(f"a={aa}: g2' closed={c2:.8f} FD={fd2:.8f} diff={abs(c2-fd2):.2e}")
