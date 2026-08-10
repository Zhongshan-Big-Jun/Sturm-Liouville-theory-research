# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
# reuse helpers from part3
import importlib.util
spec = importlib.util.spec_from_file_location("p3", r"F:\LaTeX\BVE research\scripts\audit_o3a_pdf_part3.py")
# can't import (runs everything). Reimplement minimal pieces.
def y1_mp(a, b, q, s):
    y, dy = mp.mpf('0'), mp.mpf('1')
    om = s; t = a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s*q; t = b-a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s; t = 1-b
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    return y
def eigvals_mp(a, b, q, kmax=2, N=20000):
    top = 2*mp.pi + mp.mpf('1e-3')
    lo0 = mp.mpf('1e-9')
    prev = y1_mp(a, b, q, lo0); gprev = lo0; signs = []
    for i in range(1, N+1):
        g = lo0 + (top-lo0)*i/N
        v = y1_mp(a, b, q, g)
        if prev*v < 0:
            lo, hi = gprev, g
            for _ in range(150):
                mid = (lo+hi)/2
                if y1_mp(a, b, q, mid)*y1_mp(a, b, q, lo) <= 0: hi = mid
                else: lo = mid
            signs.append((lo+hi)/2)
            if len(signs) >= kmax: break
        prev = v; gprev = g
    return signs[:kmax]
def mode_mp(a, b, q, s):
    om1 = s
    yA, dyA = mp.sin(om1*a)/om1, mp.cos(om1*a)
    om2 = s*q
    ya, dya = yA, dyA
    c, sn = mp.cos(om2*(b-a)), mp.sin(om2*(b-a))
    yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
    om3 = s
    n = (a/2 - mp.sin(2*s*a)/(4*s))/s**2
    amp2 = ya**2 + (dya/om2)**2
    cross = ya*dya/om2
    L = b-a
    n += q**2 * ( amp2*L/2 + (ya**2 - (dya/om2)**2)*mp.sin(2*om2*L)/(4*om2) + cross*(1-mp.cos(2*om2*L))/(2*om2) )
    amp2b = yb**2 + (dyb/om3)**2
    crossb = yb*dyb/om3
    L = 1-b
    n += amp2b*L/2 + (yb**2 - (dyb/om3)**2)*mp.sin(2*om3*L)/(4*om3) + crossb*(1-mp.cos(2*om3*L))/(2*om3)
    return ya, yb, n
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))
def alpha2_of_c(q, c):
    if c < 1:
        f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
        lo, hi = mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20')
    else:
        f = lambda x: mp.pi - mp.atan(q*mp.tan(x)) - c*x
        lo, hi = mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))

R = 2.0; q = mp.sqrt(mp.mpf(R))
xi = mp.mpf('0.25')
a, b = xi, 1-xi
c = q*(mp.mpf('0.5')-xi)/xi
print("xi=0.25, R=2: c =", mp.nstr(c, 10))
s1, s2 = eigvals_mp(a, b, q)
print("s1 =", mp.nstr(s1, 20), " s2 =", mp.nstr(s2, 20))
alpha1 = s1*xi; alpha2 = s2*xi
print("alpha1 =", mp.nstr(alpha1, 20), " alpha1_of_c =", mp.nstr(alpha1_of_c(q, c), 20))
print("alpha2 =", mp.nstr(alpha2, 20), " alpha2_of_c =", mp.nstr(alpha2_of_c(q, c), 20))
# check phase equations
print("tan(a1)tan(c*a1) - 1/q =", mp.nstr(mp.tan(alpha1)*mp.tan(c*alpha1) - 1/q, 4))
print("q*tan(a2)+tan(c*a2) =", mp.nstr(q*mp.tan(alpha2)+mp.tan(c*alpha2), 4))
print("alpha1 in (0,pi/2)?", 0 < alpha1 < mp.pi/2, " alpha2 in (0,pi/2)?", 0 < alpha2 < mp.pi/2)
print("c*alpha2 in (pi/2,pi)?", mp.pi/2 < c*alpha2 < mp.pi)
# SR and Fe
ya1, yb1, n1 = mode_mp(a, b, q, s1)
ya2, yb2, n2 = mode_mp(a, b, q, s2)
SR = s1**2*ya1**2/n1 - s2**2*ya2**2/n2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))
Fe_val = Mf(q, c, alpha1) - Mf(q, c, alpha2)
print("SR =", mp.nstr(SR, 6), " pred =", mp.nstr(2*(c+q)/xi**2*Fe_val, 6))
print("Fe =", mp.nstr(Fe_val, 6))
# D check: lambda2-lambda1 vs formula (12)
D = s2**2 - s1**2
D_pred = 4*(c+q)**2/q**2*(alpha2**2 - alpha1**2)
print("D =", mp.nstr(D, 10), " D_pred =", mp.nstr(D_pred, 10), " diff:", mp.nstr(abs(D-D_pred), 4))
