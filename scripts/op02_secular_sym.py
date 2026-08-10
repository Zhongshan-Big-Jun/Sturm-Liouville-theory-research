# -*- coding: utf-8 -*-
"""#2: symbolic secular equation F_n(y) for the alternating (2n+1)-block config.
T_cell for [1,R] pair (both phases = y), T_final for last [1] block.  M = T_final * T_cell^n.
Dirichlet: M[0,1] = 0."""
import sympy as sp
w, s = sp.symbols('w s', positive=True)   # w = omega (sqrt lambda), s = sqrt(R)
y = sp.symbols('y')
C, S = sp.cos(y), sp.sin(y)

def T1(phase, rho):
    ww = w*sp.sqrt(rho)
    return sp.Matrix([[sp.cos(phase), sp.sin(phase)/ww], [-ww*sp.sin(phase), sp.cos(phase)]])

# cell [1: st, R: t]: both phases = y;  T_cell = T(block2) @ T(block1)
Tcell = T1(y, 1)  # block1
# block2: rho = R, phase y
Tcell = T1(y, s**2) @ Tcell
Tfinal = T1(y, 1)

for n in (1, 2, 3, 4):
    M = Tfinal * Tcell**n
    D = sp.simplify(sp.together(M[0,1] * w))  # clear 1/w
    # express in C,S
    D2 = sp.expand(D).subs({sp.sin(y): S, sp.cos(y): C})
    D2 = sp.simplify(sp.trigsimp(D2, method='fu'))
    print(f"n={n}: M01*w = {D2}")
