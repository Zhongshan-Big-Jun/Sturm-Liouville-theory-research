import json, sympy as sp
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
print('=== collected by A ===')
for (mon, coeff) in sorted(sp.Poly(NJ2, A).terms(), key=lambda kv: -kv[0][0]):
    print('A^%d : %s' % (mon[0], sp.factor(coeff)))
print()
print('=== collected by t ===')
for (mon, coeff) in sorted(sp.Poly(NJ2, t).terms(), key=lambda kv: -kv[0][0]):
    print('t^%d : %s' % (mon[0], sp.factor(coeff)))
