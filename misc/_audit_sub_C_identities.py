# _audit_sub_C_identities.py — symbolic verification of remaining closed forms
import sympy as sp
from sympy import Rational as R, symbols, pi, sqrt, diff, simplify, expand, together, tan, sin, cos, cot, atan
ok_all = []
def ck(name, cond):
    ok_all.append((name, bool(cond)))
    print(("PASS" if cond else "FAIL"), name)

x, q, w, v, z, th = symbols('x q w v z th', positive=True)
b = symbols('b', real=True)

# ---------- 1. W-decompositions ----------
A, sg, cg, st, ct, t = symbols('A sg cg st ct t')
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
G5 = expand(B5 - A*B4)
W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
W3 = -2*A**3*sg*t*st*ct**5
W4 = A**2*sg*t*B4*st*ct**3
W5 = -A*cg**2*sg*t*B5*st*ct
W6 = 4*A**2*cg*sg**2*t**2*ct**4
W7 = -A*cg*sg**2*t**2*B7*ct**2
W8 = 6*cg**3*sg**4*t**2
z_ = symbols('z_')
ck("W12 = z(1-z)(A^2 cg B2 - 2A^3 B1 z)", expand(W1+W2 - z_*(1-z_)*(A**2*cg*B2 - 2*A**3*B1*z_)).subs(z_, ct**2) == 0)
ck("W45 = A sg t st ct (A B4 (ct^2-cg^2) - cg^2 G5)", expand(W4+W5 - A*sg*t*st*ct*(A*B4*(ct**2-cg**2) - cg**2*G5)) == 0)
Qz = 4*A**2*z_**2 - A*B7*z_ + 6*cg**2*sg**2
ck("W678 = t^2 cg sg^2 Q(ct^2)", expand(W6+W7+W8 - t**2*cg*sg**2*Qz.subs(z_, ct**2)) == 0)

# ---------- 2. lem:track ----------
g = symbols('g', positive=True)
cgv = cos(g); sgv = sin(g)
D = sqrt(1+3*sgv**2)
ck("cos(tau) = cg/D", simplify(cos(atan(2*tan(g))) - cgv/D) == 0)
ck("sin(tau) = 2 sg/D", simplify(sin(atan(2*tan(g))) - 2*sgv/D) == 0)
D2 = 1+3*sgv**2
ck("z-(1-z-) = 4 sg^2 cg^2/D^4", simplify(cgv**2/D2*(1 - cgv**2/D2) - 4*sgv**2*cgv**2/D2**2) == 0)
tt = symbols('tt')
f = tt*sin(tt)*cos(tt)**5
ck("f'(t) = cos^4 t (sin t cos t + t(1-6 sin^2 t))", simplify(diff(f, tt) - cos(tt)**4*(sin(tt)*cos(tt) + tt*(1-6*sin(tt)**2))) == 0)
h = tt*sin(tt)*cos(tt)
ck("h''(t) = 2(cos 2t - t sin 2t)", simplify(diff(h, tt, 2) - 2*(cos(2*tt) - tt*sin(2*tt))) == 0)

# ---------- 3. C4: L'(v) = N/(10 T^2) ----------
vv = symbols('vv')
Tv = tan(pi - sp.Rational(5,2)*vv)
wv = tan(vv)
c3 = 50*wv**2*vv - 24*wv**3 + 176*wv - 50*vv
c5 = 150*wv - 100*vv
N_expr = 125*wv*vv + 50*Tv*(vv*(1+wv**2)+wv) + 20*Tv**2 + c3*Tv**3 + (20-125*wv*vv)*Tv**4 + c5*Tv**5
L = (1+Tv**2)*(wv*(5*vv/Tv - 3) + 2*vv) - sp.Rational(6,5)*Tv*(1+wv**2)
dL = diff(L, vv)
ck("L'(v) = N/(10 T^2)", simplify(dL*10*Tv**2 - N_expr) == 0)

# ---------- 4. lem:boundary ----------
qq = symbols('qq')
wb = sqrt(2*qq+1)
s = wb
th_s = atan(1/s)
subs_b = {w: s, q: qq, x: None}
# M2(q,w)
Aq = pi - atan(w/qq)
M2 = 4*Aq**2*w*qq - 7*Aq*qq**2 - 9*Aq*w**2 + 2*Aq*(qq**2+w**2)/(1+w**2) + atan(w)*(4*Aq*w - 5*qq - 9*qq*w**2)
# express in theta: q = cos2th/(2 sin^2 th), w = cot th
th_ = symbols('th_')
qth = cos(2*th_)/(2*sin(th_)**2)
wth = cot(th_)
M2b = M2.subs({qq: qth, w: wth, atan(w/qq): 2*th_, atan(w): pi/2 - th_})
M2b = simplify(M2b)
rhs_b = 2*(2*th_-pi)*cot(th_)**2*((2*th_-pi)*cot(th_)+2/sin(th_)**2)
ck("M2(q,w_b) = 2(2th-pi)cot^2 th [(2th-pi)cot th + 2/sin^2 th]", simplify(M2b - rhs_b) == 0)
ck("bracket*sin^2 th = 2-(pi/2-th)sin 2th", simplify(((2*th_-pi)*cot(th_)+2/sin(th_)**2)*sin(th_)**2 - (2-(pi/2-th_)*sin(2*th_))) == 0)
# dqM2 = N(z)/(2 z^2 (z^2+1)^2)
zz = symbols('zz')
zsub = tan(th_)
qq2 = cos(2*th_)/(2*sin(th_)**2)
dM2dth = diff(M2b, th_)
dqM2_th = simplify(dM2dth / diff(qq2, th_))
Pz = 32*zz*(zz**2+1)**2
Qz = -10*zz**6 - 32*pi*zz**5 + 42*zz**4 - 64*pi*zz**3 + 2*zz**2 - 32*pi*zz + 46
Rz = 5*pi*zz**6 - 10*zz**5 + 8*pi**2*zz**5 - 21*pi*zz**4 - 40*zz**3 + 16*pi**2*zz**3 - pi*zz**2 - 14*zz + 8*pi**2*zz - 23*pi
N_z = atan(zz)**2*Pz + atan(zz)*Qz + Rz
lhs = dqM2_th.subs(tan(th_), zz).subs(sin(th_), zz/sqrt(1+zz**2)).subs(cos(th_), 1/sqrt(1+zz**2))
lhs = simplify(lhs)
rhs = N_z/(2*zz**2*(zz**2+1)**2)
ck("dqM2 = N(z)/(2 z^2 (z^2+1)^2)", simplify(lhs - rhs) == 0)
Tz = pi**2/36*Pz + pi/6*Qz + Rz
Tz_exp = expand(Tz)
Tz_claimed = sp.Rational(10,3)*pi*zz**6 + (sp.Rational(32,9)*pi**2 - 10)*zz**5 - 14*pi*zz**4 + (sp.Rational(64,9)*pi**2 - 40)*zz**3 - sp.Rational(2,3)*pi*zz**2 + (sp.Rational(32,9)*pi**2 - 14)*zz - sp.Rational(46,3)*pi
ck("T(z) expansion", expand(Tz_exp - Tz_claimed) == 0)

# ---------- 5. lem:B1 ----------
gg = symbols('gg')
t_ = atan(gg)
A1 = pi - atan(gg/1)
M2_1 = 4*A1**2*gg - 7*A1 - 9*A1*gg**2 + 2*A1*(1+gg**2)/(1+gg**2) + atan(gg)*(4*A1*gg - 5 - 9*gg**2)
gfun = diff(M2_1, qq).subs(qq, 1)
gfun = simplify(gfun)
gpp = diff(gfun, gg, 2)
gpp_claimed = -2*(9*gg**6*t_ + 9*gg**5 + 27*gg**4*t_ + 24*gg**3 + 19*gg**2*t_ + 20*pi*gg**2 + 31*gg + t_ + 4*pi)/(1+gg**2)**3
ck("g''(w) formula", simplify(gpp - gpp_claimed) == 0)
ck("g'(0) = 4 pi^2", simplify(diff(gfun, gg).subs(gg, 0) - 4*pi**2) == 0)
ck("g'(sqrt3) closed form", simplify(diff(gfun, gg).subs(gg, sqrt(3)) - (sp.Rational(16,9)*pi**2 - sp.Rational(41,6)*sqrt(3)*pi - 15)) == 0)
bb = symbols('bb')
gp45 = simplify(diff(gfun, gg).subs(gg, sp.Rational(4,5)))
g45 = simplify(gfun.subs(gg, sp.Rational(4,5)))
g45_claimed = -sp.Rational(19,25)*bb - sp.Rational(346,41)*pi + sp.Rational(16,5)*(bb-pi)**2 - sp.Rational(1076,205)
gp45_claimed = -sp.Rational(2152,205)*bb - sp.Rational(2560,1681)*pi + 4*(bb-pi)**2 - sp.Rational(15008,1681)
ck("g(4/5) closed form (b=arctan(4/5))", simplify(g45.subs(atan(sp.Rational(4,5)), bb) - g45_claimed) == 0)
ck("g'(4/5) closed form", simplify(gp45.subs(atan(sp.Rational(4,5)), bb) - gp45_claimed) == 0)
ck("dg/db < 0 at 4/5", sp.diff(g45_claimed, bb) < 0)
ck("dg/dpi > 0 at 4/5", sp.diff(g45_claimed, pi).subs(pi, sp.Rational(31415,10000)) > 0)
ck("dg'/db < 0", sp.diff(gp45_claimed, bb) < 0)
ck("dg'/dpi > 0", sp.diff(gp45_claimed, pi).subs(pi, sp.Rational(31415,10000)) > 0)

# ---------- 6. lem:M2 (a),(b) ----------
w_ = symbols('w_')
h_ = 4*w_*(pi - atan(w_)) - 5 - 9*w_**2
ck("M2(1,w) = pi h(w)", simplify(M2.subs(qq, 1) - pi*h_) == 0)
ck("h''(w) = -8/(1+w^2)^2 - 18", simplify(diff(h_, w_, 2) + 8/(1+w_**2)**2 + 18) == 0)
Aq2 = pi - atan(w_/qq)
M2q = 4*Aq2**2*w_*qq - 7*Aq2*qq**2 - 9*Aq2*w_**2 + 2*Aq2*(qq**2+w_**2)/(1+w_**2) + atan(w_)*(4*Aq2*w_ - 5*qq - 9*qq*w_**2)
d2 = diff(M2q, qq, 2)
t2 = atan(w_)
N2 = -Aq2*(7*qq**4*w_**2 + 5*qq**4 + 14*qq**2*w_**4 + 10*qq**2*w_**2 - w_**6 - 3*w_**4) - 7*qq**3*w_**3 - 5*qq**3*w_ - qq*w_**5 - 4*qq*w_**4*t2 + qq*w_**3 - 4*qq*w_**2*t2
ck("d2_q M2 = 2 N2/((q^2+w^2)^2 (1+w^2))", simplify(d2 - 2*N2/((qq**2+w_**2)**2*(1+w_**2))) == 0)

# ---------- 7. CORNER G2(1/2;q) ----------
q2 = symbols('q2', positive=True)
xx = acos_x = symbols('xx')
# x with cos x = q/(q+1)
Gx = symbols('Gx')
Phi_x = cos(x)**2 + q2**2*sin(x)**2
D_x = q2 + sp.Rational(1,2)*Phi_x
G = -Phi_x*(3+2*x*cot(x))/D_x + 2*(sp.Rational(1,2))*x*Phi_x*(q2**2-1)*sin(x)*cos(x)/D_x**2
# substitute cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1)
Gcorner = G.subs({cos(x): q2/(q2+1), sin(x): sqrt(2*q2+1)/(q2+1), cot(x): cos(x)/sin(x)})
Gcorner = simplify(Gcorner)
claim_corner = 2*q2*(q2+1)*(pi-x-3*sqrt(2*q2+1)/(q2+1))/(2*q2+1)**sp.Rational(3,2)
ck("G2(1/2;q) closed form", simplify(Gcorner - claim_corner.subs(sqrt(2*q2+1)/(q2+1), sin(x))) == 0)

# ---------- 8. j1e1: d/dq(Phi/D) along curve + Phi/D = x sinx cosx / W0 ----------
xr = symbols('xr', positive=True)
qqr = symbols('qqr', positive=True)
cc1 = atan(1/(qqr*tan(xr)))/xr
Phi_r = cos(xr)**2 + qqr**2*sin(xr)**2
Dr = qqr + cc1*Phi_r
dPhiD = simplify(diff(Phi_r/Dr, qqr))
claimed = (qqr**2*sin(xr)**2 - cos(xr)**2)/Dr**2 + Phi_r**2*tan(xr)/(xr*Dr**2*(qqr**2*tan(xr)**2+1))
ck("d/dq (Phi/D) along curve = claimed", simplify(dPhiD - claimed) == 0)
th_ = symbols('th_')
W0 = xr*sin(th_)*cos(th_) + th_*sin(xr)*cos(xr)
ck("Phi/D = x sinx cosx / W0 (th = c1 x)", simplify(Phi_r/Dr - xr*sin(xr)*cos(xr)/W0.subs(th_, cc1*xr)) == 0)

# ---------- 9. G2id ----------
gg2 = symbols('gg2')
A2_ = pi - gg2
Phi2 = cos(gg2)**2 + q**2*sin(gg2)**2
D2_ = q + (t/A2_)*Phi2
W0_2 = 3 - 2*A2_*cot(gg2)
P2 = (t/A2_)*A2_*Phi2*(q**2-1)*sin(gg2)*cos(gg2)/D2_**2
G2_expr = -Phi2*W0_2/D2_ - 2*P2
# compare with G(pi-gamma; t/A)
Phi_g = cos(gg2)**2 + q**2*sin(gg2)**2
Dg = q + (t/A2_)*Phi_g
G_from_def = -Phi_g*(3+2*A2_*cot(gg2)*(-1))/Dg + 2*(t/A2_)*A2_*Phi_g*(q**2-1)*sin(gg2)*(-cos(gg2))/Dg**2
ck("G2id: G2 = -Phi W0/D - 2P", simplify(G_from_def - G2_expr) == 0)

# ---------- 10. IN = G2 * POS ----------
wq = symbols('wq', positive=True)
Aq3 = pi - atan(wq/q)
IN = (q**2+wq**2)*Aq3*(2*Aq3*q - 3*wq + 2*atan(wq)) - 3*wq*q*(1+wq**2)*atan(wq)
M2q3 = diff(IN, wq)
M2_claimed = 4*Aq3**2*wq*q - 7*Aq3*q**2 - 9*Aq3*wq**2 + 2*Aq3*(q**2+wq**2)/(1+wq**2) + atan(wq)*(4*Aq3*wq - 5*q - 9*q*wq**2)
ck("M2 = dw IN formula", simplify(M2q3 - M2_claimed) == 0)
# IN = G2*POS: G2 at gamma = pi - A, with tan gamma = w/q
sgv2 = wq/sqrt(q**2+wq**2); cgv2 = q/sqrt(q**2+wq**2)
Phi_g2 = cgv2**2 + q**2*sgv2**2
Dg2 = q + (atan(wq)/Aq3)*Phi_g2
G2v = -Phi_g2*(3+2*Aq3*cot(pi-Aq3))/Dg2 + 2*(atan(wq)/Aq3)*Aq3*Phi_g2*(q**2-1)*sin(pi-Aq3)*cos(pi-Aq3)/Dg2**2
G2v = simplify(G2v)
POS = (q + (atan(wq)/Aq3)*Phi_g2)**2*Aq3*(q**2+wq**2)*wq/(Phi_g2*q)
ck("IN = G2 * POS", simplify(IN - G2v*POS) == 0)

fails = [n for n, ok in ok_all if not ok]
print()
print("IDENTITIES: %d checks, %d failed" % (len(ok_all), len(fails)))
for n, ok in ok_all:
    if not ok: print("  FAIL:", n)
