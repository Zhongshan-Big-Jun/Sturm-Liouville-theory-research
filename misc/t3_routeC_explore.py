# -*- coding: utf-8 -*-
"""t3_routeC_explore.py: pieces of Gx and H2 on T2; monotonicity probes."""
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar

def comps(A, c):
    t = c*A
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    D = q + c*Phi
    u = A*Phi/D
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/D
    V = H - A0
    G = u*V
    Phix = 2*(q*q-1)*sx*cx
    ux = (Phi + A*Phix)/D - A*Phi*c*Phix/(D*D)
    A0x = -3/(A*A) - 2/(sx*sx)
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*D - 2*c*(q*q-1)*sx*cx*c*Phix)/(D*D)
    Gx = ux*V + u*(Hx - A0x)
    return q, u, V, G, ux, Hx, A0x, Gx, Phi, D

def inT2(A, c):
    t = c*A
    q = -tan(t)/tan(A)
    return q >= 1 and q <= 2 and c >= mpf('0.4') and c <= mpf('0.5')

# piece ranges
rng = {}
for key in ['ux','Hx','A0x','u','V','p1','p2','p3','Gx','H2']:
    rng[key] = [mpf('1e30'), mpf('-1e30')]
N=300
argmin = {}
for i in range(N+1):
    A = Amin + mpf(i)*(Amax-Amin)/N
    for j in range(N+1):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/N
        if not inT2(A,c): continue
        q,u,V,G,ux,Hx,A0x,Gx,Phi,D = comps(A,c)
        p1 = ux*V; p2 = u*Hx; p3 = -u*A0x
        vals = {'ux':ux,'Hx':Hx,'A0x':A0x,'u':u,'V':V,'p1':p1,'p2':p2,'p3':p3,'Gx':Gx,'H2':u*Gx}
        for k,v in vals.items():
            if v < rng[k][0]: rng[k][0]=v; argmin[k]=(float(A),float(c))
            if v > rng[k][1]: rng[k][1]=v
for k in rng:
    print('%-4s: [%8.4f, %8.4f]  min at (A,c)=(%.4f,%.4f)' % (k, rng[k][0], rng[k][1], argmin[k][0], argmin[k][1]))

# Gx at the two key corners and along c=0.4 line
print()
print('corner (2pi/3, 1/2):', comps(Amin, mpf('0.5'))[7])
print('corner (x*, 0.4):', comps(Amax, mpf('0.4'))[7])
# Gx along q=1 curve (c = pi/A - 1)
print('Gx along q=1 curve:')
for k in range(6):
    A = Amin + mpf(k)*(Amax-Amin)/5
    c = mppi/A - 1
    if c < mpf('0.4') or c > mpf('0.5'): continue
    q,u,V,G,ux,Hx,A0x,Gx,Phi,D = comps(A,c)
    print('  A=%.4f c=%.4f q=%.3f Gx=%.5f uGx=%.5f' % (A,c,q,Gx,u*Gx))
