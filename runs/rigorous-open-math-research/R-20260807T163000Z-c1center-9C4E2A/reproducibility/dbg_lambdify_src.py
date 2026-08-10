# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.prec = 200
import sympy as sp, pickle
d = pickle.load(open("R1_partials_exprs.pkl","rb"))
s1s, s2s, a_s, b_s, R_s = sp.symbols("s1 s2 a b R")
expr = sp.sympify(d["R1"])
expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(1, 2), lambda t: sp.sqrt(t.base))
expr = expr.replace(lambda t: t.is_Pow and t.exp == sp.Rational(-1, 2), lambda t: 1/sp.sqrt(t.base))
mods = [{"sin": iv.sin, "cos": iv.cos, "sqrt": iv.sqrt}, "mpmath"]
f = sp.lambdify((s1s, s2s, a_s, b_s, R_s), expr, modules=mods)
import inspect
src = inspect.getsource(f)
print(src[:3000])
