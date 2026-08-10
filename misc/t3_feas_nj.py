# -*- coding: utf-8 -*-
"""t3_feas_nj: box-bound feasibility for NJ < 0 (23 terms)."""
import json, math
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]

gL, gR = 0.655, math.pi/3
tL, tR = 0.4*(2*math.pi/3), 0.5*(math.pi-0.655)
Amin, Amax = 2*math.pi/3, math.pi-0.655

def powmaxmin(lo, hi, p, r):
    vals = []
    for x in [lo, hi]:
        vals.append((math.sin(x)**p)*(math.cos(x)**r))
    if p>0 and r>0:
        xc = math.atan(p/r)
        if lo < xc < hi:
            vals.append((math.sin(xc)**p)*(math.cos(xc)**r))
    return max(vals), min(vals)

pos = [(m,c) for m,c in zip(monoms,coeffs) if c>0]
neg = [(m,c) for m,c in zip(monoms,coeffs) if c<0]
def ub(m):
    a,b,p,rr,s,v = m
    return Amax**a * tR**b * powmaxmin(gL,gR,p,rr)[0] * powmaxmin(tL,tR,s,v)[0]
def lb(m):
    a,b,p,rr,s,v = m
    return Amin**a * tL**b * powmaxmin(gL,gR,p,rr)[1] * powmaxmin(tL,tR,s,v)[1]
Pu = sum(c*ub(m) for m,c in pos)
Ql = sum((-c)*lb(m) for m,c in neg)
print('NJ: pos_ub=%.4e negmag_lb=%.4e ratio=%.4f %s' % (Pu, Ql, Pu/Ql, 'OK' if Pu<Ql else 'FAIL'))

# also try tighter box using the t-gamma coupling constraints: t in [0.4A, 0.5A] for gamma in [gL,gR]
# effective t range given gamma: t_min(g)=max(g,0.4(pi-g)), t_max(g)=min(atan(2tan g), 0.5(pi-g))
# scan per-gamma-box: partition gamma into K boxes, compute t range per box as [min t_min, max t_max]? that relaxes per box too.
# Simpler: global t range from constraints:
tmin_eff = 0.4*(2*math.pi/3)  # at g->pi/3, t->0.4A? but q>=1 needs t>=g... at g=pi/3 t=pi/3>0.4A ok
# actually t in [max(g,0.4A), min(atan(2tan g), 0.5A)]. global min of lower = ?
tL2 = 0.4*(math.pi - math.pi/3)  # = 4pi/15 = 0.8378, attained at g=pi/3? but there t=pi/3. hmm
# the lower bound max(g, 0.4A): at g=pi/3: max=pi/3. at g=0.655: max(0.655,0.995)=0.995. min over g of max(g,0.4(pi-g)):
#   g <= 0.4(pi-g) iff g <= 2pi/7. For g in (0.655, 2pi/7): lower=0.4(pi-g) decreasing from 0.995 to 0.8976.
#   for g in (2pi/7, pi/3): lower = g increasing from 0.8976 to 1.0472.
#   so global min of lower = 0.8976 at g=2pi/7.
# upper min(atan(2tan g),0.5(pi-g)): at g=0.841 cross; max of upper over g: 0.5A at g where A max -> g=0.655: 1.243; but at g=0.655 upper=atan(2tan0.655)=0.9938 < 0.5A.
#   upper(g): for g<0.841: atan(2tan g) increasing 0.9938->1.1503; for g>0.841: 0.5(pi-g) decreasing 1.1503->1.0472. max = 1.1503 at g=0.841.
print('effective t range: [%.4f, %.4f]' % (0.8976, 1.1503))
# redo bounds with effective t range
tL3, tR3 = 0.8976, 1.1503
def ub2(m):
    a,b,p,rr,s,v = m
    return Amax**a * tR3**b * powmaxmin(gL,gR,p,rr)[0] * powmaxmin(tL3,tR3,s,v)[0]
def lb2(m):
    a,b,p,rr,s,v = m
    return Amin**a * tL3**b * powmaxmin(gL,gR,p,rr)[1] * powmaxmin(tL3,tR3,s,v)[1]
Pu2 = sum(c*ub2(m) for m,c in pos)
Ql2 = sum((-c)*lb2(m) for m,c in neg)
print('NJ eff-box: pos_ub=%.4e negmag_lb=%.4e ratio=%.4f %s' % (Pu2, Ql2, Pu2/Ql2, 'OK' if Pu2<Ql2 else 'FAIL'))
