# -*- coding: utf-8 -*-
"""Full corrected scan over T2 (fixed Gc sign) + verify J2 against NJ2."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
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
    # CORRECT Gc: g2 = u*(-2*(q^2-1)*s*b*q/D^2) with b=-cos x > 0
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    J = G*G + Gc - u*Gx
    return dict(q=q, c=c, u=u, G=G, Gx=Gx, Gc=Gc, J=J, H1=G*G+Gc, uGx=u*Gx)

# verify against NJ2 at a few points
import json
A_, t_ = __import__('sympy').symbols('A t')
sg, cg, st, ct = __import__('sympy').symbols('sg cg st ct')
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
NJ2 = sum(int(rj['coeffs'][i])*A_**m[0]*t_**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
P = 2*(A_*st*ct + t_*sg*cg)
fN = __import__('sympy').lambdify((A_,t_,sg,cg,st,ct), NJ2, 'numpy')
fP = __import__('sympy').lambdify((A_,t_,sg,cg,st,ct), P, 'numpy')
def J2_poly(g, q):
    A = mppi-g; t = atan(q*tan(g))
    return float(fN(A,t,sin(g),cos(g),sin(t),cos(t))/fP(A,t,sin(g),cos(g),sin(t),cos(t))**4)
for (g,q) in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(0.65565,2.0),(float(mppi/3),1.0)]:
    x = mppi-mpf(str(g)); th = atan(mpf(str(q))*tan(mpf(str(g))))
    r = comps(x, th)
    print('J2: NJ2/P^4=%.8f comps=%.8f diff=%.1e' % (J2_poly(g,q), r['J'], abs(J2_poly(g,q)-float(r['J']))))

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 200
R = {k: [mpf('1e30'), mpf('-1e30'), None, None] for k in ['G','Gc','Gx','u','uGx','H1','J']}
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(-1, N+2):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N if (0 <= j <= N) else (th_lo if j<0 else th_hi)
        if th < th_lo or th > th_hi: continue
        r = comps(x, th)
        vals = {'G': r['G'], 'Gc': r['Gc'], 'Gx': r['Gx'], 'u': r['u'], 'uGx': r['uGx'], 'H1': r['H1'], 'J': r['J']}
        for k in vals:
            if vals[k] < R[k][0]: R[k][0], R[k][2] = vals[k], (float(x), float(th), float(r['q']), float(r['c']))
            if vals[k] > R[k][1]: R[k][1], R[k][3] = vals[k], (float(x), float(th), float(r['q']), float(r['c']))
for k in ['G','Gc','Gx','u','uGx','H1','J']:
    print('%s: min=%.6f at %s ; max=%.6f at %s' % (k, R[k][0], R[k][2], R[k][1], R[k][3]))
