# -*- coding: utf-8 -*-
"""t3_b2_q1_factor2: factor B2 on q=1 line (st=s, ct=c direct)."""
import sympy as sp

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
w = sp.symbols('w', positive=True)

G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
      + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
      + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
      - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
      + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
B2 = -sg*t*G0 + A*st*ct*(cg*G1 - A*w*F)

g = sp.symbols('g', positive=True)
s, c = sp.symbols('s c', positive=True)
# q=1 line: A = pi-g, t = g, sg = s, cg = c, st = s, ct = c, w = c^2
sub = {A: sp.pi-g, t: g, sg: s, cg: c, st: s, ct: c, w: c**2}
B2_q1 = sp.expand(B2.subs(sub))
print('B2_q1 terms:', len(sp.Add.make_args(B2_q1)))
try:
    fac = sp.factor(B2_q1)
    print('factor:', fac)
except Exception as e:
    print('factor failed:', e)
# check sign at g=2pi/7 and g=pi/3 numerically
import math
gv = 2*math.pi/7
val = float(B2_q1.subs({g: gv, s: math.sin(gv), c: math.cos(gv)}).evalf(20))
print('B2q1(2pi/7) =', val)
gv = math.pi/3
val = float(B2_q1.subs({g: gv, s: math.sin(gv), c: math.cos(gv)}).evalf(20))
print('B2q1(pi/3) =', val)
