# -*- coding: utf-8 -*-
"""verify_algebra_sym.py -- symbolic verification of the core identities.
1. IN = G2 * POS with POS = D^2 A (q^2+u^2) u / (Phi q)   [derived from G2 on the odd curve]
2. M2 = dIN/du and dM2/dq formulas
3. C4: on the curve (c = 0.4, A = 2.5v, t = v): IN = A * K(v)
"""
import sympy as sp
q, u = sp.symbols('q u', positive=True)
A = sp.pi - sp.atan(u/q)
t = sp.atan(u)
IN = (q**2+u**2)*A*(2*A*q - 3*u + 2*t) - 3*t*u*q*(1+u**2)
print('=== 1. IN = G2 * POS ===')
# G2 on the odd curve in (q,u) coords: A = pi - arctan(u/q), c = t/A, Phi = q^2(1+u^2)/(q^2+u^2)
Ph = q**2*(1+u**2)/(q**2+u**2)
c = t/A
D = q + c*Ph
# G2 = -Ph*W/D + 2*c*A*Ph*(q^2-1)*sinA*cosA/D^2,  sinA = sin(pi-gamma) = u/sqrt(q^2+u^2)... use tan gamma = u/q
# sin(gamma) = u/sqrt(q^2+u^2), cos(gamma) = q/sqrt(q^2+u^2); sinA = sin gamma, cosA = -cos gamma
sg = u/sp.sqrt(q**2+u**2)
cg = q/sp.sqrt(q**2+u**2)
sA, cA = sg, -cg
W = 3 + 2*A*(cA/sA)
G2 = -Ph*W/D + 2*c*A*Ph*(q**2-1)*sA*cA/D**2
POS = D**2*A*(q**2+u**2)*u/(Ph*q)
diff = sp.simplify(IN - G2*POS)
print('  diff(IN - G2*POS) =', sp.simplify(diff))
print('=== 2. dIN/du and dM2/dq ===')
M2 = sp.diff(IN, u)
M2_claimed = 4*A**2*u*q - 7*A*q**2 - 9*A*u**2 + 2*A*(q**2+u**2)/(1+u**2) + t*(4*A*u - 5*q - 9*q*u**2)
print('  diff(M2 - claimed):', sp.simplify(M2 - M2_claimed))
dM2dq = sp.diff(M2_claimed, q)
S = q**2+u**2
dM2dq_claimed = (4*A**2*u + 8*A*u**2*q/S - 7*q**2*u/S - 14*A*q - 9*u**3/S
                 + 2*u/(1+u**2) + 4*A*q/(1+u**2) + t*(4*u**2/S - 5 - 9*u**2))
print('  diff(dM2/dq - claimed):', sp.simplify(dM2dq - dM2dq_claimed))
print('  M2(1,u) - pi*(4u(pi-atan u) - 5 - 9u^2):', sp.simplify(M2_claimed.subs(q,1) - sp.pi*(4*u*(sp.pi - sp.atan(u)) - 5 - 9*u**2)))
print('=== 3. C4: IN = A*K(v) on the curve ===')
v = sp.symbols('v', positive=True)
w = sp.pi - sp.Rational(5,2)*v
q_c = sp.sin(v)*sp.cos(w)/(sp.cos(v)*sp.sin(w))
u_c = sp.tan(v)
IN_curve = IN.subs({q: q_c, u: u_c}).subs(sp.atan(u_c), v)  # t = v on the curve
A_c = sp.Rational(5,2)*v
K = (q_c**2+u_c**2)*(5*v*q_c - 3*u_c + 2*v) - sp.Rational(6,5)*u_c*q_c*(1+u_c**2)
print('  diff(IN_curve - A*K):', sp.trigsimp(sp.simplify(IN_curve - A_c*K)))
