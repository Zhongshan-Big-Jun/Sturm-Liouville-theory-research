# -*- coding: utf-8 -*-
"""t3_b_q1line: B on q=1 line, factor."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
# B = dNJdt/(2 A^2 cg)
g = sp.symbols('g', positive=True)
s, c = sp.symbols('s c', positive=True)
sub = {A: sp.pi-g, t: g, sg: s, cg: c, st: s, ct: c}
B_q1 = sp.expand(dNJdt.subs(sub))
print('dNJdt on q1 line (factor):')
try:
    print(sp.factor(B_q1))
except Exception as e:
    print('factor failed:', e)
# numeric spot check
def ev(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    import sympy as sp2
    d = sp2.lambdify((A,t,sg,cg,st,ct), dNJdt, 'numpy')
    return float(d(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))
print('dNJ/dt at (2pi/3, 0.5) =', ev(2*math.pi/3, 0.5))
# evaluate B_q1 at g=2pi/7 with s=sin(2pi/7), c=cos(2pi/7)
gv = 2*math.pi/7
print('B_q1 at g=2pi/7:', float(B_q1.subs({g: gv, s: math.sin(gv), c: math.cos(gv)}).evalf(20)))
