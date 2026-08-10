# -*- coding: utf-8 -*-
"""t3_Gx_mono_domains.py: monotonicity of Gx on extended domains + c=1/2 curve bound."""
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar

def comps_xth(x, th):
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
    ux = (Phi + x*(-2*s*b*(q*q-1)))/den - x*Phi*c*(-2*s*b*(q*q-1))/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*(b*b - s*s)*den - 2*c*(q*q-1)*s*(-b)*c*(-2*s*b*(q*q-1)))/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return q, Gx

h = mpf('1e-6')
random.seed(29)
def scan(name, ok, N=900):
    ddx=[]; ddt=[]
    for _ in range(N):
        x = xmin + mpf(random.random())*(xmax-xmin)
        th = mpf(random.random())*mpf('1.2430')
        if not ok(x,th): continue
        q0,Gx0 = comps_xth(x,th)
        Gx1 = comps_xth(x+h,th)[1]; Gx2 = comps_xth(x,th+h)[1]
        ddx.append(float((Gx1-Gx0)/h)); ddt.append(float((Gx2-Gx0)/h))
    if ddx: print('%s: dGx/dx [%.3f, %.3f], dGx/dth [%.3f, %.3f]  (n=%d)' % (name, min(ddx),max(ddx),min(ddt),max(ddt),len(ddx)))
    else: print(name, 'no samples')

# Domain A (case theta <= pi/3): x in [2pi/3, x*], th in [pi-x, pi/3], q<=2
scan('A: th<=pi/3, q<=2', lambda x,th: th<=mppi/3 and th>=mppi-x and -tan(th)/tan(x)<=2)
# Domain B (case theta >= pi/3): x in [2pi/3, x*], th in [pi/3, 0.5x], q<=2
scan('B: th>=pi/3, c<=1/2, q<=2', lambda x,th: th>=mppi/3 and th<=mpf('0.5')*x and -tan(th)/tan(x)<=2)
# Full T2
scan('T2', lambda x,th: th>=max(mpf('0.4')*x, mppi-x) and th<=min(mpf('0.5')*x, atan(-2*tan(x))) and -tan(th)/tan(x)<=2 and -tan(th)/tan(x)>=1)

# c=1/2 curve: Gx(x, x/2) for x in [2pi/3, x*]
print()
lo = (mpf('1e30'), None)
for i in range(2001):
    x = xmin + mpf(i)*(xmax-xmin)/2000
    q,Gx = comps_xth(x, x/2)
    if Gx < lo[0]: lo = (Gx, (float(x), float(q)))
print('Gx on c=1/2 curve: min %.6f at x=%.4f (q=%.3f)' % (lo[0], lo[1][0], lo[1][1]))
# q=1 curve: Gx(x, pi-x)
lo = (mpf('1e30'), None)
for i in range(2001):
    x = xmin + mpf(i)*(xmax-xmin)/2000
    th = mppi - x
    if th < mpf('0.4')*x: break
    q,Gx = comps_xth(x, th)
    if Gx < lo[0]: lo = (Gx, (float(x), float(q)))
print('Gx on q=1 curve: min %.6f at x=%.4f' % (lo[0], lo[1][0]))
# Gx at (2pi/3, th) for th in [?, pi/3]
lo = (mpf('1e30'), None)
for i in range(2001):
    th = mpf('0.5') + mpf(i)*(mppi/3-mpf('0.5'))/2000
    q,Gx = comps_xth(xmin, th)
    if Gx < lo[0]: lo = (Gx, (float(th), float(q)))
print('Gx on x=2pi/3 vertical: min %.6f at th=%.4f (q=%.3f)' % (lo[0], lo[1][0], lo[1][1]))
