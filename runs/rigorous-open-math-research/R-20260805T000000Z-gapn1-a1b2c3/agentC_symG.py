# -*- coding: utf-8 -*-
import sympy as sp
mu, c = sp.symbols('mu c', positive=True)
A = 1 + mu*c
G = (mu+c)**2/(3*mu**2)*(2*mu**2/A**2 + mu/(A*(1+c)))
dG = sp.simplify(sp.diff(G, mu))
print("dG/dmu =", dG)
num, den = sp.fraction(sp.together(dG))
print("numerator:", sp.expand(num))
print("denominator:", sp.expand(den))
# check numerator negativity via factorization
print("factor numerator:", sp.factor(num))
# Try substitute t = c-1 >= 0 and s = mu-1 > 0
t, s = sp.symbols('t s', nonnegative=True)
num_sub = num.subs({c: t+1, mu: s+1})
print("num(s,t):", sp.factor(sp.expand(num_sub)))
