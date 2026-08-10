# -*- coding: utf-8 -*-
"""t3_dGx_xt2.py: numerators of dGx/dx|th and dGx/dth|x."""
import sympy as sp
s, b, S, C, x, th = sp.symbols('s b S C x th', positive=True)
q = S*b/(C*s)
Phi = b**2/C**2
Delta = b*s*th + C*S*x
u = x*Phi/Delta
A0 = sp.Rational(3)/x - 2*b/s
H = 2*th*(C**2*s**2 - S**2*b**2)/Delta
V = H - A0
G = u*V
# Gx = partial_x G at fixed (q,p); we use the closed form from t3_routeC_sympy3 (Gx expression in these vars)
# recompute: ux = d/dx u at fixed (q,p): Phi_x = 2bs(1-q^2) (using ds/dx=-b, db/dx=s)
Phix = 2*s*b*(1-q**2)
Dq = q + (th/x)*Phi
ux = (Phi + x*Phix)/Dq - x*Phi*(th/x)*Phix/Dq**2
A0x = -3/x**2 - 2/s**2
Hx = -2*(th/x)*(q**2-1)*((s**2-b**2)*Dq - s*b*(th/x)*Phix)/Dq**2
Gx = ux*V + u*(Hx - A0x)
Gx = sp.cancel(Gx)
print('Gx denom check:', sp.factor(sp.denom(Gx)))
# partial derivative w.r.t. x at fixed th:
dGxdx = sp.diff(Gx, x) + sp.diff(Gx, s)*(-b) + sp.diff(Gx, b)*s
dGxdt = sp.diff(Gx, th) + sp.diff(Gx, S)*C + sp.diff(Gx, C)*(-S)
for nm, e in [('dGx/dx', dGxdx), ('dGx/dth', dGxdt)]:
    e = sp.cancel(e)
    num = sp.factor(sp.expand(sp.numer(e)))
    den = sp.factor(sp.denom(e))
    print('== %s ==' % nm)
    print('num terms:', len(sp.Add.make_args(num)))
    print('num:', num)
    print('den:', den)
    print()
