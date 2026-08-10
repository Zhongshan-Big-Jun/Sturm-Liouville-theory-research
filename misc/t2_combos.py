# -*- coding: utf-8 -*-
"""Max of G^2+Gc and related combinations on T2."""
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
u = x*Ph/D
fG  = sp.lambdify((x,c,q), G,  'numpy')
fGx = sp.lambdify((x,c,q), Gx, 'numpy')
fGc = sp.lambdify((x,c,q), Gc, 'numpy')
fu  = sp.lambdify((x,c,q), u,  'numpy')

pi = np.pi
def c2(gv, qv): return np.arctan(qv*np.tan(gv))/(pi-gv)

Ng, Nq = 500, 400
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
xv = pi - GG; cv = c2(GG, QQ)
mask = (cv > 0.4) & (cv < 0.5)
Gv, Gcv, Gxv, uv = fG(xv,cv,QQ), fGc(xv,cv,QQ), fGx(xv,cv,QQ), fu(xv,cv,QQ)

combos = {
  'G^2+Gc': Gv**2 + Gcv,
  'G^2': Gv**2,
  'G^2+Gc-u*Gx': Gv**2 + Gcv - uv*Gxv,
  'Gc': Gcv,
}
for name, C in combos.items():
    Cm = C[mask]
    i,j = np.unravel_index(np.argmax(C), C.shape)  # NOTE: global, may be outside T2
    # masked max
    Cmasked = np.where(mask, C, -np.inf)
    i2,j2 = np.unravel_index(np.argmax(Cmasked), C.shape)
    print('%s: T2 max=%.6f at (g=%.4f,q=%.4f,c=%.4f) | full-box max=%.6f' % (
        name, Cmasked.max(), GG[i2,j2], QQ[i2,j2], c2(GG[i2,j2],QQ[i2,j2]), C.max()))
