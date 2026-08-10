# t3_Vbounds.py: margins for V<=1, V>=-1/2; A0+|H| max; corner-region |H| >= -A0-1
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
    return A, c, u, V, H, A0, Phi/den, Phi
bestA0H = (mpf('-1e30'), None)
worstV = (mpf('1e30'), None); bestV = (mpf('-1e30'), None)
N=400
for i in range(N+1):
    g = gstar + mpf(i)*(mppi/3-gstar)/N
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q < 1 or q > 2: continue
        A,c,u,V,H,A0,pD,Phi = comps(g,q)
        v = A0 + abs(H)
        if v > bestA0H[0]: bestA0H = (v, (float(g),float(q),float(A),float(c)))
        if V < worstV[0]: worstV = (V, (float(g),float(q),float(A),float(c)))
        if V > bestV[0]: bestV = (V, (float(g),float(q),float(A),float(c)))
print('A0+|H| max on T2: %.6f at (g,q,A,c)=%s' % (bestA0H[0], bestA0H[1]))
print('V min: %.6f at %s ; V max: %.6f at %s' % (worstV[0], worstV[1], bestV[0], bestV[1]))
# H2(pi/3, q) for q in [1,2]
def H2_p3(q):
    g = mppi/3
    A,c,u,V,H,A0,pD,Phi = comps(g,q)
    # recompute Gx pieces at gamma=pi/3
    t = atan(q*tan(g)); sx, cx = sin(g), -cos(g)
    den = q + c*Phi
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return u*Gx, Gx, u
lo = (mpf('1e30'), None)
for q in [mpf(1) + mpf(k)/40 for k in range(41)]:
    H2,Gx,u = H2_p3(q)
    if H2 < lo[0]: lo = (H2, (float(q), float(Gx), float(u)))
print('H2(pi/3,q) min over q in [1,2]: %.6f at q=%.4f (Gx=%.4f, u=%.4f)' % (lo[0], lo[1][0], lo[1][1], lo[1][2]))
for q in [1.0, 1.2, 1.5, 1.8, 2.0]:
    H2,Gx,u = H2_p3(mpf(q))
    print('  q=%.2f: H2=%.5f Gx=%.5f u=%.5f' % (q, H2, Gx, u))
