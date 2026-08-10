# -*- coding: utf-8 -*-
"""sym_order1_check.py - first-order check: secular-equation expansion reproduces lambda_k'."""
import sympy as sp
pi = sp.pi
a, b, e, s = sp.symbols("a b e s", real=True)
q = sp.sqrt(1+e)
w = b - a

def F(s_):
    th = q*s_*w
    cb, sb = sp.cos(s_*(1-b)), sp.sin(s_*(1-b))
    sa, ca = sp.sin(s_*a), sp.cos(s_*a)
    ct, st = sp.cos(th), sp.sin(th)
    return cb*(sa*ct + ca*st/q) + sb*(ca*ct - q*sa*st)

def root1(k):
    s0 = k*pi
    Fexp = sp.series(F(s0 + e*s), e, 0, 2).removeO()
    c1 = sp.diff(Fexp, e).subs(e, 0)
    # c1 = F'(s0)*s + F1(s0); F'(s0) = cos(k pi) = (-1)^k
    s1 = sp.solve(sp.Eq(c1, 0), s)[0]
    return sp.simplify(s1)

for k in (1, 2):
    s1 = root1(k)
    lam1 = 2*k*pi*s1
    lam1 = sp.expand_trig(lam1)
    lam1 = sp.simplify(lam1)
    print("k =", k)
    print("  s1 =", s1)
    print("  lam1' =", lam1)
    print()
