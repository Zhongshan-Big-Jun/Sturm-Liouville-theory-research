# -*- coding: utf-8 -*-
"""t3_dAd_ranges: scan pieces of dNJ2/dA|c over the loose region."""
import sympy as sp, json, math, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
c = sp.symbols('c', positive=True)
w = sp.symbols('w', positive=True)

with open('misc/t3_dAd_clean.pkl','rb') as fh: d = pickle.load(fh)
P0, P1, Pw1 = d['P0'], d['P1'], d['Pw1']
f0 = sp.lambdify((A,c,sg,cg,w), P0, 'numpy')
f1 = sp.lambdify((A,c,sg,cg,w), P1, 'numpy')
fw = sp.lambdify((A,c,sg,cg,w), Pw1, 'numpy')

Amin, Amax = 2*math.pi/3, math.pi-0.655
rng = {k: [1e30,-1e30] for k in ['P0','P1','Pw1','full']}
arg = {}
N = 100
for i in range(N+1):
    for j in range(N+1):
        Av = Amin + i*(Amax-Amin)/N
        cv = 0.4 + j*0.1/N
        if Av*(1+cv) < math.pi: continue
        gv = math.pi-Av
        sgv = math.sin(gv); cgv = math.cos(gv)
        wv = math.cos(cv*Av)**2
        p0 = float(f0(Av, cv, sgv, cgv, wv))
        p1 = float(f1(Av, cv, sgv, cgv, wv))
        pw = float(fw(Av, cv, sgv, cgv, wv))
        full = p0 + math.sqrt(1-wv)*p1 + math.sqrt(wv*(1-wv))*pw
        for k, v in [('P0',p0),('P1',p1),('Pw1',pw),('full',full)]:
            if v < rng[k][0]: rng[k][0]=v; arg[k]=('min',Av,cv)
            if v > rng[k][1]: rng[k][1]=v; arg[k]=('max',Av,cv)
for k in rng:
    print('%s: in [%.2f, %.2f]  %s' % (k, rng[k][0], rng[k][1], arg[k]))
