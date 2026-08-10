# -*- coding: utf-8 -*-
"""sym_phi_closedform.py - exact closed form of phi(b) = -R1_1(a0; a0, b)/f_const'(a0)
[DERIVATION] first-order perturbation theory (all integrals elementary).
[EVIDENCE] numeric cross-checks printed; not proofs."""
import sympy as sp
import json, os

x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
# exact trig constants at a0 = acos(1/4)/pi
s1 = sp.sqrt(15)/4
c1 = sp.Rational(1,4)

def trigs_const(expr):
    # expand sin(n*pi*alpha), cos(n*pi*alpha) to polynomials in sin(pi*alpha), cos(pi*alpha)
    e = sp.expand_trig(expr)
    e = e.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
    e = sp.expand(e)
    return sp.simplify(e)

def lam_prime(k):
    return -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))

def A_k(xx, k):
    return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)

def term1(xx, k, lp):
    return (lp/(k*pi))*(sp.sin(k*pi*xx)/(2*k*pi) - xx*sp.cos(k*pi*xx)/2)

def term2(xx, k, xp):
    return (sp.Rational(1,4))*(sp.sin(k*pi*(xx-2*alpha)) - sp.sin(k*pi*(xx-2*xp))) - (k*pi/2)*(xp-alpha)*sp.cos(k*pi*xx)

def R1_1_term(k):
    print("  k=%d: lambda_prime..." % k)
    lp = lam_prime(k)
    print("  k=%d: y1(a0)..." % k)
    y1a = -(1/(k*pi))*term1(alpha, k, lp)
    print("  k=%d: J1..." % k)
    J1 = sp.integrate(sp.sin(k*pi*x)*term1(x, k, lp), (x, 0, 1))
    print("  k=%d: J2b..." % k)
    J2b = sp.integrate(sp.sin(k*pi*x)*term2(x, k, x), (x, alpha, b))
    print("  k=%d: J2c..." % k)
    J2c = sp.integrate(sp.sin(k*pi*x)*term2(x, k, b), (x, b, 1))
    J2 = J2b + J2c
    nk1 = -(2/(k**2*pi**2))*(J1 + J2) + (1/(k**2*pi**2))*(A_k(b, k) - A_k(alpha, k))
    nk0 = sp.Rational(1,2)/(k*pi)**2
    sk = sp.sin(k*pi*alpha)
    w1a = y1a*sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    uk0 = sp.sqrt(2)*sk
    R1k = lp*uk0**2 + 2*(k*pi)**2*uk0*w1a
    print("  k=%d: simplify constants..." % k)
    R1k = trigs_const(sp.expand(R1k))
    return sp.factor(sp.expand(R1k))

print("step 1/3: compute R1_1 terms")
R11 = R1_1_term(1)
print("R11 done")
R12 = R1_1_term(2)
print("R12 done")
R1_1 = sp.expand(R11 - R12)
R1_1 = trigs_const(R1_1)
print("step 2/3: phi and phi'")
fc = sp.Rational(15,4)*pi**3*sp.sqrt(15)
phi = sp.simplify(-R1_1/fc)
dphi = sp.simplify(sp.diff(phi, b))
print("step 3/3: output")
print("a0 =", sp.N(sp.acos(sp.Rational(1,4))/pi, 20))
print("R1_1 =", R1_1)
print()
print("phi(b) =", phi)
print()
print("phi'(b) =", dphi)
print()
a0v = sp.acos(sp.Rational(1,4))/pi
pts = [a0v, sp.Rational(45,100), sp.Rational(51,100), sp.Rational(6,10), sp.Rational(69,100), sp.Rational(77,100), sp.Rational(86,100), sp.Rational(95,100)]
for v in pts:
    print("b=%s: phi=%s  phi'=%s" % (sp.N(v,10), sp.N(phi.subs(b, v), 14), sp.N(dphi.subs(b, v), 14)))
here = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(here, "s33_r1plus.json")))
print()
print("cross-check vs s33_r1plus.json:")
for row in ref["phi_table"]:
    bv = row["b"]; ref_phi = row["phi"]
    sym_phi = float(sp.N(phi.subs(b, sp.Float(bv)), 30))
    print("  b=%.4f ref=%.10f sym=%.10f diff=%.2e" % (bv, ref_phi, sym_phi, abs(sym_phi-ref_phi)))
