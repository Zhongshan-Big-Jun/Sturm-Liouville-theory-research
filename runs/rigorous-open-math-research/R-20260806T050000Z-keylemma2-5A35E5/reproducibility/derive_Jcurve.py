# -*- coding: utf-8 -*-
"""derive_Jcurve.py -- closed forms of dG_even/dx (even curve, c=E(x)/x) and
dG_odd/dg (odd curve, c=atan(q tan g)/(pi-g)), to test J1>0 <=> dG_even/dx<0 etc."""
import sympy as sp

q, x = sp.symbols('q x', positive=True)
s, co = sp.sin(x), sp.cos(x)
t = s/co
Phi = co**2 + q**2*s**2

# ---- even curve: alpha = x, c = E(x)/x = atan(1/(q tan x))/x ----
cE = sp.atan(1/(q*t))/x
D = q + cE*Phi
K = q**2 - 1
W = 3 + 2*x*co/s
GE = -Phi*W/D + 2*cE*x*Phi*K*s*co/D**2
dGE_dx = sp.diff(GE, x)
print('dG_even/dx (alpha_1 curve):')
print(sp.cancel(dGE_dx))
print()
