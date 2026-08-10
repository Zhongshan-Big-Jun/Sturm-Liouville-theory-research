# -*- coding: utf-8 -*-
"""Uniform-grid iv certification for monotonicity claims.
Claims: (a) dJ1_2d/dx>0, (b) dJ1_2d/dq>0 on [0.8411,1.1220]x[1,2];
(c) dJ2_2d/dg>0 on [0.695,pi/3]x[1,2].
Need iv evaluators for these derivatives: use finite-difference-free approach: compute via
J(x,c,q) as explicit function, then derivative of J1_2d = J(x, c1(x,q), q):
d/dx = J_x + J_c * dc1/dx. We have J_iv but need Jx_iv, Jc_iv partial derivatives.
Implement Jx_iv, Jc_iv via formulas (J = G^2 + Gx*xp + Gc):
Jx = 2G*Gx + Gxx*xp + Gx*xpx + Gcx
Jc = 2G*Gc + Gxc*xp + Gx*xpc + Gcc
Need second partials Gxx, Gcx, Gxc, Gcc, xpx, xpc. Symbolic, then hardcode via sympy->mpmath? 
Use sympy to generate code strings for these, then exec with mpmath.
"""
import sympy as sp
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
Gp_ = sp.simplify(Gx_*xp_ + Gc_)
J_ = sp.simplify(G**2 + Gp_)
# partials
Gx_x = sp.simplify(sp.diff(Gx_, X))
Gx_c = sp.simplify(sp.diff(Gx_, C))
Gc_x = sp.simplify(sp.diff(Gc_, X))
Gc_c = sp.simplify(sp.diff(Gc_, C))
xp_x = sp.simplify(sp.diff(xp_, X))
xp_c = sp.simplify(sp.diff(xp_, C))
Jx_ = sp.simplify(2*G*Gx_ + Gx_x*xp_ + Gx_*xp_x + Gc_x)
Jc_ = sp.simplify(2*G*Gc_ + Gx_c*xp_ + Gx_*xp_c + Gc_c)

# generate python functions via lambdify with mpmath (regular mpf eval for derivative check),
# then build iv versions by string substitution.
import mpmath as mp
funcs = {}
for nm, expr in [('G',G),('Gx',Gx_),('Gc',Gc_),('Jx',Jx_),('Jc',Jc_)]:
    fn = sp.lambdify((X,C,Q), expr, modules='mpmath')
    funcs[nm] = fn
print("lambdified G, Gx, Gc, Jx, Jc")
# sanity check vs numeric
def PhiN(x,q): return mp.cos(x)**2+q*q*mp.sin(x)**2
def GN(x,c,q):
    Ph=PhiN(x,q); D=q+c*Ph; W=3+2*x/mp.tan(x)
    return -Ph*W/D+2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def JN(x,c,q):
    Ph=PhiN(x,q); D=q+c*Ph; xp=-x*Ph/D
    W=3+2*x/mp.tan(x)
    Gv=GN(x,c,q); h=mp.mpf('1e-6')
    Gpv=((GN(x+h,c,q)-GN(x-h,c,q))/(2*h))*xp
    sc=mp.sin(x)*mp.cos(x)
    Gc_=Ph*W*Ph/(D*D)+2*x*Ph*(q*q-1)*sc/(D*D)-2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv+Gpv+Gc_
for (xv,cv,qv) in [(mp.mpf('1.0'),mp.mpf('0.45'),mp.mpf('1.5')),(mp.mpf('2.2'),mp.mpf('0.45'),mp.mpf('1.5'))]:
    print("at (%.3f,%.3f,%.3f): Jx_sym=%.4f Jx_num=%.4f Jc_sym=%.4f Jc_num=%.4f" % (
        xv,cv,qv,
        float(funcs['Jx'](xv,cv,qv)), float((JN(xv+mp.mpf('1e-6'),cv,qv)-JN(xv-mp.mpf('1e-6'),cv,qv))/(2*mp.mpf('1e-6'))),
        float(funcs['Jc'](xv,cv,qv)), float((JN(xv,cv+mp.mpf('1e-6'),qv)-JN(xv,cv-mp.mpf('1e-6'),qv))/(2*mp.mpf('1e-6')))))
