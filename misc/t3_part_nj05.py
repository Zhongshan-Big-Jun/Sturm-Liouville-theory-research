# -*- coding: utf-8 -*-
"""t3_part_nj05: partition u for P05<0 directly (monomial bounds)."""
import json, math
with open('misc/t3_P05.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
pos = [(m,c) for m,c in zip(monoms,coeffs) if c>0]
neg = [(m,c) for m,c in zip(monoms,coeffs) if c<0]
def powmm(lo, hi, p, q):
    vals = [math.sin(lo)**p*math.cos(lo)**q, math.sin(hi)**p*math.cos(hi)**q]
    if p>0 and q>0:
        tc = math.atan(p/q)
        if lo < tc < hi: vals.append(math.sin(tc)**p*math.cos(tc)**q)
    return max(vals), min(vals)
def feas(N):
    uL, uR = math.pi/3, (math.pi-0.655)/2
    nf=0; worst=0
    for i in range(N):
        lo = uL + i*(uR-uL)/N; hi = uL + (i+1)*(uR-uL)/N
        Pu = sum(c*(hi**m[0])*powmm(lo,hi,m[1],m[2])[0] for m,c in pos)
        Ql = sum((-c)*(lo**m[0])*powmm(lo,hi,m[1],m[2])[1] for m,c in neg)
        ratio = Pu/Ql if Ql>0 else float('inf')
        worst = max(worst, ratio)
        if Pu >= Ql: nf += 1
    return nf, worst
for N in [5,10,15,20,30,40,60]:
    nf, wr = feas(N)
    print('P05<0: N=%d fail=%d worst_ratio=%.4f' % (N, nf, wr))
