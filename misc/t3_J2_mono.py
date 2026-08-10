# -*- coding: utf-8 -*-
"""t3_J2_mono: J2_2d monotonicity and max location over T2."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
P = 2*(A*st*ct + t*sg*cg)
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')
fP = sp.lambdify((A,t,sg,cg,st,ct), P, 'numpy')

def J2_gq(g, q):
    A = math.pi-g
    t = math.atan(q*math.tan(g))
    return float(fN(A, t, math.sin(g), math.cos(g), math.sin(t), math.cos(t)) / fP(A,t,math.sin(g),math.cos(g),math.sin(t),math.cos(t))**4)

gstar = 0.6556493289387357
glo, ghi = gstar, math.pi/3
def qlo(g): return math.tan(0.4*(math.pi-g))/math.tan(g)
def qhi(g): return math.tan(0.5*(math.pi-g))/math.tan(g)

# max of J2 over T2
best = (1e30, None); worst = (-1e30, None)
for i in range(200):
    g = glo + i*(ghi-glo)/200
    ql, qh = qlo(g), qhi(g)
    for j in range(200):
        q = ql + j*(qh-ql)/200
        if q < 1 or q > 2: continue
        v = J2_gq(g,q)
        if v < best[0]: best = (v,(g,q))
        if v > worst[0]: worst = (v,(g,q))
print('J2 over T2: [%.4f, %.4f]; max at (g,q)=(%.4f, %.3f)' % (best[0], worst[0], worst[1][0], worst[1][1]))
# derivatives
def dJ2dq(g, q, h=1e-6):
    return (J2_gq(g,q+h) - J2_gq(g,q-h))/(2*h)
def dJ2dg(g, q, h=1e-6):
    return (J2_gq(g+h,q) - J2_gq(g-h,q))/(2*h)
loD, hiD = 1e30, -1e30
for i in range(100):
    g = glo + i*(ghi-glo)/100
    ql, qh = qlo(g), qhi(g)
    for j in range(100):
        q = ql + j*(qh-ql)/100
        if q < 1 or q > 2: continue
        v = dJ2dq(g,q)
        loD = min(loD, v); hiD = max(hiD, v)
print('dJ2/dq over T2: [%.4f, %.4f]' % (loD, hiD))
loD, hiD = 1e30, -1e30
for i in range(100):
    g = glo + i*(ghi-glo)/100
    ql, qh = qlo(g), qhi(g)
    for j in range(100):
        q = ql + j*(qh-ql)/100
        if q < 1 or q > 2: continue
        v = dJ2dg(g,q)
        loD = min(loD, v); hiD = max(hiD, v)
print('dJ2/dg over T2: [%.4f, %.4f]' % (loD, hiD))
# NJ2 at the two corners
for (g,q) in [(gstar, 2.0), (math.pi/3, 1.0)]:
    A = math.pi-g; t = math.atan(q*math.tan(g))
    nj = float(fN(A, t, math.sin(g), math.cos(g), math.sin(t), math.cos(t)))
    print('NJ2 at (g=%.6f, q=%.1f) = %.6f' % (g, q, nj))
