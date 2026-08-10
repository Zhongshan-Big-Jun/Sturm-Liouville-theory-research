# -*- coding: utf-8 -*-
"""sym_phi_closedform3.py - corrected closed form of phi(b) (w1a division bug fixed).
[DERIVATION] all integrals elementary (closed-form antiderivatives).
[EVIDENCE] numeric cross-checks vs s33_r1plus.json; not proofs."""
import sympy as sp
import json, os
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
s1 = sp.sqrt(15)/4; c1 = sp.Rational(1,4)

def H(xx, k): return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)
def F(xx, k, c): return sp.Rational(1,2)*(xx*sp.cos(2*k*pi*c) - sp.sin(2*k*pi*xx-2*k*pi*c)/(2*k*pi))
def G(xx, k): return sp.sin(k*pi*xx)**2/(2*k*pi)
def M(xx, k): return sp.Rational(1,2)*(-xx*sp.cos(2*k*pi*xx)/(2*k*pi) + sp.sin(2*k*pi*xx)/(4*k**2*pi**2) + alpha*sp.cos(2*k*pi*xx)/(2*k*pi))
def Bval(e, lo, hi): return sp.expand(e.subs(x, hi) - e.subs(x, lo))

def R1_1_term(k):
    lp = -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))
    Pk = sp.sin(k*pi*alpha)/(2*k*pi) - alpha*sp.cos(k*pi*alpha)/2
    y1a = -(1/(k*pi))*(lp/(k*pi))*Pk
    ant1 = (1/(4*k*pi))*(F(x,k,alpha) + H(x,k)) - sp.Rational(1,2)*M(x,k)
    p1 = Bval(ant1, alpha, b)
    ant2 = (1/(4*k*pi))*(F(x,k,alpha) - F(x,k,b)) - sp.Rational(1,2)*(b-alpha)*G(x,k)
    p2 = Bval(ant2, b, 1)
    Qint = sp.expand(p1 + p2)
    Pint = sp.Rational(3,8)/(k*pi)
    termA = -(2/(k**2*pi**2))*((lp/(k*pi))*Pint + (k*pi)*Qint)
    termB = (1/(k**2*pi**2))*(H(b,k) - H(alpha,k))
    nk1 = sp.expand(termA + termB)
    nk0 = sp.Rational(1,2)/(k*pi)**2
    sk = sp.sin(k*pi*alpha)
    w1a = y1a/sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)   # CORRECTED: division
    uk0 = sp.sqrt(2)*sk
    R1k = sp.expand(lp*uk0**2 + 2*(k*pi)**2*uk0*w1a)
    return sp.expand(R1k)

R1_1 = sp.expand(R1_1_term(1) - R1_1_term(2))
R1_1 = sp.expand_trig(R1_1)
R1_1 = sp.expand(R1_1.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1}))
R1_1 = sp.simplify(sp.trigsimp(R1_1))
fc = sp.Rational(15,4)*pi**3*sp.sqrt(15)
phi = sp.simplify(-R1_1/fc)
dphi = sp.diff(phi, b)
a0 = sp.acos(sp.Rational(1,4))/pi
print("R1_1 =", R1_1, flush=True)
print("phi(b) =", phi, flush=True)
print("phi'(b) =", dphi, flush=True)
# numeric eval helper
def ev(e, bv):
    e2 = e.subs(b, sp.Float(bv, 35))
    e2 = sp.expand_trig(e2)
    e2 = e2.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
    e2 = sp.expand(e2).subs(alpha, sp.Float(float(a0), 35))
    return float(sp.N(e2, 30))
print("a0 =", float(a0))
pts = [a0, sp.Rational(45,100), sp.Rational(51,100), sp.Rational(6,10), sp.Rational(69,100), sp.Rational(77,100), sp.Rational(86,100), sp.Rational(95,100)]
for v in pts:
    print("b=%s: phi=%s  phi'=%s" % (sp.N(v,10), ev(phi, v), ev(dphi, v)), flush=True)
here = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(here, "s33_r1plus.json")))
print("cross-check vs s33_r1plus.json:", flush=True)
for row in ref["phi_table"]:
    bv = row["b"]; ref_phi = row["phi"]
    sv = ev(phi, bv)
    print("  b=%.4f ref=%.10f sym=%.10f diff=%.2e" % (bv, ref_phi, sv, abs(sv-ref_phi)), flush=True)
print("phi(a0) =", ev(phi, float(a0)))
print("phi(b0) =", ev(phi, 1-float(a0)))
