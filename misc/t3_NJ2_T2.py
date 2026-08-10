# -*- coding: utf-8 -*-
"""t3_NJ2_T2: NJ2 max and monotonicity over actual T2."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
f = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')

def NJ_gq(g, q):
    A = math.pi-g
    t = math.atan(q*math.tan(g))
    return float(f(A, t, math.sin(g), math.cos(g), math.sin(t), math.cos(t)))

gstar = 0.6556493289387357
glo, ghi = gstar, math.pi/3
def qlo(g): return math.tan(0.4*(math.pi-g))/math.tan(g)
def qhi(g): return math.tan(0.5*(math.pi-g))/math.tan(g)

best = (1e30, None); worst = (-1e30, None)
for i in range(300):
    g = glo + i*(ghi-glo)/300
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, 1.0)
    for j in range(300):
        q = ql + j*(qh-ql)/300
        if q < 1 or q > 2: continue
        v = NJ_gq(g,q)
        if v < best[0]: best = (v,(g,q))
        if v > worst[0]: worst = (v,(g,q))
print('NJ2 over T2: [%.2f, %.2f]; max at (g,q)=(%.4f, %.4f)' % (best[0], worst[0], worst[1][0], worst[1][1]))
# derivatives over T2
def dq(g, q, h=1e-6): return (NJ_gq(g,q+h)-NJ_gq(g,q-h))/(2*h)
def dg(g, q, h=1e-6): return (NJ_gq(g+h,q)-NJ_gq(g-h,q))/(2*h)
loQ, hiQ, loG, hiG = 1e30, -1e30, 1e30, -1e30
argQ = argG = None
for i in range(150):
    g = glo + i*(ghi-glo)/150
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, 1.0)
    for j in range(150):
        q = ql + j*(qh-ql)/150
        if q < 1 or q > 2: continue
        vq = dq(g,q); vg = dg(g,q)
        if vq < loQ: loQ=vq; argQ=('min',g,q)
        if vq > hiQ: hiQ=vq
        if vg < loG: loG=vg; argG=('min',g,q)
        if vg > hiG: hiG=vg
print('dNJ2/dq over T2: [%.2f, %.2f] min at %s' % (loQ, hiQ, argQ))
print('dNJ2/dg over T2: [%.2f, %.2f] min at %s' % (loG, hiG, argG))
