# -*- coding: utf-8 -*-
"""sym_phi_secondorder.py - second-order perturbation of the sheet via the secular equation.
[DERIVATION] s_k(eps) = k*pi + s1k*eps + s2k*eps^2; then lambda_k, u_k(a), f(a), R1_1, R1_2, phi_2.
[EVIDENCE] numeric cross-checks vs the exact secular solver in verify_phi2_exact.py."""
import sympy as sp
import json, os, time
pi = sp.pi
a, b, e, s, x = sp.symbols("a b e s x", real=True)
q = sp.sqrt(1 + e)
w = b - a

t0 = time.time()
def F(s_):
    th = q*s_*w
    cb, sb = sp.cos(s_*(1-b)), sp.sin(s_*(1-b))
    sa, ca = sp.sin(s_*a), sp.cos(s_*a)
    ct, st = sp.cos(th), sp.sin(th)
    return cb*(sa*ct + ca*st/q) + sb*(ca*ct - q*sa*st)

def nk(s_, q_):
    w_ = b - a; be = 1 - b
    al = s_*a; th = q_*s_*w_
    I1 = a/2 - sp.sin(2*al)/(4*s_)
    Icc = w_/2 + sp.sin(2*th)/(4*q_*s_); Iss = w_/2 - sp.sin(2*th)/(4*q_*s_)
    Ics = sp.sin(th)**2/(2*q_*s_)
    sa = sp.sin(al); ca = sp.cos(al)
    I2 = sa**2*Icc + (ca/q_)**2*Iss + 2*sa*(ca/q_)*Ics
    yb = sa*sp.cos(th) + (ca/q_)*sp.sin(th)
    ypb = -q_*sp.sin(th)*sa + sp.cos(th)*ca
    Icc3 = be/2 + sp.sin(2*s_*be)/(4*s_); Iss3 = be/2 - sp.sin(2*s_*be)/(4*s_)
    Ics3 = sp.sin(s_*be)**2/(2*s_)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s_**2
    return (I1 + q_**2*I2)/s_**2 + I3

s1v, s2v = sp.symbols("s1v s2v", real=True)

def root_coeffs(k):
    s0 = k*pi
    se = s0 + s1v*e + s2v*e**2
    Fexp = sp.series(F(se), e, 0, 3).removeO()
    c1 = sp.simplify(sp.expand_trig(sp.diff(Fexp, e).subs(e, 0)))
    sol1 = sp.solve(sp.Eq(c1, 0), s1v)[0]
    c2 = sp.simplify(sp.expand_trig(sp.diff(Fexp, e, 2).subs(e, 0)/2))
    c2 = c2.subs(s1v, sol1)
    sol2 = sp.solve(sp.Eq(c2, 0), s2v)[0]
    return sol1, sol2

s11, s12 = root_coeffs(1)
s21, s22 = root_coeffs(2)
print("s11 =", sp.simplify(sp.expand_trig(s11)))
print("s12 =", sp.simplify(sp.expand_trig(s12)))
print("s21 =", sp.simplify(sp.expand_trig(s21)))
print("s22 =", sp.simplify(sp.expand_trig(s22)))
print("root coeffs done %.1fs" % (time.time()-t0), flush=True)

def lam_coeffs(k, s1, s2):
    # lambda = (k pi + s1 e + s2 e^2)^2
    lp = 2*k*pi*s1
    lpp = s1**2 + 2*k*pi*s2
    return sp.simplify(sp.expand_trig(lp)), sp.simplify(sp.expand_trig(lpp))

l1p, l1pp = lam_coeffs(1, s11, s12)
l2p, l2pp = lam_coeffs(2, s21, s22)
print("lambda1' =", l1p)
print("lambda1'' =", l1pp)
print("lambda2' =", l2p)
print("lambda2'' =", l2pp, flush=True)

def f_a_coeffs(k, s1, s2, order=2):
    """u_k(a)^2 = y_k(a)^2 / n_k expanded to order 2; lambda_k to order 2."""
    s0 = k*pi
    se = s0 + s1*e + s2*e**2
    qser = sp.series(q, e, 0, 3).removeO()
    yk = sp.sin(se*a)/se
    nke = sp.series(nk(se, qser), e, 0, 3).removeO()
    u2 = sp.series(yk**2/nke, e, 0, 3).removeO()
    lk = sp.series(se**2, e, 0, 3).removeO()
    fk = sp.series(lk*u2, e, 0, 3).removeO()
    c1 = sp.simplify(sp.expand_trig(sp.diff(fk, e).subs(e, 0)))
    c2 = sp.simplify(sp.expand_trig(sp.diff(fk, e, 2).subs(e, 0)/2))
    return c1, c2

f1_1, f1_2 = f_a_coeffs(1, s11, s12)
f2_1, f2_2 = f_a_coeffs(2, s21, s22)
R1_1 = sp.simplify(sp.expand_trig(f1_1 - f2_1))
R1_2 = sp.simplify(sp.expand_trig(f1_2 - f2_2))
print("R1_1(a,b) =", R1_1)
print("R1_2(a,b) =", R1_2, flush=True)

# phi and phi_2 at a = a0
s15 = sp.sqrt(15)
fc = sp.Rational(15,4)*pi**3*s15
a0 = sp.acos(sp.Rational(1,4))/pi

def ev(e2, bv, av=None):
    if av is None: av = a0
    e3 = e2.subs({a: av, b: sp.Float(bv, 40)})
    e3 = sp.expand_trig(e3)
    e3 = sp.expand(e3).subs(a0, sp.Float(float(a0), 40))
    return float(sp.N(e3, 25))

# R1_1(a0,b) vs known closed form (from sym_phi_closedform3, R1_1 expression at a=a0)
R1_1_a0 = R1_1.subs(a, a0)
# check numerically at a few b vs reference s33_r1plus.json
ref = json.load(open("s33_r1plus.json"))
print("R1_1(a0,b) vs ref:", flush=True)
ok = True
for row in ref["phi_table"][:8]:
    bv = row["b"]; ref_phi = row["phi"]
    r11 = ev(R1_1_a0, bv)
    ref_r11 = -ref_phi*fc  # phi = -R1_1/fc
    d = abs(r11 - ref_r11)
    ok = ok and d < 1e-6
    print("  b=%.4f R1_1=%.10f ref=%.10f diff=%.2e" % (bv, r11, ref_r11, d))
print("R1_1 match:", ok, flush=True)

# phi_2(b): -[ f_const''(a0) phi^2/2 + d_a R1_1(a0,b) phi + R1_2(a0,b) ] / f_const'(a0)
fc_a = sp.diff(2*pi**2*(sp.sin(pi*a)**2 - 4*sp.sin(2*pi*a)**2), a)
fca0 = sp.simplify(fc_a.subs(a, a0))
fc_aa = sp.simplify(sp.diff(fc_a, a).subs(a, a0))
phi = sp.simplify(-R1_1_a0/fc)
dR1_1a = sp.simplify(sp.expand_trig(sp.diff(R1_1, a).subs(a, a0)))
phi2 = sp.simplify(-(sp.Rational(1,2)*fc_aa*phi**2 + dR1_1a*phi + R1_2.subs(a, a0))/fc)
print("f_const'(a0) =", sp.simplify(fca0))
print("f_const''(a0) =", sp.simplify(fc_aa))
print("d_a R1_1(a0,b) =", dR1_1a, flush=True)
print("phi2(b) =", phi2, flush=True)

# numeric table of phi, phi2 at sample b
pts = [sp.Float(float(a0), 20), sp.Rational(45,100), sp.Rational(5,10), sp.Rational(6,10), sp.Rational(7,10), sp.Rational(8,10), sp.Rational(9,10)]
out = []
for v in pts:
    out.append(dict(b=float(v), phi=ev(phi, v), phi2=ev(phi2, v)))
    print("b=%.4f  phi=%.10f  phi2=%.10f" % (float(v), out[-1]["phi"], out[-1]["phi2"]), flush=True)
json.dump(out, open("phi2_table.json", "w"), indent=1)
print("total %.1fs" % (time.time()-t0))
