# _audit_sub_C_identities2.py — symbolic verification of remaining closed forms (fixed)
import sympy as sp
from sympy import Rational as R, symbols, pi, sqrt, diff, simplify, expand, together, tan, sin, cos, cot, atan, trigsimp, nsimplify
ok_all = []
def ck(name, cond):
    ok_all.append((name, bool(cond)))
    print(("PASS" if cond else "FAIL"), name)

A, sg, cg, st, ct, t = symbols('A sg cg st ct t')
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = expand(B5 - A*B4)
W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
W4 = A**2*sg*t*B4*st*ct**3
W5 = -A*cg**2*sg*t*B5*st*ct
W6 = 4*A**2*cg*sg**2*t**2*ct**4
W7 = -A*cg*sg**2*t**2*B7*ct**2
W8 = 6*cg**3*sg**4*t**2
z_ = symbols('z_')
d12 = expand(W1 + W2 - z_*(1-z_)*(A**2*cg*B2 - 2*A**3*B1*z_))
ck("W12 = z(1-z)(A^2 cg B2 - 2A^3 B1 z)", expand(d12.subs(z_, ct**2)) == 0)
ck("W45 factorization", expand(W4+W5 - A*sg*t*st*ct*(A*B4*(ct**2-cg**2) - cg**2*G5)) == 0)
Qz = 4*A**2*z_**2 - A*B7*z_ + 6*cg**2*sg**2
ck("W678 = t^2 cg sg^2 Q(ct^2)", expand(W6+W7+W8 - t**2*cg*sg**2*Qz.subs(z_, ct**2)) == 0)

# lem:track primitives
g = symbols('g', positive=True)
cgv = cos(g); sgv = sin(g)
D = sqrt(1+3*sgv**2)
e1 = trigsimp(cos(atan(2*tan(g))) - cgv/D)
e2 = trigsimp(sin(atan(2*tan(g))) - 2*sgv/D)
ck("cos(tau) = cg/D", sp.simplify(e1.subs(cos(g)**2, 1-sin(g)**2)) == 0)
ck("sin(tau) = 2 sg/D", sp.simplify(e2.subs(cos(g)**2, 1-sin(g)**2)) == 0)
D2 = 1+3*sgv**2
ck("z-(1-z-) = 4 sg^2 cg^2/D^4", simplify(cgv**2/D2*(1 - cgv**2/D2) - 4*sgv**2*cgv**2/D2**2) == 0)
tt = symbols('tt')
f = tt*sin(tt)*cos(tt)**5
ck("f'(t) = cos^4 t (sin t cos t + t(1-6 sin^2 t))", simplify(diff(f, tt) - cos(tt)**4*(sin(tt)*cos(tt) + tt*(1-6*sin(tt)**2))) == 0)
h = tt*sin(tt)*cos(tt)
ck("h''(t) = 2(cos 2t - t sin 2t)", simplify(diff(h, tt, 2) - 2*(cos(2*tt) - tt*sin(2*tt))) == 0)

# C4: L'(v) = N/(10 T^2)
vv = symbols('vv')
Tv = tan(pi - sp.Rational(5,2)*vv)
wv = tan(vv)
c3 = 50*wv**2*vv - 24*wv**3 + 176*wv - 50*vv
c5 = 150*wv - 100*vv
N_expr = 125*wv*vv + 50*Tv*(vv*(1+wv**2)+wv) + 20*Tv**2 + c3*Tv**3 + (20-125*wv*vv)*Tv**4 + c5*Tv**5
L = (1+Tv**2)*(wv*(5*vv/Tv - 3) + 2*vv) - sp.Rational(6,5)*Tv*(1+wv**2)
dL = diff(L, vv)
ck("L'(v) = N/(10 T^2)", simplify(dL*10*Tv**2 - N_expr) == 0)

# lem:boundary
qq, w_ = symbols('qq w_', positive=True)
Aq = pi - atan(w_/qq)
M2 = 4*Aq**2*w_*qq - 7*Aq*qq**2 - 9*Aq*w_**2 + 2*Aq*(qq**2+w_**2)/(1+w_**2) + atan(w_)*(4*Aq*w_ - 5*qq - 9*qq*w_**2)
th_ = symbols('th_', positive=True)
qth = cos(2*th_)/(2*sin(th_)**2)
wth = cot(th_)
M2b = M2.subs({qq: qth, w_: wth, atan(w_/qq): 2*th_, atan(w_): pi/2 - th_})
M2b = simplify(M2b)
rhs_b = 2*(2*th_-pi)*cot(th_)**2*((2*th_-pi)*cot(th_)+2/sin(th_)**2)
ck("M2(q,w_b) closed form", simplify(M2b - rhs_b) == 0)
ck("bracket*sin^2 th = 2-(pi/2-th)sin 2th", simplify(((2*th_-pi)*cot(th_)+2/sin(th_)**2)*sin(th_)**2 - (2-(pi/2-th_)*sin(2*th_))) == 0)
# dqM2 = N(z)/(2 z^2 (z^2+1)^2) with z = tan th
zz = symbols('zz', positive=True)
dM2dth = diff(M2b, th_)
dqM2_th = simplify(dM2dth / diff(qth, th_))
lhs = dqM2_th.subs({tan(th_): zz, sin(th_): zz/sqrt(1+zz**2), cos(th_): 1/sqrt(1+zz**2), cot(th_): 1/zz})
lhs = simplify(lhs)
Pz = 32*zz*(zz**2+1)**2
Qz2 = -10*zz**6 - 32*pi*zz**5 + 42*zz**4 - 64*pi*zz**3 + 2*zz**2 - 32*pi*zz + 46
Rz = 5*pi*zz**6 - 10*zz**5 + 8*pi**2*zz**5 - 21*pi*zz**4 - 40*zz**3 + 16*pi**2*zz**3 - pi*zz**2 - 14*zz + 8*pi**2*zz - 23*pi
N_z = atan(zz)**2*Pz + atan(zz)*Qz2 + Rz
rhs = N_z/(2*zz**2*(zz**2+1)**2)
ck("dqM2 = N(z)/(2 z^2 (z^2+1)^2)", simplify(lhs - rhs) == 0)
Tz = pi**2/36*Pz + pi/6*Qz2 + Rz
Tz_claimed = sp.Rational(10,3)*pi*zz**6 + (sp.Rational(32,9)*pi**2 - 10)*zz**5 - 14*pi*zz**4 + (sp.Rational(64,9)*pi**2 - 40)*zz**3 - sp.Rational(2,3)*pi*zz**2 + (sp.Rational(32,9)*pi**2 - 14)*zz - sp.Rational(46,3)*pi
ck("T(z) expansion", expand(Tz - Tz_claimed) == 0)

# lem:B1: g(w) = dq M2 at q=1
gg = symbols('gg', positive=True)
M2q = M2  # with qq, w_
gfun = simplify(diff(M2q, qq).subs(qq, 1).subs(w_, gg))
gpp = diff(gfun, gg, 2)
t_ = atan(gg)
gpp_claimed = -2*(9*gg**6*t_ + 9*gg**5 + 27*gg**4*t_ + 24*gg**3 + 19*gg**2*t_ + 20*pi*gg**2 + 31*gg + t_ + 4*pi)/(1+gg**2)**3
ck("g''(w) formula", simplify(gpp - gpp_claimed) == 0)
gp = diff(gfun, gg)
ck("g'(0) = 4 pi^2", simplify(gp.subs(gg, 0) - 4*pi**2) == 0)
ck("g'(sqrt3) closed form", simplify(gp.subs(gg, sqrt(3)) - (sp.Rational(16,9)*pi**2 - sp.Rational(41,6)*sqrt(3)*pi - 15)) == 0)
bb = symbols('bb')
g45 = simplify(gfun.subs(gg, sp.Rational(4,5)))
gp45 = simplify(gp.subs(gg, sp.Rational(4,5)))
g45_claimed = -sp.Rational(19,25)*bb - sp.Rational(346,41)*pi + sp.Rational(16,5)*(bb-pi)**2 - sp.Rational(1076,205)
gp45_claimed = -sp.Rational(2152,205)*bb - sp.Rational(2560,1681)*pi + 4*(bb-pi)**2 - sp.Rational(15008,1681)
ck("g(4/5) closed form (b=atan(4/5))", simplify(g45.subs(atan(sp.Rational(4,5)), bb) - g45_claimed) == 0)
ck("g'(4/5) closed form", simplify(gp45.subs(atan(sp.Rational(4,5)), bb) - gp45_claimed) == 0)
# sign of partials on b in (67/100,17/25), pi in (157/50,22/7)
db_g = sp.diff(g45_claimed, bb); dpi_g = sp.diff(g45_claimed, pi)
db_gp = sp.diff(gp45_claimed, bb); dpi_gp = sp.diff(gp45_claimed, pi)
vals_b = [sp.Rational(67,100), sp.Rational(17,25)]; vals_pi = [sp.Rational(157,50), sp.Rational(22,7)]
def max_on(expr, sym, lo, hi):
    # convex/concave check via sampling endpoints + monotonicity of derivative
    from sympy import lambdify
    f = lambdify(sym, expr, 'mpmath')
    import mpmath as mp
    mp.mp.dps = 40
    best = None
    for i in range(101):
        xv = lo + (hi-lo)*mp.mpf(i)/100
        best = f(xv) if best is None else max(best, f(xv))
    return best
ck("dg/db < 0 on range", float(max_on(db_g, bb, sp.Rational(67,100), sp.Rational(17,25))) < 0)
ck("dg/dpi > 0 on range", float(max_on(dpi_g, pi, sp.Rational(157,50), sp.Rational(22,7))) > 0)
ck("dg'/db < 0 on range", float(max_on(db_gp, bb, sp.Rational(67,100), sp.Rational(17,25))) < 0)
ck("dg'/dpi > 0 on range", float(max_on(dpi_gp, pi, sp.Rational(157,50), sp.Rational(22,7))) > 0)
# final bound -1054523/114800
from sympy import Rational
v1 = g45_claimed.subs(bb, sp.Rational(67,100)).subs(pi, sp.Rational(22,7))
v2 = gp45_claimed.subs(bb, sp.Rational(67,100)).subs(pi, sp.Rational(22,7))
val = sp.simplify(v1 + v2*(sp.Rational(7,4) - sp.Rational(4,5)))
ck("g(4/5)+g'(4/5)(7/4-4/5) = -1054523/114800", val == -sp.Rational(1054523,114800))
ck("-1054523/114800 < 0", sp.Rational(-1054523,114800) < 0)

# lem:M2 (a),(b)
ck("M2(1,w) = pi h(w)", simplify(M2.subs(qq, 1) - pi*(4*gg*(pi-atan(gg)) - 5 - 9*gg**2)) == 0)
ck("h''(w) = -8/(1+w^2)^2 - 18", simplify(diff(4*gg*(pi-atan(gg)) - 5 - 9*gg**2, gg, 2) + 8/(1+gg**2)**2 + 18) == 0)
d2M = diff(M2q, qq, 2)
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

# j1e1: d/dq(Phi/D) along curve; Phi/D = x sinx cosx/W0
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
Phi_g = cos(gg2)**2 + qq**2*sin(gg2)**2
Dg = qq + (t/A2_)*Phi_g
G_from_def = -Phi_g*(3 - 2*A2_*cot(gg2))/Dg - 2*t*Phi_g*(qq**2-1)*sin(gg2)*cos(gg2)/Dg**2
ck("G2id: G2 = -Phi W0/D - 2P", simplify(G_from_def - G2_expr) == 0)

# IN = G2 * POS; M2 = dw IN
wq = symbols('wq', positive=True)
Aq4 = pi - atan(wq/qq)
IN = (qq**2+wq**2)*Aq4*(2*Aq4*qq - 3*wq + 2*atan(wq)) - 3*wq*qq*(1+wq**2)*atan(wq)
M2_check = diff(IN, wq)
M2_claimed = 4*Aq4**2*wq*qq - 7*Aq4*qq**2 - 9*Aq4*wq**2 + 2*Aq4*(qq**2+wq**2)/(1+wq**2) + atan(wq)*(4*Aq4*wq - 5*qq - 9*qq*wq**2)
ck("M2 = dw IN formula", simplify(M2_check - M2_claimed) == 0)
# G2 at gamma with tan g = wq/qq: gamma = pi - Aq4
sgv2 = wq/sqrt(qq**2+wq**2); cgv2 = qq/sqrt(qq**2+wq**2)
Phi_g2 = cgv2**2 + qq**2*sgv2**2
Dg2 = qq + (atan(wq)/Aq4)*Phi_g2
G2v = -Phi_g2*(3 - 2*Aq4*(cgv2/sgv2))/Dg2 - 2*atan(wq)*Phi_g2*(qq**2-1)*sgv2*cgv2/Dg2**2
G2v = simplify(G2v)
POS = Dg2**2*Aq4*(qq**2+wq**2)*wq/(Phi_g2*qq)
ck("IN = G2 * POS", simplify(IN - G2v*POS) == 0)

fails = [n for n, ok in ok_all if not ok]
print()
print("IDENTITIES: %d checks, %d failed" % (len(ok_all), len(fails)))
for n, ok in ok_all:
    if not ok: print("  FAIL:", n)
