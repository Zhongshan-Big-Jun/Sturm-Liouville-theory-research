# -*- coding: utf-8 -*-
"""keylemma_lib.py -- independent high-precision core for the KEY LEMMA problem.
Run: R-20260806T011500Z-keylemma-E58FB1.  Re-derived from scratch; mpmath 60-digit.
All root solves are plain bisection exploiting strict monotonicity (E, O strictly
decreasing, so E - c*alpha and O - c*alpha are strictly decreasing: unique root).
"""
import mpmath as mp

def Phi(alpha, q):
    return mp.cos(alpha)**2 + q*q*mp.sin(alpha)**2

def Wfun(alpha):
    # W(alpha) = 3 + 2 alpha cot(alpha)
    return 3 + 2*alpha/mp.tan(alpha)

def E_curve(alpha, q):
    # even secular curve: beta = E(alpha) = arctan(1/(q tan alpha)), alpha in (0, pi/2)
    return mp.atan(1.0/(q*mp.tan(alpha)))

def O_curve(alpha, q):
    # odd secular curve: beta = O(alpha), alpha in (0, pi)
    # O is continuous with value pi/2 at alpha = pi/2 (tan(pi/2) is divergent;
    # the exact value is pi/2).  Special-case it to avoid floating-point tan(pi/2).
    if alpha == mp.pi/2:
        return mp.pi/2
    if alpha < mp.pi/2:
        return mp.pi - mp.atan(q*mp.tan(alpha))
    else:
        return mp.atan(-q*mp.tan(alpha))

def bisect(f, lo, hi, tol=None, maxit=400):
    if tol is None:
        tol = mp.mpf(10)**(-(mp.mp.dps-5))
    flo, fhi = f(lo), f(hi)
    if flo*fhi > 0:
        raise ValueError('no sign change')
    for _ in range(maxit):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0 or (hi-lo)/2 < tol:
            return mid
        if flo*fm < 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo+hi)/2

def alpha1_of_c(c, q):
    """solve E(alpha) = c*alpha on (0, pi/2); unique root, E-c*alpha strictly decreasing."""
    if c == 0:
        return mp.pi/2
    return bisect(lambda a: E_curve(a, q) - c*a, mp.mpf('1e-50'), mp.pi/2)

def alpha2_of_c(c, q):
    """solve O(alpha) = c*alpha on (0, pi); unique root (c in (0, inf))."""
    if c == 0:
        return mp.pi
    return bisect(lambda a: O_curve(a, q) - c*a, mp.mpf('1e-50'), mp.pi)

def Mfun(alpha, c, q):
    return q*(q*q-1)*alpha*alpha*mp.sin(alpha)**2/(q + c*Phi(alpha, q))

def M1_of_c(c, q):
    return Mfun(alpha1_of_c(c, q), c, q)

def M2_of_c(c, q):
    return Mfun(alpha2_of_c(c, q), c, q)

def F_of_c(c, q):
    return M1_of_c(c, q) - M2_of_c(c, q)

def Gfun(alpha, c, q):
    """G(alpha;c) = (d/dc) log M(alpha(c),c) along either curve (slope -q/Phi)."""
    Ph = Phi(alpha, q)
    W = Wfun(alpha)
    return -Ph*W/(q + c*Ph) + 2*c*alpha*Ph*(q*q-1)*mp.sin(alpha)*mp.cos(alpha)/(q + c*Ph)**2

def G1_of_c(c, q):
    return Gfun(alpha1_of_c(c, q), c, q)

def G2_of_c(c, q):
    return Gfun(alpha2_of_c(c, q), c, q)

def u_from_c(c, q):
    return q/(2.0*(c+q))

def f_sym_formula(c, q):
    u = u_from_c(c, q)
    return 2*(c+q)*F_of_c(c, q)/(q*u*u*(q*q-1))

def half_problem_s(R, u, which, digits=50):
    """first half-problem eigenvalue square root s: even (Neumann at 1/2) or odd (Dirichlet).
    rho = 1 on [0,u], R on [u,1/2].  Independent of the phase solver."""
    mp.mp.dps = digits
    qq = mp.sqrt(R)
    v = mp.mpf(1)/2 - u
    if which == 'even':
        f = lambda s: mp.cos(s*u)*mp.cos(s*qq*v) - qq*mp.sin(s*u)*mp.sin(s*qq*v)
        lo, hi = mp.mpf('1e-50'), mp.pi*mp.mpf('0.99999')
    else:
        f = lambda s: qq*mp.sin(s*u)*mp.cos(s*qq*v) + mp.cos(s*u)*mp.sin(s*qq*v)
        lo, hi = mp.mpf('1e-50'), mp.pi*mp.mpf('1.99999')
    return bisect(f, lo, hi)

