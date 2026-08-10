# -*- coding: utf-8 -*-
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
Jf = sp.lambdify((X,C,Q), J_s, modules='mpmath')
import inspect
src = inspect.getsource(Jf)
print(src[:4000])
