# t3_J2gq.py: J2 as function of q at fixed gamma over T2; find sign pattern of dJ2/dq
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)
def comps(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = mpf(3)/A + 2*cx/sx
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
    return G*G+Gc - u*Gx, G, Gc, Gx, u

for gv in [0.66, 0.7, 0.75, 0.8, 0.8976, 0.95, 1.0]:
    gl, gh = max(qlo(mpf(gv)),mpf(1)), min(qhi(mpf(gv)),mpf(2))
    print('gamma=%.4f: q in [%.4f, %.4f]' % (gv, float(gl), float(gh)))
    prev = None; rows=[]
    for j in range(41):
        q = gl + mpf(j)*(gh-gl)/40
        J2,G,Gc,Gx,u = comps(mpf(str(gv)), q)
        rows.append((float(q), float(J2)))
    for (q,J2) in rows:
        print('   q=%.4f J2=%.4f' % (q, J2))
