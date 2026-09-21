# -*- coding: utf-8 -*-
"""05_interval_value.py
Rigorous interval enclosure of u* and Dbar(u*) via mpmath.iv (directed
rounding interval arithmetic), and the strict inequality Dbar(u*) < 3 pi^2
with explicit margin.

Method (all evaluations are rigorous interval extensions; mpmath.iv uses
directed rounding):
 1. Approximate u0 (root of S) with plain high-precision floats.
 2. Rigorous bisection for u*: keep a bracket [L, H] with F(L) < 0 < F(H)
    verified by interval evaluation at points; S is strictly increasing
    locally on the bracket (Part I proves the sign structure of S: exactly
    one root, sign - then +).  The bracket certifies u* in [L, H].
 3. Enclose a(u) = unique root of tan a = a(1-1/(2u)) on (pi/2, pi) by the
    same bisection at the bracket endpoints (F(a;u) is strictly increasing
    in a on (pi/2, pi), Part I).
 4. Dbar(u*) in mu2([L,H]) - mu1([L,H]) by monotone interval extension.
 5. Compare with the rigorous interval 3 pi^2.

ASCII punctuation. Run: python 05_interval_value.py
"""
import mpmath as mp
from mpmath import iv
iv.dps = 45
mp.mp.dps = 50

def bracket_root(F, x_lo, x_hi, tol):
    """F: (mpf point) -> interval.  F is strictly increasing on [x_lo, x_hi]
    with F(x_lo) < 0 < F(x_hi) (verified by the caller or by evaluation).
    Return (L, H) with F(L) < 0 < F(H) and H - L <= tol, a rigorous bracket
    of the unique root of F = 0."""
    L, H = mp.mpf(x_lo), mp.mpf(x_hi)
    # verify sign separation at the start
    fl = F(L); fh = F(H)
    assert fl.b < 0 and fh.a > 0, "initial bracket not sign-separated"
    while H - L > tol:
        m = (L + H)/2
        fm = F(m)
        if fm.b < 0:
            L = m
        elif fm.a > 0:
            H = m
        else:
            # 0 in F(m): m is within the evaluation width of the root;
            # the current bracket [L, H] already contains the root and is
            # sign-separated; stop (width may be a bit above tol, but the
            # bracket is rigorous).  Optionally widen nothing.
            break
    return (L, H)

def F_a_iv(a, u):
    """F(a;u) = tan a - a(1 - 1/(2u)) as an interval; u, a are mpf points."""
    uu = mp.mpf(u)
    return iv.tan(iv.mpf((mp.mpf(a), mp.mpf(a)))) - iv.mpf((mp.mpf(a), mp.mpf(a)))*(1 - 1/(2*uu))

def a_root(u, tol=mp.mpf('1e-40')):
    """Rigorous bracket of the unique root of F(a;u) = 0 on (pi/2, pi)."""
    F = lambda a: F_a_iv(a, u)
    # verify sign separation at endpoints: F(pi/2+) < 0, F(pi-) > 0
    a_lo = mp.mpf('1.57079632679489661923132169163975144209858469968755') + mp.mpf('1e-45')
    a_hi = mp.mpf('3.14159265358979323846264338327950288419716939937511') - mp.mpf('1e-45')
    fl = F(a_lo); fh = F(a_hi)
    if not (fl.b < 0 and fh.a > 0):
        # near the endpoints tan blows up; scan for a sign-separated bracket
        for k in range(1, 1000):
            x = a_lo + (a_hi - a_lo)*k/1000
            fx = F(x)
            if fx.b < 0:
                a_lo = x
            elif fx.a > 0:
                a_hi = x
                break
    return bracket_root(F, a_lo, a_hi, tol)

def S_point(u):
    """Interval evaluation of S at the point u in (0,1/2)."""
    aL, aH = a_root(u)
    aint = iv.mpf((mp.mpf(aL), mp.mpf(aH)))
    uc = iv.mpf((mp.mpf(u), mp.mpf(u)))
    mu1 = iv.pi**2/(4*uc*uc)
    mu2 = (aint/uc)**2
    I2 = uc/2 - iv.sin(2*aint)*uc/(4*aint)
    return mu1*2/uc - mu2*iv.sin(aint)**2/I2

# 1. approximate root (plain high-precision floats, non-rigorous)
def a_of(u):
    return mp.findroot(lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u)),
                       (mp.pi/2 + mp.mpf('0.7'), mp.pi - mp.mpf('0.7')))
def Sf(u):
    a = a_of(u)
    mu1 = mp.pi**2/(4*u**2); mu2 = (a/u)**2
    I2 = u/2 - mp.sin(2*a)*u/(4*a)
    return mu1*2/u - mu2*mp.sin(a)**2/I2
u0 = mp.findroot(Sf, mp.mpf('0.32992250812'))
print("float u0 =", mp.nstr(u0, 40))

# 2. rigorous bracket of u* via bisection with sign-separated invariant
tol_u = mp.mpf('1e-40')
L0 = u0 - mp.mpf('1e-20'); H0 = u0 + mp.mpf('1e-20')
L, H = bracket_root(S_point, L0, H0, tol_u)
print("S(L) =", S_point(L), " S(H) =", S_point(H))
print("rigorous bracket u* in [", mp.nstr(L, 40), ",", mp.nstr(H, 40), "]")
print("bracket width =", mp.nstr(H - L, 5))

# 3. enclosures at the bracket endpoints
aL, _ = a_root(L)
aH, _ = a_root(H)
aint = iv.mpf((mp.mpf(aL), mp.mpf(aH)))
ucell = iv.mpf((mp.mpf(L), mp.mpf(H)))
mu1_iv = iv.pi**2/(4*ucell*ucell)
mu2_iv = (aint/ucell)**2
Dbar_iv = mu2_iv - mu1_iv
print("a(u*) in [", mp.nstr(aL, 35), ",", mp.nstr(aH, 35), "]")
print("mu1(u*) in", mu1_iv)
print("mu2(u*) in", mu2_iv)
print("Dbar(u*) in", Dbar_iv)
three_pi2 = 3*iv.pi**2
print("3 pi^2 in", three_pi2)
margin = three_pi2.a - Dbar_iv.b
print("margin (3 pi^2 - Dbar(u*)) >= ", mp.nstr(margin, 15))
print("ratio Dbar/(3 pi^2) in [", mp.nstr(Dbar_iv.a/three_pi2.b, 18), ",",
      mp.nstr(Dbar_iv.b/three_pi2.a, 18), "]")

assert Dbar_iv.b < three_pi2.a
assert Dbar_iv.a > mp.mpf('24.94386613')
assert Dbar_iv.b < mp.mpf('24.94386614')
assert L < mp.mpf('0.329922509') and H > mp.mpf('0.329922507')
print("PASS")