# -*- coding: utf-8 -*-
"""Fix Gx via sp.diff directly; re-verify all symbolic formulas."""
import sympy as sp
import mpmath as mp
X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
Gx_ = sp.simplify(sp.diff(G, X))
Gc_ = sp.simplify(sp.diff(G, C))
xp_ = -X*Ph/D
Gf = sp.lambdify((X,C,Q), G, modules='mpmath')
Gxf = sp.lambdify((X,C,Q), Gx_, modules='mpmath')
Gcf = sp.lambdify((X,C,Q), Gc_, modules='mpmath')

def GN(x,c,q):
    Ph=mp.cos(x)**2+q*q*mp.sin(x)**2; D=q+c*Ph; W=3+2*x/mp.tan(x)
    return -Ph*W/D+2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
h=mp.mpf('1e-7')
ok=True
for (xv,cv,qv) in [(mp.mpf('1.0'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('2.2'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('0.9'),mp.mpf('0.4'),mp.mpf('2.0')),(mp.mpf('2.4'),mp.mpf('0.42'),mp.mpf('1.8'))]:
    gx_sym=float(Gxf(xv,cv,qv)); gx_num=float((GN(xv+h,cv,qv)-GN(xv-h,cv,qv))/(2*h))
    gc_sym=float(Gcf(xv,cv,qv)); gc_num=float((GN(xv,cv+h,qv)-GN(xv,cv-h,qv))/(2*h))
    d = abs(gx_sym-gx_num)
    ok = ok and d < 1e-4
    print("(%.3f,%.3f,%.3f): Gx sym=%.6f num=%.6f (diff %.2e) | Gc sym=%.6f num=%.6f" % (xv,cv,qv,gx_sym,gx_num,d,gc_sym,gc_num))
print("ALL OK:", ok)
# now J, Jx, Jc via sp.diff chain
Gp_ = sp.simplify(Gx_*xp_ + Gc_)
J_ = sp.simplify(G**2 + Gp_)
Jx_ = sp.simplify(sp.diff(J_, X))
Jc_ = sp.simplify(sp.diff(J_, C))
Jf = sp.lambdify((X,C,Q), J_, modules='mpmath')
Jxf = sp.lambdify((X,C,Q), Jx_, modules='mpmath')
Jcf = sp.lambdify((X,C,Q), Jc_, modules='mpmath')
def JN(x,c,q):
    Ph=mp.cos(x)**2+q*q*mp.sin(x)**2; D=q+c*Ph; xp=-x*Ph/D
    Gv=GN(x,c,q); Gx0=(GN(x+h,c,q)-GN(x-h,c,q))/(2*h)
    Gc0=(GN(x,c+h,q)-GN(x,c-h,q))/(2*h)
    return Gv*Gv+Gx0*xp+Gc0
for (xv,cv,qv) in [(mp.mpf('1.0'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('2.2'),mp.mpf('0.45'),mp.mpf('1.5'))]:
    j_sym=float(Jf(xv,cv,qv)); j_num=float(JN(xv,cv,qv))
    jx_sym=float(Jxf(xv,cv,qv)); jx_num=float((JN(xv+h,cv,qv)-JN(xv-h,cv,qv))/(2*h))
    jc_sym=float(Jcf(xv,cv,qv)); jc_num=float((JN(xv,cv+h,qv)-JN(xv,cv-h,qv))/(2*h))
    print("(%.3f,%.3f,%.3f): J sym=%.6f num=%.6f | Jx sym=%.6f num=%.6f | Jc sym=%.6f num=%.6f" % (xv,cv,qv,j_sym,j_num,jx_sym,jx_num,jc_sym,jc_num))
