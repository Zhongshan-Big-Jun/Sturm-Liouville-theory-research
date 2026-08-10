# -*- coding: utf-8 -*-
"""t3_poly2: robust polynomial pipeline for G, Gc, Gx, u, J2_2d (all numerators polynomial)."""
import sympy as sp, pickle, json

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

def poly_num(expr):
    n, dd = sp.fraction(sp.together(expr))
    n = sp.expand(n)
    return n, sp.expand(dd)

G  = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P

# Gx as sum of terms, each converted to polynomial numerator with common denom P^3*den_extra
den_extra = cg**3*sg**3*ct**6
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/D3
numGx = sp.Integer(0)
for tt in [t1,t2,t3,t4]:
    n, dd = sp.fraction(sp.together(tt*P**3*den_extra))
    n = sp.expand(n); dd = sp.expand(dd)
    print('  term denom:', sp.factor(dd) if dd != 1 else 1)
    numGx = numGx + n
numGx = sp.expand(numGx)
Gx = numGx/(P**3*den_extra)

# J2_2d numerator over P^4*den_extra
nG, _ = sp.fraction(sp.together(G))
nGc, _ = sp.fraction(sp.together(Gc))
nu, _ = sp.fraction(sp.together(u))
NumJ = sp.expand(nG**2*den_extra) + sp.expand(nGc*P*den_extra) - sp.expand(nu*numGx)
NumJ = sp.expand(NumJ)
print('NumJ polynomial?', all(sp.degree(sp.fraction(sp.together(NumJ))[1], sym) == 0 for sym in [A,t,sg,cg,st,ct]))
# reduce: J2_2d = NumJ/(P^4*den_extra); check divisibility by den_extra
q0, rem0 = sp.div(NumJ, den_extra)
print('div by den_extra:', rem0 == 0)
if rem0 == 0:
    NJ = sp.expand(q0)
    atoms = [A,t,sg,cg,st,ct]
    poly = sp.Poly(NJ, *atoms)
    coeffs = poly.coeffs(); monoms = poly.monoms()
    print('NJ terms:', len(monoms), 'deg:', poly.total_degree())
    pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
    print('pos:', len(pos), 'sum_pos:', sum(pos), 'max_pos:', max(pos))
    print('neg:', len(neg), 'sum_neg:', sum(neg), 'min_neg:', min(neg))
    res = {'nterms': len(monoms), 'deg': poly.total_degree(),
           'monoms': [list(m) for m in monoms], 'coeffs': [str(c) for c in coeffs]}
    with open('misc/t3_NJ.json','w') as fh: json.dump(res, fh)
    tm = sorted(zip(monoms, coeffs), key=lambda x: -int(x[1]))
    print('--- top 8 pos ---')
    for m,c in tm[:8]: print('  %6d A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c,m[0],m[1],m[2],m[3],m[4],m[5]))
    print('--- top 8 neg ---')
    for m,c in tm[-8:]: print('  %6d A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c,m[0],m[1],m[2],m[3],m[4],m[5]))

with open('misc/t3_poly.pkl','wb') as fh:
    pickle.dump({'G':G,'Gc':Gc,'Gx':Gx,'u':u,'P':P,'numGx':numGx,'den_extra':den_extra,'NumJ':NumJ}, fh)
print('saved misc/t3_poly.pkl')
