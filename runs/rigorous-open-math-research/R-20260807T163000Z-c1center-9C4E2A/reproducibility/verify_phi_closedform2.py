# -*- coding: utf-8 -*-
"""verify corrected closed form vs s33_r1plus.json + phi' positivity scan."""
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
    w1a = y1a/sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    uk0 = sp.sqrt(2)*sk
    return sp.expand(lp*uk0**2 + 2*(k*pi)**2*uk0*w1a)
R1_1 = sp.expand(R1_1_term(1) - R1_1_term(2))
R1_1 = sp.expand_trig(R1_1)
R1_1 = sp.expand(R1_1.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1}))
R1_1 = sp.simplify(sp.trigsimp(R1_1))
fc = sp.Rational(15,4)*pi**3*sp.sqrt(15)
phi = sp.simplify(-R1_1/fc)
dphi = sp.diff(phi, b)
a0e = sp.acos(sp.Rational(1,4))/pi
def ev(e, bv):
    bvf = float(sp.N(bv, 30))
    e2 = e.subs(b, sp.Float(bvf, 40))
    e2 = sp.expand_trig(e2)
    e2 = e2.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
    e2 = sp.expand(e2).subs(alpha, sp.Float(float(sp.N(a0e,30)), 40))
    return float(sp.N(e2, 35))
here = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(here, "s33_r1plus.json")))
print("cross-check vs s33_r1plus.json:", flush=True)
mx = 0.0
for row in ref["phi_table"]:
    bv = row["b"]; ref_phi = row["phi"]
    sv = ev(phi, bv)
    mx = max(mx, abs(sv-ref_phi))
    print("  b=%.4f ref=%.10f sym=%.10f diff=%.2e" % (bv, ref_phi, sv, abs(sv-ref_phi)), flush=True)
print("max diff = %.2e" % mx, flush=True)
print("phi(a0) = %.12e" % ev(phi, a0e), flush=True)
print("phi(b0) = %.12f" % ev(phi, 1-float(sp.N(a0e,30))), flush=True)
# phi' scan on [a0, 0.98]
import numpy as np
a0f = float(sp.N(a0e, 30))
grid = np.linspace(a0f, 0.98, 2001)
vals = np.array([ev(dphi, sp.Float(t, 40)) for t in grid])
print("dphi scan [a0,0.98]: min=%.6f max=%.6f pos=%s" % (vals.min(), vals.max(), bool((vals>0).all())), flush=True)
i0 = int(np.argmin(np.abs(grid - 0.5)))
print("sample dphi at b=0.5:", vals[i0], " grid[%d]=%.4f" % (i0, grid[i0]), flush=True)
