# -*- coding: utf-8 -*-
"""t3_setup4: explicit denominator clearing, no sp.cancel.
Quantities in atoms (A,t,sg,cg,st,ct); g=pi-A; sg=sin g, cg=cos g."""
import sympy as sp

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
P = 2*(A*st*ct + t*sg*cg)

q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
K    = cg/(2*A*sg*ct**2)      # D = P*K
D, D2, D3 = P*K, (P*K)**2, (P*K)**3

# G, Gc, u: rational with denom P^1..P^3
G  = (4*A**2*cg**2 - 6*A*sg*cg)/P + 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 - 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P

# Gx term by term (rational), then clear denominators to P^3
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi**2*q2m1*sc_/D3
Gx_terms = [t1, t2, t3, t4]

# Multiply each by P^3 and expand; then check polynomial in atoms after clearing sg,ct denominators
def poly_part(expr, extra_den=None):
    e = sp.expand(expr)
    if extra_den:
        e = sp.expand(e*extra_den)
    return e

# find common: multiply all by P^3
GxP3 = sum(sp.expand(tt*P**3) for tt in Gx_terms)
# clear remaining denominators (sg, ct, A factors): multiply by sg^? ct^? — inspect
GxP3 = sp.expand(GxP3)
print('Gx*P^3 (before clearing) terms:', len(sp.Add.make_args(GxP3)))

# Since D = P*K, K=cg/(2Asgct^2): t1 has 1/K = 2Asgct^2/cg, t2,t3 1/K^2, t4 1/K^3
# multiply by cg^3 to clear 1/cg^k, then by sg^3 ct^6 for 1/sg^k ct^{2k}
mult = cg**3*sg**3*ct**6
GxP3c = sp.expand(GxP3*mult)
print('Gx*P^3*cg^3*sg^3*ct^6 terms:', len(sp.Add.make_args(GxP3c)))
# final: Gx = GxP3c / (P^3 * cg^3 sg^3 ct^6)
den_extra = cg**3*sg**3*ct**6
print('Gx extra denominator:', den_extra)

# J2 = G^2 + Gc - u*Gx ; common denom P^4 * den_extra
G2   = sp.expand(G**2)
# G^2 denom P^4
# Gc denom P^3 -> *P
# uGx denom P * P^3*den_extra = P^4*den_extra
NumJ = sp.expand(G2*P**4*den_extra) + sp.expand(Gc*P**4*den_extra) - sp.expand(u*Gx*P**4*den_extra)
NumJ = sp.expand(NumJ)
print('J2 numerator terms (denom P^4 * cg^3 sg^3 ct^6):', len(sp.Add.make_args(NumJ)))

import pickle
data = dict(G=G,Gc=Gc,Gx=Gx,u=u,P=P,GxP3c=GxP3c,den_extra=den_extra,NumJ=NumJ)
with open('misc/t3_symbols4.pkl','wb') as fh: pickle.dump(data, fh)
print('saved misc/t3_symbols4.pkl')
