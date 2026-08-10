# _audit_sub_C_j2dec_full.py — full symbolic verification of lem:j2dec and lem:j2bounds algebra
import sympy as sp
import time

# Primitives: gamma with sg=sin g, cg=cos g; t with st=sin t, ct=cos t
A, sg, cg, st, ct, t = sp.symbols('A sg cg st ct t', positive=True)
q = sp.Symbol('q', positive=True)
# constraints: sg^2+cg^2=1, st^2+ct^2=1, q = st*cg/(ct*sg)  (tan t = q tan g)
# We work with rational functions and reduce modulo these three relations.

def reduce_poly(p, sg, cg, st, ct):
    # reduce p modulo sg^2+cg^2-1 and st^2+ct^2-1
    p = sp.expand(p)
    p = sp.rem(p, sg**2 + cg**2 - 1, sg)
    p = sp.rem(p, st**2 + ct**2 - 1, st)
    return sp.expand(p)

Phi = cg**2 + q**2*sg**2
D = q + (t/A)*Phi   # c = t/A
x = sp.pi - A       # x = pi - gamma  (symbolic pi, A = pi - gamma)

def G_expr(x, c, q):
    Phi_x = sp.cos(x)**2 + q**2*sp.sin(x)**2
    D_x = q + c*Phi_x
    G = -Phi_x*(3 + 2*x*sp.cot(x))/D_x + 2*c*x*Phi_x*(q**2-1)*sp.sin(x)*sp.cos(x)/D_x**2
    return G

# Build J = G^2 + G_c - u G_x with u = x Phi/D, all at (x,c)
x_s, c_s = sp.symbols('xs cs', positive=True)
Phi_s = sp.cos(x_s)**2 + q**2*sp.sin(x_s)**2
D_s = q + c_s*Phi_s
G_s = -Phi_s*(3 + 2*x_s*sp.cot(x_s))/D_s + 2*c_s*x_s*Phi_s*(q**2-1)*sp.sin(x_s)*sp.cos(x_s)/D_s**2
G_c = sp.diff(G_s, c_s)
G_x = sp.diff(G_s, x_s)
u_s = x_s*Phi_s/D_s
J_s = sp.simplify(G_s**2 + G_c - u_s*G_x)
print('J symbolic built')

# substitute x_s = pi - A, c_s = t/A; then replace trig(pi-A) etc.
J2 = J_s.subs({x_s: sp.pi - A, c_s: t/A})
J2 = sp.simplify(J2)
print('J2 substituted')

# now replace q by st*cg/(ct*sg); replace sin/cos of (pi-A) and of t
J2 = J2.subs(q, st*cg/(ct*sg))
J2 = sp.simplify(J2)
print('q substituted')

# W terms (eq:wterms) with B1..B7, G5
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
Mf = 2*A**2*cg**2 - A**2 - 8*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = sp.expand(B5 - A*B4)
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
claim = 2*A**2*cg*W/Delta**4   # J2^(2) = N/(16 Delta^4), N=32 A^2 cg W

# difference J2 - claim; reduce to common denominator and check numerator reduces to 0
diff = sp.simplify(J2 - claim)
print('diff simplified, size:', sp.count_ops(diff))
num, den = sp.fraction(sp.together(diff))
num = sp.expand(num)
print('num degree in A:', sp.degree(num, A), 'in sg:', sp.degree(num, sg), 'in st:', sp.degree(num, st))
# reduce modulo the three relations
num = sp.rem(num, sg**2 + cg**2 - 1, sg)
num = sp.rem(num, st**2 + ct**2 - 1, st)
num = sp.expand(num)
print('after reduction num ops:', sp.count_ops(num))
print('NUM IS ZERO:', num == 0)
