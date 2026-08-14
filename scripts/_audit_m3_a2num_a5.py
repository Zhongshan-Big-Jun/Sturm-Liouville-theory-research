# -*- coding: utf-8 -*-
"""Independent audit A2-numeric + A5:
Numerically validate the P dict (E1/E2/E5/E6) against the exact closed.py
expressions at several random symbolic-parameter points (u small), and
verify the big.json last-row mapping and the STRICT observable formulas.
"""
import pickle, json, random
import numpy as np
import math
import sympy as sp
from sympy import pi

u = sp.symbols('u', positive=True)
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

# Use closed.py's exact system (imported fresh) to evaluate E1,E2,E5,E6
import sys
sys.path.insert(0, r'scripts')
import _gapn2_largeR_closed as cl

def eval_P0_dict(name, K, A, B, C, uv, nmax=10):
    val = 0.0
    for m in range(0, nmax + 1):
        key = (name, m)
        if key in P0:
            val += float(P0[key].subs({sp.Symbol('K'): K, sp.Symbol('A'): A,
                                       sp.Symbol('B'): B, sp.Symbol('C'): C})) * uv**m
    return val

print('=== A2-numeric: series dict vs exact closed system at sample points ===')
random.seed(20260814)
mxerr = {n: 0.0 for n in ['E1', 'E2', 'E5', 'E6']}
for trial in range(8):
    K = 3.0 + random.random()*2.0
    A = 0.3 + random.random()*0.6
    B = 0.1 + random.random()*0.4
    C = random.random()*3.0
    uv = 0.02 + random.random()*0.12
    eps = uv**3
    k2 = K*uv
    k3 = K*uv + C*uv**5
    p1 = float(math.pi/2 + A*uv**2)
    p3 = float(math.pi/4 + B*uv**2)
    z = np.array([k2, k3, p1, p3])
    f = cl.system(z, eps)  # numeric E1,E2,E5,E6
    for i, nm in enumerate(['E1', 'E2', 'E5', 'E6']):
        s = eval_P0_dict(nm, K, A, B, C, uv)
        err = abs(s - f[i])
        mxerr[nm] = max(mxerr[nm], err)
for n in ['E1', 'E2', 'E5', 'E6']:
    print('  max |series - exact closed| over 8 sample points for %s = %.3e' % (n, mxerr[n]))

print()
print('=== A5: big.json last row ===')
data = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
last = data[-1]
R, uu, K, a, b = last[0], last[1], last[2], last[3], last[4]
Dk_u7 = last[5]
DR = last[6]
print('last row fields: R=%.8f u=%.12f K=%.8f a=%.8f b=%.8f Dk/u^7=%.8f D*R=%.8f extra=%.8f'
      % (last[0], last[1], last[2], last[3], last[4], last[5], last[6], last[7]))

# manager anchor: u == R^{-1/6}
u_anchor = R**(-1/6)
print('u = R^{-1/6}?  R^{-1/6}=%.12f  data u=%.12f  diff=%.2e' % (u_anchor, uu, abs(uu - u_anchor)))

# Dk/u^5 = c(u); from last row, c ~ (Dk/u^7)*u^2
c_from_Dk = (Dk_u7)*uu*uu
print('c(u) from Dk/u^7 * u^2 = %.8f  (limit c0=1.4741 EVIDENCE)' % c_from_Dk)

# STRICT relation D*R = 2 K c + c^2 u^4  (use data K and c_from_Dk)
DR_check = 2*K*c_from_Dk + c_from_Dk**2*uu**4
print('2*K*c + c^2*u^4 = %.8f  vs data D*R = %.8f  (diff %.2e)'
      % (DR_check, DR, abs(DR_check - DR)))

# Dk/u^5 = c(u): from data, Dk/u^5 = (Dk/u^7)*u^2
print('Dk/u^5 = %.8f' % c_from_Dk)

# a0*K0=2 check with EVIDENCE limits K0=3.4553, a0=0.5788
K0f = 3.4553
a0f = 0.5788
print('EVIDENCE fit: a0*K0 = %.6f  (should be 2; diff %.2e)' % (a0f*K0f, abs(a0f*K0f - 2)))
print('a0 = 2/K0 = %.6f  vs fit a0=0.5788 = %.6f' % (2/K0f, a0f))

# D*R limit 2*K0*C0 with C0=1.4741
C0f = 1.4741
print('2*K0*C0 = %.6f  (deliverable claim 10.18692)' % (2*K0f*C0f))

# consistency candidate C = 1 + b0*K0/2 + 3*pi/(2*K0) - K0^2/12 at even-only seed
B0f = 0.2898
import math
Cchk = 1 + B0f*K0f/2 + 3*math.pi/(2*K0f) - K0f**2/12
print('consistency candidate at even-only seed = %.6f  (deliverable 1.86956)' % Cchk)

# hard constant E5_5 = K0^3/2
print('K0^3/2 = %.6f  (deliverable: ~20.63 at K0=3.46)' % (K0f**3/2))
print('K0^3/2 at K0=3.46 = %.6f' % (3.46**3/2))
