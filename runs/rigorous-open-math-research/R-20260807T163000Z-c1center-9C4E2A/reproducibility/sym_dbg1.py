# -*- coding: utf-8 -*-
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

k = 1
s0 = k*pi
Fexp = sp.series(F(s0 + e*s), e, 0, 2).removeO()
c0 = Fexp.subs(e, 0)
c1 = sp.diff(Fexp, e).subs(e, 0)
print("c0 =", sp.simplify(c0))
print("c1 =", sp.expand_trig(c1))
print("c1 simplified =", sp.simplify(sp.expand_trig(c1)))
