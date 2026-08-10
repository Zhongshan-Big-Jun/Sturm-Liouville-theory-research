# -*- coding: utf-8 -*-
"""Speed test: adaptive sign verifier on the hard fact TA_B2 inc [0.72,0.724]."""
import sys, time
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, D2, der_sign2, der_sign_adaptive, PI, d2_sin, d2_cos, d2_atan

GLO, GHI = F(655,1000), F(10472,10000)

def comps2(g):
    A = PI - g
    sg = d2_sin(g); cg = d2_cos(g)
    D2v = I(1) + 3*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2v*D2v)
    TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2v*D2v)
    return TA_B2, TA_M

t0 = time.time()
ok, n = der_sign_adaptive(lambda g: comps2(g)[0], F(72,100), F(724,1000), True)
print('adaptive TA_B2 inc [0.72,0.724]:', ok, 'boxes:', n, 'time %.1fs' % (time.time()-t0))
t0 = time.time()
ok2, n2 = der_sign2(lambda g: comps2(g)[0], F(72,100), F(724,1000), True, base_n=64)
print('uniform der_sign2:', ok2, n2, 'time %.1fs' % (time.time()-t0))
