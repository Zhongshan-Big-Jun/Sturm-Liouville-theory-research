# -*- coding: utf-8 -*-
"""t3_debug: check denominator of composed dG_dg precisely."""
import sympy as sp
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
P = 2*(A*st*ct + t*sg*cg)
p = A*st*ct + t*sg*cg
q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
K    = cg/(2*A*sg*ct**2)
D, D2, D3 = P*K, (P*K)**2, (P*K)**3
G  = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/D3
den_extra = cg**3*sg**3*ct**6
GxP3c = sum(sp.expand(tt*P**3*den_extra) for tt in [t1,t2,t3,t4])
Gx = GxP3c/(P**3*den_extra)

def d_dt(f): return sp.diff(f, t) + ct*sp.diff(f, st) - st*sp.diff(f, ct)
def d_dg(f): return -sp.diff(f, A) + cg*sp.diff(f, sg) - sg*sp.diff(f, cg)
dG_dt = d_dt(G); dG_dg_part = d_dg(G)
v = dG_dg_part + dG_dt*st*ct/(sg*cg)
n, d = sp.fraction(sp.together(v))
print('den of composed dG_dg:', sp.factor(sp.expand(d)))
n2, d2 = sp.fraction(sp.together(sp.expand(v)))
print('den of expanded composed dG_dg:', sp.factor(sp.expand(d2)))
# test polynomiality
tst = sp.expand(sp.together(sp.expand(v)*sg*p**3))
print('after *sg*p^3, fraction:', sp.fraction(sp.together(tst))[1])
