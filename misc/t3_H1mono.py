# t3_H1mono.py: directional derivatives of H1 = G^2+Gc over D
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
rows = []
random.seed(7)
for _ in range(400):
    A = Amin + mpf(random.random())*(Amax-Amin)
    c = mpf('0.4') + mpf(random.random())*mpf('0.1')
    if A*(1+c) < mppi: continue
    u0,G0,Gc0,Gx0,q0,V0 = comps(A,c)
    _,Ga,_,_,_,_ = comps(A+h,c)
    _,_,Gcb,_,_,_ = comps(A,c+h)
    dA = (Ga*Ga+Gcb - (G0*G0+Gc0))  # this mixes; compute properly below
    _,G1,Gc1,_,_,_ = comps(A+h,c)
    _,G2,Gc2,_,_,_ = comps(A,c+h)
    dH1dA = ((G1*G1+Gc1)-(G0*G0+Gc0))/h
    dH1dc = ((G2*G2+Gc2)-(G0*G0+Gc0))/h
    rows.append((float(A),float(c),float(dH1dA),float(dH1dc),float(G0),float(Gc0)))
loA = min(r[2] for r in rows); hiA = max(r[2] for r in rows)
loc = min(r[3] for r in rows); hic = max(r[3] for r in rows)
print('dH1/dA over D: [%.3f, %.3f]' % (loA, hiA))
print('dH1/dc over D: [%.3f, %.3f]' % (loc, hic))
negA = [r for r in rows if r[2] < 0]
posc = [r for r in rows if r[3] > 0]
print('dH1/dA<0 count:', len(negA), ' dH1/dc>0 count:', len(posc))
if negA: print('  sample dH1/dA<0:', negA[:5])
if posc: print('  sample dH1/dc>0:', posc[:5])
