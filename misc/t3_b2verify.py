# -*- coding: utf-8 -*-
"""t3_b2verify: verify B2 decomposition vs direct dNJ2/dt."""
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
    t = cv*Av; g = math.pi-Av
    sg = math.sin(g); cg = math.cos(g); w = math.cos(t)**2
    G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
          + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
          + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
          - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
    G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
          + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
    F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
    B2 = -sg*t*G0 + A*math.sqrt(w*(1-w))*(cg*G1 - A*w*F)
    return 32*A**2*cg*B2
for Av, cv in [(2*math.pi/3, 0.5), (2.3, 0.42), (math.pi-0.655, 0.5), (2.244, 0.4), (2.4866, 0.4365)]:
    print(f'A={Av:.4f} c={cv:.4f}: direct={direct(Av,cv):.4f} viaB2={viaB2(Av,cv):.4f}')
