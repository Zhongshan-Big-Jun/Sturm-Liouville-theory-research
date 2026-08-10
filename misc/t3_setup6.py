# -*- coding: utf-8 -*-
"""t3_setup6: fix Gx assembly; verify forms numerically; save pkl."""
import sympy as sp

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
P = 2*(A*st*ct + t*sg*cg)

q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
K    = cg/(2*A*sg*ct**2)
D, D2, D3 = P*K, (P*K)**2, (P*K)**3

G  = (4*A**2*cg**2 - 6*A*sg*cg)/P + 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 - 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P

t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi**2*q2m1*sc_/D3
den_extra = cg**3*sg**3*ct**6
GxP3c = sum(sp.expand(tt*P**3*den_extra) for tt in [t1,t2,t3,t4])
Gx = GxP3c/(P**3*den_extra)

NumJ = sp.expand(G**2*P**4*den_extra) + sp.expand(Gc*P**4*den_extra) - sp.expand(u*Gx*P**4*den_extra)
NumJ = sp.expand(NumJ)

import mpmath as mp
mp.mp.dps = 30
x0, c0, q0 = sp.symbols('x0 c0 q0', positive=True)
sx0, cx0 = sp.sin(x0), sp.cos(x0)
Ph0 = cx0**2 + q0**2*sx0**2
D0  = q0 + c0*Ph0
W0  = 3 + 2*x0*cx0/sx0
sc0 = sx0*cx0
G0  = -Ph0*W0/D0 + 2*c0*x0*Ph0*(q0**2-1)*sc0/D0**2
Gx0 = sp.diff(G0, x0); Gc0 = sp.diff(G0, c0); u0 = x0*Ph0/D0
fG0 = sp.lambdify((x0,c0,q0), G0, 'mpmath'); fGx0 = sp.lambdify((x0,c0,q0), Gx0, 'mpmath')
fGc0 = sp.lambdify((x0,c0,q0), Gc0, 'mpmath'); fu0 = sp.lambdify((x0,c0,q0), u0, 'mpmath')

maxerr = 0
for gv, qv in [(0.7,1.5),(0.9,1.2),(1.0,1.5),(0.66,1.9),(1.0472,1.0),(0.85,2.0),(0.75,1.05)]:
    Av = mp.pi - gv; tv = mp.atan(qv*mp.tan(gv))
    sv = dict(A=Av, t=tv, sg=mp.sin(gv), cg=mp.cos(gv), st=mp.sin(tv), ct=mp.cos(tv))
    Gv  = float(sp.N(G.subs(sv),25)); Gcv = float(sp.N(Gc.subs(sv),25)); Gxv = float(sp.N(Gx.subs(sv),25)); uv = float(sp.N(u.subs(sv),25))
    xv, cv, qvf = float(Av), float(tv/Av), float(qv)
    r0 = (float(fG0(xv,cv,qvf)), float(fGx0(xv,cv,qvf)), float(fGc0(xv,cv,qvf)), float(fu0(xv,cv,qvf)))
    for a,b in zip((Gv,Gxv,Gcv,uv), r0):
        maxerr = max(maxerr, abs(a-b))
    print('g=%.4f q=%.3f  atom=(%.6f,%.6f,%.6f,%.6f) orig=(%.6f,%.6f,%.6f,%.6f)' % (gv,qv,Gv,Gxv,Gcv,uv,*r0))
print('max abs err:', maxerr)

import pickle
data = dict(G=G,Gc=Gc,Gx=Gx,u=u,P=P,GxP3c=GxP3c,den_extra=den_extra,NumJ=NumJ)
with open('misc/t3_symbols5.pkl','wb') as fh: pickle.dump(data, fh)
print('saved misc/t3_symbols5.pkl; NumJ terms:', len(sp.Add.make_args(NumJ)))
