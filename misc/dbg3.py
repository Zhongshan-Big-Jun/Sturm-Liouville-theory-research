# -*- coding: utf-8 -*-
import sys, time
sys.path.insert(0, 'misc')
from fractions import Fraction as F
from rigid1d import I, I_sin, I_cos
import mpmath as mp
mp.mp.dps = 30
x = I(F(7,10), F(7,10))
s = I_sin(x)
print('sin(0.7) width:', float(s.width()), 'val:', float(s.lo), float(s.hi), 'true', mp.sin(mp.mpf('0.7')))
c = I_cos(x)
print('cos(0.7) width:', float(c.width()), 'val:', float(c.lo), float(c.hi), 'true', mp.cos(mp.mpf('0.7')))
# what about width propagation: cg^4
print('cg^4 width:', float((c**4).width()))
# sin on tiny interval
x2 = I(F(6999,10000), F(7001,10000))
s2 = I_sin(x2)
print('sin[0.6999,0.7001] width:', float(s2.width()), 'true width ~', float(mp.sin(mp.mpf('0.7001'))-mp.sin(mp.mpf('0.6999'))))
