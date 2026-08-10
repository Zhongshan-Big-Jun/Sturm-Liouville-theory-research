# -*- coding: utf-8 -*-
"""t3_z1_parts: parts of dNJ2/dg over T2."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

g = sp.symbols('g', positive=True)
q = sp.symbols('q', positive=True)
dtdg = q*(1+sp.tan(g)**2)/(1+q**2*sp.tan(g)**2)
part1 = sp.expand(sp.diff(NJ2, A)*(-1) + sp.diff(NJ2, sg)*cg - sp.diff(NJ2, cg)*sg)   # A/gamma rotation part
part2 = sp.expand(sp.diff(NJ2, t)*dtdg + sp.diff(NJ2, st)*ct*dtdg - sp.diff(NJ2, ct)*st*dtdg)  # t part
f1 = sp.lambdify((A,t,sg,cg,st,ct,g,q), part1, 'numpy')
f2 = sp.lambdify((A,t,sg,cg,st,ct,g,q), part2, 'numpy')

gstar = 0.6556493289387357
lo1, hi1, lo2, hi2 = 1e30, -1e30, 1e30, -1e30
arg1 = arg2 = None
for i in range(150):
    g = gstar + i*(math.pi/3-gstar)/150
    ql = max(math.tan(0.4*(math.pi-g))/math.tan(g), 1.0)
    qh = min(math.tan(0.5*(math.pi-g))/math.tan(g), 2.0)
    if qh < 1: continue
    for j in range(150):
        q = ql + j*(qh-ql)/150
        Av = math.pi-g; tv = math.atan(q*math.tan(g))
        v1 = float(f1(Av, tv, math.sin(g), math.cos(g), math.sin(tv), math.cos(tv), g, q))
        v2 = float(f2(Av, tv, math.sin(g), math.cos(g), math.sin(tv), math.cos(tv), g, q))
        if v1 < lo1: lo1=v1; arg1=(g,q)
        if v1 > hi1: hi1=v1
        if v2 < lo2: lo2=v2; arg2=(g,q)
        if v2 > hi2: hi2=v2
print('part1 (A/sg/cg rotation): [%.1f, %.1f] min at %s' % (lo1, hi1, arg1))
print('part2 (t via B2):         [%.1f, %.1f] min at %s' % (lo2, hi2, arg2))
