# -*- coding: utf-8 -*-
"""t3_signs: verify composed derivative signs + extremum locations on T2."""
import sympy as sp, numpy as np

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
G  = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/D3
den_extra = cg**3*sg**3*ct**6
GxP3c = sum(sp.expand(tt*P**3*den_extra) for tt in [t1,t2,t3,t4])
Gx = GxP3c/(P**3*den_extra)

def d_dt(f): return sp.diff(f, t) + ct*sp.diff(f, st) - st*sp.diff(f, ct)
def d_dg(f): return -sp.diff(f, A) + cg*sp.diff(f, sg) - sg*sp.diff(f, cg)
dG_dt = d_dt(G); dG_dg = d_dg(G); dGc_dt = d_dt(Gc); dGc_dg = d_dg(Gc); dGx_dt = d_dt(Gx); dGx_dg = d_dg(Gx)
comp = {
 'dG_dq': dG_dt, 'dG_dg': dG_dg + dG_dt*st*ct/(sg*cg),
 'dGc_dq': dGc_dt, 'dGc_dg': dGc_dg + dGc_dt*st*ct/(sg*cg),
 'dGx_dq': dGx_dt, 'dGx_dg': dGx_dg + dGx_dt*st*ct/(sg*cg),
}
fl = {}
for k in ['G','Gc','Gx','u'] + list(comp.keys()):
    fl[k] = sp.lambdify((A,t,sg,cg,st,ct), eval(k), 'numpy')

Ng, Nq = 500, 420
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
AA = np.pi - GG; TT = np.arctan(QQ*np.tan(GG)); cc = TT/AA
mask = (cc > 0.4) & (cc < 0.5)
S = dict(A=AA[mask], t=TT[mask], sg=np.sin(GG[mask]), cg=np.cos(GG[mask]), st=np.sin(TT[mask]), ct=np.cos(TT[mask]))
print('T2 pts:', mask.sum())
for k in ['dG_dq','dG_dg','dGc_dq','dGc_dg','dGx_dq','dGx_dg']:
    v = fl[k](**S)
    i = np.argmax(v); j = np.argmin(v)
    print('%-8s: [%9.4f, %9.4f]  (need %s)' % (k, v.min(), v.max(), '<0' if k in ('dG_dq','dG_dg','dGc_dq','dGx_dq','dGx_dg') else '>0'))
# where are the extrema of G, Gc, Gx, u, J
for k in ['G','Gc','Gx','u']:
    v = fl[k](**S)
    i = np.argmax(v); j = np.argmin(v)
    print('%-3s max %9.4f at (g=%.4f,q=%.4f,c=%.4f) ; min %9.4f at (g=%.4f,q=%.4f,c=%.4f)' % (
        k, v.max(), GG[mask][i], QQ[mask][i], TT[mask][i]/AA[mask][i], v.min(), GG[mask][j], QQ[mask][j], TT[mask][j]/AA[mask][j]))
v = fl['u']*fl['Gx']
i = np.argmin(v)
print('uGx min %9.4f at (g=%.4f,q=%.4f)' % (v.min(), GG[mask][i], QQ[mask][i]))
v = fl['G']**2+fl['Gc']
i = np.argmax(v)
print('G2+Gc max %9.4f at (g=%.4f,q=%.4f)' % (v.max(), GG[mask][i], QQ[mask][i]))
v = fl['G']**2+fl['Gc']-fl['u']*fl['Gx']
i = np.argmax(v)
print('J2_2d max %9.4f at (g=%.4f,q=%.4f,c=%.4f)' % (v.max(), GG[mask][i], QQ[mask][i], TT[mask][i]/AA[mask][i]))
