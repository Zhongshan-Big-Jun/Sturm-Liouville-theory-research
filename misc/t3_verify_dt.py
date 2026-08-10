# -*- coding: utf-8 -*-
"""t3_verify_dt: verify dNJ/dt decomposition vs direct evaluation."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJdt = sp.expand(sp.diff(NJ, t) + ct*sp.diff(NJ, st) - st*sp.diff(NJ, ct))
dNJdt_l = sp.lambdify((A,t,sg,cg,st,ct), dNJdt, 'numpy')

def ev_dt(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    return float(dNJdt_l(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))
def ev_dt_fd(Av, cv, h=1e-6):
    def nj(cc):
        tv = cc*Av; gv = math.pi-Av
        sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
        return float(NJ.subs(sv).evalf(25))
    return (nj(cv+h)-nj(cv-h))/(2*h) / Av   # dNJ/dc = A*dNJ/dt
for Av, cv in [(2.1,0.45),(2.3,0.42),(2.45,0.48),(2*math.pi/3,0.5),(math.pi-0.655,0.4365)]:
    d1 = ev_dt(Av,cv); d2 = ev_dt_fd(Av,cv)
    print(f'A={Av:.4f} c={cv:.4f}: dNJ/dt(sympy)={d1:+.6f}  dNJ/dc/A(fd)={d2:+.6f}')
