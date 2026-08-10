# -*- coding: utf-8 -*-
"""t3_Gx_parts: decompose Gx and check Phi/D >= 2/3."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
mp.dps = 30

def comps(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = 3/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*sx*cx/(den*den)
    Gc = du*V + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return dict(A=A,c=c,sx=sx,cx=cx,Phi=Phi,den=den,u=u,A0=A0,H=H,V=V,G=G,du=du,dH=dH,Gc=Gc,
                Phix=Phix,denx=denx,ux=ux,A0x=A0x,Hx=Hx,Gx=Gx,PhiD=Phi/den)

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

rng = {k: [mpf(1e30), mpf(-1e30)] for k in ['PhiD','uxV','uHx','umA0x','Gx','u','G','Gc','V','H','A0','du','dH']}
for i in range(250):
    g = glo + mpf(i)*(ghi-glo)/250
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(250):
        q = ql + mpf(j)*(qh-ql)/250
        if q < 1 or q > 2: continue
        d = comps(g,q)
        vals = {'PhiD':d['PhiD'], 'uxV':d['ux']*d['V'], 'uHx':d['u']*d['Hx'], 'umA0x':-d['u']*d['A0x'],
                'Gx':d['Gx'], 'u':d['u'], 'G':d['G'], 'Gc':d['Gc'], 'V':d['V'], 'H':d['H'], 'A0':d['A0'], 'du':d['du'], 'dH':d['dH']}
        for k, v in vals.items():
            if v < rng[k][0]: rng[k][0]=v
            if v > rng[k][1]: rng[k][1]=v
for k in rng:
    print('%s: [%.6f, %.6f]' % (k, rng[k][0], rng[k][1]))
# check Gx = uxV + uHx - uA0x at a point
d = comps(mpf('0.9'), mpf('1.2'))
print('check: uxV+uHx-uA0x = %.8f vs Gx = %.8f' % (d['ux']*d['V']+d['u']*d['Hx']-d['u']*d['A0x'], d['Gx']))
