# -*- coding: utf-8 -*-
from fractions import Fraction as F
import sys; sys.path.insert(0, 'misc')
from rigid1d import I, I_sin, I_cos, PI
import mpmath as mp
mp.mp.dps = 30
# test sin(1.31) should be 0.966149
s = I_sin(I(F(131,100), F(131,100)))
print('sin(1.31) in', s, ' true', mp.sin(mp.mpf('1.31')))
c = I_cos(I(F(131,100), F(131,100)))
print('cos(1.31) in', c, ' true', mp.cos(mp.mpf('1.31')))
# sin on interval [0.655, 0.66]
s2 = I_sin(I(F(655,1000), F(66,100)))
print('sin[0.655,0.66] in', s2, ' true', mp.sin(mp.mpf('0.655')), mp.sin(mp.mpf('0.66')))
# test basic ops
print('2/3 + 1/7 =', I(F(2,3)) + I(F(1,7)))
print('pi interval:', PI)
