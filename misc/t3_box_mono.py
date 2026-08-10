# -*- coding: utf-8 -*-
"""t3_box_mono: B2 min over full box; NJ2 on q=2 and gamma=pi/3 lines."""
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
# NJ2 on q=2 line
lo, hi, arglo = 1e30, -1e30, None
for i in range(2001):
    g = glo + i*(ghi-glo)/2000
    v = NJ_gq(g, 2.0)
    if v < lo: lo = v; arglo = (g,i)
    if v > hi: hi = v
print('NJ2(g, q=2) on [g*, pi/3]: [%.1f, %.1f]; min at g=%.6f' % (lo, hi, arglo[0]))
# NJ2 on gamma=pi/3 line
lo, hi, arglo = 1e30, -1e30, None
for i in range(2001):
    q = 1 + i/2000
    v = NJ_gq(math.pi/3, q)
    if v < lo: lo = v; arglo = (q,i)
    if v > hi: hi = v
print('NJ2(pi/3, q) on [1,2]: [%.1f, %.1f]; min at q=%.6f' % (lo, hi, arglo[0]))
# NJ2 at corner (pi/3, 2)
print('NJ2(pi/3, 2) =', NJ_gq(math.pi/3, 2.0))
# dNJ2/dg at fixed q over the box
def dg(g, q, h=1e-6):
    return (NJ_gq(g+h,q) - NJ_gq(g-h,q))/(2*h)
loD, hiD, argD = 1e30, -1e30, None
for i in range(100):
    g = glo + i*(ghi-glo)/100
    for j in range(100):
        q = 1 + j/100
        v = dg(g,q)
        if v < loD: loD=v; argD=('min',g,q)
        if v > hiD: hiD=v
print('dNJ2/dg over box: [%.1f, %.1f] at %s' % (loD, hiD, argD))
