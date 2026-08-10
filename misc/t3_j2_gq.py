# -*- coding: utf-8 -*-
"""t3_j2_gq: express J2_2d in (gamma, q)."""
import sympy as sp, pickle

g, q = sp.symbols('g q', positive=True)
sg, cg = sp.sin(g), sp.cos(g)
# t = atan(q*tan(g)); st = q*sg/sqrt(1+q^2*sg^2/cg^2)*... use: tan t = q tan g => st = q tan g / sqrt(1+q^2 tan^2 g), ct = 1/sqrt(1+q^2 tan^2 g)
D = sp.sqrt(1 + q**2*sg**2/cg**2)
st = q*sg/(cg*D)
ct = 1/D
A = sp.pi - g
t = sp.atan(q*sg/cg)
# build G, Gc, u, Gx from t3_poly definitions
P = 2*(A*st*ct + t*sg*cg)
G = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u = 2*A**2*sg*cg/P
# Gx: need numGx... use the polynomial pipeline pieces
from sympy import sqrt
q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi = cg**2/ct**2
Phi_x = -2*q2m1*sg*cg
W = 3 - 2*A*cg/sg
W_x = -2*cg/sg - 2*A/sg**2
sc_ = -sg*cg
cos2x = cg**2 - sg**2
c = t/A
K = cg/(2*A*sg*ct**2)
D2_, D3_ = (P*K)**2, (P*K)**3
t1 = -(Phi_x*W + Phi*W_x)/(P*K)
t2 = Phi*W*c*Phi_x/(P*K)**2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/(P*K)**2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/(P*K)**3
Gx = t1+t2+t3+t4
J2 = sp.expand(G**2 + Gc - u*Gx)
J2 = sp.trigsimp(sp.expand(J2))
print('J2(g,q) =')
print(J2)
