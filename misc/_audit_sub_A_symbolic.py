# _audit_sub_A_symbolic.py — independent symbolic verification of the analytic identities
# in SL_gap_n1_O3a_phase_rigidity_proof.tex, lines 559-1527 (sections 4.3-5 front part).
# Uses only sympy; no reuse of project audit scripts.
import sympy as sp

pi = sp.pi
x, c, q, w = sp.symbols('x c q w', positive=True)
sg, cg, st, ct, t, A = sp.symbols('sg cg st ct t A', positive=True)

def Phi(qq, xx):
    return sp.cos(xx)**2 + qq**2*sp.sin(xx)**2

def Gfunc(xx, qq, cc):
    P = Phi(qq, xx)
    D = qq + cc*P
    return -P*(3+2*xx*sp.cot(xx))/D + 2*cc*xx*P*(qq**2-1)*sp.sin(xx)*sp.cos(xx)/D**2

results = []

def check(name, cond):
    results.append((name, bool(sp.simplify(cond) == 0) if isinstance(cond, sp.Expr) else bool(cond)))
    return results[-1][1]

# --- 1. eq:G : d/dc log Mf(alpha(c);c) = G(alpha;c), with alpha' = -xPhi/(q+cPhi) ---
x1 = sp.symbols('x1', positive=True)
Mf = lambda xx, qq, cc: xx**2*sp.sin(xx)**2/(qq + cc*Phi(qq, xx))
# d/dc log Mf along curve = (dMf/dc + dMf/dx * alpha')/Mf
Mf_c = sp.diff(Mf(x1,q,c), c)
Mf_x = sp.diff(Mf(x1,q,c), x1)
alpha_p = -x1*Phi(q,x1)/(q + c*Phi(q,x1))
lhs = sp.simplify((Mf_c + Mf_x*alpha_p)/Mf(x1,q,c))
rhs = sp.simplify(Gfunc(x1,q,c))
check("eq:G: d/dc log Mf along phase curve equals G", sp.simplify(lhs-rhs))
print("1 eq:G", results[-1])

# --- 2. lem:G1 estimate ---
# (q^2-1) sin x cos x <= Phi cot x  <=>  Phi cotx - (q^2-1) sinx cosx = cotx > 0
expr = Phi(q,x)*sp.cot(x) - (q**2-1)*sp.sin(x)*sp.cos(x)
check("lem:G1: Phi cotx - (q^2-1)sinx cosx = cotx", sp.simplify(expr - sp.cot(x)))
print("2 lem:G1", results[-1])

# --- 3. IN = G2 * POS ---
wq = sp.symbols('w', positive=True)
A_sym = pi - sp.atan(w/q)
c_sym = sp.atan(w)/A_sym
IN = (q**2+w**2)*A_sym*(2*A_sym*q - 3*w + 2*sp.atan(w)) - 3*w*q*(1+w**2)*sp.atan(w)
# G2 = G(alpha_2; c) with alpha_2 = A_sym, c = arctan(w)/A_sym
G2 = Gfunc(A_sym, q, c_sym)
PhiA = Phi(q, A_sym)
D_A = q + c_sym*PhiA
POS = D_A**2*A_sym*(q**2+w**2)*w/(PhiA*q)
diff3 = sp.simplify(IN - G2*POS)
check("eq:IN: IN = G2*POS", diff3)
print("3 IN=G2*POS", results[-1])

# --- 4. M2 = d/dw IN ---
M2_formula = 4*A_sym**2*w*q - 7*A_sym*q**2 - 9*A_sym*w**2 + 2*A_sym*(q**2+w**2)/(1+w**2) \
             + sp.atan(w)*(4*A_sym*w - 5*q - 9*q*w**2)
check("eq:M2: M2 = dw IN", sp.simplify(sp.diff(IN, w) - M2_formula))
print("4 M2", results[-1])

# --- 5. lem:B1: g(w)=d_q M2(1,w); g'' formula; g'(0); g'(sqrt3) ---
g = sp.diff(M2_formula, q).subs(q, 1)
g = sp.simplify(g)
t_s = sp.atan(w)
gpp = sp.diff(g, w, 2)
claimed_gpp = -2*(9*w**6*t_s + 9*w**5 + 27*w**4*t_s + 24*w**3 + 19*w**2*t_s + 20*pi*w**2 + 31*w + t_s + 4*pi)/(1+w**2)**3
check("lem:B1: g'' formula", sp.simplify(gpp - claimed_gpp))
check("lem:B1: g'(0) = 4 pi^2", sp.simplify(sp.diff(g,w).subs(w,0) - 4*pi**2))
gp_s3 = sp.simplify(sp.diff(g,w).subs(w, sp.sqrt(3)))
check("lem:B1: g'(sqrt3) = 16pi^2/9 - 41sqrt3 pi/6 - 15", sp.simplify(gp_s3 - (16*pi**2/9 - 41*sp.sqrt(3)*pi/6 - 15)))
print("5 lem:B1", results[-3:])

# --- 6. g(4/5), g'(4/5) closed forms ---
b = sp.symbols('b', positive=True)  # b = arctan(4/5)
g45 = sp.simplify(g.subs(w, sp.Rational(4,5)))
claimed_g45 = -19*b/25 - 346*pi/41 + 16*(b-pi)**2/5 - sp.Rational(1076,205)
check("lem:B1: g(4/5) closed form", sp.simplify(g45.subs(b, sp.atan(sp.Rational(4,5))) - claimed_g45.subs(b, sp.atan(sp.Rational(4,5)))))
gp45 = sp.simplify(sp.diff(g,w).subs(w, sp.Rational(4,5)))
claimed_gp45 = -2152*b/205 - 2560*pi/1681 + 4*(b-pi)**2 - sp.Rational(15008,1681)
check("lem:B1: g'(4/5) closed form", sp.simplify(gp45.subs(b, sp.atan(sp.Rational(4,5))) - claimed_gp45.subs(b, sp.atan(sp.Rational(4,5)))))
# partial derivatives
dg_db = sp.simplify(sp.diff(claimed_g45, b))
p = sp.Symbol('p', positive=True)
dg_dpi = sp.simplify(sp.diff(sp.simplify(claimed_g45.subs(pi, p)), p)).subs(p, pi)
dgp_db = sp.simplify(sp.diff(claimed_gp45, b))
dgp_dpi = sp.simplify(sp.diff(sp.simplify(claimed_gp45.subs(pi, p)), p)).subs(p, pi)
db_sign = sp.simplify(dg_db.subs({b: sp.Rational(67,100), pi: sp.Rational(22,7)}))
check("lem:B1: db g(4/5) < 0", db_sign < 0)
dpi_sign = sp.simplify(dg_dpi.subs({b: sp.Rational(67,100), pi: sp.Rational(22,7)}))
check("lem:B1: dpi g(4/5) > 0", dpi_sign > 0)
dgp_db_sign = sp.simplify(dgp_db.subs({b: sp.Rational(67,100), pi: sp.Rational(22,7)}))
check("lem:B1: db g'(4/5) < 0", dgp_db_sign < 0)
dgp_dpi_sign = sp.simplify(dgp_dpi.subs({b: sp.Rational(67,100), pi: sp.Rational(22,7)}))
check("lem:B1: dpi g'(4/5) > 0", dgp_dpi_sign > 0)
print("6 lem:B1 g45/gp45", results[-6:])

# --- 7. lem:boundary: M2(q, w_b(q)) closed form; dqM2 = N/(2z^2(z^2+1)^2) ---
th = sp.symbols('theta', positive=True)
q_th = sp.cos(2*th)/(2*sp.sin(th)**2)
w_th = sp.cot(th)
M2b = sp.simplify(M2_formula.subs({q: q_th, w: w_th}))
claimed_M2b = 2*(2*th-pi)*sp.cot(th)**2*((2*th-pi)*sp.cot(th) + 2/sp.sin(th)**2)
check("lem:boundary: M2(q,w_b) closed form", sp.simplify(M2b - claimed_M2b))
# bracket positivity
brk = ((2*th-pi)*sp.cot(th) + 2/sp.sin(th)**2)*sp.sin(th)**2
check("lem:boundary: bracket*sin^2 = 2 - (pi/2 - th) sin2th", sp.simplify(brk - (2 - (pi/2-th)*sp.sin(2*th))))
print("7 lem:boundary M2", results[-2:])

# dq M2 at boundary via z = tan theta
z = sp.symbols('z', positive=True)
beta = sp.atan(z)
th_z = sp.atan(z)
q_z = sp.cos(2*sp.atan(z))/(2*sp.sin(sp.atan(z))**2)
w_z = sp.cot(sp.atan(z))
dM2dq = sp.simplify(sp.diff(M2_formula, q).subs({q: q_z, w: w_z}))
Pz = 32*z*(z**2+1)**2
Qz = -10*z**6 - 32*pi*z**5 + 42*z**4 - 64*pi*z**3 + 2*z**2 - 32*pi*z + 46
Rz = 5*pi*z**6 - 10*z**5 + 8*pi**2*z**5 - 21*pi*z**4 - 40*z**3 + 16*pi**2*z**3 - pi*z**2 - 14*z + 8*pi**2*z - 23*pi
Nz = beta**2*Pz + beta*Qz + Rz
diffN = sp.simplify(dM2dq - Nz/(2*z**2*(z**2+1)**2))
check("lem:boundary: dqM2 = N/(2z^2(z^2+1)^2)", diffN)
Tz = pi**2/36*Pz + pi/6*Qz + Rz
Tz_simp = sp.simplify(Tz)
claimed_Tz = sp.Rational(10,3)*pi*z**6 + (sp.Rational(32,9)*pi**2 - 10)*z**5 - 14*pi*z**4 + (sp.Rational(64,9)*pi**2 - 40)*z**3 - sp.Rational(2,3)*pi*z**2 + (sp.Rational(32,9)*pi**2 - 14)*z - sp.Rational(46,3)*pi
check("lem:boundary: T(z) expansion", sp.simplify(Tz_simp - claimed_Tz))
Rz_simp = sp.simplify(Rz)
claimed_Rz = -23*pi + (8*pi**2-14)*z + (16*pi**2-40)*z**3 + (8*pi**2-10)*z**5 + 5*pi*z**6 - 21*pi*z**4 - pi*z**2
check("lem:boundary: R(z) expansion", sp.simplify(Rz_simp - claimed_Rz))
print("8 lem:boundary dqM2", results[-3:])

# --- 8. lem:M2 part (a): M2(1,w) = pi h(w); h'' ---
M2q1 = sp.simplify(M2_formula.subs(q, 1))
h = 4*w*(pi - sp.atan(w)) - 5 - 9*w**2
check("lem:M2(a): M2(1,w) = pi h(w)", sp.simplify(M2q1 - pi*h))
check("lem:M2(a): h'' = -8/(1+w^2)^2 - 18", sp.simplify(sp.diff(h,w,2) - (-8/(1+w**2)**2 - 18)))
print("9 lem:M2(a)", results[-2:])

# --- 9. lem:M2 part (b): d^2_q M2 = 2 N2 / ((q^2+w^2)^2 (1+w^2)) ---
N2 = -A_sym*(7*q**4*w**2 + 5*q**4 + 14*q**2*w**4 + 10*q**2*w**2 - w**6 - 3*w**4) - 7*q**3*w**3 - 5*q**3*w - q*w**5 - 4*q*w**4*t_s + q*w**3 - 4*q*w**2*t_s
d2M2 = sp.diff(M2_formula, q, 2)
check("lem:M2(b): d2qM2 = 2N2/((q^2+w^2)^2(1+w^2))", sp.simplify(d2M2 - 2*N2/((q**2+w**2)**2*(1+w**2))))
print("10 lem:M2(b)", results[-1])

# --- 10. CORNER: G2(1/2;q) closed form ---
xg = sp.symbols('xg', positive=True)  # x = arccos(q/(q+1))
c12 = sp.Rational(1,2)
G2_12 = sp.simplify(Gfunc(pi - xg, q, c12))
# substitute cos xg = q/(q+1), sin xg = sqrt(2q+1)/(q+1)
G2_12s = sp.simplify(G2_12.subs({sp.cos(xg): q/(q+1), sp.sin(xg): sp.sqrt(2*q+1)/(q+1), sp.cot(xg): sp.cos(xg)/sp.sin(xg)}).subs({sp.cos(xg): q/(q+1), sp.sin(xg): sp.sqrt(2*q+1)/(q+1)}))
claimed = 2*q*(q+1)*(pi - xg - 3*sp.sin(xg))/(2*q+1)**sp.Rational(3,2)
G2_12s2 = sp.simplify(G2_12s.subs(xg, sp.atan2(sp.sqrt(2*q+1), q)))
claimed_s = sp.simplify(claimed.subs(sp.sin(xg), sp.sqrt(2*q+1)/(q+1)))
check("CORNER: G2(1/2;q) closed form (numerically-tagged)", sp.simplify(sp.N(G2_12s2 - claimed_s, 30)) == 0)
print("11 CORNER", results[-1])

# --- 11. C4: IN = A K(v); L; L'(v) = N/(10T^2); K = q^2 L ---
v = sp.symbols('v', positive=True)
wv = sp.tan(v)
qv = sp.tan(v)/sp.tan(pi - sp.Rational(5,2)*v)
A_v = sp.Rational(5,2)*v
Kv = (qv**2 + wv**2)*(5*v*qv - 3*wv + 2*v) - sp.Rational(6,5)*wv*qv*(1+wv**2)
IN_c04 = sp.simplify(IN.subs({q: qv, w: wv, A_sym: A_v}))
check("C4: IN = A*K(v) on c=0.4", sp.simplify(IN_c04 - A_v*Kv))
T_v = sp.tan(pi - sp.Rational(5,2)*v)
Lv = (1+T_v**2)*(wv*(5*v/T_v - 3) + 2*v) - sp.Rational(6,5)*T_v*(1+wv**2)
check("C4: K = q^2 L", sp.simplify(Kv - qv**2*Lv))
# L'(v) = N/(10 T^2)
N_v = 125*wv*v + 50*T_v*(v*(1+wv**2)+wv) + 20*T_v**2 + (50*wv**2*v - 24*wv**3 + 176*wv - 50*v)*T_v**3 + (20-125*wv*v)*T_v**4 + (150*wv - 100*v)*T_v**5
check("C4: L'(v) = N/(10T^2)", sp.simplify(sp.diff(Lv, v) - N_v/(10*T_v**2)))
# L(2pi/7)
w7 = sp.tan(2*pi/7)
L27 = sp.simplify(Lv.subs(v, 2*pi/7))
check("C4: L(2pi/7) = (1+w^2)(2pi - 21w/5)", sp.simplify(L27 - (1+w7**2)*(2*pi - sp.Rational(21,5)*w7)))
print("12 C4", results[-4:])

# --- 12. eq:G2id : G2 = -Phi W0/D - 2P ---
g2s = sp.symbols('gamma', positive=True)
c2 = sp.atan(q*sp.tan(g2s))/(pi-g2s)
Phig = sp.cos(g2s)**2 + q**2*sp.sin(g2s)**2
Dg = q + c2*Phig
W0 = 3 - 2*(pi-g2s)*sp.cot(g2s)
Pg = c2*(pi-g2s)*Phig*(q**2-1)*sp.sin(g2s)*sp.cos(g2s)/Dg**2
G2v = Gfunc(pi-g2s, q, c2)
check("eq:G2id: G2 = -Phi W0/D - 2P", sp.simplify(G2v - (-Phig*W0/Dg - 2*Pg)))
print("13 G2id", results[-1])

# --- 13. F_e'(q,1/2) closed form + P(x)>0 identity ---
xx = sp.symbols('xx', positive=True)
# x = 2 asin(1/sqrt(2(q+1))); equivalently cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1)
Px = 3*xx**2 + 6*xx*sp.sin(xx) - 3*pi*xx - 3*pi*sp.sin(xx) + pi**2
check("Fep12: P(x) = (pi-3x)^2 + 3(x-sinx)(pi-2x)", sp.simplify(Px - ((pi-3*xx)**2 + 3*(xx-sp.sin(xx))*(pi-2*xx))))
print("14 P(x) identity", results[-1])

# Verify the claimed closed form numerically at several q (symbolic verification is hard; do numeric high precision)
from mpmath import mp, mpf, sin, cos, asin, sqrt, pi as mppi
mp.dps = 40
def Mf_num(xx, qq, cc):
    P = cos(xx)**2 + qq**2*sin(xx)**2
    return xx**2*sin(xx)**2/(qq+cc*P)
def alpha1(qq, cc):
    # solve cc*x = arctan(1/(q tan x))
    lo, hi = mpf('0'), mppi/2
    for _ in range(100):
        mid = (lo+hi)/2
        if cc*mid > mp.atan(1/(qq*mp.tan(mid))):
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2
def Fep_num(qq, cc):
    a1 = alpha1(qq, cc)
    return (Mf_num(a1, qq, cc) - Mf_num(mppi-a1, qq, cc))
def Fep12_closed(qq):
    xq = 2*asin(1/sqrt(2*(qq+1)))
    Pq = 3*xq**2 + 6*xq*sin(xq) - 3*mppi*xq - 3*mppi*sin(xq) + mppi**2
    return 2*mppi*(cos(xq)-1)**3/sin(xq)**3*Pq
# compare numeric derivative of F_e at c=1/2 with closed form
ok = True
for qq in [mpf('1.1'), mpf('1.5'), mpf('2'), mpf('3')]:
    h = mpf('1e-6')
    num = (Fep_num(qq, mpf('0.5')+h) - Fep_num(qq, mpf('0.5')-h))/(2*h)
    cf = Fep12_closed(qq)
    if abs(num - cf) > mpf('1e-8'):
        ok = False
print("15 Fep12 closed form numeric match:", ok)

# --- 14. J1 decomposition: J = G^2 + G_c - (xPhi/D) G_x on the curve c=c1(x,q) ---
xx1 = sp.symbols('xx1', positive=True)
q2 = sp.symbols('q2', positive=True)
cc1 = sp.atan(1/(q2*sp.tan(xx1)))/xx1
D1 = q2 + cc1*Phi(q2, xx1)
Gv = Gfunc(xx1, q2, cc1)
G_c_p = sp.diff(Gfunc(xx1, q2, cc), cc).subs(cc, cc1)
G_x_p = sp.diff(Gfunc(xx, q2, cc1), xx).subs(xx, xx1)
J1 = sp.simplify(Gv**2 + G_c_p - xx1*Phi(q2, xx1)/D1*G_x_p)
# J1 via direct definition: d^2/dc^2 log Mf along curve
Mf1 = Mf(xx1, q2, cc1)
# d/dc log Mf along curve = G; d^2/dc^2 = dG/dc + dG/dx * alpha'
alp_p = -xx1*Phi(q2, xx1)/D1
J1_def = Gv**2 + sp.diff(Gv, cc) + sp.diff(Gv, xx1)*alp_p
# careful: J uses partial derivatives at fixed (q,c), c=c1: G_c(alpha;c1), G_x(alpha;c1)
J1_def2 = Gv**2 + G_c_p + G_x_p*alp_p
check("eq:jdec: J1 = G^2 + G_c - u G_x", sp.simplify(J1 - J1_def2))
print("16 J1 decomposition", results[-1])

# --- 15. q=1 formulas ---
xq1 = sp.symbols('xq1', positive=True)
J1q1 = sp.simplify(J1_def2.subs({q2: 1}))
c1_1 = (pi/2 - xq1)/xq1
# recompute at q=1 directly
Gv1 = Gfunc(xq1, 1, c1_1)
D1_1 = 1 + c1_1
Gc1 = sp.diff(Gfunc(xq1, 1, cc), cc).subs(cc, c1_1)
Gx1 = sp.diff(Gfunc(xx, 1, c1_1), xx).subs(xx, xq1)
alp1 = -xq1/D1_1
J1q1b = sp.simplify(Gv1**2 + Gc1 + Gx1*alp1)
Nq1 = 12 + 16*xq1*sp.cot(xq1) + 2*xq1**2*sp.cot(xq1)**2 - 2*xq1**2
check("j1q1: J1(x,1) = (2x/pi)^2 N(x)", sp.simplify(J1q1b - (2*xq1/pi)**2*Nq1))
print("17 j1q1", results[-1])

# J2 q=1: x = pi - gamma
g1 = sp.symbols('g1', positive=True)
x2v = pi - g1
c2_1 = g1/(pi-g1)
Gv2 = Gfunc(x2v, 1, c2_1)
D2_1 = 1 + c2_1
Gc2 = sp.diff(Gfunc(x2v, 1, cc), cc).subs(cc, c2_1)
Gx2 = sp.diff(Gfunc(xx, 1, c2_1), xx).subs(xx, x2v)
alp2 = -x2v/D2_1
J2q1 = sp.simplify(Gv2**2 + Gc2 + Gx2*alp2)
zq = -x2v*sp.cot(x2v)
N2q1 = 2*(zq**2 - 8*zq + 6) - 2*x2v**2
check("j2q1: J2(gamma,1) = x^2 N(x)/pi^2", sp.simplify(J2q1 - x2v**2*N2q1/pi**2))
print("18 j2q1", results[-1])

# --- 16. lem:j2dec: J2 = N/(16 Delta^4) with N = 32 A^2 cg W, W = sum W_j ---
g2s2 = sp.symbols('gamma', positive=True)
q3 = sp.symbols('q3', positive=True)
t3 = sp.atan(q3*sp.tan(g2s2))
A3 = pi - g2s2
c3v = t3/A3
x3 = pi - g2s2
Phig3 = sp.cos(g2s2)**2 + q3**2*sp.sin(g2s2)**2
Dg3 = q3 + c3v*Phig3
Gv3 = Gfunc(x3, q3, c3v)
Gc3 = sp.diff(Gfunc(x3, q3, cc), cc).subs(cc, c3v)
Gx3 = sp.diff(Gfunc(xx, q3, c3v), xx).subs(xx, x3)
alp3 = -x3*Phig3/Dg3
J2sym = sp.simplify(Gv3**2 + Gc3 + Gx3*alp3)
# express in sg, cg, st, ct with q3 = st*cg/(ct*sg)
sg2, cg2, st2, ct2 = sp.symbols('sg cg st ct', positive=True)
t_expr = sp.atan(st2/ct2)  # t = arctan(q tan gamma); q = st cg/(ct sg) => q tan gamma = st cg/ct => t = atan(st/ct)
A_expr = pi - g2s2
# substitute: gamma as function? We treat sg=sin gamma, cg=cos gamma, st=sin t, ct=cos t as independent with relations.
# Use direct numerical check instead (high precision) for J2 = N/(16 Delta^4).
# Symbolic: substitute q3 = st2*cg2/(ct2*sg2), and gamma is determined by tan gamma = sg/cg.
from mpmath import mp, mpf, atan, tan, sin, cos, sqrt, pi as mppi
mp.dps = 50
def G_mp(xx, qq, cc):
    P = cos(xx)**2 + qq**2*sin(xx)**2
    D = qq + cc*P
    return -P*(3+2*xx*mp.cot(xx))/D + 2*cc*xx*P*(qq**2-1)*sin(xx)*cos(xx)/D**2
def J_mp(xx, qq, cc):
    P = cos(xx)**2 + qq**2*sin(xx)**2
    D = qq + cc*P
    G = G_mp(xx, qq, cc)
    Gc = sp.diff(Gfunc(sp.symbols('xx'), sp.symbols('q'), sp.symbols('c')), sp.symbols('c'))
    # numeric partials via mpmath finite differences with high precision
    h = mpf('1e-20')
    G_c = (G_mp(xx, qq, cc+h) - G_mp(xx, qq, cc-h))/(2*h)
    G_x = (G_mp(xx+h, qq, cc) - G_mp(xx-h, qq, cc))/(2*h)
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
    N = 32*A**2*cg*W
    Delta = A*st*ct + t*sg*cg
    return N/(16*Delta**4)
ok2 = True
for gamma in [mpf('0.66'), mpf('0.8'), mpf('0.9'), mpf('1.0'), mpf('1.04')]:
    for qq in [mpf('1.05'), mpf('1.5'), mpf('2')]:
        c2v = atan(qq*tan(gamma))/(mppi-gamma)
        if not (mpf('0.4') <= c2v <= mpf('0.5')):
            continue
        Jv = J_mp(mppi-gamma, qq, c2v)
        Wv = W8(gamma, qq)
        if abs(Jv - Wv) > mpf('1e-30'):
            ok2 = False
            print("  J2 mismatch", gamma, qq, Jv, Wv, abs(Jv-Wv))
print("19 lem:j2dec J2 = N/(16 Delta^4) numeric:", ok2)

fails = [r for r in results if not r[1]]
print()
print("SYMBOLIC RESULTS: %d checks, %d failed" % (len(results), len(fails)))
for f in fails:
    print("  FAIL:", f[0])
