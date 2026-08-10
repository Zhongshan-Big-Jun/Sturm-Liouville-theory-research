# -*- coding: utf-8 -*-
"""t3_routeC_sympy2.py: closed forms of Gx and H2 in positive vars (s,b,S,C,x,th)."""
import sympy as sp
x, th, q, p = sp.symbols('x th q p', positive=True)
sx, cx, st, ct = sp.symbols('sx cx st ct')
sub = {sx: sp.Symbol('s'), cx: -sp.Symbol('b'), st: sp.Symbol('S'), ct: sp.Symbol('C')}
s, b, S, C = sp.symbols('s b S C', positive=True)
sub = {sx: s, cx: -b, st: S, ct: C}

Phi = q**2*sx**2 + cx**2
D = q + p*Phi
u = x*Phi/D
A0 = sp.Rational(3)/x + 2*cx/sx
H = 2*p*(q**2-1)*sx*cx/D
V = H - A0
# derivatives at fixed (q,p): d/dx
Phi_x = sp.diff(Phi, sx)*sp.diff(sx,x) + sp.diff(Phi, cx)*sp.diff(cx,x)  # uses dsx/dx = cx, dcx/dx = -sx
D_x = p*Phi_x
u_x = (Phi + x*Phi_x)/D - x*Phi*D_x/D**2
A0_x = -3/x**2 + 2*(-1/sx**2)   # d/dx cot x = -csc^2 x... careful: cot x = cx/sx
H_x = sp.diff(H, sx)*sp.diff(sx,x) + sp.diff(H, cx)*sp.diff(cx,x) + sp.diff(H, x)
G = u*V
G_x = sp.diff(G, sx)*sp.diff(sx,x) + sp.diff(G, cx)*sp.diff(cx,x) + sp.diff(G, x)
G_c = sp.diff(G, p)

# now substitute q = S*b/(C*s), p = th/x
qsub = S*b/(C*s)
psub = th/x
res = {}
for nm, ex in [('Phi',Phi),('D',D),('u',u),('A0',A0),('H',H),('V',V),('u_x',u_x),('A0_x',A0_x),('H_x',H_x),('G_x',G_x),('G_c',G_c)]:
    e = ex.subs({sx:s, cx:-b, st:S, ct:C}).subs({q:qsub, p:psub})
    e = sp.simplify(sp.expand(e))
    res[nm] = e
    print('== %s ==' % nm)
    print(sp.factor(e))
    print()
# H2 = u*Gx
H2 = sp.simplify(res['u']*res['G_x'])
print('== H2 = u*Gx ==')
print(sp.factor(H2))
import pickle
pickle.dump(res, open('misc/t3_routeC_forms.pkl','wb'))
