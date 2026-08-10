# -*- coding: utf-8 -*-
"""t3_verify_J2: verify J2 = G^2+Gc-uGx == NJ2/P^4."""
import sympy as sp, json, math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
mp.dps = 30

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
P = 2*(A*st*ct + t*sg*cg)
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'numpy')
fP = sp.lambdify((A,t,sg,cg,st,ct), P, 'numpy')

def J2_poly(g, q):
    A = mppi-g; t = atan(q*tan(g))
    return float(fN(A, t, sin(g), cos(g), sin(t), cos(t))/fP(A,t,sin(g),cos(g),sin(t),cos(t))**4)

def J2_direct(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = 3/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    G = u*(H - A0)
    du = -A*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*sx*cx/(den*den)
    Gc = du*(H-A0) + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*(H-A0) + u*(Hx - A0x)
    return G*G + Gc - u*Gx, G, Gc, Gx, u

for (g,q) in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(0.65565,2.0),(math.pi/3,1.0),(0.85,1.8)]:
    jp = J2_poly(mpf(str(g)), mpf(str(q)))
    jd, G, Gc, Gx, u = J2_direct(mpf(str(g)), mpf(str(q)))
    print('(g=%.5f, q=%.2f): NJ2/P^4 = %.8f ; direct = %.8f ; diff = %.2e' % (g,q,jp,jd,abs(jp-jd)))
