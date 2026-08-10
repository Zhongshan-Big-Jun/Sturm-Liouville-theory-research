# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D, d_sin, d_cos, d_atan, PI
PI = I(F(31415926,10000000), F(31415927,10000000))  # tighter pi
def comps(g):
    A = PI - g
    sg = d_sin(g); cg = d_cos(g)
    D2 = I(1) + 3*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2*D2)
    return TA_B2
# point eval at 0.7
t0=time.time()
g = D(I(F(7,10), F(7,10)), I(1))
r = comps(g)
print('TA_B2(0.7) interval: [%.6f, %.6f] (%.1e s)' % (float(r.v.lo), float(r.v.hi), time.time()-t0))
print('TA_B2 derivative at point: [%.4f, %.4f]' % (float(r.d.lo), float(r.d.hi)))
# small interval [0.7, 0.701]
t0=time.time()
g = D(I(F(7,10), F(701,1000)), I(1))
r = comps(g)
print('TA_B2 d on [0.7,0.701]: [%.4f, %.4f] (%.2f s)' % (float(r.d.lo), float(r.d.hi), time.time()-t0))
# medium [0.7, 0.71]
t0=time.time()
g = D(I(F(7,10), F(71,100)), I(1))
r = comps(g)
print('TA_B2 d on [0.7,0.71]: [%.4f, %.4f] (%.2f s)' % (float(r.d.lo), float(r.d.hi), time.time()-t0))
