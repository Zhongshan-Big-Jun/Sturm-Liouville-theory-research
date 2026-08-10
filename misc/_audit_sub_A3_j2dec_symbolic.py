# _audit_sub_A3_j2dec_symbolic.py — full symbolic verification of lem:j2dec identity
import sympy as sp
from sympy import sin, cos, atan, cot, pi, sqrt, simplify, expand, Rational, symbols, tan
import time

gamma, t = symbols('gamma t', positive=True)
A = pi - gamma
sg, cg, st, ct = symbols('sg cg st ct', positive=True)
# q = tan t / tan gamma = st*cg/(ct*sg)
q_expr = st*cg/(ct*sg)
c_expr = t/A
x = pi - gamma

def Phi(qq, xx): return cos(xx)**2 + qq**2*sin(xx)**2
def G_expr(xx, qq, cc):
    P = Phi(qq, xx); D = qq + cc*P
    return -P*(3+2*xx*cot(xx))/D + 2*cc*xx*P*(qq**2-1)*sin(xx)*cos(xx)/D**2

# Work with gamma and t directly; replace sin(gamma)->sg, cos(gamma)->cg, sin(t)->st, cos(t)->ct at the END,
# but derivatives need the functional forms first. Strategy: build G as function of (gamma,t), take partials
# w.r.t. c and x treating q as constant (partial derivatives at fixed q!), i.e. G_c = dG/dc |_{q,x fixed},
# G_x = dG/dx |_{q,c fixed}. Then substitute along the curve.
# To do this cleanly we compute G_c, G_x as functions of (x, q, c) first.
xx, qq, cc = symbols('xx qq cc', positive=True)
G = G_expr(xx, qq, cc)
G_c = sp.diff(G, cc)
G_x = sp.diff(G, xx)
J = G**2 + G_c - xx*Phi(qq, xx)/(qq+cc*Phi(qq, xx))*G_x

# Now substitute the curve: x = pi-gamma, q = q_expr, c = t/A, then gamma via sg/cg and t via st/ct.
# We substitute AFTER, using trig identities: sin(gamma)=sg, cos(gamma)=cg, sin(t)=st, cos(t)=ct.
subs1 = {xx: pi-gamma, qq: q_expr, cc: t/A}
Jc = J.subs(subs1)
# replace sin(gamma), cos(gamma), sin(t), cos(t), tan
Jc = Jc.subs({sin(gamma): sg, cos(gamma): cg, tan(gamma): sg/cg, sin(t): st, cos(t): ct, tan(t): st/ct})
Jc = sp.factor(sp.trigsimp(Jc))
print("Jc simplified (preliminary)")

# reduce mod sg^2+cg^2-1, st^2+ct^2-1 using a groebner-ish substitution
Jc2 = sp.simplify(Jc)
# Now the claimed RHS:
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = B5 - A*B4
W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
W3 = -2*A**3*sg*t*st*ct**5
W4 = A**2*sg*t*B4*st*ct**3
W5 = -A*cg**2*sg*t*B5*st*ct
W6 = 4*A**2*cg*sg**2*t**2*ct**4
W7 = -A*cg*sg**2*t**2*B7*ct**2
W8 = 6*cg**3*sg**4*t**2
W = W1+W2+W3+W4+W5+W6+W7+W8
Delta = A*st*ct + t*sg*cg
RHS = 32*A**2*cg*W/(16*Delta**4)
RHS = sp.factor(sp.trigsimp(RHS))
diff = sp.simplify(Jc2 - RHS)
# force Pythagorean relations: substitute sg^2 = 1-cg^2, st^2 = 1-ct^2 repeatedly
def reduce_pyth(e):
    e2 = e
    for _ in range(6):
        e2 = sp.simplify(e2.subs(sg**2, 1-cg**2))
        e2 = sp.simplify(e2.subs(st**2, 1-ct**2))
    return sp.simplify(e2)
d1 = reduce_pyth(diff)
print("diff after pyth reduction:", sp.N(d1, 20) if d1 != 0 else 0)
print("SYMBOLIC J2=N/(16D^4):", d1 == 0)
