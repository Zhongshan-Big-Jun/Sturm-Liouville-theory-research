# _audit_sub_A2_symbolic.py — part 2: J1 decomposition, q=1 formulas, lem:j2dec algebra, j2bounds algebra
import sympy as sp
from mpmath import mp, mpf, sin, cos, tan, atan, cot, sqrt, pi as mppi

pi = sp.pi
xx, c = sp.symbols('xx c', positive=True)
q = sp.symbols('q', positive=True)

def Phi(qq, x): return sp.cos(x)**2 + qq**2*sp.sin(x)**2
def Gfunc(x, qq, cc):
    P = Phi(qq, x); D = qq + cc*P
    return -P*(3+2*x*sp.cot(x))/D + 2*cc*x*P*(qq**2-1)*sp.sin(x)*sp.cos(x)/D**2

res = []
def check(name, ok):
    res.append((name, bool(ok)))
    print(("PASS" if ok else "FAIL"), name)

# --- J1 decomposition: J = G^2 + G_c - u G_x on curve c=c1(x,q) ---
x1, q1 = sp.symbols('x1 q1', positive=True)
c1v = sp.atan(1/(q1*sp.tan(x1)))/x1
D1 = q1 + c1v*Phi(q1, x1)
Gv = Gfunc(x1, q1, c1v)
G_c_p = sp.diff(Gfunc(x1, q1, c), c).subs(c, c1v)
G_x_p = sp.diff(Gfunc(xx, q1, c1v), xx).subs(xx, x1)
alp_p = -x1*Phi(q1, x1)/D1
J1 = sp.simplify(Gv**2 + G_c_p + G_x_p*alp_p)
check("J1 = G^2 + G_c + G_x*alpha'", sp.simplify(J1 - (Gv**2 + G_c_p + G_x_p*alp_p)) == 0)

# --- q=1 formulas ---
xq1 = sp.symbols('xq1', positive=True)
c1_1 = (pi/2 - xq1)/xq1
Gv1 = Gfunc(xq1, 1, c1_1)
D1_1 = 1 + c1_1
Gc1 = sp.diff(Gfunc(xq1, 1, c), c).subs(c, c1_1)
Gx1 = sp.diff(Gfunc(xx, 1, c1_1), xx).subs(xx, xq1)
alp1 = -xq1/D1_1
J1q1b = sp.simplify(Gv1**2 + Gc1 + Gx1*alp1)
Nq1 = 12 + 16*xq1*sp.cot(xq1) + 2*xq1**2*sp.cot(xq1)**2 - 2*xq1**2
check("J1(x,1) = (2x/pi)^2 N(x)", sp.simplify(J1q1b - (2*xq1/pi)**2*Nq1) == 0)

g1 = sp.symbols('g1', positive=True)
x2v = pi - g1
c2_1 = g1/(pi-g1)
Gv2 = Gfunc(x2v, 1, c2_1)
D2_1 = 1 + c2_1
Gc2 = sp.diff(Gfunc(x2v, 1, c), c).subs(c, c2_1)
Gx2 = sp.diff(Gfunc(xx, 1, c2_1), xx).subs(xx, x2v)
alp2 = -x2v/D2_1
J2q1 = sp.simplify(Gv2**2 + Gc2 + Gx2*alp2)
zq = -x2v*sp.cot(x2v)
N2q1 = 2*(zq**2 - 8*zq + 6) - 2*x2v**2
check("J2(gamma,1) = x^2 N(x)/pi^2", sp.simplify(J2q1 - x2v**2*N2q1/pi**2) == 0)

# --- lem:j2dec: W decomposition identities (symbolic, modulo Pythagorean relations) ---
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct', positive=True)
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
M = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.simplify(B5 - A*B4)
check("M = B2 - 2 A cg B1", sp.simplify(M - (B2 - 2*A*cg*B1)) == 0)
check("G5 = B5 - A B4", sp.simplify(G5 - (B5 - A*B4)) == 0)

W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
W3 = -2*A**3*sg*t*st*ct**5
W4 = A**2*sg*t*B4*st*ct**3
W5 = -A*cg**2*sg*t*B5*st*ct
W6 = 4*A**2*cg*sg**2*t**2*ct**4
W7 = -A*cg*sg**2*t**2*B7*ct**2
W8 = 6*cg**3*sg**4*t**2
W = W1+W2+W3+W4+W5+W6+W7+W8
# W12 identity
z = sp.symbols('z', positive=True)
W12 = sp.simplify((W1+W2).subs(ct**2, z).subs(st**2, 1-z))
check("W1+W2 = z(1-z)(A^2 cg B2 - 2A^3 B1 z)", sp.simplify(W12 - z*(1-z)*(A**2*cg*B2 - 2*A**3*B1*z)) == 0)
# W6+W7+W8 = t^2 cg sg^2 Q(z), Q(z)=4A^2 z^2 - A B7 z + 6 cg^2 sg^2
Qz = 4*A**2*z**2 - A*B7*z + 6*cg**2*sg**2
W678 = sp.simplify((W6+W7+W8).subs(ct**2, z).subs(st**2, 1-z))
check("W6+W7+W8 = t^2 cg sg^2 Q(z)", sp.simplify(W678 - t**2*cg*sg**2*Qz) == 0)
# W4+W5 with B5 = G5 + A B4
W45 = sp.simplify(W4+W5)
check("W4+W5 = A sg t st ct (A B4(ct^2-cg^2) - cg^2 G5)",
      sp.simplify(W45 - A*sg*t*st*ct*(A*B4*(ct**2-cg**2) - cg**2*G5)) == 0)

# --- J2 = N/(16 Delta^4) numeric identity (high precision) ---
mp.dps = 50
def G_mp(xx, qq, cc):
    P = cos(xx)**2 + qq**2*sin(xx)**2
    D = qq + cc*P
    return -P*(3+2*xx*cot(xx))/D + 2*cc*xx*P*(qq**2-1)*sin(xx)*cos(xx)/D**2
def J_mp(xx, qq, cc):
    h = mpf('1e-18')
    G = G_mp(xx, qq, cc)
    G_c = (G_mp(xx, qq, cc+h) - G_mp(xx, qq, cc-h))/(2*h)
    G_x = (G_mp(xx+h, qq, cc) - G_mp(xx-h, qq, cc))/(2*h)
    P = cos(xx)**2 + qq**2*sin(xx)**2
    D = qq + cc*P
    return G**2 + G_c - xx*P/D*G_x
def W8(gamma, qq):
    sg = sin(gamma); cg = cos(gamma)
    t = atan(qq*tan(gamma))
    st = sin(t); ct = cos(t)
    A = mppi - gamma
    D = sqrt(1+3*sg**2)
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
    return 32*A**2*cg*W/(16*Delta**4)
ok = True
import random
random.seed(7)
for _ in range(12):
    gamma = mpf(random.uniform(0.655, 1.0472))
    qq = mpf(random.uniform(1.0, 2.0))
    c2v = atan(qq*tan(gamma))/(mppi-gamma)
    Jv = J_mp(mppi-gamma, qq, c2v)
    Wv = W8(gamma, qq)
    if abs(Jv - Wv) > mpf('1e-28'):
        ok = False
        print("  J2 mismatch", gamma, qq, abs(Jv-Wv))
check("lem:j2dec J2 = N/(16 Delta^4) (12 random points)", ok)

# also verify N is polynomial: expand W in terms of A,t,sg,cg,st,ct with Pythagorean reduction
Ws = sp.expand(W)
Ws2 = sp.factor(sp.simplify(Ws.subs(st**2, 1-ct**2)))
print("W reduced terms count:", len(sp.Poly(Ws2, A, t, sg, cg, ct).terms()))

fails = [r for r in res if not r[1]]
print()
print("PART2: %d checks, %d failed" % (len(res), len(fails)))
for f in fails: print("  FAIL:", f[0])
