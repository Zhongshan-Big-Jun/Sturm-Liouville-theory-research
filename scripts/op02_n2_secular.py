# -*- coding: utf-8 -*-
"""#2 n=2: derive half-string secular equations (correct order) with sympy.
Half-string [1,R,1] widths (a,b,c/2) on [0,1/2]; Dirichlet nu1 = lambda2, mixed mu2 = lambda3.
"""
import sympy as sp
w, R = sp.symbols('w R', positive=True)
a, b, c = sp.symbols('a b c', positive=True)
s = sp.sqrt(R)

# shooting: u(0)=0, u'(0)=1
# block1 (rho=1, len a): ww=w
# block2 (rho=R, len b): ww=w*s
# block3 (rho=1, len c/2): ww=w
u1 = sp.sin(w*a)/w; up1 = sp.cos(w*a)
u2 = u1*sp.cos(w*s*b) + up1*sp.sin(w*s*b)/(w*s)
up2 = -u1*w*s*sp.sin(w*s*b) + up1*sp.cos(w*s*b)
u3 = u2*sp.cos(w*c/2) + up2*sp.sin(w*c/2)/w
up3 = -u2*w*sp.sin(w*c/2) + up2*sp.cos(w*c/2)

Dir = sp.simplify(sp.together(u3))
Mix = sp.simplify(sp.together(up3))
print("Dirichlet secular numerator:", sp.factor(sp.expand(Dir* w**3)))
print()
print("Mixed secular numerator:", sp.factor(sp.expand(Mix*w**3)))
