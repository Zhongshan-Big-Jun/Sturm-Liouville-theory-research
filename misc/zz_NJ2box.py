# -*- coding: utf-8 -*-
"""NJ2 sign over the whole box [0.655,1.0472]x[1,2] (mapped via gamma,q), and relation J = NJ2/(16*Delta^4)."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 40
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')

def vals(g, q):
    A = mp.pi - g
    t = mp.atan(q*mp.tan(g))
    return dict(A=A, t=t, sg=mp.sin(g), cg=mp.cos(g), st=mp.sin(t), ct=mp.cos(t))

import numpy as np
glo, ghi = 0.655, 1.0472
N = 200
mn = (1e30, None); mx = (-1e30, None)
for i in range(N+1):
    g = glo + (ghi-glo)*i/N
    for j in range(N+1):
        q = 1 + j/N
        v = vals(g, q)
        n = float(fN(v['A'], v['t'], v['sg'], v['cg'], v['st'], v['ct']))
        if n < mn[0]: mn = (n, (g, q))
        if n > mx[0]: mx = (n, (g, q))
print('NJ2 over box [0.655,1.0472]x[1,2]: min %.4f max %.4f' % (mn[0], mx[0]))
print('NJ2 at L (pi/3,1):', float(fN(*[vals(mp.pi/3, 1)[k] for k in ['A','t','sg','cg','st','ct']])))
# check J = NJ2/(16 Delta^4) at sample points with comps
def compsJ(x, th):
    q = -mp.tan(th)/mp.tan(x)
    s, b = mp.sin(x), -mp.cos(x)
    S, C = mp.sin(th), mp.cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mp.mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    return G*G + Gc - u*Gx
for (g, q) in [(0.7, 1.5), (0.9, 1.2), (1.0, 1.1), (0.65565, 2.0), (mp.pi/3, 1.0)]:
    v = vals(g, q)
    n = fN(v['A'], v['t'], v['sg'], v['cg'], v['st'], v['ct'])
    Delta = v['A']*v['st']*v['ct'] + v['t']*v['sg']*v['cg']
    x = mp.pi - g; th = v['t']
    Jc = compsJ(x, th)
    print('g=%.4f q=%.2f: J_comps=%.8f  NJ2/(16D^4)=%.8f  diff=%.1e' % (g, q, Jc, n/(16*Delta**4), abs(Jc - n/(16*Delta**4))))
