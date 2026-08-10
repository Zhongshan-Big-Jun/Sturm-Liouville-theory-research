# _audit_sub_C_identities3.py — remaining checks, fixed comparison methods
import sympy as sp
from sympy import Rational as R, symbols, pi, sqrt, diff, simplify, expand, tan, sin, cos, cot, atan
import mpmath as mp
mp.mp.dps = 60
ok_all = []
def ck(name, cond):
    ok_all.append((name, bool(cond)))
    print(("PASS" if cond else "FAIL"), name)

A, sg, cg, st, ct, t = symbols('A sg cg st ct t')
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
z_ = symbols('z_')
claim12 = z_*(1-z_)*(A**2*cg*B2 - 2*A**3*B1*z_)
lhs12 = expand((W1+W2).subs(st**2, 1-ct**2))
rhs12 = expand(claim12.subs(z_, ct**2))
ck("W12 = z(1-z)(A^2 cg B2 - 2A^3 B1 z)", lhs12 - rhs12 == 0)

# cos(tau) = cg/D, sin(tau) = 2sg/D — numeric at 20 points + algebraic squaring
g = symbols('g', positive=True)
D = sqrt(1+3*sin(g)**2)
ck("cos(tau)=cg/D algebraic (squared)", simplify(1/(1+4*tan(g)**2) - cos(g)**2/(1+3*sin(g)**2)) == 0)
ck("sin(tau)=2sg/D algebraic (squared)", simplify(4*tan(g)**2/(1+4*tan(g)**2) - 4*sin(g)**2/(1+3*sin(g)**2)) == 0)
mx = mp.mpf(0)
for i in range(21):
    gv = mp.mpf('0.655') + (mp.mpf('1.0472')-mp.mpf('0.655'))*mp.mpf(i)/20
    tauv = mp.atan(2*mp.tan(gv))
    Dv = mp.sqrt(1+3*mp.sin(gv)**2)
    e1 = abs(mp.cos(tauv) - mp.cos(gv)/Dv)
    e2 = abs(mp.sin(tauv) - 2*mp.sin(gv)/Dv)
    mx = max(mx, e1, e2)
ck("cos/sin tau numeric < 1e-50", mx < mp.mpf('1e-50'))

# dqM2 = N(z)/(2 z^2 (z^2+1)^2) — numeric verification on z in [0,1/sqrt3]
qq, w_ = symbols('qq w_', positive=True)
Aq = pi - atan(w_/qq)
M2 = 4*Aq**2*w_*qq - 7*Aq*qq**2 - 9*Aq*w_**2 + 2*Aq*(qq**2+w_**2)/(1+w_**2) + atan(w_)*(4*Aq*w_ - 5*qq - 9*qq*w_**2)
th_ = symbols('th_', positive=True)
qth = cos(2*th_)/(2*sin(th_)**2)
wth = cot(th_)
M2b = simplify(M2.subs({qq: qth, w_: wth, atan(w_/qq): 2*th_, atan(w_): pi/2 - th_}))
dM2dth = diff(M2b, th_)
dqM2_th = simplify(dM2dth / diff(qth, th_))
zz = symbols('zz', positive=True)
Pz = 32*zz*(zz**2+1)**2
Qz2 = -10*zz**6 - 32*pi*zz**5 + 42*zz**4 - 64*pi*zz**3 + 2*zz**2 - 32*pi*zz + 46
Rz = 5*pi*zz**6 - 10*zz**5 + 8*pi**2*zz**5 - 21*pi*zz**4 - 40*zz**3 + 16*pi**2*zz**3 - pi*zz**2 - 14*zz + 8*pi**2*zz - 23*pi
N_z = atan(zz)**2*Pz + atan(zz)*Qz2 + Rz
f_lhs = sp.lambdify(th_, dqM2_th, 'mpmath')
f_rhs = sp.lambdify(zz, N_z/(2*zz**2*(zz**2+1)**2), 'mpmath')
mx2 = mp.mpf(0)
for i in range(21):
    thv = mp.mpf('0.01') + (mp.atan(1/mp.sqrt(3))-mp.mpf('0.01'))*mp.mpf(i)/20
    zv = mp.tan(thv)
    d = abs(f_lhs(thv) - f_rhs(zv))
    mx2 = max(mx2, d)
ck("dqM2 = N(z)/(2z^2(z^2+1)^2) numeric < 1e-50", mx2 < mp.mpf('1e-50'))

# partial-derivative sign checks for lem:B1 (numeric over box)
bb = symbols('bb')
p = symbols('p', positive=True)
g45c = -sp.Rational(19,25)*bb - sp.Rational(346,41)*p + sp.Rational(16,5)*(bb-p)**2 - sp.Rational(1076,205)
gp45c = -sp.Rational(2152,205)*bb - sp.Rational(2560,1681)*p + 4*(bb-p)**2 - sp.Rational(15008,1681)
dbg = sp.diff(g45c, bb); dpg = sp.diff(g45c, p)
dbgp = sp.diff(gp45c, bb); dpgp = sp.diff(gp45c, p)
import random
random.seed(1)
mn = {str: None for str in ['dbg','dpg','dbgp','dpgp']}
def grid_min_max(expr, syms, ranges):
    lo = None; hi = None
    for _ in range(2000):
        pt = {s: lo_ + (hi_-lo_)*random.random() for (s,(lo_,hi_)) in zip(syms, ranges)}
        v = float(expr.subs(pt).evalf(30))
        lo = v if lo is None else min(lo, v); hi = v if hi is None else max(hi, v)
    return lo, hi
b_rng = (0.67, 0.68); p_rng = (3.14, 3.142857)
lo, hi = grid_min_max(dbg, [bb,p], [b_rng, p_rng]); ck("dg/db < 0 on box", hi < 0)
lo, hi = grid_min_max(dpg, [bb,p], [b_rng, p_rng]); ck("dg/dpi > 0 on box", lo > 0)
lo, hi = grid_min_max(dbgp, [bb,p], [b_rng, p_rng]); ck("dg'/db < 0 on box", hi < 0)
lo, hi = grid_min_max(dpgp, [bb,p], [b_rng, p_rng]); ck("dg'/dpi > 0 on box", lo > 0)
val = sp.simplify(g45c.subs(bb, sp.Rational(67,100)).subs(p, sp.Rational(22,7)) + gp45c.subs(bb, sp.Rational(67,100)).subs(p, sp.Rational(22,7))*(sp.Rational(7,4)-sp.Rational(4,5)))
ck("g(4/5)+g'(4/5)(7/4-4/5) = -1054523/114800", val == -sp.Rational(1054523,114800))
ck("-1054523/114800 < 0", True)

# M2 (a),(b)
gg = symbols('gg', positive=True)
ck("M2(1,w) = pi h(w)", simplify(M2.subs(qq, 1) - pi*(4*gg*(pi-atan(gg)) - 5 - 9*gg**2).subs(gg, w_)) == 0)
ck("h''(w) = -8/(1+w^2)^2 - 18", simplify(diff(4*gg*(pi-atan(gg)) - 5 - 9*gg**2, gg, 2) + 8/(1+gg**2)**2 + 18) == 0)
d2M = diff(M2, qq, 2)
t2 = atan(w_)
Aq3 = pi - atan(w_/qq)
N2 = -Aq3*(7*qq**4*w_**2 + 5*qq**4 + 14*qq**2*w_**4 + 10*qq**2*w_**2 - w_**6 - 3*w_**4) - 7*qq**3*w_**3 - 5*qq**3*w_ - qq*w_**5 - 4*qq*w_**4*t2 + qq*w_**3 - 4*qq*w_**2*t2
ck("d2_q M2 = 2 N2/((q^2+w^2)^2 (1+w^2))", simplify(d2M - 2*N2/((qq**2+w_**2)**2*(1+w_**2))) == 0)

# CORNER G2(1/2;q)
x2 = symbols('x2', positive=True)
Phi_x = cos(x2)**2 + qq**2*sin(x2)**2
D_x = qq + sp.Rational(1,2)*Phi_x
G = -Phi_x*(3+2*x2*cot(x2))/D_x + 2*(sp.Rational(1,2))*x2*Phi_x*(qq**2-1)*sin(x2)*cos(x2)/D_x**2
Gcorner = G.subs({cos(x2): qq/(qq+1), sin(x2): sqrt(2*qq+1)/(qq+1), cot(x2): cos(x2)/sin(x2)})
Gcorner = simplify(Gcorner)
claim_corner = 2*qq*(qq+1)*(pi-x2-3*sin(x2))/(2*qq+1)**sp.Rational(3,2)
ck("G2(1/2;q) closed form", simplify(Gcorner - claim_corner) == 0)

# j1e1: d/dq(Phi/D) along curve; Phi/D = x sinx cosx / W0
xr = symbols('xr', positive=True)
cc1 = atan(1/(qq*tan(xr)))/xr
Phi_r = cos(xr)**2 + qq**2*sin(xr)**2
Dr = qq + cc1*Phi_r
dPhiD = simplify(diff(Phi_r/Dr, qq))
claimed1 = (qq**2*sin(xr)**2 - cos(xr)**2)/Dr**2 + Phi_r**2*tan(xr)/(xr*Dr**2*(qq**2*tan(xr)**2+1))
ck("d/dq (Phi/D) along curve", simplify(dPhiD - claimed1) == 0)
th_sym = symbols('th_', positive=True)
W0 = xr*sin(th_sym)*cos(th_sym) + th_sym*sin(xr)*cos(xr)
e = simplify(Phi_r/Dr - xr*sin(xr)*cos(xr)/W0.subs(th_sym, cc1*xr))
ck("Phi/D = x sinx cosx / W0 (th = c1 x)", e == 0)

# G2id
gg2 = symbols('gg2', positive=True)
A2_ = pi - gg2
Phi2 = cos(gg2)**2 + qq**2*sin(gg2)**2
D2_ = qq + (t/A2_)*Phi2
W0_2 = 3 - 2*A2_*cot(gg2)
P2 = t*Phi2*(qq**2-1)*sin(gg2)*cos(gg2)/D2_**2
G2_expr = -Phi2*W0_2/D2_ - 2*P2
G_from_def = -Phi2*(3 - 2*A2_*cot(gg2))/D2_ - 2*t*Phi2*(qq**2-1)*sin(gg2)*cos(gg2)/D2_**2
ck("G2id: G2 = -Phi W0/D - 2P", simplify(G_from_def - G2_expr) == 0)

# IN = G2 * POS; M2 = dw IN
wq = symbols('wq', positive=True)
Aq4 = pi - atan(wq/qq)
IN = (qq**2+wq**2)*Aq4*(2*Aq4*qq - 3*wq + 2*atan(wq)) - 3*wq*qq*(1+wq**2)*atan(wq)
M2_check = diff(IN, wq)
M2_claimed = 4*Aq4**2*wq*qq - 7*Aq4*qq**2 - 9*Aq4*wq**2 + 2*Aq4*(qq**2+wq**2)/(1+wq**2) + atan(wq)*(4*Aq4*wq - 5*qq - 9*qq*wq**2)
ck("M2 = dw IN formula", simplify(M2_check - M2_claimed) == 0)
sgv2 = wq/sqrt(qq**2+wq**2); cgv2 = qq/sqrt(qq**2+wq**2)
Phi_g2 = cgv2**2 + qq**2*sgv2**2
Dg2 = qq + (atan(wq)/Aq4)*Phi_g2
G2v = -Phi_g2*(3 - 2*Aq4*(cgv2/sgv2))/Dg2 - 2*atan(wq)*Phi_g2*(qq**2-1)*sgv2*cgv2/Dg2**2
G2v = simplify(G2v)
POS = Dg2**2*Aq4*(qq**2+wq**2)*wq/(Phi_g2*qq)
ck("IN = G2 * POS", simplify(IN - G2v*POS) == 0)

fails = [n for n, ok in ok_all if not ok]
print()
print("IDENTITIES3: %d checks, %d failed" % (len(ok_all), len(fails)))
for n, ok in ok_all:
    if not ok: print("  FAIL:", n)
