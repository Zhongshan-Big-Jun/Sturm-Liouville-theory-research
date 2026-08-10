# -*- coding: utf-8 -*-
"""lambdify with iv module dict; test J on interval."""
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 50
X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
Gx_s = sp.simplify(sp.diff(G, X))
Gc_s = sp.simplify(sp.diff(G, C))
xp_s = -X*Ph/D
Gp_s = sp.simplify(Gx_s*xp_s + Gc_s)
J_s = sp.simplify(G**2 + Gp_s)
Jx_s = sp.simplify(sp.diff(J_s, X))
Jc_s = sp.simplify(sp.diff(J_s, C))
mods = {'sin': iv.sin, 'cos': iv.cos, 'tan': iv.tan, 'mpf': iv.mpf, 'pi': iv.pi}
Jf = sp.lambdify((X,C,Q), J_s, modules=mods)
Jxf = sp.lambdify((X,C,Q), Jx_s, modules=mods)
Jcf = sp.lambdify((X,C,Q), Jc_s, modules=mods)
x = iv.mpf([mp.mpf('0.9'), mp.mpf('1.0')]); c = iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')]); q = iv.mpf([mp.mpf(1), mp.mpf(2)])
for nm, f in [("J",Jf),("Jx",Jxf),("Jc",Jcf)]:
    try:
        r = f(x,c,q)
        print(nm, "iv ok:", r)
    except Exception as e:
        print(nm, "iv fail:", e)
