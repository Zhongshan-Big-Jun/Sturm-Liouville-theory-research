# -*- coding: utf-8 -*-
"""t3_b2segments: B2 on (1) q=1 line t=pi-A, (2) c=0.4 line t=0.4A."""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg = sp.symbols('sg cg', positive=True)
w = sp.symbols('w', positive=True)
G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
      + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
      + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
      - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
      + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
B2 = -sg*t*G0 + A*sp.sqrt(w*(1-w))*(cg*G1 - A*w*F)

# segment 2: c=0.4, t=0.4A; w = cos^2(0.4A); gamma = pi - A
g = sp.symbols('g', positive=True)  # gamma
# param by gamma on segment 2: A = pi-g, t = 0.4(pi-g), gamma in [0.655, 2pi/7]
A2 = sp.pi - g; t2 = sp.Rational(2,5)*(sp.pi - g)
sg2 = sp.sin(g); cg2 = sp.cos(g); w2 = sp.cos(t2)**2
B2_seg2 = sp.expand(B2.subs({A: A2, t: t2, sg: sg2, cg: cg2, w: w2}))
B2_seg2 = sp.trigsimp(sp.expand(B2_seg2))
print('B2 seg2 (c=0.4):')
print(sp.simplify(B2_seg2))
print()
# segment 1: q=1, t = gamma, A = pi-g
t1 = g
B2_seg1 = sp.expand(B2.subs({A: sp.pi-g, t: g, sg: sp.sin(g), cg: sp.cos(g), w: sp.cos(g)**2}))
print('B2 seg1 (q=1):')
print(sp.simplify(B2_seg1))
