# -*- coding: utf-8 -*-
"""q=1 baseline, corrected: J=(W^2+W+x*W')/(1+c)^2."""
import mpmath as mp
mp.mp.dps = 40
def W(x): return 3 + 2*x/mp.tan(x)
def Wp(x): return 2/mp.tan(x) - 2*x/mp.sin(x)**2
def J1_1(c):
    x = mp.pi/(2*(1+c))
    return (W(x)**2 + W(x) + x*Wp(x))/(1+c)**2
def J2_1(c):
    x = mp.pi/(1+c)
    return (W(x)**2 + W(x) + x*Wp(x))/(1+c)**2
mn1=mp.inf; mx1=-mp.inf; mn2=mp.inf; mx2=-mp.inf
for i in range(2001):
    c = mp.mpf('0.4')+mp.mpf('0.1')*i/2000
    j1 = J1_1(c); j2 = J2_1(c)
    mn1=min(mn1,j1); mx1=max(mx1,j1); mn2=min(mn2,j2); mx2=max(mx2,j2)
print("J1(1,c): [%.6f, %.6f]" % (mn1,mx1))
print("J2(1,c): [%.6f, %.6f]" % (mn2,mx2))
# check monotonicity in c
mn=mp.inf; mx=-mp.inf
h=mp.mpf('1e-6')
for i in range(200):
    c = mp.mpf('0.4')+mp.mpf('0.1')*i/200
    v=(J1_1(c+h)-J1_1(c-h))/(2*h)
    mn=min(mn,v); mx=max(mx,v)
print("dJ1(1,c)/dc: [%.4f, %.4f]" % (mn,mx))
mn=mp.inf; mx=-mp.inf
for i in range(200):
    c = mp.mpf('0.4')+mp.mpf('0.1')*i/200
    v=(J2_1(c+h)-J2_1(c-h))/(2*h)
    mn=min(mn,v); mx=max(mx,v)
print("dJ2(1,c)/dc: [%.4f, %.4f]" % (mn,mx))
