# -*- coding: utf-8 -*-
"""Debug: test lambdified Jc on a small interval box."""
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 40
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
Gx_expr = sp.simplify(dt1 + dt2)
dt1c = Ph*W*Ph/(D**2)
dt2c = 2*X*Ph*(Q**2-1)*sc/(D**2) - 2*(2*C*X*Ph*(Q**2-1)*sc)*Ph/(D**3)
Gc_expr = sp.simplify(dt1c + dt2c)
xp = -X*Ph/D
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)
Jc = sp.simplify(sp.diff(J, C))
print("Jc ops:", sp.count_ops(Jc))
Jc_l = sp.lambdify((X,C,Q), Jc, modules='mpmath')
x = iv.mpf([mp.mpf('0.9'), mp.mpf('1.0')])
c = iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')])
q = iv.mpf([mp.mpf(1), mp.mpf(2)])
try:
    r = Jc_l(x,c,q)
    print("Jc box:", r)
except Exception as e:
    import traceback; traceback.print_exc()
# test smaller
x2 = iv.mpf([mp.mpf('0.95'), mp.mpf('0.96')])
try:
    r = Jc_l(x2,c,q)
    print("Jc small box:", r)
except Exception as e:
    import traceback; traceback.print_exc()
