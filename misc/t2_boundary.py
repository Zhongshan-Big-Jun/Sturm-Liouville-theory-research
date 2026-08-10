# -*- coding: utf-8 -*-
"""Max of J2_2d on T2 boundary curves: q=1, q=2, c2=0.4, c2=0.5."""
import numpy as np
import sympy as sp

x, c, q = sp.symbols('x c q', positive=True)
sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)
fJ = sp.lambdify((x,c,q), J, 'numpy')

pi = np.pi
def J2(gv, qv):
    xv = pi - gv; cv = np.arctan(qv*np.tan(gv))/(pi-gv)
    return fJ(xv, cv, qv)

# boundary curves
N = 2000
# q=1: gamma in (gamma(1,2/5), gamma(1,1/2)) = (0.4pi/1.4, pi/3)
gq1 = np.linspace(0.4*pi/1.4, pi/3, N)
J1 = J2(gq1, 1.0)
# q=2: gamma in (gamma(2,2/5), gamma(2,1/2)) ~ (0.65565, 0.841)
# find gamma(2,1/2) numerically: c2(g,2)=0.5
from scipy.optimize import brentq
def c2(gv, qv): return np.arctan(qv*np.tan(gv))/(pi-gv)
ga = brentq(lambda g: c2(g,2)-0.5, 0.8, 0.9)
gb = 0.65565
print('gamma(2,1/2) ~', ga)
gq2 = np.linspace(gb, ga, N)
J2v = J2(gq2, 2.0)
# c2=0.4 curve: param by q in [1,2], gamma solves c2(g,q)=0.4
def g_of_c(qv, cval, lo, hi):
    return brentq(lambda g: c2(g,qv)-cval, lo, hi)
g04 = np.array([g_of_c(qv, 0.4, 0.6, 1.0) for qv in np.linspace(1,2,N)])
J04 = J2(g04, np.linspace(1,2,N))
g05 = np.array([g_of_c(qv, 0.5, 0.8, 1.1) for qv in np.linspace(1,2,N)])
J05 = J2(g05, np.linspace(1,2,N))

for nm, Jv, loc in [('q=1', J1, 'g in [0.8976, pi/3]'), ('q=2', J2v, 'g in [0.65565, 0.841]'),
                    ('c2=0.4', J04, 'q in [1,2]'), ('c2=0.5', J05, 'q in [1,2]')]:
    i = np.argmax(Jv)
    print('%s: max J = %.6f at index %d (%s)' % (nm, Jv[i], i, loc))
    # show values at ends
    print('   J at ends: %.6f ... %.6f' % (Jv[0], Jv[-1]))
