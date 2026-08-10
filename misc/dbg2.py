# -*- coding: utf-8 -*-
from fractions import Fraction as F
import sys; sys.path.insert(0, 'misc')
import rigid1d as R
x = R.I(F(655,1000), F(66,100))
s = R.I_sin(x)
print('sin[0.655,0.66]:', float(s.lo), float(s.hi))
c = (x.lo+x.hi)/2; w = (x.hi-x.lo)/2
print('c,w:', float(c), float(w))
sc, cc = R._sin_cos_series(c)
print('sc,cc:', float(sc.lo), float(sc.hi), float(cc.lo), float(cc.hi))
# manual: sin_u, cos_u intervals
N_=26
su = F(0); sign=1; p=w; fact=F(1)
for k in range(N_):
    su = su + sign*p/fact; sign=-sign; p=p*w*w; fact=fact*F((2*k+2)*(2*k+3))
rem = w**(2*N_+1)/F(__import__('math').factorial(2*N_+1))
cu = F(1); sign=-1; p=w*w; fact=F(2)
for k in range(1,N_):
    cu = cu + sign*p/fact; sign=-sign; p=p*w*w; fact=fact*F((2*k+1)*(2*k+2))
rem2 = w**(2*N_)/F(__import__('math').factorial(2*N_))
print('sin_u interval:', float(-(su+rem)), float(su+rem))
print('cos_u interval:', float(cu-rem2), float(cu+rem2))
