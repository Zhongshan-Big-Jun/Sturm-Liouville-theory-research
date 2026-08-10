# -*- coding: utf-8 -*-
"""Verify Gx, Gc, xp symbolic formulas vs numeric."""
import sympy as sp
import mpmath as mp
X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
Wp = 2*cx/sx - 2*X/sx**2
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
dPhi = 2*sc*(Q**2-1); dD = C*dPhi; dsc = cx**2 - sx**2
term1 = -Ph*W/D; term2 = 2*C*X*Ph*(Q**2-1)*sc/(D**2)
dt1 = -(dPhi*W + Ph*Wp)/D + Ph*W*dD/(D**2)
A = 2*C*(Q**2-1)
num2 = A*(X*dPhi*sc + Ph*dsc + Ph*sc)
dt2 = num2/(D**2) - 2*C*X*Ph*(Q**2-1)*sc*2*dD/(D**3)
Gx_ = sp.simplify(dt1 + dt2)
dt1c = Ph*W*Ph/(D**2)
dt2c = 2*X*Ph*(Q**2-1)*sc/(D**2) - 2*(2*C*X*Ph*(Q**2-1)*sc)*Ph/(D**3)
Gc_ = sp.simplify(dt1c + dt2c)
xp_ = -X*Ph/D
Gf = sp.lambdify((X,C,Q), G, modules='mpmath')
Gxf = sp.lambdify((X,C,Q), Gx_, modules='mpmath')
Gcf = sp.lambdify((X,C,Q), Gc_, modules='mpmath')
xpf = sp.lambdify((X,C,Q), xp_, modules='mpmath')

def GN(x,c,q):
    Ph=mp.cos(x)**2+q*q*mp.sin(x)**2; D=q+c*Ph; W=3+2*x/mp.tan(x)
    return -Ph*W/D+2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
h=mp.mpf('1e-7')
for (xv,cv,qv) in [(mp.mpf('1.0'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('2.2'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('0.9'),mp.mpf('0.4'),mp.mpf('2.0'))]:
    gx_sym=float(Gxf(xv,cv,qv)); gx_num=float((GN(xv+h,cv,qv)-GN(xv-h,cv,qv))/(2*h))
    gc_sym=float(Gcf(xv,cv,qv)); gc_num=float((GN(xv,cv+h,qv)-GN(xv,cv-h,qv))/(2*h))
    xp_sym=float(xpf(xv,cv,qv)); xp_num=float(-xv*(mp.cos(xv)**2+qv*qv*mp.sin(xv)**2)/(qv+cv*(mp.cos(xv)**2+qv*qv*mp.sin(xv)**2)))
    print("(%.3f,%.3f,%.3f): Gx sym=%.6f num=%.6f | Gc sym=%.6f num=%.6f | xp sym=%.6f num=%.6f" % (xv,cv,qv,gx_sym,gx_num,gc_sym,gc_num,xp_sym,xp_num))
