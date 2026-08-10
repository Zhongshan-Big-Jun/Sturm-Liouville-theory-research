# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D2, PI, d2_sin, d2_cos, d2_atan

def comps2(g):
    A = PI - g
    sg = d2_sin(g); cg = d2_cos(g)
    D2v = I(1) + 3*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2v*D2v)
    return TA_B2

# examine d1/d2 of TA_B2 at a point and over a small piece in [0.72,0.724]
c = F(722,1000)
w = F(1,10**6)
piece = I(c - w, c + w)
v_piece = comps2(D2(piece, I(1), I(0)))
v_center = comps2(D2(I(c, c), I(1), I(0)))
print('center d1:', v_center.d1)
print('piece d1:', v_piece.d1)
print('center d2:', v_center.d2)
print('piece d2:', v_piece.d2)
print('M:', max(v_piece.d2.abs().hi, v_center.d2.abs().hi))
