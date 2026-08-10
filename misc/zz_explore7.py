import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
dNJdt = sp.diff(NJ2, t)
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
fd = sp.lambdify((A,t,sg,cg,st,ct), dNJdt, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
for (g,q) in [(0.7,1.2),(0.8,1.5),(0.9,1.5),(1.0,1.9),(1.0472,2.0),(0.655,1.0)]:
    h = mp.mpf('1e-8')
    fdq = (NJ(g,q+h)-NJ(g,q-h))/(2*h)
    A_ = mp.pi-g; t_ = mp.atan(q*mp.tan(g))
    chain = fd(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))*mp.tan(g)/(1+q*q*mp.tan(g)**2)
    print('(g,q)=(%.3f,%.3f): fd diff %.6f  chain %.6f' % (g,q,fdq,chain))
