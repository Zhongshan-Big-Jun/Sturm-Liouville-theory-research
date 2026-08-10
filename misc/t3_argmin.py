# t3_argmin.py: find argmins/argmaxes on D and T2
import math
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
    return u, G, Gc, Gx, q

def scan(region):
    best = {}
    N = 800
    for i in range(N+1):
        A = Amin + mpf(i)*(Amax-Amin)/N
        for j in range(N+1):
            c = mpf('0.4') + mpf(j)*mpf('0.1')/N
            if A*(1+c) < mppi: continue
            if region=='T2':
                u,G,Gc,Gx,q = comps(A,c)
                if q > 2: continue
            else:
                u,G,Gc,Gx,q = comps(A,c)
            H1 = G*G+Gc; H2 = u*Gx
            for k,v in [('u',u),('Gx',Gx),('H2',H2),('H1',H1)]:
                key = k+'min' if k in ('u','Gx','H2') else k+'max'
                if key not in best or (v < best[key][0] if 'min' in key else v > best[key][0]):
                    best[key] = (v,(float(A),float(c)))
    return best
for reg in ['D','T2']:
    b = scan(reg)
    print('==', reg)
    for k in ['umin','Gxmin','H2min','H1max']:
        print('  %s = %.8f at (A,c) = (%.5f, %.4f)' % (k, b[k][0], b[k][1][0], b[k][1][1]))
    # corner values
    u,G,Gc,Gx,q = comps(2*mppi/3, mpf('0.5'))
    print('  corner (2pi/3, 1/2): u=%.8f Gx=%.8f H2=%.8f H1=%.8f' % (u,Gx,u*Gx,G*G+Gc))
