# -*- coding: utf-8 -*-
"""t3_mono_gq: monotonicity of NJ2 in (gamma, q) and (gamma, c) coordinates."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)

with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
f = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')

# NJ2 as function of (gamma, q): A=pi-g, t=atan(q*tan g), c=t/A, st=sin t, ct=cos t
def NJ_gq(g, q):
    A = math.pi-g
    t = math.atan(q*math.tan(g))
    return float(f(A, t, math.sin(g), math.cos(g), math.sin(t), math.cos(t)))

# numerical derivatives
def dq(g, q, h=1e-6):
    return (NJ_gq(g, q+h) - NJ_gq(g, q-h))/(2*h)
def dg(g, q, h=1e-6):
    return (NJ_gq(g+h, q) - NJ_gq(g-h, q))/(2*h)

# region in (g,q): g in [0.655, pi/3], q in [1,2]
glo, ghi = 0.655, math.pi/3
loDq, hiDq, loDg, hiDg = 1e30, -1e30, 1e30, -1e30
argDq = argDg = None
for i in range(80):
    g = glo + i*(ghi-glo)/80
    for j in range(80):
        q = 1 + j/80
        vq = dq(g,q); vg = dg(g,q)
        if vq < loDq: loDq=vq; argDq=('min',g,q)
        if vq > hiDq: hiDq=vq; argDq=('max',g,q)
        if vg < loDg: loDg=vg; argDg=('min',g,q)
        if vg > hiDg: hiDg=vg; argDg=('max',g,q)
print('dNJ2/dq in [%.1f, %.1f] at %s' % (loDq, hiDq, argDq))
print('dNJ2/dg in [%.1f, %.1f] at %s' % (loDg, hiDg, argDg))
# true curve region: g in [2pi/7, pi/3], q in [1,2], c in (0.4,0.5)
glo2, ghi2 = 2*math.pi/7, math.pi/3
loDq, hiDq, loDg, hiDg = 1e30, -1e30, 1e30, -1e30
for i in range(80):
    g = glo2 + i*(ghi2-glo2)/80
    for j in range(80):
        q = 1 + j/80
        vq = dq(g,q); vg = dg(g,q)
        loDq = min(loDq, vq); hiDq = max(hiDq, vq)
        loDg = min(loDg, vg); hiDg = max(hiDg, vg)
print('on true region: dNJ2/dq in [%.1f, %.1f]; dNJ2/dg in [%.1f, %.1f]' % (loDq, hiDq, loDg, hiDg))
