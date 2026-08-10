# -*- coding: utf-8 -*-
"""R1_eps_coeffs.py - build R1_1(a,b) = d R1/d eps|0 and R1_2(a,b) = d^2 R1/d eps^2|0
as FACTORED sympy expressions (no expansion), lambdify-able for interval arithmetic.
R1 = g1/n1 - g2/n2, g_k = sin^2(s_k a), n_k = n(s_k, a, b, 1+e),
s_k(e) = k*pi + s_k1 e + s_k2 e^2.
Pieces: n, n_s, n_R, n_ss, n_sR, n_RR, g, g_s, g_ss at (s=k*pi, R=1).
Output: R1_eps_coeffs.pkl with lambdified float+iv functions; numeric validation vs FD."""
import sympy as sp
import pickle, time, os
import numpy as np
pi = sp.pi
t0 = time.time()
a, b, s, R = sp.symbols("a b s R", real=True)
m = sp.sqrt(R); Lw = b - a; be = 1 - b
al = s*a; th = s*m*Lw
I1 = a/2 - sp.sin(2*al)/(4*s)
Icc = Lw/2 + sp.sin(2*th)/(4*s*m); Iss = Lw/2 - sp.sin(2*th)/(4*s*m)
Ics = sp.sin(th)**2/(2*s*m)
sa, ca = sp.sin(al), sp.cos(al)
I2 = sa**2*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
yb = sa*sp.cos(th) + (ca/m)*sp.sin(th)
ypb = -m*sp.sin(th)*sa + sp.cos(th)*ca
Icc3 = be/2 + sp.sin(2*s*be)/(4*s); Iss3 = be/2 - sp.sin(2*s*be)/(4*s)
Ics3 = sp.sin(s*be)**2/(2*s)
I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/s**2
n_expr = (I1 + R*I2)/s**2 + I3
g_expr = sp.sin(s*a)**2
n_s = sp.diff(n_expr, s); n_R = sp.diff(n_expr, R)
n_ss = sp.diff(n_s, s); n_sR = sp.diff(n_s, R); n_RR = sp.diff(n_R, R)
g_s = sp.diff(g_expr, s); g_ss = sp.diff(g_s, s)
print("pieces built %.1fs" % (time.time()-t0), flush=True)

d = pickle.load(open("pert_coeffs.pkl", "rb"))
s11 = sp.sympify(d["s11"]); s12 = sp.sympify(d["s12"])
s21 = sp.sympify(d["s21"]); s22 = sp.sympify(d["s22"])

def pieces_at(s0):
    sub = {s: s0, R: 1}
    return (n_expr.subs(sub), n_s.subs(sub), n_R.subs(sub), n_ss.subs(sub),
            n_sR.subs(sub), n_RR.subs(sub), g_expr.subs(sub), g_s.subs(sub), g_ss.subs(sub))

def R1k1(n0, ns, nR, g0, gs, sk1):
    gp = gs*sk1; np_ = ns*sk1 + nR
    return gp/n0 - g0*np_/n0**2

def R1k2(n0, ns, nR, nss, nsR, nRR, g0, gs, gss, sk1, sk2):
    # (1/2) d^2/deps^2 [g/n] at 0 ; g'' = gss*sk1^2 + gs*sk2 ; n'' = nss*sk1^2 + 2 nsR sk1 + nRR + ns*sk2
    gp = gs*sk1; gpp = gss*sk1**2 + 2*gs*sk2
    np_ = ns*sk1 + nR; npp = nss*sk1**2 + 2*nsR*sk1 + nRR + 2*ns*sk2
    # (g/n)''/2 = (gpp n - 2 gp np_ ... use: (g/n)'' = (gpp n - g npp)/n^2 - 2 (gp n - g np_) np_ / n^3 ... derive:
    # d(g/n) = (gp n - g np)/n^2 ; d2/2 = (1/2)[(gpp n + gp np - gp np - g npp)/n^2 - 2 (gp n - g np) np / n^3]
    #        = (1/2)[(gpp n - g npp)/n^2 - 2 (gp n - g np) np/n^3]
    return sp.Rational(1,2)*((gpp*n0 - g0*npp)/n0**2 - 2*(gp*n0 - g0*np_)*np_/n0**3)

p1 = pieces_at(pi); p2 = pieces_at(2*pi)
T1_1 = R1k1(p1[0], p1[1], p1[2], p1[6], p1[7], s11); T2_1 = R1k1(p2[0], p2[1], p2[2], p2[6], p2[7], s21)
R11_expr = T1_1 - T2_1
T1_2 = R1k2(p1[0], p1[1], p1[2], p1[3], p1[4], p1[5], p1[6], p1[7], p1[8], s11, s12); T2_2 = R1k2(p2[0], p2[1], p2[2], p2[3], p2[4], p2[5], p2[6], p2[7], p2[8], s21, s22)
R12_expr = T1_2 - T2_2
print("coeffs built %.1fs  sizes %d %d" % (time.time()-t0, len(str(R11_expr)), len(str(R12_expr))), flush=True)

# numeric validation vs high-precision FD of the exact R1
import mpmath as mp
mp.mp.dps = 40
def sec_mp(sv, av, bv, eps):
    q = mp.sqrt(1+eps)
    al = sv*av; be = sv*(1-bv); th = q*sv*(bv-av)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))
def norm_mp(sv, av, bv, eps):
    q = mp.sqrt(1+eps); Lw = bv-av; be = 1-bv
    al = sv*av; th = q*sv*Lw
    I1 = av/2 - mp.sin(2*al)/(4*sv)
    Icc = Lw/2 + mp.sin(2*th)/(4*q*sv); Iss = Lw/2 - mp.sin(2*th)/(4*q*sv)
    Ics = mp.sin(th)**2/(2*q*sv)
    s1, c1 = mp.sin(al), mp.cos(al)
    I2 = s1**2*Icc + (c1/q)**2*Iss + 2*s1*(c1/q)*Ics
    yb = s1*mp.cos(th) + (c1/q)*mp.sin(th)
    ypb = -q*mp.sin(th)*s1 + mp.cos(th)*c1
    Icc3 = be/2 + mp.sin(2*sv*be)/(4*sv); Iss3 = be/2 - mp.sin(2*sv*be)/(4*sv)
    Ics3 = mp.sin(sv*be)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + q**2*I2)/sv**2 + I3
def root_mp(k, av, bv, eps):
    return mp.findroot(lambda s: sec_mp(s, av, bv, eps), k*mp.pi, tol=1e-35, maxsteps=60)
def f_at(av, bv, eps):
    s1 = root_mp(1, av, bv, eps); s2 = root_mp(2, av, bv, eps)
    n1 = norm_mp(s1, av, bv, eps); n2 = norm_mp(s2, av, bv, eps)
    y1a = mp.sin(s1*av)/s1; y2a = mp.sin(s2*av)/s2
    return s1**2*y1a**2/n1 - s2**2*y2a**2/n2

fR11 = sp.lambdify((a, b), R11_expr, "numpy")
fR12 = sp.lambdify((a, b), R12_expr, "numpy")
a0v = float(mp.acos(mp.mpf(1)/4)/mp.pi)
print("=== validation vs FD ===")
for (av, bv) in [(a0v, 0.5), (a0v, 0.7), (a0v, 0.9), (a0v+0.01, 0.6), (a0v-0.02, 0.8)]:
    am, bm = mp.mpf(av), mp.mpf(bv)
    d1 = float(mp.diff(lambda e: f_at(am, bm, e), 0, 1))
    d2 = float(mp.diff(lambda e: f_at(am, bm, e), 0, 2))
    c1 = float(fR11(av, bv)); c2 = float(fR12(av, bv))
    print("(a=%.4f,b=%.3f): R11=%.6f vs FD %.6f (err %.1e);  R12=%.4f vs FD %.4f (err %.1e)"
          % (av, bv, c1, d1, abs(c1-d1), c2, d2, abs(c2-d2)))
with open("R1_eps_coeffs.pkl", "wb") as fh:
    pickle.dump({"R11": str(R11_expr), "R12": str(R12_expr)}, fh)
print("saved R1_eps_coeffs.pkl, total %.1fs" % (time.time()-t0))
