# -*- coding: utf-8 -*-
"""t3_b2seg2: segment 2 (c=0.4) with expand only."""
import sympy as sp

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

g = sp.symbols('g', positive=True)
# seg2: A=pi-g, t=0.4(pi-g)
A2 = sp.pi - g; t2 = sp.Rational(2,5)*(sp.pi - g)
B2s2 = sp.expand(B2.subs({A: A2, t: t2, sg: sp.sin(g), cg: sp.cos(g), w: sp.cos(t2)**2}))
B2s2 = sp.expand(B2s2)
print('seg2 terms:', len(sp.Add.make_args(B2s2)))
# substitute cos(g)^2 -> z, sin(g)*cos(g) -> s*c... use s=sin g, c=cos g as independent with s^2+c^2=1
s, c = sp.symbols('s c', positive=True)
B2s2p = sp.expand(B2s2.subs({sp.sin(g): s, sp.cos(g): c, sp.cos(sp.Rational(2,5)*(sp.pi-g)): sp.sqrt(1-s**2) if False else sp.cos(sp.Rational(2,5)*sp.pi - sp.Rational(2,5)*g)}))
print(B2s2p)
