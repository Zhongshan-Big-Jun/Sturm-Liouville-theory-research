# -*- coding: utf-8 -*-
import json, sympy as sp
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
W = sp.expand(NJ2/(32*A*A*cg))
B1 = A*cg - 2*sg
B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
T1 = -2*A**3*B1*st*st*ct**4
T2 = A*A*cg*B2*st*st*ct*ct
T3 = -2*A**3*sg*t*st*ct**5
T4 = A*A*sg*t*B4*st*ct**3
T5 = -A*cg*cg*sg*t*B5*st*ct
T6 = 4*A*A*cg*sg*sg*t*t*ct**4
T7 = -A*cg*sg*sg*t*t*B7*ct*ct
T8 = 6*cg**3*sg**4*t*t
S = sp.expand(T1+T2+T3+T4+T5+T6+T7+T8)
diff = sp.expand(W - S)
print('diff nonzero; terms:')
for term in sp.Add.make_args(diff):
    print('  ', term)
# is diff zero under sg^2+cg^2=1, st^2+ct^2=1? reduce with those relations
rels = [sg**2+cg**2-1, st**2+ct**2-1]
def reduce_mod(expr, rels, gens):
    # polynomial reduction via groebner-free: substitute sg^2 = 1-cg^2 etc iteratively
    e = sp.expand(expr)
    for _ in range(20):
        e2 = sp.expand(e.subs({sg**2: 1-cg**2}).subs({st**2: 1-ct**2}))
        if e2 == e: break
        e = e2
    return sp.expand(e)
d2 = reduce_mod(diff, rels, None)
print('diff reduced with sg^2=1-cg^2, st^2=1-ct^2 :', d2)
print('is zero?', d2 == 0)
