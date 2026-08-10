# -*- coding: utf-8 -*-
import sympy as sp
pi = sp.pi
b = sp.symbols("b", real=True)
s15 = sp.sqrt(15)
# a0 as a symbol; we need pi*a0 = acos(1/4) but expressions contain pi*a0.
pa0 = sp.Symbol("pa0", positive=True)  # pi*a0 = arccos(1/4)
u = sp.cos(2*pi*b); v = sp.sin(2*pi*b)
m = 56*pa0 - 6*s15
n = 2*pa0 + 3*s15
expr = (1-u)*(m*(1+u)+n) + 2*s15*pi*(1-b)*(4*u-1)*v
# phi' * 60 pi = expr
d1 = sp.diff(expr, b); d2 = sp.diff(expr, b, 2); d3 = sp.diff(expr, b, 3)
subs = {sp.sin(2*pi): 0, sp.cos(2*pi): 1}
d1v = sp.simplify(d1.subs(b, 1))
d2v = sp.simplify(d2.subs(b, 1))
d3v = sp.simplify(d3.subs(b, 1))
print("phi'(1)*60pi =", d1v)
print("phi''(1)*60pi =", d2v)
print("phi'''(1)*60pi =", sp.factor(d3v))
Fc0 = sp.Rational(15,4)*pi**3*s15
print("phi''' =", sp.simplify(d3v/(60*pi)))
print("-Fc0*phi''' =", sp.simplify(-Fc0*d3v/(60*pi)))
# numeric with pa0 = arccos(1/4) ~ 1.318116071652818
pa0v = 1.318116071652818
print("numeric phi''' =", float(sp.N(d3v/(60*pi), 40).subs(pa0, pa0v)))
print("numeric -Fc0*phi''' =", float(sp.N(-Fc0*d3v/(60*pi), 40).subs(pa0, pa0v)))
