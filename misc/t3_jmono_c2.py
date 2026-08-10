# -*- coding: utf-8 -*-
"""t3_jmono_c2: monotonicity of J2_2d in c via lambdify (fast)."""
import sympy as sp, math, numpy as np, pickle

with open('misc/t3_poly.pkl','rb') as fh: d = pickle.load(fh)
G, Gc, Gx, u, P = d['G'], d['Gc'], d['Gx'], d['u'], d['P']
A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
J2 = G**2 + Gc - u*Gx
fJ = sp.lambdify((A,t,sg,cg,st,ct), J2, 'numpy')
def Jvec(Av, cv):
    tv = cv*Av
    return fJ(Av, tv, np.sin(Av), -np.cos(Av), np.sin(tv), np.cos(tv))
Amin, Amax = 2*math.pi/3, math.pi-0.655
NA, Nc = 400, 300
Avs = np.linspace(Amin, Amax, NA+1); cvs = np.linspace(0.4, 0.5, Nc+1)
AA, CC = np.meshgrid(Avs, cvs, indexing='ij')
mask = AA*(1+CC) >= math.pi - 1e-12
JJ = Jvec(AA, CC)
print('J2_2d on relaxed region: [%.4f, %.4f]' % (JJ[mask].min(), JJ[mask].max()))
# slope in c via finite diff
dc = 1e-6
s = (Jvec(AA, CC+dc) - Jvec(AA, CC-dc))/(2*dc)
print('dJ2_2d/dc on relaxed: [%.4f, %.4f]' % (s[mask].min(), s[mask].max()))
# where is max
i = np.unravel_index(np.argmax(JJ), JJ.shape)
print('max at A=%.4f c=%.4f (g=%.4f)' % (AA[i], CC[i], math.pi-AA[i]))
