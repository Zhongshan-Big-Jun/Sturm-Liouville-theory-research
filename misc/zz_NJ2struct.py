# -*- coding: utf-8 -*-
"""Explore NJ2 structure: factor, group by (st,ct) powers, reduce via st^2+ct^2=1."""
import json, sympy as sp
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
print('factor attempt (may be slow)...')
f1 = sp.factor(NJ2)
print('factor:', f1)
print()
# collect by (st,ct) powers
c1 = sp.collect(NJ2, [st, ct])
print('collected by st,ct:')
print(c1)
print()
# group by total degree in (sg,cg,st,ct): all even => substitute a=sg^2,b=cg^2,u=st^2,v=ct^2 plus cross terms?
# collect as polynomial in (st*ct) and st^2, ct^2:
print('as poly in (st,ct) with sg,cg,A,t coefficients:')
for (mon, coeff) in sorted(sp.Poly(NJ2, st, ct).terms(), key=lambda kv: kv[0], reverse=True):
    print('  st^%d ct^%d : %s' % (mon[0], mon[1], sp.factor(coeff)))
