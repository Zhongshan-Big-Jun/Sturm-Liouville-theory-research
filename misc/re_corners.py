# -*- coding: utf-8 -*-
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt, acos
mp.dps = 40

def comps(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, s=s, b=b, S=S, C=C, Phi=Phi, c=c, u=u, A0=A0, H=H, V=V, G=G, Gx=Gx, Gc=Gc, J2=G*G+Gc-u*Gx)

# right corner R: (gamma,q) = (gstar, 2)
gstar = mpf('0.65564932893873566325493245529469')
xR = mppi - gstar
thR = 2*xR/5
r = comps(xR, thR)
print('R: x=%.8f th=%.8f q=%.8f c=%.8f' % (xR, thR, r['q'], r['c']))
for k in ['u','A0','H','V','G','Gx','Gc']:
    print('  %s = %.10f' % (k, r[k]))
print('  H1=G^2+Gc = %.10f' % (r['G']**2 + r['Gc']))
print('  J2 = %.10f' % r['J2'])
# left corner L
xL = 2*mppi/3; thL = mppi/3
r2 = comps(xL, thL)
print('L: G=%.6f Gc=%.6f Gx=%.6f u=%.6f H1=%.6f J2=%.6f' % (r2['G'], r2['Gc'], r2['Gx'], r2['u'], r2['G']**2+r2['Gc'], r2['J2']))
# along q=1: G,Gc,Gx,u
for xv in [2*mppi/3, mpf('2.1'), mpf('2.15'), mpf('2.2'), mpf('2.24399')]:
    r3 = comps(xv, mppi-xv)
    print('q=1 x=%.5f: G=%.5f Gc=%.5f Gx=%.5f u=%.5f H1=%.5f' % (xv, r3['G'], r3['Gc'], r3['Gx'], r3['u'], r3['G']**2+r3['Gc']))
