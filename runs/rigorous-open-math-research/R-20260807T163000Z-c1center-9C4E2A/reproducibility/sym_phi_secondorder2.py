# -*- coding: utf-8 -*-
"""sym_phi_secondorder2.py - fast second-order perturbation via manual Taylor expansion of trig args.
Helper: trig of polynomial-in-e arguments expanded by hand (no nested sp.series)."""
import sympy as sp
import time
pi = sp.pi
a, b, e = sp.symbols("a b e", real=True)
s1v, s2v = sp.symbols("s1v s2v", real=True)
t0 = time.time()

def exp2(expr):
    """keep terms up to e^2 (Poly-based truncation)."""
    p = sp.Poly(sp.expand(expr), e)
    return sp.Add(*[p.coeff_monomial(e**j)*e**j for j in range(min(3, p.degree()+1))])

def tsin(arg, n=3):
    """sin(arg) to order e^n with arg a polynomial in e of deg <= n."""
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.sin(c0)*c_r + sp.cos(c0)*s_r)

def tcos(arg, n=3):
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.cos(c0)*c_r - sp.sin(c0)*s_r)

# q = sqrt(1+e) to order 2 (order 3 for safety in products)
q2 = 1 + e/2 - e**2/8 + e**3/16
qinv2 = 1 - e/2 + 3*e**2/8

def build_root(k):
    """return s(eps) = k*pi + s1*e + s2*e^2 (s1,s2 symbolic) and F-coefficients."""
    s0 = k*pi
    # F = cb*(sa*ct + ca*st/q) + sb*(ca*ct - q*sa*st),  th = q s w
    se = s0 + s1v*e + s2v*e**2
    th = sp.expand(q2*se*(b-a))
    sa = tsin(se*a); ca = tcos(se*a)
    sb = tsin(se*(1-b)); cb = tcos(se*(1-b))
    st = tsin(th); ct = tcos(th)
    F = sp.expand(cb*(sa*ct + ca*st*qinv2) + sb*(ca*ct - sa*st*q2))
    F = exp2(F)
    c1 = sp.expand(sp.diff(F, e).subs(e, 0))
    c2 = sp.expand(sp.diff(F, e, 2).subs(e, 0)/2)
    c1s = sp.trigsimp(sp.expand_trig(c1))
    sol1 = sp.solve(sp.Eq(c1s, 0), s1v)[0]
    c2s = sp.simplify(sp.expand_trig(c2.subs(s1v, sol1)))
    sol2 = sp.solve(sp.Eq(c2s, 0), s2v)[0]
    return sol1, sol2

s11, s12 = build_root(1)
s21, s22 = build_root(2)
print("s11 =", sp.simplify(sp.expand_trig(s11)))
print("s12 =", sp.simplify(sp.expand_trig(s12)))
print("s21 =", sp.simplify(sp.expand_trig(s21)))
print("s22 =", sp.simplify(sp.expand_trig(s22)), flush=True)
print("roots %.1fs" % (time.time()-t0))

def build_lam(k, s1, s2):
    lp = sp.expand(2*k*pi*s1)
    lpp = sp.expand(s1**2 + 2*k*pi*s2)
    return sp.trigsimp(sp.expand_trig(lp)), sp.trigsimp(sp.expand_trig(lpp))

l1p, l1pp = build_lam(1, s11, s12)
l2p, l2pp = build_lam(2, s21, s22)
print("lambda1' =", l1p)
print("lambda1'' =", l1pp)
print("lambda2' =", l2p)
print("lambda2'' =", l2pp, flush=True)
print("lams %.1fs" % (time.time()-t0))
