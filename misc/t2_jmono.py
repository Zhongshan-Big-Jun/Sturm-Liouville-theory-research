# -*- coding: utf-8 -*-
"""Check composed dJ2_2d/dq and dJ2_2d/dgamma on the full box (float64)."""
import numpy as np
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
g = sp.symbols('gamma', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)
# partials of J
Jx = sp.diff(J, x); Jc = sp.diff(J, c); Jq = sp.diff(J, q)

fJ  = sp.lambdify((x,c,q), J,  'numpy')
fJx = sp.lambdify((x,c,q), Jx, 'numpy')
fJc = sp.lambdify((x,c,q), Jc, 'numpy')
fJq = sp.lambdify((x,c,q), Jq, 'numpy')

pi = np.pi
def c2(gv, qv): return np.arctan(qv*np.tan(gv))/(pi-gv)
def dc2_dg(gv, qv):
    t = qv*np.tan(gv)
    return (qv/np.cos(gv)**2/(1+t*t)*(pi-gv) + np.arctan(t))/(pi-gv)**2
def dc2_dq(gv, qv):
    t = qv*np.tan(gv)
    return np.tan(gv)/(1+t*t)/(pi-gv)

Ng, Nq = 400, 320
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
xv = pi - GG; cv = c2(GG, QQ)
mask = (cv > 0.4) & (cv < 0.5)
print('T2 pts:', mask.sum(), '/', mask.size)

dJ_dg = -fJx(xv,cv,QQ) + fJc(xv,cv,QQ)*dc2_dg(GG,QQ)
dJ_dq =  fJq(xv,cv,QQ) + fJc(xv,cv,QQ)*dc2_dq(GG,QQ)

for name, D in [('dJ/dg',dJ_dg),('dJ/dq',dJ_dq)]:
    Dm = D[mask]
    print('%s: min=%.5f max=%.5f' % (name, Dm.min(), Dm.max()))
    i,j = np.unravel_index(np.argmax(D), D.shape)
    print('   max at g=%.5f q=%.5f c=%.5f' % (GG[i,j], QQ[i,j], c2(GG[i,j],QQ[i,j])))
    i,j = np.unravel_index(np.argmin(D), D.shape)
    print('   min at g=%.5f q=%.5f c=%.5f' % (GG[i,j], QQ[i,j], c2(GG[i,j],QQ[i,j])))
# also on full box
for name, D in [('dJ/dg-full',dJ_dg),('dJ/dq-full',dJ_dq)]:
    print('%s full box: min=%.5f max=%.5f' % (name, D.min(), D.max()))
