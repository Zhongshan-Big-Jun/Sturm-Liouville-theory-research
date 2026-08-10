# -*- coding: utf-8 -*-
"""Symbolic derivatives of M,B2,B4,B5,B7,G5 as functions of gamma; check sign bounds."""
import sympy as sp
g = sp.symbols('g', positive=True)
A = sp.pi - g
sg, cg = sp.sin(g), sp.cos(g)
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.expand(B5 - A*B4)
for name, f in [('M',M),('B2',B2),('B4',B4),('B5',B5),('B7',B7),('G5',G5)]:
    d1 = sp.trigsimp(sp.diff(f, g))
    d2 = sp.trigsimp(sp.diff(f, g, 2))
    print(name, 'd1:', sp.factor(d1))
    print(name, 'd2:', sp.factor(d2))
    print()
