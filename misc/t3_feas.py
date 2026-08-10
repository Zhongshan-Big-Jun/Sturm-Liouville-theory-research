# -*- coding: utf-8 -*-
"""t3_feas: box-bound feasibility for sign of each numerator polynomial over T2 atom box.
Mononomial bound: A^a t^b SG^p CG^r ST^s CT^v over independent box ranges.
SG^p CG^r max/min over gamma in [gL,gR], ST^s CT^v over t in [tL,tR].
"""
import numpy as np, math, json

# atom box ranges (superset of T2)
gL, gR = 0.655, math.pi/3
tL, tR = 0.4*(2*math.pi/3), 0.5*(math.pi-0.655)   # 4pi/15=0.8378, 1.2433
Amin, Amax = 2*math.pi/3, math.pi-0.655

def powmaxmin(lo, hi, f, p, r):
    # max/min of f(x)^p * g(x)^r where f=sin, g=cos over x in [lo,hi]
    # for sin^p cos^r: critical at tan x = p/r (if p,r>0) inside range
    vals = []
    for x in [lo, hi]:
        vals.append((math.sin(x)**p)*(math.cos(x)**r))
    if p>0 and r>0:
        xc = math.atan(p/r)
        if lo < xc < hi:
            vals.append((math.sin(xc)**p)*(math.cos(xc)**r))
    return max(vals), min(vals)

with open('misc/t3_num6.json', encoding='utf-8') as fh:
    res = json.load(fh)

for k, r in res.items():
    monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
    # split
    pos = [(m,c) for m,c in zip(monoms,coeffs) if c>0]
    neg = [(m,c) for m,c in zip(monoms,coeffs) if c<0]
    def ubound(m):
        a,b,p,rr,s,v = m
        sgmx, _ = powmaxmin(gL, gR, math.sin, p, rr)
        stmx, _ = powmaxmin(tL, tR, math.sin, s, v)
        return Amax**a * tR**b * sgmx * stmx
    def lbound(m):
        a,b,p,rr,s,v = m
        _, sgmn = powmaxmin(gL, gR, math.sin, p, rr)
        _, stmn = powmaxmin(tL, tR, math.sin, s, v)
        return Amin**a * tL**b * sgmn * stmn
    Pu = sum(c*ubound(m) for m,c in pos)
    Ql = sum((-c)*lbound(m) for m,c in neg)   # negative part magnitude lower bound
    print('%-8s: pos_ub=%.4e  negmag_lb=%.4e  ratio=%.4f  %s' % (k, Pu, Ql, Pu/Ql, 'OK' if Pu < Ql else 'FAIL'))
