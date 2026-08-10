# -*- coding: utf-8 -*-
"""t3_b2_boundary_factor: symbolic factor of B2 on q1 line and c=0.4 slice."""
import sympy as sp

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
w = sp.symbols('w', positive=True)

# B2 symbolic
G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
      + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
      + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
      - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
      + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
B2 = -sg*t*G0 + A*sp.sqrt(w*(1-w))*(cg*G1 - A*w*F)

g = sp.symbols('g', positive=True)
s, c = sp.symbols('s c', positive=True)

# q=1 line: A = pi-g, t = g, sg=s, cg=c, st=s, ct=c, w=c^2
sub_q1 = {A: sp.pi-g, t: g, sg: s, cg: c, st: s, ct: c, w: c**2}
B2_q1 = sp.expand(B2.subs(sub_q1))
print('B2_q1 terms:', len(sp.Add.make_args(B2_q1)))
try:
    print('factor:', sp.factor(B2_q1))
except Exception as e:
    print('factor failed:', e)

# c=0.4 slice: t = 2A/5, gamma = pi-A
u = sp.symbols('u', positive=True)
# parametrize A = 5u/2, t = u  =>  c = 2/5; gamma = pi - 5u/2
# for A in [5pi/7, pi-0.655]: u = 2A/5 in [2pi/7, 2(pi-0.655)/5]
sub_c04 = {A: sp.Rational(5,2)*u, t: u, sg: sp.sin(sp.pi - sp.Rational(5,2)*u), cg: sp.cos(sp.pi - sp.Rational(5,2)*u),
           st: sp.sin(u), ct: sp.cos(u), w: sp.cos(u)**2}
B2_c04 = sp.expand(B2.subs(sub_c04))
B2_c04 = sp.trigsimp(B2_c04)
print()
print('B2_c04 trigsimp terms:', len(sp.Add.make_args(sp.expand(B2_c04))))
try:
    print('factor:', sp.factor(sp.expand(B2_c04)))
except Exception as e:
    print('factor failed:', e)
