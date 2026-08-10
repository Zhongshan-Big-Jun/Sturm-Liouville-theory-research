# -*- coding: utf-8 -*-
"""Independent symbolic audit of SL_gap_n1_O3a_phase_rigidity_proof.tex (session 45, part B)."""
import sympy as sp
from fractions import Fraction as F
import math

pi = sp.pi
res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

q, c, x = sp.symbols("q c x", positive=True)
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2

# ============ A. eq:alphap / lem:dimred chain ============
E = sp.atan(1/(q*sp.tan(x)))
check("A1 E' = -q/Phi (0<x<pi/2)", sp.simplify(sp.expand_trig(sp.diff(E, x) + q/Phi)) == 0)
O1 = pi - sp.atan(q*sp.tan(x))
check("A2 O' = -q/Phi (0<x<pi/2 branch)", sp.simplify(sp.expand_trig(sp.diff(O1, x) + q/Phi)) == 0)
O2 = sp.atan(-q*sp.tan(x))
check("A3 O' = -q/Phi (pi/2<x<pi branch)", sp.simplify(sp.expand_trig(sp.diff(O2, x) + q/Phi)) == 0)
alph = sp.Symbol("alpha", positive=True)
Phia = sp.cos(alph)**2 + q**2*sp.sin(alph)**2
alpha_p = -alph*Phia/(q + c*Phia)
check("A4 eq:alphap", sp.simplify(sp.expand_trig(alph/(sp.diff(E, x).subs(x, alph) - c) - alpha_p)) == 0)
x2 = sp.Symbol("x2", positive=True)
Phix2 = sp.cos(x2)**2 + q**2*sp.sin(x2)**2
ddc = 2*(c+q)*x2**2 + (c+q)**2*2*x2*(-x2*Phix2/(q+c*Phix2))
ddc_doc = -2*q*(c+q)*(q**2-1)*x2**2*sp.sin(x2)**2/(q+c*Phix2)
check("A5 d/dc((c+q)^2 x^2)", sp.simplify(sp.expand_trig(ddc - ddc_doc)) == 0)
Mf1, Mf2 = sp.symbols("Mf1 Mf2", positive=True)
Dc = sp.Rational(4,1)/q**2 * (-2*q*(c+q)*(q**2-1)*Mf2 + 2*q*(c+q)*(q**2-1)*Mf1)
check("A6 eq:Dc", sp.simplify(Dc - 8*(c+q)*(q**2-1)/q*(Mf1 - Mf2)) == 0)
xi = q/(2*(c+q))
check("A7 eq:dimred coefficient 2(c+q)/xi^2 = 8(c+q)^3/q^2",
      sp.simplify(2*(c+q)/xi**2 - 8*(c+q)**3/q**2) == 0)
q0 = sp.Symbol("q0", nonnegative=True)
W1 = 1 + q0*sp.sin(x)**2
J = sp.sin(x)**2/W1
check("A8 (d/dx)log J = 2cotx/W", sp.simplify(sp.expand_trig(sp.diff(sp.log(J), x) - 2*sp.cot(x)/W1)) == 0)
tau = sp.Symbol("tau", positive=True)
lhs = 2*tau*sp.cot(tau*x)/W1.subs(x, tau*x) - 2*sp.cot(x)/W1
rhs = (sp.Rational(2,1)/x)*(tau*x*sp.cot(tau*x)/W1.subs(x, tau*x) - x*sp.cot(x)/W1)
check("A9 r_tau log-derivative identity", sp.simplify(sp.expand_trig(lhs - rhs)) == 0)

# ============ B. F_e'(q,1/2) closed form + P(x) ============
qq = sp.Symbol("qq", positive=True)
xx = sp.acos(qq/(qq+1))
sxv = sp.sqrt(2*qq+1)/(qq+1)
cxv = qq/(qq+1)
def Gexpr(ph, DD, z):
    return -ph*(3 + 2*z*sp.cos(z)/sp.sin(z))/DD + 2*sp.Rational(1,2)*z*ph*(qq**2-1)*sp.sin(z)*sp.cos(z)/DD**2
Ph1 = sp.cos(xx)**2 + qq**2*sp.sin(xx)**2
D1 = qq + sp.Rational(1,2)*Ph1
G1 = Gexpr(Ph1, D1, xx)
Mf1b = xx**2*sp.sin(xx)**2/D1
Ph2 = sp.cos(sp.pi-xx)**2 + qq**2*sp.sin(sp.pi-xx)**2
D2 = qq + sp.Rational(1,2)*Ph2
G2 = Gexpr(Ph2, D2, sp.pi-xx)
Mf2b = (sp.pi-xx)**2*sp.sin(sp.pi-xx)**2/D2
Fp = sp.expand_trig(Mf1b*G1 - Mf2b*G2)
Fp = Fp.subs(sp.sin(sp.pi-xx), sxv).subs(sp.cos(sp.pi-xx), -cxv)
Fp = Fp.subs(sp.sin(xx), sxv).subs(sp.cos(xx), cxv)
Px = 3*xx**2 + 6*xx*sp.sin(xx) - 3*pi*xx - 3*pi*sp.sin(xx) + pi**2
rhs = 2*pi*(sp.cos(xx)-1)**3/sp.sin(xx)**3*Px
rhs = rhs.subs(sp.sin(xx), sxv).subs(sp.cos(xx), cxv)
check("B1 F_e'(q,1/2) closed form", sp.simplify(sp.expand_trig(Fp - rhs)) == 0)
Px1 = 3*xx**2 + 6*xx*sp.sin(xx) - 3*pi*xx - 3*pi*sp.sin(xx) + pi**2
Px2 = (pi-3*xx)**2 + 3*(xx - sp.sin(xx))*(pi - 2*xx)
check("B2 P(x) = (pi-3x)^2 + 3(x-sinx)(pi-2x)", sp.simplify(sp.expand(Px1 - Px2)) == 0)
print("   B3: x < pi/3 for q>1  (q/(q+1) > 1/2 <=> q>1)")
xalt = 2*sp.asin(1/sp.sqrt(2*(qq+1)))
check("B4 cos(2asin(1/sqrt(2(q+1)))) = q/(q+1)",
      sp.simplify(sp.expand_trig(sp.cos(xalt)) - qq/(qq+1)) == 0)
print("   B5: P(x) > 0 via (pi-3x)^2 + 3(x-sinx)(pi-2x)")

# ============ C. eq:G2id + lem:G2m2 ============
gm = sp.Symbol("gm", positive=True)
A_ = pi - gm
Phi_g = sp.cos(gm)**2 + q**2*sp.sin(gm)**2
D_g = q + c*Phi_g
W0 = 3 - 2*A_*sp.cot(gm)
Pv = c*A_*Phi_g*(q**2-1)*sp.sin(gm)*sp.cos(gm)/D_g**2
G2full = -Phi_g*(3 + 2*(pi-gm)*sp.cot(pi-gm))/D_g + 2*c*(pi-gm)*Phi_g*(q**2-1)*sp.sin(pi-gm)*sp.cos(pi-gm)/D_g**2
check("C1 eq:G2id", sp.simplify(sp.expand_trig(G2full - (-Phi_g*W0/D_g - 2*Pv))) == 0)
check("C2 Phi/D <= 65/66 arithmetic", F(13,8)/(1+F(13,20)) == F(65,66))
u_g = q*sp.sin(gm)**2 + sp.cos(gm)**2/q
check("C3 u_qq = 2 cos^2/q^3 > 0", sp.simplify(sp.diff(u_g, q, 2) - 2*sp.cos(gm)**2/q**3) == 0)
check("C4 endpoint u(2) = 3/2 sin^2 + 1/2",
      sp.simplify(u_g.subs(q, 2) - (sp.Rational(3,2)*sp.sin(gm)**2 + sp.Rational(1,2))) == 0)
check("C5 W0(pi/3) = 3 - 4pi/(3sqrt3)",
      sp.simplify(W0.subs({gm: pi/3}) - (3 - 4*pi/(3*sp.sqrt(3)))) == 0)
check("C6 d/dg((pi-g)cotg) formula",
      sp.simplify(sp.diff((pi-gm)*sp.cot(gm), gm) - (-sp.cot(gm) - (pi-gm)*sp.csc(gm)**2)) == 0)
print("   C7: 4*3.1415/(3*1.7321) > 2.418 ->", 4*3.1415/(3*1.7321) > 2.418)
Phis = sp.Symbol("Phi", positive=True)
fPhi = Phis*(q**2-1)/(q+c*Phis)**2
check("C8 f'(Phi) formula", sp.simplify(sp.diff(fPhi, Phis) - (q**2-1)*(q-c*Phis)/(q+c*Phis)**3) == 0)
check("C9 q - c q^2 = q(1-cq)", sp.simplify(q - c*q**2 - q*(1-c*q)) == 0)
hq = (q**2-1)/(1+sp.Rational(2,5)*q)**2
check("C10 h'(q) formula", sp.simplify(sp.diff(hq, q) - 2*(q+sp.Rational(2,5))/(1+sp.Rational(2,5)*q)**3) == 0)
check("C11 h(2) = 25/27", sp.simplify(hq.subs(q, 2) - sp.Rational(25,27)) == 0)
print("   C12: 25(pi-0.655)/108 < 0.576 ->", 25*(3.1416-0.655)/108 < 0.576)
check("C13 combination 0.582+2*0.576 < 2", F(582,1000) + 2*F(576,1000) < 2)

# ============ D. thm:j1e1 steps (i)-(vii) ============
Phi_x = sp.cos(x)**2 + q**2*sp.sin(x)**2
Dq = q + c*Phi_x
check("D1 Phi-q at q=1 = 0", sp.simplify(Phi_x.subs(q, 1) - 1) == 0)
check("D2 d/dq(Phi-q) = 2q sin^2 x - 1", sp.simplify(sp.diff(Phi_x - q, q) - (2*q*sp.sin(x)**2 - 1)) == 0)
check("D3 2 sin^2 x - 1 = -cos 2x", sp.simplify(sp.expand_trig(2*sp.sin(x)**2 - 1 + sp.cos(2*x))) == 0)
u = x*Phi_x/Dq
ux_doc = (Phi_x*Dq + 2*x*q*(q**2-1)*sp.sin(x)*sp.cos(x))/Dq**2
check("D4 u_x formula", sp.simplify(sp.expand_trig(sp.diff(u, x) - ux_doc)) == 0)
check("D5 D - c(q^2-1)sin^2x = q+c", sp.simplify(Dq - c*(q**2-1)*sp.sin(x)**2 - (q+c)) == 0)
A3 = 3/x + 2*sp.cot(x)
H = 2*c*(q**2-1)*sp.sin(x)*sp.cos(x)/Dq
Gx0 = -Phi_x*(3+2*x*sp.cot(x))/Dq + 2*c*x*Phi_x*(q**2-1)*sp.sin(x)*sp.cos(x)/Dq**2
check("D6 G = u(H-A)", sp.simplify(sp.expand_trig(Gx0 - u*(H-A3))) == 0)
W3 = 3 + 2*x*sp.cot(x)
t1 = Phi_x**2*W3/Dq**2
t2 = 2*x*Phi_x*(q**2-1)*sp.sin(x)*sp.cos(x)*(q - c*Phi_x)/Dq**3
check("D7 G_c = t1 + t2", sp.simplify(sp.expand_trig(sp.diff(Gx0, c) - (t1+t2))) == 0)
check("D8 (2/3)^2(3+2pi/(3sqrt3)) = 4/3 + 8pi/(27sqrt3)",
      sp.simplify(sp.Rational(4,9)*(3 + 2*pi/(3*sp.sqrt(3))) - (sp.Rational(4,3) + 8*pi/(27*sp.sqrt(3)))) == 0)
print("   D9: 8*3.1415/(27*1.7321) > 161/300 ->", 8*3.1415/(27*1.7321) > 161/300)
c1 = sp.atan(1/(q*sp.tan(x)))/x
Dc1 = q + c1*Phi_x
ddq = sp.diff(Phi_x/Dc1, q)
ddq_doc = (q**2*sp.sin(x)**2 - sp.cos(x)**2)/Dc1**2 + Phi_x**2*sp.tan(x)/(x*Dc1**2*(q**2*sp.tan(x)**2 + 1))
check("D10 d/dq(Phi/D) closed form (curve c1)", sp.simplify(sp.expand_trig(ddq - ddq_doc)) == 0)
f1x = (2*x/pi)**2*(3+2*x*sp.cot(x))
check("D11 f'(x) formula", sp.simplify(sp.expand_trig(sp.diff(f1x, x) - 8*x/pi**2*(3+3*x*sp.cot(x)-x**2*sp.csc(x)**2))) == 0)
print("   D12: 3+3(5pi/14)tan(pi/7)-(4/3)(5pi/14)^2 > 0 ->",
      3+3*(5*3.1415/14)*math.tan(math.pi/7)-(4/3)*(5*3.1416/14)**2 > 0)
print("   D13: 3/(0.841)^2 < 3000/707 ->", 3/0.841**2 < 3000/707)
print("   D14: 0.7418^2 > 0.55 ->", 0.7418**2 > 0.55)   # hence 2/sin^2 < 200/55
uc = x*sp.sin(2*x)/(sp.sin(4*x/5) + sp.Rational(2,5)*sp.sin(2*x))
Fv = sp.Rational(89,100)*sp.sin(4*x/5) - (x - sp.Rational(89,250))*sp.sin(2*x)
check("D15 u_c - 89/100 = -F/denom", sp.simplify(sp.expand_trig(uc - sp.Rational(89,100) + Fv/(sp.sin(4*x/5) + sp.Rational(2,5)*sp.sin(2*x)))) == 0)
Fpp = sp.diff(Fv, x, 2)
check("D16 F''(x) formula", sp.simplify(sp.expand_trig(Fpp - (-sp.Rational(356,625)*sp.sin(4*x/5) - 4*sp.cos(2*x) + 4*(x-sp.Rational(89,250))*sp.sin(2*x)))) == 0)
y = sp.Symbol("y", positive=True)
gfun = (y/2 - sp.Rational(89,250))*sp.sin(y) - sp.cos(y)
check("D17 g'(y) formula", sp.simplify(sp.expand_trig(sp.diff(gfun, y) - (sp.Rational(3,2)*sp.sin(y) + (y/2-sp.Rational(89,250))*sp.cos(y)))) == 0)
print("   D18: (3/2)sin(0.8975)-0.766cos(0.8975) > 0 ->",
      (3/2)*math.sin(0.8975) - 0.766*math.cos(0.8975) > 0)
check("D19 combination 6499/7500", sp.Rational(4) + sp.Rational(187,100) - (sp.Rational(89,100)**2*8 - sp.Rational(4,3)) == sp.Rational(6499,7500))

# ============ E. q=1 lines ============
c1_1 = (pi/2 - x)/x
check("E1 D(x,1) = pi/(2x)", sp.simplify(1 + c1_1 - pi/(2*x)) == 0)
z = x*sp.cot(x)
G1x = -(3 + 2*x*sp.cot(x))/(1 + c1_1)
G1c = (3 + 2*x*sp.cot(x))/(1 + c1_1)**2
G1xx = sp.diff(-(3 + 2*x*sp.cot(x)), x)/(1 + c1_1)
u1 = x/(1 + c1_1)
J1 = sp.simplify(sp.expand_trig(G1x**2 + G1c - u1*G1xx))
N1 = 12 + 16*z + 2*z**2 - 2*x**2
check("E2 J1(x,1) = (2x/pi)^2 N(x)", sp.simplify(sp.expand_trig(J1 - (2*x/pi)**2*N1)) == 0)
check("E3 N = 2(z^2+8z+6) - 2x^2", sp.simplify(sp.expand_trig(N1 - (2*(z**2 + 8*z + 6) - 2*x**2))) == 0)
print("   E4: 2(1/4+4+6)-2*1.26 = 17.98 > 17.9")
xq = pi - gm
c2_1 = gm/(pi - gm)
D2q = 1 + c2_1
check("E5 D(x,1) = pi/x (second phase)", sp.simplify(D2q - pi/xq) == 0)
z2v = -xq*sp.cot(xq)
N2 = 12 + 16*xq*sp.cot(xq) + 2*xq**2*sp.cot(xq)**2 - 2*xq**2
check("E6 N2 = 2(z^2 - 8z + 6) - 2x^2", sp.simplify(sp.expand_trig(N2 - (2*(z2v**2 - 8*z2v + 6) - 2*xq**2))) == 0)
print("   E7: z range [2pi/(3sqrt3), (5pi/7)cot(2pi/7)] subset (1.19, 2.5):",
      2*math.pi/(3*math.sqrt(3)) > 1.19, (5*math.pi/7)/math.tan(2*math.pi/7) < 2.5)
print("   E8: 2(4-8*(8pi/21)+6) - 2(2pi/3)^2 < -7 ->",
      2*(4 - 8*(8*3.1415/21) + 6) - 2*(2*3.1416/3)**2 < -7)

# ============ F. lem:j2bounds algebra + mu + table ============
A2_, t2_, sg_, cg_, st_, ct_ = sp.symbols("A2 t2 sg cg st ct", positive=True)
B1_ = A2_*cg_ - 2*sg_
B2_ = 4*A2_**2*cg_**2 - A2_**2 - 12*A2_*cg_*sg_ + 6*sg_**2
M_ = 2*A2_**2*cg_**2 - A2_**2 - 8*A2_*cg_*sg_ + 6*sg_**2
B4_ = 7*A2_*cg_**2 - A2_*sg_**2 - 4*cg_*sg_
B5_ = A2_**2*cg_**2 - A2_**2*sg_**2 + 2*A2_**2 + 12*A2_*cg_*sg_ - 12*sg_**2
B7_ = 3*A2_*cg_**2 + A2_*sg_**2 + 8*cg_*sg_
G5_ = B5_ - A2_*B4_
W1_ = -2*A2_**3*B1_*st_**2*ct_**4
W2_ = A2_**2*cg_*B2_*st_**2*ct_**2
W3_ = -2*A2_**3*sg_*t2_*st_*ct_**5
W4_ = A2_**2*sg_*t2_*B4_*st_*ct_**3
W5_ = -A2_*cg_**2*sg_*t2_*B5_*st_*ct_
W6_ = 4*A2_**2*cg_*sg_**2*t2_**2*ct_**4
W7_ = -A2_*cg_*sg_**2*t2_**2*B7_*ct_**2
W8_ = 6*cg_**3*sg_**4*t2_**2
zz_ = ct_**2
dF1 = sp.expand(W1_+W2_ - zz_*(1-zz_)*(A2_**2*cg_*B2_ - 2*A2_**3*B1_*zz_))
dF1 = sp.expand(dF1.subs(st_**2, 1-ct_**2))
check("F1 W1+W2 = z(1-z)(A^2 cg B2 - 2A^3 B1 z) (mod st^2+ct^2=1)", dF1 == 0)
check("F2 M = B2 - 2A cg B1", sp.expand(M_ - (B2_ - 2*A2_*cg_*B1_)) == 0)
check("F3 A^2 cg B2 - 2A^3 B1 z = A^2 cg M + 2A^3 B1 (cg^2 - z)",
      sp.expand(A2_**2*cg_*B2_ - 2*A2_**3*B1_*zz_ - (A2_**2*cg_*M_ + 2*A2_**3*B1_*(cg_**2 - zz_))) == 0)
check("F4 W4+W5 = A sg t st ct (A B4 (ct^2-cg^2) - cg^2 G5)",
      sp.expand(W4_+W5_ - A2_*sg_*t2_*st_*ct_*(A2_*B4_*(ct_**2-cg_**2) - cg_**2*G5_)) == 0)
Qz_ = 4*A2_**2*zz_**2 - A2_*B7_*zz_ + 6*cg_**2*sg_**2
check("F5 W6+W7+W8 = t^2 cg sg^2 Q(z)",
      sp.expand(W6_+W7_+W8_ - t2_**2*cg_*sg_**2*Qz_) == 0)
D2v_ = 1 + 3*sg_**2
check("F7 D^2 - cg^2 = 4 sg^2", sp.expand((D2v_ - cg_**2 - 4*sg_**2).subs(cg_**2, 1-sg_**2)) == 0)
check("F8 cos^2 tau = cg^2/D^2", sp.simplify(sp.expand_trig(1/(1+4*sp.tan(gm)**2) - sp.cos(gm)**2/(1+3*sp.sin(gm)**2))) == 0)
check("F9 sin tau = 2 sg / D (via tan tau = 2 tan g)",
      sp.simplify(sp.expand_trig(sp.tan(sp.atan(2*sp.tan(gm)))*sp.cos(gm)/sp.sqrt(1+3*sp.sin(gm)**2) - 2*sp.sin(gm)/sp.sqrt(1+3*sp.sin(gm)**2))) == 0)
check("F10 mu corner = 27921/20000", F(3,8)+F(1,40)+F(11,10)-F(63,100)*F(33,200) == F(27921,20000))
check("F11 27921/20000 > 139/100", F(27921,20000) > F(139,100))
rows = [(F(11,5),F(3,10),F(57,50),F(91,25)), (F(13,5),F(3,10),F(3,2),F(22,5)),
        (F(27,10),F(3,10),F(3,2),F(9,2)), (F(13,5),F(3,10),F(3,2),F(22,5)),
        (F(2),F(3,20),F(3,2),F(73,20)), (F(2),F(3,20),F(19,10),F(81,20)),
        (F(19,10),F(1,10),F(19,10),F(39,10)), (F(9,5),F(1,10),F(19,10),F(19,5)),
        (F(3,5),F(1,25),F(4,3),F(148,75)),
        (F(3,8),F(1,40),F(11,10),F(27921,20000))]
for i,(ta,tb,tc,mu) in enumerate(rows):
    if i == 9:
        check("F12 table row 10 (with T_D)", ta+tb+tc-F(63,100)*F(33,200) == mu)
    else:
        check("F12 table row %d" % (i+1), ta+tb+tc == mu)

# ============ G. Fepos / Feneg identities ============
c2g = sp.atan(q*sp.tan(gm))/(pi - gm)
import mpmath as mp
mp.mp.dps = 40
G1_ok = True
for gv, qv in [(0.7,1.5),(0.9,1.2),(1.0,1.1),(0.655,2.0),(mp.pi/3,1.0),(1.0472,1.5),(0.8,1.9)]:
    c2v = mp.atan(qv*mp.tan(gv))/(mp.pi-gv)
    lhs = mp.atan(1/(qv*mp.tan(gv))) - c2v*gv
    rhs = mp.pi*(mp.mpf(1)/2 - c2v)
    G1_ok = G1_ok and abs(lhs-rhs) < mp.mpf("1e-35")
check("G1 E(g)-cg = pi(1/2-c) (atan identity, numeric cross-check)", G1_ok)
phi_c = gm**2*sp.sin(gm)**2/(q + c2g*(sp.cos(gm)**2 + q**2*sp.sin(gm)**2))
Mf_a2 = (pi-gm)**2*sp.sin(pi-gm)**2/(q + c2g*(sp.cos(pi-gm)**2 + q**2*sp.sin(pi-gm)**2))
check("G2 Mf(alpha2;c) = ((pi-g)/g)^2 phi_c(g)",
      sp.simplify(sp.expand_trig(Mf_a2 - ((pi-gm)/gm)**2*phi_c)) == 0)
check("G3 Mf(pi/2;0) = pi^2/(4q)", sp.simplify((pi/2)**2*sp.sin(pi/2)**2/q - pi**2/(4*q)) == 0)
check("G4 Mf(pi;0) = 0", sp.simplify(pi**2*sp.sin(pi)**2/q) == 0)

# ============ H. independent J2 = 2 A^2 cg W / Delta^4 (modulo relations) ============
print()
print("--- H. independent J2 decomposition (symbolic, may take a while) ---")
xH2, qHs, cHs = sp.symbols("xH2 qHs cHs", positive=True)
PhiH = sp.cos(xH2)**2 + qHs**2*sp.sin(xH2)**2
DH = qHs + cHs*PhiH
GH = -PhiH*(3 + 2*xH2*sp.cot(xH2))/DH + 2*cHs*xH2*PhiH*(qHs**2-1)*sp.sin(xH2)*sp.cos(xH2)/DH**2
uH = xH2*PhiH/DH
GHx = sp.diff(GH, xH2)          # partial d/dx at fixed (q, c)
GHc = sp.diff(GH, cHs)          # partial d/dc at fixed (x, q)
J2raw = sp.expand(GH**2 + GHc - uH*GHx)
# second phase parameterization: x = pi - gamma = A, sin x = sg, cos x = -cg,
# q = st*cg/(ct*sg), c = t/A
subsH = {sp.sin(xH2): sg_, sp.cos(xH2): -cg_, sp.cot(xH2): -cg_/sg_, xH2: A2_,
         qHs: st_*cg_/(ct_*sg_), cHs: t2_/A2_}
J2raw = sp.expand(J2raw.subs(subsH))
Wsum = sp.expand(W1_+W2_+W3_+W4_+W5_+W6_+W7_+W8_)
Delta_ = A2_*st_*ct_ + t2_*sg_*cg_
J2cf = 2*A2_**2*cg_*Wsum/Delta_**4
diffH = sp.together(J2raw - J2cf)
numH = sp.expand(sp.fraction(diffH)[0])
gbH = sp.groebner([sg_**2 + cg_**2 - 1, st_**2 + ct_**2 - 1], A2_, t2_, sg_, cg_, st_, ct_)
remH = gbH.reduce(numH)[1]
check("H1 J2raw = 2 A^2 cg W / Delta^4 (modulo trig relations)", remH == 0)

print()
print("SUMMARY:", sum(1 for _, ok in res if ok), "PASS /", len(res), "total")
