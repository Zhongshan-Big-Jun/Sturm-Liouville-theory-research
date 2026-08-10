# -*- coding: utf-8 -*-
"""phi2_closed.py - build phi_2(b) and phi_2'(b) as factored lambdifiable
expressions.  phi_2(b) = -[R1^2(a0,b) + phi(b)*d_a R1^1(a0,b)
+ f_const''(a0)*phi(b)^2/2]/f_const'(a0).  Validate vs high-precision data."""
import sympy as sp
import pickle, time, os
import numpy as np
pi = sp.pi
t0 = time.time()
d = pickle.load(open("R1_eps_coeffs.pkl", "rb"))
R11 = sp.sympify(d["R11"]); R12 = sp.sympify(d["R12"])
syms = sorted(R11.free_symbols | R12.free_symbols, key=str)
a, b = syms[0], syms[1]
print("symbols:", a, b, flush=True)
dR11_a = sp.diff(R11, a)
print("dR11_a built %.1fs, size=%d" % (time.time()-t0, len(str(dR11_a))), flush=True)

s15 = sp.sqrt(15)
a0v = sp.acos(sp.Rational(1,4))/pi
f1 = 15*sp.pi**3*s15/4
f2 = -75*sp.pi**4/2

def phi_expr(bv):
    fc = 15*pi**3*s15/4
    R1_1 = pi*(1920*s15*pi**2*a0v**2 - 1920*s15*pi**2*a0v*bv + 64*s15*pi*a0v*sp.sin(2*pi*bv)
               + 448*s15*pi*a0v*sp.sin(4*pi*bv) + 2700*pi*a0v - 1920*pi*bv*sp.cos(2*pi*bv)**2
               + 960*pi*bv*sp.cos(2*pi*bv) + 960*pi*bv + 960*sp.sin(2*pi*bv) - 480*sp.sin(4*pi*bv)
               + 1920*pi*sp.cos(2*pi*bv)**2 - 960*pi*sp.cos(2*pi*bv) - 2310*pi - 225*s15)/1024
    return -R1_1/fc
phi_b = phi_expr(b)
R12_a0 = R12.subs(a, a0v)
dR11_a0 = dR11_a.subs(a, a0v)
phi2_expr = -(R12_a0 + phi_b*dR11_a0 + f2*phi_b**2/2)/f1
phi2p_expr = sp.diff(phi2_expr, b)
print("phi2 built %.1fs sizes %d %d" % (time.time()-t0, len(str(phi2_expr)), len(str(phi2p_expr))), flush=True)

f_phi2 = sp.lambdify(b, phi2_expr, "numpy")
f_phi2p = sp.lambdify(b, phi2p_expr, "numpy")
print("=== validation (measured: phi_2(b0)=-0.00613, phi_2'(0.58)~-0.138, max|phi_2'|~0.277) ===")
for bv in [0.45, 0.5, 0.55, 0.58, 0.58043, 0.7, 0.8, 0.9, 0.95, 0.99]:
    print("b=%.4f: phi_2=%.6f  phi_2'=%.6f" % (bv, float(f_phi2(bv)), float(f_phi2p(bv))))
bg = np.linspace(0.45, 0.99, 1000)
print("max|phi_2| =", max(abs(float(f_phi2(x))) for x in bg))
print("max|phi_2'| =", max(abs(float(f_phi2p(x))) for x in bg))
print("min phi_2' =", min(float(f_phi2p(x)) for x in bg))
with open("phi2_closed.pkl", "wb") as fh:
    pickle.dump({"phi2": str(phi2_expr), "phi2p": str(phi2p_expr)}, fh)
print("saved phi2_closed.pkl, total %.1fs" % (time.time()-t0))
