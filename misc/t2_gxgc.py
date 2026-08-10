# -*- coding: utf-8 -*-
"""Gx and G^2+Gc extrema location analysis on T2."""
import numpy as np
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
fG  = sp.lambdify((x,c,q), G,  'numpy')
fGx = sp.lambdify((x,c,q), Gx, 'numpy')
fGc = sp.lambdify((x,c,q), Gc, 'numpy')

pi = np.pi
def vals(gv, qv):
    xv = pi - gv; cv = np.arctan(qv*np.tan(gv))/(pi-gv)
    return fG(xv,cv,qv), fGx(xv,cv,qv), fGc(xv,cv,qv)

# Gx along gamma=pi/3, q in [1,2]
N = 3000
q1 = np.linspace(1, 2, N)
gx_at_pi3 = np.array([vals(pi/3, qv)[1] for qv in q1])
print('Gx(pi/3, q) over q in [1,2]: min=%.6f at q=%.4f, value at q=1: %.6f, q=2: %.6f' % (
    gx_at_pi3.min(), q1[np.argmin(gx_at_pi3)], gx_at_pi3[0], gx_at_pi3[-1]))

# Gx and G^2+Gc min/max on T2 grid (masked), with location
Ng, Nq = 500, 400
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
xv = pi - GG; cv = np.arctan(QQ*np.tan(GG))/(pi-GG)
mask = (cv > 0.4) & (cv < 0.5)
Gv, Gxv, Gcv = fG(xv,cv,QQ), fGx(xv,cv,QQ), fGc(xv,cv,QQ)
S = Gv**2 + Gcv
for nm, M in [('Gx', Gxv), ('G^2+Gc', S), ('G', Gv), ('Gc', Gcv)]:
    Mm = np.where(mask, M, np.nan)
    imn = np.nanargmin(Mm); imx = np.nanargmax(Mm)
    i,j = np.unravel_index(imn, M.shape); i2,j2 = np.unravel_index(imx, M.shape)
    print('%s: T2 min=%.6f at (g=%.4f,q=%.4f,c=%.4f) | T2 max=%.6f at (g=%.4f,q=%.4f,c=%.4f)' % (
        nm, Mm[i,j], GG[i,j], QQ[i,j], cv[i,j], Mm[i2,j2], GG[i2,j2], QQ[i2,j2], cv[i2,j2]))

# J2 max point (masked)
Jv = Gv**2 + Gcv - (pi-GG)*Ph_np(xv, QQ)/(QQ+cv*Ph_np(xv,QQ))*Gxv
