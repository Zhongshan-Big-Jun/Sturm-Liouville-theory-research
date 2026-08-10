# -*- coding: utf-8 -*-
"""Profile: how slow is one full comps AD evaluation at a point, and on an interval?"""
import sys, time
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D, PI
import importlib, rigid1d
importlib.reload(rigid1d)
from rigid1d import I, D, d_sin, d_cos, d_atan, PI
from fractions import Fraction as F

def comps(g):
    A = PI - g
    sg = d_sin(g); cg = d_cos(g)
    D2 = I(1) + 3*sg*sg
    B1 = A*cg - 2*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    tan = sg/cg
    tmax = d_atan(2*tan)
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2*D2)
    TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2*D2)
    TC = F(791,2500)*G5*A*sg*cg*cg
    TB = 2*A**3*sg*sg*tmax*cg**5/(D2*D2*D2.sqrt())
    z = cg*cg/D2
    Qlo = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    Fv = tmax*tmax*cg*sg*sg
    return TA_B2, TC, TB, Qlo, Fv

t0 = time.time()
g = D(I(F(7,10), F(7,10)), I(1))
r = comps(g)
print('point eval time: %.3f s' % (time.time()-t0))
print('TA_B2 at 0.7:', float(r[0].v.lo), float(r[0].v.hi))
t0 = time.time()
g = D(I(F(655,1000), F(72,100)), I(1))
r = comps(g)
print('interval [0.655,0.72] eval time: %.3f s' % (time.time()-t0))
print('TA_B2 derivative interval:', float(r[0].d.lo), float(r[0].d.hi))
