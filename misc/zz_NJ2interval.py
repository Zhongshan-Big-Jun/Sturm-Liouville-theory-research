# -*- coding: utf-8 -*-
"""Loose interval bound for NJ2 on the box using independent ranges."""
import json, mpmath as mp
mp.mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
# variable ranges over the box [0.655,1.0472]x[1,2]:
# A = pi-g in [pi-1.0472, pi-0.655]
# t = atan(q tan g): min at (g=0.655,q=1): 0.655; max at (g=1.0472,q=2): atan(2 tan(1.0472))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
Amin, Amax = mp.pi-ghi, mp.pi-glo
tmin = mp.atan(mp.tan(glo))
tmax = mp.atan(2*mp.tan(ghi))
sgmin, sgmax = mp.sin(glo), mp.sin(ghi)
cgmin, cgmax = mp.cos(ghi), mp.cos(glo)
stmin, stmax = mp.sin(tmin), mp.sin(tmax)
ctmin, ctmax = mp.cos(tmax), mp.cos(tmin)
ranges = {'A': (Amin, Amax), 't': (tmin, tmax), 'sg': (sgmin, sgmax), 'cg': (cgmin, cgmax), 'st': (stmin, stmax), 'ct': (ctmin, ctmax)}
print('ranges:')
for k, (a, b) in ranges.items(): print('  %s: [%.4f, %.4f]' % (k, a, b))
pos = mp.mpf(0); neg = mp.mpf(0)
for i, m in enumerate(rj['monoms']):
    coeff = mp.mpf(int(rj['coeffs'][i]))
    exps = m
    vmax = mp.mpf(1); vmin = mp.mpf(1)
    for k, e in zip(['A','t','sg','cg','st','ct'], exps):
        if e > 0:
            vmax *= ranges[k][1]**e
            vmin *= ranges[k][0]**e
    if coeff > 0:
        pos += coeff*vmax
    else:
        neg += coeff*vmin
print('pos sum bound: %.3f ; neg sum bound: %.3f ; total: %.3f' % (pos, neg, pos+neg))
