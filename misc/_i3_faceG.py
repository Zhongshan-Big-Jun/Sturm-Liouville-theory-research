# -*- coding: utf-8 -*-
"""Proper scan of G on faces of B1."""
import mpmath as mp
mp.mp.dps = 40
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)

x0,x1 = mp.mpf('0.8411'),mp.mpf('1.1220')
# face c=0.5
mx=-mp.inf; arg=None
for i in range(60+1):
    x = x0+(x1-x0)*i/60
    for j in range(60+1):
        q = 1+1*j/60
        v = G(x, mp.mpf('0.5'), q)
        if v>mx: mx=v; arg=(x,q)
print("G(x,0.5,q): max %.6f at %s" % (mx,arg))
# face q=1
mx=-mp.inf; arg=None
for i in range(60+1):
    x = x0+(x1-x0)*i/60
    for j in range(60+1):
        c = mp.mpf('0.4')+mp.mpf('0.1')*j/60
        v = G(x, c, mp.mpf(1))
        if v>mx: mx=v; arg=(x,c)
print("G(x,c,1): max %.6f at %s" % (mx,arg))
# face x=1.122
mx=-mp.inf; arg=None
for i in range(60+1):
    q = 1+1*i/60
    for j in range(60+1):
        c = mp.mpf('0.4')+mp.mpf('0.1')*j/60
        v = G(x1, c, q)
        if v>mx: mx=v; arg=(q,c)
print("G(1.122,c,q): max %.6f at %s" % (mx,arg))
# dG/dq sign on face x=1.122
h=mp.mpf('1e-6')
mn=mp.inf; mxv=-mp.inf
for i in range(30+1):
    q = 1+1*i/30
    for j in range(30+1):
        c = mp.mpf('0.4')+mp.mpf('0.1')*j/30
        v = (G(x1,c,q+h)-G(x1,c,q-h))/(2*h)
        mn=min(mn,v); mxv=max(mxv,v)
print("dG/dq at x=1.122: [%.4f, %.4f]" % (mn,mxv))
