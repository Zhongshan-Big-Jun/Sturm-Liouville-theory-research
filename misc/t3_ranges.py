# -*- coding: utf-8 -*-
"""t3_ranges: precise E3 ranges on T2 + composed derivative signs (cross-check only)."""
import numpy as np

# load atom forms
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
 'dG_dq': dG_dt,
 'dG_dg': dG_dg + dG_dt*st*ct/(sg*cg),
 'dGc_dq': dGc_dt,
 'dGc_dg': dGc_dg + dGc_dt*st*ct/(sg*cg),
 'dGx_dq': dGx_dt,
 'dGx_dg': dGx_dg + dGx_dt*st*ct/(sg*cg),
}
fl = {}
for k in ['G','Gc','Gx','u']:
    fl[k] = sp.lambdify((A,t,sg,cg,st,ct), eval(k), 'numpy')
for k,v in comp.items():
    fl[k] = sp.lambdify((A,t,sg,cg,st,ct), v, 'numpy')

Ng, Nq = 400, 340
gv = np.linspace(0.655, 1.0472, Ng+1); qv = np.linspace(1.0, 2.0, Nq+1)
GG, QQ = np.meshgrid(gv, qv, indexing='ij')
AA = np.pi - GG
TT = np.arctan(QQ*np.tan(GG))
cc = TT/AA
mask = (cc > 0.4) & (cc < 0.5)
S = dict(A=AA[mask], t=TT[mask], sg=np.sin(GG[mask]), cg=np.cos(GG[mask]), st=np.sin(TT[mask]), ct=np.cos(TT[mask]))
print('T2 grid points:', mask.sum())

ranges = {}
for k in ['G','Gc','Gx','u']:
    v = fl[k](**S)
    ranges[k] = (v.min(), v.max())
    i = np.argmax(v); gi = GG[mask][i]
    print('%-4s in [%8.4f, %8.4f]  max at g=%.4f q=%.4f' % (k, v.min(), v.max(), GG[mask][i], QQ[mask][i]))
v = fl['G']**2 + fl['Gc']**2*0  # G^2
ranges['G2'] = (v.min(), v.max())
print('G^2 in [%.4f, %.4f]' % (v.min(), v.max()))
v = fl['u']*fl['Gx']
print('uGx in [%.4f, %.4f]' % (v.min(), v.max()))
v = fl['G']**2 + fl['Gc']
print('G^2+Gc in [%.4f, %.4f]' % (v.min(), v.max()))
v = fl['G']**2 + fl['Gc'] - fl['u']*fl['Gx']
print('J2_2d in [%.4f, %.4f]' % (v.min(), v.max()))

print('--- composed derivative signs ---')
for k in ['dG_dq','dG_dg','dGc_dq','dGc_dg','dGx_dq','dGx_dg']:
    v = fl[k](**S)
    print('%-8s: min=%.5f max=%.5f' % (k, v.min(), v.max()))

# check the u>=4pi/9 lemma ingredients
r = np.sin(2*S['t'])/np.sin(2*S['g'])
print('r = sin2t/sin2g: min=%.4f max=%.4f' % (r.min(), r.max()))
print('t+g: min=%.4f (pi/2=%.4f)' % ((S['t']+S['g']).min(), np.pi/2))
print('c = t/A: min=%.4f max=%.4f ; A: min=%.4f max=%.4f' % (S['t']/S['A']*0+ (S['t']/S['A']).min(), (S['t']/S['A']).max(), S['A'].min(), S['A'].max()))
print('u vs 4pi/9=%.6f : u min=%.6f' % (4*np.pi/9, fl['u'](**S).min()))
