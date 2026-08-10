# -*- coding: utf-8 -*-
"""t3_dNJ2dg: decompose dNJ2/dg at fixed q on T2."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

# dNJ2/dg at fixed q: A=pi-g, t=atan(q tan g)
# dNJ2/dg = (dNJ2/dA)(dA/dg) + (dNJ2/dt)(dt/dg) + (dNJ2/dsg)(dsg/dg) + (dNJ2/dcg)(dcg/dg) + (dNJ2/dst)(dst/dg) + (dNJ2/dct)(dct/dg)
# with all partials treating other variables fixed
# dA/dg = -1, dsg/dg = cg, dcg/dg = -sg, dt/dg = q(1+tan^2 g)/(1+q^2 tan^2 g), dst/dg = ct*dt/dg, dct/dg = -st*dt/dg
g = sp.symbols('g', positive=True)
q = sp.symbols('q', positive=True)
dtdg = q*(1+sp.tan(g)**2)/(1+q**2*sp.tan(g)**2)
expr = (sp.diff(NJ2, A)*(-1) + sp.diff(NJ2, t)*dtdg + sp.diff(NJ2, sg)*cg - sp.diff(NJ2, cg)*sg
        + sp.diff(NJ2, st)*ct*dtdg - sp.diff(NJ2, ct)*st*dtdg)
expr = sp.expand(expr)
# substitute A = pi - g, sg = sin g, cg = cos g, t = atan(q tan g): keep symbolic A,t,sg,cg,st,ct as atoms
# replace A->pi-g etc AFTER simplifying? Let's keep as function of (g, q, A, t, sg, cg, st, ct)
print('expr terms:', len(sp.Add.make_args(expr)))
# numerical eval
f = sp.lambdify((A,t,sg,cg,st,ct,g,q), expr, 'numpy')
gstar = 0.6556493289387357
def ev(gv, qv):
    Av = math.pi-gv; tv = math.atan(qv*math.tan(gv))
    return float(f(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv), gv, qv))
lo, hi, arglo = 1e30, -1e30, None
for i in range(100):
    g = gstar + i*(math.pi/3-gstar)/100
    ql = max(math.tan(0.4*(math.pi-g))/math.tan(g), 1.0)
    qh = min(math.tan(0.5*(math.pi-g))/math.tan(g), 2.0)
    if qh < 1: continue
    for j in range(100):
        q = ql + j*(qh-ql)/100
        v = ev(g,q)
        if v < lo: lo=v; arglo=(g,q)
        if v > hi: hi=v
print('dNJ2/dg over T2: [%.1f, %.1f], min at (g,q)=(%.4f, %.4f)' % (lo, hi, arglo[0], arglo[1]))
# check: is dtdg the correct factor? verify vs numeric derivative
def NJ_gq(gv, qv):
    Av = math.pi-gv; tv = math.atan(qv*math.tan(gv))
    import sympy as sp2
    fN = sp2.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')
    return float(fN(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))
h=1e-6
gv, qv = 1.0, 1.5
num = (NJ_gq(gv+h,qv)-NJ_gq(gv-h,qv))/(2*h)
print('numeric dNJ2/dg at (1.0,1.5):', num, ' vs formula:', ev(gv, qv))
