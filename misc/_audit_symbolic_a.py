# -*- coding: utf-8 -*-
"""Independent symbolic audit of SL_gap_n1_O3a_phase_rigidity_proof.tex core identities (session 45)."""
import sympy as sp

x, q, c, m, w, y, z, th, be, bv = sp.symbols('x q c m w y z th be bv', positive=True)
pi = sp.pi
res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)

# ---- A. eq:psi ----
q0 = sp.Symbol('q0', nonnegative=True)
W = 1 + q0*sp.sin(x)**2
Psi = x*sp.cos(x)/sp.sin(x)/W
lhs = sp.expand_trig(sp.simplify(W**2*sp.sin(x)**2*sp.diff(Psi, x)))
rhs = sp.expand_trig(sp.simplify(sp.sin(x)*sp.cos(x) - x + q0*sp.sin(x)**2*(sp.sin(x)*sp.cos(x) - x*(1+2*sp.cos(x)**2))))
check('A1 eq:psi (Psi prime identity)', sp.simplify(lhs - rhs) == 0)
# second bracket sign: bracket = sin x cos x - x(1+2cos^2 x) == -G - 2x cos^2 x with G = x - sin x cos x
G = x - sp.sin(x)*sp.cos(x)
check('A2 bracket = -G - 2x cos^2 x', sp.simplify((sp.sin(x)*sp.cos(x) - x*(1+2*sp.cos(x)**2)) - (-G - 2*x*sp.cos(x)**2)) == 0)

# ---- B. eq:G (log-derivative) ----
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2
D = q + c*Phi
Mf = x**2*sp.sin(x)**2/D
alpha_p = -x*Phi/D
Gx_expr = sp.simplify(sp.diff(Mf, x)/Mf*alpha_p + sp.diff(Mf, c)/Mf)
G_doc = -Phi*(3+2*x*sp.cos(x)/sp.sin(x))/D + 2*c*x*Phi*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2
check('B1 eq:G log-derivative', sp.simplify(sp.expand_trig(Gx_expr - G_doc)) == 0)

# ---- C. IN = G2*POS ; d_w IN = M2 ----
gv = sp.Symbol('gv', positive=True)  # gamma = pi - alpha2
A2 = pi - sp.atan(w/q)
t2 = sp.atan(w)
# c = t2/A2 ; alpha2 = A2 ; gamma = pi - A2
# G2 = G(alpha2; c) with x = alpha2 = A2
Phi2 = sp.cos(A2)**2 + q**2*sp.sin(A2)**2
D2 = q + c*Phi2
G2 = sp.simplify(-Phi2*(3+2*A2*sp.cos(A2)/sp.sin(A2))/D2 + 2*c*A2*Phi2*(q**2-1)*sp.sin(A2)*sp.cos(A2)/D2**2)
G2 = sp.simplify(G2.subs(c, t2/A2))
IN_doc = (q**2 + w**2)*A2*(2*A2*q - 3*w + 2*sp.atan(w)) - 3*w*q*(1+w**2)*sp.atan(w)
POS_doc = sp.simplify((D2**2*A2*(q**2+w**2)*w/(Phi2*q)).subs(c, t2/A2))
check('C1 IN = G2*POS', sp.simplify(sp.expand_trig(IN_doc - G2*POS_doc)) == 0)
M2_doc = 4*A2**2*w*q - 7*A2*q**2 - 9*A2*w**2 + 2*A2*(q**2+w**2)/(1+w**2) + sp.atan(w)*(4*A2*w - 5*q - 9*q*w**2)
check('C2 d_w IN = M2', sp.simplify(sp.expand_trig(sp.diff(IN_doc, w) - M2_doc)) == 0)

# ---- D. lem:B1: g(w) = d_q M2(1,w) ----
A1 = pi - sp.atan(w)   # A at q=1
M2at1 = 4*A1**2*w - 7*A1 - 9*A1*w**2 + 2*A1*(1+w**2)/(1+w**2) + sp.atan(w)*(4*A1*w - 5 - 9*w**2)
M2at1 = sp.simplify(M2at1)
# compare with pi*h(w), h = 4w(pi - atan w) - 5 - 9w^2
h = 4*w*(pi - sp.atan(w)) - 5 - 9*w**2
check('D1 M2(1,w) = pi*h(w)', sp.simplify(sp.expand_trig(M2at1 - pi*h)) == 0)
# g(w) := d_q M2(1,w): differentiate M2 w.r.t. q at q=1
M2gen = 4*A2**2*w*q - 7*A2*q**2 - 9*A2*w**2 + 2*A2*(q**2+w**2)/(1+w**2) + sp.atan(w)*(4*A2*w - 5*q - 9*q*w**2)
g = sp.simplify(sp.diff(M2gen, q).subs(q, 1))
# g'' formula from document
t = sp.atan(w)
gpp_doc = -2*(9*w**6*t + 9*w**5 + 27*w**4*t + 24*w**3 + 19*w**2*t + 20*pi*w**2 + 31*w + t + 4*pi)/(1+w**2)**3
check('D2 g'' formula', sp.simplify(sp.expand_trig(sp.diff(g, w, 2) - gpp_doc)) == 0)
check('D3 g\'(0) = 4 pi^2', sp.simplify(sp.diff(g, w).subs(w, 0) - 4*pi**2) == 0)
# g'(sqrt3) closed form
gps3 = sp.simplify(sp.diff(g, w).subs(w, sp.sqrt(3)))
gps3_doc = sp.simplify(16*pi**2/9 - 41*sp.sqrt(3)*pi/6 - 15)
check('D4 g\'(sqrt3) closed form', sp.simplify(gps3 - gps3_doc) == 0)
# g(4/5), g'(4/5) closed forms
b = sp.Symbol('b')  # b = atan(4/5)
g45 = sp.simplify(g.subs(w, sp.Rational(4,5)))
g45_doc = -19*b/25 - 346*pi/41 + 16*(b-pi)**2/5 - sp.Rational(1076,205)
check('D5 g(4/5) closed form', sp.simplify(sp.expand_trig(g45 - g45_doc.subs(b, sp.atan(sp.Rational(4,5))))) == 0)
gp45 = sp.simplify(sp.diff(g, w).subs(w, sp.Rational(4,5)))
gp45_doc = -2152*b/205 - 2560*pi/1681 + 4*(b-pi)**2 - sp.Rational(15008,1681)
check('D6 g\'(4/5) closed form', sp.simplify(sp.expand_trig(gp45 - gp45_doc.subs(b, sp.atan(sp.Rational(4,5))))) == 0)
# monotonicity in b, pi (use symbol P for pi)
P = sp.Symbol('P', positive=True)
g45_P = -19*b/25 - 346*P/41 + 16*(b-P)**2/5 - sp.Rational(1076,205)
gp45_P = -2152*b/205 - 2560*P/1681 + 4*(b-P)**2 - sp.Rational(15008,1681)
gb = sp.simplify(g45_P.diff(b)); gp_b = sp.simplify(gp45_P.diff(b))
gP = sp.simplify(g45_P.diff(P)); gp_P = sp.simplify(gp45_P.diff(P))
# d_b g(4/5) = -19/25 + 32(b-P)/5 < 0 since b < 17/25 < 157/50 <= P
check('D7 d_b g(4/5) < 0', sp.simplify(gb.subs({b: sp.Rational(17,25), P: sp.Rational(157,50)})) < 0)
# d_P g(4/5) > 0 : -346/41 + 32(P-b)/5 > 0 with P >= 157/50, b <= 17/25
check('D8 d_P g(4/5) > 0', sp.simplify(gP.subs({b: sp.Rational(17,25), P: sp.Rational(157,50)})) > 0)
# d_b g'(4/5) = -2152/205 + 8(b-P) < 0
check('D9 d_b g\'(4/5) < 0', sp.simplify(gp_b.subs({b: sp.Rational(17,25), P: sp.Rational(157,50)})) < 0)
# d_P g'(4/5) = -2560/1681 + 8(P-b) > 0
check('D10 d_P g\'(4/5) > 0', sp.simplify(gp_P.subs({b: sp.Rational(17,25), P: sp.Rational(157,50)})) > 0)

# ---- E. lem:boundary ----
# q = cos2th/(2 sin^2 th), w = cot th, A = pi - 2 th  (exact on the curve)
th2 = sp.Symbol('th2', positive=True)
q_ = sp.cos(2*th2)/(2*sp.sin(th2)**2)
w_ = sp.cos(th2)/sp.sin(th2)
A2b = pi - 2*th2
M2b = 4*A2b**2*w_*q_ - 7*A2b*q_**2 - 9*A2b*w_**2 + 2*A2b*(q_**2+w_**2)/(1+w_**2) + sp.atan(w_)*(4*A2b*w_ - 5*q_ - 9*q_*w_**2)
# on the boundary curve: atan(w_) = pi/2 - th2 exactly (0 < th2 < pi/6)
M2b = sp.expand_trig(M2b.subs(sp.atan(w_), pi/2 - th2))
M2b_doc = 2*(2*th2-pi)*sp.cos(th2)**2/sp.sin(th2)**2*((2*th2-pi)*sp.cos(th2)/sp.sin(th2) + 2/sp.sin(th2)**2)
check('E1 M2 on boundary closed form', sp.simplify(sp.expand_trig(M2b - M2b_doc)) == 0)
# N(z) representation: z = tan th (0 < z <= 1/sqrt3), beta = atan z = th, A = pi - 2 th
z2 = sp.Symbol('z2', positive=True)
th_z = sp.atan(z2)
q_z = sp.cos(2*th_z)/(2*sp.sin(th_z)**2)
w_z = 1/z2
A2z = pi - 2*th_z
dM2dq = sp.diff(M2gen, q)
# on the boundary curve: atan(w) = pi/2 - th, atan(w/q) = 2*th exactly (0 < th < pi/6)
dM2dq_b = dM2dq.subs(sp.atan(w/q), 2*th_z).subs(sp.atan(w), pi/2 - th_z)
dM2dq_b = sp.simplify(sp.expand_trig(dM2dq_b.subs({q: q_z, w: w_z})))
Pz = 32*z2*(z2**2+1)**2
Qz = -10*z2**6 - 32*pi*z2**5 + 42*z2**4 - 64*pi*z2**3 + 2*z2**2 - 32*pi*z2 + 46
Rz = 5*pi*z2**6 - 10*z2**5 + 8*pi**2*z2**5 - 21*pi*z2**4 - 40*z2**3 + 16*pi**2*z2**3 - pi*z2**2 - 14*z2 + 8*pi**2*z2 - 23*pi
Nz_doc = th_z**2*Pz + th_z*Qz + Rz
check('E2 d_q M2 on boundary = N/(2z^2(z^2+1)^2)', sp.simplify(sp.expand_trig(dM2dq_b - Nz_doc/(2*z2**2*(z2**2+1)**2))) == 0)
# T(z) expansion
Tz = sp.expand(sp.pi**2/36*Pz + sp.pi/6*Qz + Rz)
Tz_doc = sp.expand(10*pi/3*z2**6 + (32*pi**2/9 - 10)*z2**5 - 14*pi*z2**4 + (64*pi**2/9 - 40)*z2**3 - 2*pi/3*z2**2 + (32*pi**2/9 - 14)*z2 - 46*pi/3)
check('E3 T(z) expansion', sp.simplify(Tz - Tz_doc) == 0)

# ---- F. lem:M2: d2_q M2 = 2 N2 / ((q^2+w^2)^2 (1+w^2)) ----
tq = sp.atan(w)
Aq = pi - sp.atan(w/q)
d2M2 = sp.simplify(sp.diff(M2gen, q, 2))
N2_doc = -Aq*(7*q**4*w**2 + 5*q**4 + 14*q**2*w**4 + 10*q**2*w**2 - w**6 - 3*w**4) - 7*q**3*w**3 - 5*q**3*w - q*w**5 - 4*q*w**4*tq + q*w**3 - 4*q*w**2*tq
check('F1 d2_q M2 = 2 N2 / ((q^2+w^2)^2 (1+w^2))', sp.simplify(sp.expand_trig(d2M2 - 2*N2_doc/((q**2+w**2)**2*(1+w**2)))) == 0)

# ---- G. lem:corner: G2(1/2; q) ----
# at c = 1/2, alpha1 = x with cos x = q/(q+1); alpha2 = pi - x
qq = sp.Symbol('qq', positive=True)
xx = sp.acos(qq/(qq+1))
# G2 at c=1/2: use G(x;c) at x = pi - xx, c = 1/2
Phic = sp.cos(pi-xx)**2 + qq**2*sp.sin(pi-xx)**2
Dc = qq + sp.Rational(1,2)*Phic
G2c = sp.simplify(-Phic*(3+2*(pi-xx)*sp.cos(pi-xx)/sp.sin(pi-xx))/Dc + 2*sp.Rational(1,2)*(pi-xx)*Phic*(qq**2-1)*sp.sin(pi-xx)*sp.cos(pi-xx)/Dc**2)
G2c_doc = 2*qq*(qq+1)*(pi-xx-3*sp.sin(xx))/(2*qq+1)**sp.Rational(3,2)
# need identity: sin(pi-xx)=sin xx, cos(pi-xx) = -cos xx = -q/(q+1)
G2c_s = sp.simplify(G2c)
G2c_doc_s = sp.simplify(G2c_doc)
# simplify using sin^2 xx = 1 - q^2/(q+1)^2 = (2q+1)/(q+1)^2 -> sin xx = sqrt(2q+1)/(q+1)
sxx = sp.sqrt((2*qq+1))/(qq+1)
G2c_sub = sp.simplify(G2c.subs(sp.sin(xx), sxx).subs(sp.cos(xx), qq/(qq+1)))
G2c_doc_sub = sp.simplify(2*qq*(qq+1)*(pi-xx-3*sxx)/(2*qq+1)**sp.Rational(3,2))
check('G1 G2(1/2;q) closed form', sp.simplify(sp.expand_trig(G2c_sub - G2c_doc_sub)) == 0)
check('G2 G2(1/2;2) > 0', bool(float(sp.N(G2c_doc.subs(qq, 2), 30)) > 0))

print()
print('SUMMARY:', sum(1 for _, ok in res if ok), 'PASS /', len(res), 'total')