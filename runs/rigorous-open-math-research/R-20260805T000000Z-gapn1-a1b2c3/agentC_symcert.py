# -*- coding: utf-8 -*-
"""Clean symbolic certificate for dG/dmu < 0 (c>=1)."""
import sympy as sp
mu, c = sp.symbols('mu c', positive=True)
A = 1 + mu*c
G = (mu+c)**2/(3*mu**2)*(2*mu**2/A**2 + mu/(A*(1+c)))
dG = sp.simplify(sp.diff(G, mu))
num, den = sp.fraction(sp.together(dG))
numf = sp.factor(num)
denf = sp.factor(den)
print("dG/dmu =", sp.simplify(numf/denf))
s, t = sp.symbols('s t', nonnegative=True)
Nst = sp.expand(num.subs({c: t+1, mu: s+1}))
print("num(s,t) =", sp.factor(Nst))
print("den(s,t) =", sp.factor(den.subs({c: t+1, mu: s+1})))
# G(1,c) check
print("G(1,c) =", sp.simplify(G.subs(mu, 1)))
# G(1,c) symbolic:
print("G(1,c) simplified:", sp.simplify((1+c)**2/3*(2/(1+c)**2 + 1/((1+c)*(1+c)))))
# explicit constants for the first-order computation
u0 = sp.acos(sp.Rational(1,4))/sp.pi
I_expr = sp.Rational(3,2)*u0 + 9*sp.sqrt(15)/(64*sp.pi) - sp.Rational(3,4)
print("I symbolic:", sp.simplify(I_expr))
print("I numeric:", float(I_expr.evalf(20)))
print("c = 4 pi^2 I numeric:", float((4*sp.pi**2*I_expr).evalf(20)))
