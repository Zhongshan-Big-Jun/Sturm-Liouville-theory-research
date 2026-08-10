# -*- coding: utf-8 -*-
from fractions import Fraction as F
import sys; sys.path.insert(0, 'misc')
from rigid1d import _sc_rational, I
c = F(131,100)
s, t = _sc_rational(c)
print('sin partial interval:', float(s.lo), float(s.hi))
print('cos partial interval:', float(t.lo), float(t.hi))
# compute partial sum manually
N=24
s=F(0); sign=1; p=c; fact=F(1)
for k in range(N):
    s = s + sign*p/fact; sign=-sign; p=p*c*c; fact=fact*F((2*k+2)*(2*k+3))
print('sin partial sum:', float(s))
import math
print('rem:', float(abs(c)**(2*N+1)/F(math.factorial(2*N+1))))
