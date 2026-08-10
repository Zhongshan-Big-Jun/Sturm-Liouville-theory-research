# t3_Gxpieces.py: ranges of Gx pieces on T2; verify Gx = ux*V + u*(Hx - A0x) with fixed-q derivatives
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar
def comps(A, c):
    t = c*A
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    D = q + c*Phi
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/D
    V = H - A0
    u = A*Phi/D
    Phix = 2*(q*q-1)*sx*cx
    ux = (Phi + A*Phix)/D - A*Phi*c*Phix/(D*D)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*D - 2*c*(q*q-1)*sx*cx*c*Phix)/(D*D)
    Gx = ux*V + u*(Hx - A0x)
    return dict(u=u,Gx=Gx,ux=ux,V=V,Hx=Hx,A0x=A0x,Phi=Phi,D=D,q=q)

rng = {k:[mpf('1e30'),mpf('-1e30')] for k in ['u','Gx','ux','V','Hx','mA0x','uxV','uHx','umA0x','Phi','D','q']}
N=300
for i in range(N+1):
    A = Amin + mpf(i)*(Amax-Amin)/N
    for j in range(N+1):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/N
        if A*(1+c) < mppi: continue
        d = comps(A,c)
        vals = dict(u=d['u'],Gx=d['Gx'],ux=d['ux'],V=d['V'],Hx=d['Hx'],mA0x=-d['A0x'],
                    uxV=d['ux']*d['V'],uHx=d['u']*d['Hx'],umA0x=d['u']*(-d['A0x']),
                    Phi=d['Phi'],D=d['D'],q=d['q'])
        for k,v in vals.items():
            if v < rng[k][0]: rng[k][0]=v
            if v > rng[k][1]: rng[k][1]=v
for k in ['u','Gx','ux','V','Hx','mA0x','uxV','uHx','umA0x','Phi','D','q']:
    print('%s: [%.5f, %.5f]' % (k, rng[k][0], rng[k][1]))
print('check sum: uxV+uHx+umA0x vs Gx at a point:')
d = comps(mpf('0.9')+2*mppi/3*0 - (mppi-mpf('0.9')), mpf('0.4'))
# just pick (A,c) = (2.3, 0.45)
d = comps(mpf('2.3'), mpf('0.45'))
print('  uxV=%.6f uHx=%.6f umA0x=%.6f sum=%.6f Gx=%.6f' % (d['ux']*d['V'], d['u']*d['Hx'], d['u']*(-d['A0x']), d['ux']*d['V']+d['u']*d['Hx']+d['u']*(-d['A0x']), d['Gx']))
