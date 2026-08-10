# -*- coding: utf-8 -*-
"""t3_Bcheck2.py: verify NJ2 = -32 A^2 cg B mod relations."""
import sympy as sp, json
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
NJ2 = sum(int(r['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(r['monoms']))
G = [sg**2 + cg**2 - 1, st**2 + ct**2 - 1]
out = sp.reduced(sp.expand(NJ2), G, [sg, cg, st, ct])
red = sp.expand(out[0][0])
B = sp.expand(red/(-32*A**2*cg))
print('B =', B)
# check NJ2 + 32 A^2 cg B in ideal
diff = sp.expand(NJ2 + 32*A**2*cg*B)
r2 = sp.reduced(diff, G, [sg, cg, st, ct])
print('remainder of diff mod ideal:', sp.expand(r2[0][0]))
# now B's sign: group B terms
print()
print('B terms:')
for term in sp.Add.make_args(sp.expand(B)):
    print('  ', term)
