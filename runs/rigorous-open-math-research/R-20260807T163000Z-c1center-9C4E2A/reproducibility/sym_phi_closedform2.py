# -*- coding: utf-8 -*-
"""sym_phi_closedform2.py - exact closed form of phi(b) via hand-derived antiderivatives.
[DERIVATION] all integrals elementary (no sympy integrate calls).
[EVIDENCE] numeric cross-checks vs s33_r1plus.json; not proofs."""
import sympy as sp
import json, os

x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi

# --- antiderivatives (verified by differentiation) ---
def F(xx, k, c):
    # Int sin(k pi x) sin(k pi (x-2c)) dx
    return sp.Rational(1,2)*(xx*sp.cos(2*k*pi*c) - sp.sin(2*k*pi*xx - 2*k*pi*c)/(2*k*pi))
def G(xx, k):
    # Int sin(k pi x) cos(k pi x) dx
    return sp.sin(k*pi*xx)**2/(2*k*pi)
def H(xx, k):
    # Int sin^2(k pi x) dx
    return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)
def M(xx, k):
    # Int (x-alpha) sin(k pi x) cos(k pi x) dx
    return sp.Rational(1,2)*(-xx*sp.cos(2*k*pi*xx)/(2*k*pi) + sp.sin(2*k*pi*xx)/(4*k**2*pi**2) + alpha*sp.cos(2*k*pi*xx)/(2*k*pi))

def Bval(expr, lo, hi):
    return sp.expand(expr.subs(x, hi) - expr.subs(x, lo))

def lam_prime(k):
    return -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))

def R1_1_term(k):
    lp = lam_prime(k)
    # y_k^1(alpha) = -(1/(k pi))*Term1(alpha) with Term1 = (lp/(k pi))*P_k(alpha)
    Pk = sp.sin(k*pi*alpha)/(2*k*pi) - alpha*sp.cos(k*pi*alpha)/2
    y1a = -(1/(k*pi))*(lp/(k*pi))*Pk
    # Q-int pieces
    # piece1: int_alpha^b sin(k pi x) Q(x; alpha, x) dx
    ant1 = (1/(4*k*pi))*(F(x,k,alpha) + H(x,k)) - sp.Rational(1,2)*M(x,k)
    p1 = Bval(ant1, alpha, b)
    # piece2: int_b^1 sin(k pi x) Q(x; alpha, b) dx
    ant2 = (1/(4*k*pi))*(F(x,k,alpha) - F(x,k,b)) - sp.Rational(1,2)*(b-alpha)*G(x,k)
    p2 = Bval(ant2, b, 1)
    Qint = sp.expand(p1 + p2)
    # P-int over [0,1] = 3/(8 k pi)
    Pint = sp.Rational(3,8)/(k*pi)
    # n_k^1 = 2 Int y0 y1 + Int_a^b y0^2 ; y0 = sin/(k pi)
    # 2 Int y0 y1 = -2/(k^2 pi^2) * [ (lp/(k pi))*Pint + (k pi)*Qint ]
    termA = -(2/(k**2*pi**2))*((lp/(k*pi))*Pint + (k*pi)*Qint)
    termB = (1/(k**2*pi**2))*(H(b,k) - H(alpha,k))
    nk1 = sp.expand(termA + termB)
    # w_k^1(alpha)
    nk0 = sp.Rational(1,2)/(k*pi)**2
    sk = sp.sin(k*pi*alpha)
    w1a = y1a*sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    uk0 = sp.sqrt(2)*sk
    R1k = sp.expand(lp*uk0**2 + 2*(k*pi)**2*uk0*w1a)
    return sp.expand(R1k)

print("computing R11, R12 ...", flush=True)
R11 = R1_1_term(1)
R12 = R1_1_term(2)
R1_1 = sp.expand(R11 - R12)
# substitute exact trig constants at alpha = a0
s1 = sp.sqrt(15)/4
c1 = sp.Rational(1,4)
R1_1 = sp.expand_trig(R1_1)
R1_1 = sp.expand(R1_1.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1}))
# replace any remaining sin/cos of (2*pi*alpha), (4*pi*alpha) etc. numerically-exactly
R1_1 = sp.expand(R1_1)
# final: collect by trig of b
R1_1 = sp.simplify(sp.trigsimp(R1_1))
fc = sp.Rational(15,4)*pi**3*sp.sqrt(15)
phi = sp.simplify(-R1_1/fc)
dphi = sp.simplify(sp.diff(phi, b))
print("a0 =", sp.N(sp.acos(sp.Rational(1,4))/pi, 20), flush=True)
print("R1_1 =", R1_1, flush=True)
print("phi(b) =", phi, flush=True)
print("phi'(b) =", dphi, flush=True)
a0v = sp.acos(sp.Rational(1,4))/pi
pts = [a0v, sp.Rational(45,100), sp.Rational(51,100), sp.Rational(6,10), sp.Rational(69,100), sp.Rational(77,100), sp.Rational(86,100), sp.Rational(95,100)]
for v in pts:
    print("b=%s: phi=%s  phi'=%s" % (sp.N(v,10), sp.N(phi.subs(b, v), 14), sp.N(dphi.subs(b, v), 14)), flush=True)
here = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(here, "s33_r1plus.json")))
print("cross-check vs s33_r1plus.json:", flush=True)
for row in ref["phi_table"]:
    bv = row["b"]; ref_phi = row["phi"]
    sym_phi = float(sp.N(phi.subs(b, sp.Float(bv)), 30))
    print("  b=%.4f ref=%.10f sym=%.10f diff=%.2e" % (bv, ref_phi, sym_phi, abs(sym_phi-ref_phi)), flush=True)
