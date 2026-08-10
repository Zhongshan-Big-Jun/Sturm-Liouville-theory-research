# t3_H2mono.py: directional derivatives of H2 = u*Gx over D
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar
def comps(A, c):
    t = c*A
    s2, c2 = sin(2*A), cos(2*A)
    st, ct = sin(2*t), cos(2*t)
    D = c*s2 - st
    u = A*s2/D
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(den*den)
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
    Gc = du*V + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return u, G, Gc, Gx, q, V

h = mpf('2e-6')
random.seed(11)
rows = []
for _ in range(600):
    A = Amin + mpf(random.random())*(Amax-Amin)
    c = mpf('0.4') + mpf(random.random())*mpf('0.1')
    if A*(1+c) < mppi: continue
    u0,_,_,Gx0,_,_ = comps(A,c)
    u1,_,_,Gx1,_,_ = comps(A+h,c)
    u2,_,_,Gx2,_,_ = comps(A,c+h)
    dA = (u1*Gx1 - u0*Gx0)/h
    dc = (u2*Gx2 - u0*Gx0)/h
    rows.append((float(A),float(c),float(dA),float(dc),float(u0),float(Gx0)))
loA = min(r[2] for r in rows); hiA = max(r[2] for r in rows)
loc = min(r[3] for r in rows); hic = max(r[3] for r in rows)
print('dH2/dA over D: [%.3f, %.3f]' % (loA, hiA))
print('dH2/dc over D: [%.3f, %.3f]' % (loc, hic))
negA = [r for r in rows if r[2] < 0]
negc = [r for r in rows if r[3] < 0]
print('dH2/dA<0:', len(negA), ' dH2/dc<0:', len(negc))
if negA: print('  A-neg samples:', negA[:4])
if negc: print('  c-neg samples:', negc[:4])
