# -*- coding: utf-8 -*-
"""t3_routeC_sympy.py: Gx, H2 as rational functions in positive vars (s,b,S,C,x,th)."""
import sympy as sp
s, b, S, C, x, th = sp.symbols('s b S C x th', positive=True)
p = th/x
q = S*b/(C*s)
# cos x = -b, sin x = s ; sin th = S, cos th = C
Phi = b**2/C**2
D = q + p*Phi
u = x*Phi/D
A0 = sp.Rational(3)/x - 2*b/s          # 3/x + 2 cot x, cot x = -b/s
H = -2*p*(q**2-1)*s*b/D                 # 2p(q^2-1) sx cx / D, cx=-b
V = sp.simplify(H - A0)
# derivatives w.r.t. x at fixed (q,p)  -- but q,p are functions of x,th! We need partial_x at fixed q,p.
# Instead compute partial_x u, partial_x H with q,p held fixed, then substitute.
# u = x*Phi/(q + p*Phi), Phi = b^2/C^2 but b = -cos x, C = cos th are the actual trig vars.
# We must be careful: the partial derivative at fixed (q,p) treats x as the independent variable.
# Let us recompute using explicit x-dependence: cos x = -b, sin x = s, b^2+s^2=1, db/dx = s, ds/dx = b.
print("sketch: use explicit x with cos x=-b, sin x=s, and db/dx=s, ds/dx=b")
