# -*- coding: utf-8 -*-
"""verify the closed form of phi(b) vs s33_r1plus.json (EVIDENCE only)."""
import sympy as sp
import json, os
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
def F(xx, k, c):
    return sp.Rational(1,2)*(xx*sp.cos(2*k*pi*c) - sp.sin(2*k*pi*xx - 2*k*pi*c)/(2*k*pi))
def G(xx, k):
    return sp.sin(k*pi*xx)**2/(2*k*pi)
def H(xx, k):
    return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)
def M(xx, k):
    return sp.Rational(1,2)*(-xx*sp.cos(2*k*pi*xx)/(2*k*pi) + sp.sin(2*k*pi*xx)/(4*k**2*pi**2) + alpha*sp.cos(2*k*pi*xx)/(2*k*pi))
def Bval(expr, lo, hi):
    return sp.expand(expr.subs(x, hi) - expr.subs(x, lo))
def lam_prime(k):
    return -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))
def R1_1_term(k):
    lp = lam_prime(k)
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
    w1a = y1a*sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    uk0 = sp.sqrt(2)*sk
    R1k = sp.expand(lp*uk0**2 + 2*(k*pi)**2*uk0*w1a)
    return sp.expand(R1k)
R11 = R1_1_term(1); R12 = R1_1_term(2)
R1_1 = sp.expand(R11 - R12)
s1 = sp.sqrt(15)/4; c1 = sp.Rational(1,4)
R1_1 = sp.expand_trig(R1_1)
R1_1 = sp.expand(R1_1.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1}))
R1_1 = sp.simplify(sp.trigsimp(R1_1))
fc = sp.Rational(15,4)*pi**3*sp.sqrt(15)
phi = sp.simplify(-R1_1/fc)
dphi = sp.diff(phi, b)
# also the same expression as a function of b only (alpha -> a0 as a number)
a0 = float(sp.acos(sp.Rational(1,4))/pi)
import mpmath as mp
mp.mp.dps = 40
phif = lambda t: complex(mp.mpf(str(sp.N(phi.subs({b: mp.mpf(t), alpha: mp.mpf(a0)}), 35))))
print("a0 =", a0)
here = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(here, "s33_r1plus.json")))
print("cross-check vs s33_r1plus.json (closed form vs reference):")
for row in ref["phi_table"]:
    bv = row["b"]; ref_phi = row["phi"]
    v = phif(bv)
    print("  b=%.4f ref=%.10f sym=%.10f diff=%.2e" % (bv, ref_phi, float(v.real), abs(float(v.real)-ref_phi)))
print()
print("phi(b) simplified (sin^4 -> cos forms):")
phi2 = sp.simplify(sp.expand(phi.rewrite(sp.cos)))
print(phi2)
print()
print("dphi simplified:")
dphi2 = sp.simplify(sp.expand(dphi.rewrite(sp.cos)))
print(dphi2)
print()
# check phi(b0) and phi(a0) values
b0 = 1 - a0
print("phi(a0) =", float(phif(a0).real))
print("phi(b0) =", float(phif(b0).real))
