# -*- coding: utf-8 -*-
"""kl2_lib.py -- independent core for run R-20260806T050000Z-keylemma2-5A35E5.
Re-derived from the normalized contract (problem_contract.md of the parent run).
All root solves: bisection on strictly monotone functions. mpmath 60 digits.
"""
import mpmath as mp

def Phi(a, q):
    return mp.cos(a)**2 + q*q*mp.sin(a)**2

def Wfun(a):
    return 3 + 2*a/mp.tan(a)

def even_beta(a, q):
    return mp.atan(1.0/(q*mp.tan(a)))

def odd_beta(a, q):
    if a == mp.pi/2:
        return mp.pi/2
    if a < mp.pi/2:
        return mp.pi - mp.atan(q*mp.tan(a))
    return mp.atan(-q*mp.tan(a))

def bisect(f, lo, hi, tol=None, maxit=500):
    if tol is None:
        tol = mp.mpf(10)**(-(mp.mp.dps - 6))
    flo = f(lo)
    fhi = f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo*fhi > 0:
        raise ValueError('no sign change on interval')
    for _ in range(maxit):
        mid = (lo + hi)/2
        fm = f(mid)
        if fm == 0 or (hi - lo)/2 < tol:
            return mid
        if flo*fm < 0:
            hi = mid
        else:
            lo = mid
            flo = fm
    return (lo + hi)/2

def alpha1(c, q):
    return bisect(lambda a: even_beta(a, q) - c*a, mp.mpf('1e-60'), mp.pi/2)

def alpha2(c, q):
    return bisect(lambda a: odd_beta(a, q) - c*a, mp.mpf('1e-60'), mp.pi)

def Mtilde(a, c, q):
    return a*a*mp.sin(a)**2/(q + c*Phi(a, q))

def Gfun(a, c, q):
    Ph = Phi(a, q)
    D = q + c*Ph
    return -Ph*Wfun(a)/D + 2*c*a*Ph*(q*q - 1)*mp.sin(a)*mp.cos(a)/D**2

def G1(c, q):
    return Gfun(alpha1(c, q), c, q)

def G2(c, q):
    return Gfun(alpha2(c, q), c, q)

def M1t(c, q):
    return Mtilde(alpha1(c, q), c, q)

def M2t(c, q):
    return Mtilde(alpha2(c, q), c, q)

def Fp_t(c, q):
    return M1t(c, q)*G1(c, q) - M2t(c, q)*G2(c, q)

def dGdc(a, c, q):
    """total derivative d/dc of G(alpha(c);c) along a curve (slope -q/Phi)."""
    Ph = Phi(a, q)
    D = q + c*Ph
    s, co = mp.sin(a), mp.cos(a)
    # G = -Ph*W/D + 2 c a Ph (q^2-1) s co / D^2
    W = Wfun(a)
    # partial c
    Gc = Ph*W*Ph/D**2 + (2*a*Ph*(q*q-1)*s*co)*(D - 2*c*Ph)/D**3
    # partial a
    Pha = 2*(q*q-1)*s*co
    Wp = 2*(s*co - a)/mp.sin(a)**2
    Wa = 0  # placeholder, compute directly below
    # d/da [ -Ph*W/D ] = -(Pha*W + Ph*Wp)/D + Ph*W*Pha*c/D^2
    d1 = -(Pha*W + Ph*Wp)/D + Ph*W*c*Pha/D**2
    # d/da [ 2 c a Ph (q2-1) s co / D^2 ]
    sc = s*co
    dsc = co*co - s*s
    d2a = 2*c*(q*q-1)*(Ph*a*dsc + Ph*sc + a*Pha*sc)/D**2
    d2b = -4*c*c*a*Ph*(q*q-1)*sc*Pha/D**3
    Ga = d1 + d2a + d2b
    ap = -a*Ph/D
    return Ga*ap + Gc

def Jfun(a, c, q):
    return Gfun(a, c, q)**2 + dGdc(a, c, q)

def Hp(c, q):
    return dGdc(alpha2(c, q), c, q) - dGdc(alpha1(c, q), c, q)

def Fpp_t(c, q):
    return M1t(c, q)*Jfun(alpha1(c, q), c, q) - M2t(c, q)*Jfun(alpha2(c, q), c, q)

def gamma_of(q, c):
    return mp.pi - alpha2(c, q)

def c_of_gamma(q, gamma):
    return mp.atan(q*mp.tan(gamma))/(mp.pi - gamma)

def B_of_gamma(q, gamma):
    """G2 * (q + c Phi)^2 / Phi in (q,gamma) coordinates; sign(G2) = sign(B)."""
    c = c_of_gamma(q, gamma)
    t = mp.tan(gamma)
    Phi = (1 + q*q*t*t)/(1 + t*t)
    return (2*(mp.pi - gamma)/t - 3)*(q + c*Phi) - 2*c*(mp.pi - gamma)*(q*q - 1)*t/(1 + t*t)

def alpha0_of_q(q):
    return 2*mp.asin(1/mp.sqrt(2*(q + 1)))
