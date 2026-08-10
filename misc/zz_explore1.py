import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
NJ2 = sp.expand(NJ2)
# individual monomial ranges
def NJ_parts(g, q):
    A_ = mp.pi-g; t_ = mp.atan(q*mp.tan(g))
    sg_, cg_, st_, ct_ = mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_)
    return A_, t_, sg_, cg_, st_, ct_
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 150
Ti = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['T1','T2','T3','T4','T5','T6','T7','T8','W']}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A_ = mp.pi-g; sg_, cg_ = mp.sin(g), mp.cos(g)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t_ = mp.atan(q*mp.tan(g))
        st_, ct_ = mp.sin(t_), mp.cos(t_)
        B1 = A_*cg_-2*sg_; B2 = 4*A_**2*cg_**2-A_**2-12*A_*cg_*sg_+6*sg_**2
        B4 = 7*A_*cg_**2-A_*sg_**2-4*cg_*sg_; B5 = A_**2*cg_**2-A_**2*sg_**2+2*A_**2+12*A_*cg_*sg_-12*sg_**2
        B7 = 3*A_*cg_**2+A_*sg_**2+8*cg_*sg_
        vals = {
          'T1': -2*A_**3*B1*st_**2*ct_**4,
          'T2': A_**2*cg_*B2*st_**2*ct_**2,
          'T3': -2*A_**3*sg_*t_*st_*ct_**5,
          'T4': A_**2*sg_*t_*B4*st_*ct_**3,
          'T5': -A_*cg_**2*sg_*t_*B5*st_*ct_,
          'T6': 4*A_**2*cg_*sg_**2*t_**2*ct_**4,
          'T7': -A_*cg_*sg_**2*t_**2*B7*ct_**2,
          'T8': 6*cg_**3*sg_**4*t_**2,
        }
        vals['W'] = sum(vals[k] for k in ['T1','T2','T3','T4','T5','T6','T7','T8'])
        for k, v in vals.items():
            if v < Ti[k][0]: Ti[k][0] = v
            if v > Ti[k][1]: Ti[k][1] = v
for k in ['T1','T2','T3','T4','T5','T6','T7','T8','W']:
    print('%s: [%.5f, %.5f]' % (k, Ti[k][0], Ti[k][1]))
