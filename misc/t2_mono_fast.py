# -*- coding: utf-8 -*-
"""Fast float64 reconnaissance of composed monotonicity on T2 (signs only)."""
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
Gxx = sp.diff(Gx, x); Gxc = sp.diff(Gx, c); Gxq = sp.diff(Gx, q)
Gcx = sp.diff(Gc, x); Gcc = sp.diff(Gc, c); Gcq = sp.diff(Gc, q)
Gq = sp.diff(G, q); ux = sp.diff(u, x); uc = sp.diff(u, c); uq = sp.diff(u, q)

fG   = sp.lambdify((x,c,q), G,   'numpy'); fGx  = sp.lambdify((x,c,q), Gx,  'numpy')
fGc  = sp.lambdify((x,c,q), Gc,  'numpy'); fu   = sp.lambdify((x,c,q), u,   'numpy')
fGx_x= sp.lambdify((x,c,q), Gxx, 'numpy'); fGx_c= sp.lambdify((x,c,q), Gxc, 'numpy'); fGx_q= sp.lambdify((x,c,q), Gxq,'numpy')
fGc_x= sp.lambdify((x,c,q), Gcx, 'numpy'); fGc_c= sp.lambdify((x,c,q), Gcc, 'numpy'); fGc_q= sp.lambdify((x,c,q), Gcq,'numpy')
fG_q = sp.lambdify((x,c,q), Gq,  'numpy')
fu_x = sp.lambdify((x,c,q), ux,  'numpy'); fu_c = sp.lambdify((x,c,q), uc, 'numpy'); fu_q = sp.lambdify((x,c,q), uq, 'numpy')

pi = np.pi
def c2(gv, qv): return np.arctan(qv*np.tan(gv))/(pi-gv)
def dc2_dg(gv, qv):
    t = qv*np.tan(gv)
    return (qv/np.cos(gv)**2/(1+t*t)*(pi-gv) + np.arctan(t))/(pi-gv)**2
def dc2_dq(gv, qv):
    t = qv*np.tan(gv)
    return np.tan(gv)/(1+t*t)/(pi-gv)

Ng, Nq = 300, 240
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
xv = pi - GG; cv = c2(GG, QQ)
mask = (cv > 0.4) & (cv < 0.5)
print('T2 pts:', mask.sum(), '/', mask.size)

# composed derivatives via chain rule
dG_dg  = -fGx(xv,cv,QQ) + fGc(xv,cv,QQ)*dc2_dg(GG,QQ)
dG_dq  =  fG_q(xv,cv,QQ) + fGc(xv,cv,QQ)*dc2_dq(GG,QQ)
dGc_dg = -fGc_x(xv,cv,QQ) + fGc_c(xv,cv,QQ)*dc2_dg(GG,QQ)
dGc_dq =  fGc_q(xv,cv,QQ) + fGc_c(xv,cv,QQ)*dc2_dq(GG,QQ)
dGx_dg = -fGx_x(xv,cv,QQ) + fGx_c(xv,cv,QQ)*dc2_dg(GG,QQ)
du_dg  = -fu_x(xv,cv,QQ) + fu_c(xv,cv,QQ)*dc2_dg(GG,QQ)
du_dq  =  fu_q(xv,cv,QQ) + fu_c(xv,cv,QQ)*dc2_dq(GG,QQ)

for name, D, exp in [('dG/dg',dG_dg,'<0'),('dG/dq',dG_dq,'<0'),('dGc/dg',dGc_dg,'>0'),
                     ('dGc/dq',dGc_dq,'<0'),('dGx/dg',dGx_dg,'<0'),('du/dg',du_dg,'?'),('du/dq',du_dq,'?')]:
    Dm = D[mask]
    print('%s: min=%.4f max=%.4f  (expect %s)' % (name, Dm.min(), Dm.max(), exp))
    # where does max/min occur
    i,j = np.unravel_index(np.argmax(D), D.shape); gi,gj = GG[i,j], QQ[i,j]
    print('   max at g=%.4f q=%.4f c=%.4f' % (gi, gj, c2(gi,gj)))
