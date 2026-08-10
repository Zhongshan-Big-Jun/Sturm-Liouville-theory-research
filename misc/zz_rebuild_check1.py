import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
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
Tsum = sp.expand(T1+T2+T3+T4+T5+T6+T7+T8)
diff = sp.expand(W - Tsum)
def reduce_sq(expr, v, other):
    p = sp.Poly(expr, v)
    if p.degree() < 0: return sp.Integer(0)
    res = sp.Integer(0)
    for k in range(p.degree()+1):
        ck = p.coeff_monomial(v**k)
        if ck == 0: continue
        if k % 2 == 0:
            res += ck * (1 - other)**(k//2)
        else:
            res += ck * v * (1 - other)**((k-1)//2)
    return sp.expand(res)
for _ in range(6):
    diff = reduce_sq(diff, st, ct**2)
    diff = reduce_sq(diff, ct, st**2)
    diff = reduce_sq(diff, sg, cg**2)
    diff = reduce_sq(diff, cg, sg**2)
print('diff terms:', len(sp.Add.make_args(diff)))
print('W == T1+..+T8 modulo trig relations:', diff == 0)
