# -*- coding: utf-8 -*-
"""t3_b2verify2: fixed."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dNJ2dt = sp.expand(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct))
f = sp.lambdify((A,t,sg,cg,st,ct), dNJ2dt, 'numpy')
def direct(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    return float(f(Av, tv, math.sin(gv), math.cos(gv), math.sin(tv), math.cos(tv)))
def viaB2(Av, cv):
    tv = cv*Av; gv = math.pi-Av
    sgg = math.sin(gv); cgg = math.cos(gv); wv = math.cos(tv)**2
    G0 = (2*Av**3*cgg**4*wv - Av**3*cgg**4 - 2*Av**3*cgg**2*sgg**2*wv + Av**3*cgg**2*sgg**2 - 28*Av**3*cgg**2*wv**2 + 25*Av**3*cgg**2*wv - 2*Av**3*cgg**2
          + 4*Av**3*sgg**2*wv**2 - 3*Av**3*sgg**2*wv + 12*Av**3*wv**3 - 10*Av**3*wv**2 - 2*Av**2*cgg**5*sgg - 2*Av**2*cgg**3*sgg**3
          + 30*Av**2*cgg**3*sgg*wv - 10*Av**2*cgg**3*sgg + 2*Av**2*cgg*sgg**3*wv + 8*Av**2*cgg*sgg*wv**2 - 12*Av**2*cgg*sgg*wv
          - 8*Av*cgg**2*sgg**2*wv + 12*Av*cgg**2*sgg**2 - 12*cgg**3*sgg**3)
    G1 = (-8*Av**3*cgg**2 + 2*Av**3 - Av**2*cgg**3*sgg + Av**2*cgg*sgg**3 + 22*Av**2*cgg*sgg + 6*Av*cgg**2*sgg**2*tv**2 - 12*Av*cgg**2*sgg**2
          + 2*Av*sgg**4*tv**2 - 12*Av*sgg**2 + 16*cgg*sgg**3*tv**2 + 12*cgg*sgg**3)
    F = (-16*Av**2*cgg**3 + 12*Av**2*cgg*wv - 4*Av**2*cgg + 41*Av*cgg**2*sgg + Av*sgg**3 - 22*Av*sgg*wv + 16*Av*sgg + 16*cgg*sgg**2*tv**2 - 20*cgg*sgg**2)
    B2 = -sgg*tv*G0 + Av*math.sqrt(wv*(1-wv))*(cgg*G1 - Av*wv*F)
    return 32*Av**2*cgg*B2
for Av, cv in [(2*math.pi/3, 0.5), (2.3, 0.42), (math.pi-0.655, 0.5), (2.244, 0.4), (2.4866, 0.4365)]:
    print(f'A={Av:.4f} c={cv:.4f}: direct={direct(Av,cv):.4f} viaB2={viaB2(Av,cv):.4f}')
