# -*- coding: utf-8 -*-
"""sym_R11.py - derive R1_1(a,b) = d/deps R1(a,b,eps)|_{eps=0} in closed form,
using s_k1 (first-order root coefficients, small closed forms) and the norm
partials at eps=0.  R1 = sin^2(s1 a)/n1 - sin^2(s2 a)/n2.
Output: pickle R11.pkl with the expression (factored) + numeric spot checks."""
import sympy as sp
import pickle, time, os
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
print("base built %.1fs" % (time.time()-t0), flush=True)

# partials at general (s, a, b, R); then specialize R=1, s=k*pi
def part(expr, x):
    return sp.diff(expr, x)
n_s = part(n_expr, s); n_R = part(n_expr, R)
g_s = part(g_expr, s)
print("partials %.1fs" % (time.time()-t0), flush=True)

d = pickle.load(open("pert_coeffs.pkl", "rb"))
s11 = sp.sympify(d["s11"]); s21 = sp.sympify(d["s21"])
print("s_k1 loaded %.1fs" % (time.time()-t0), flush=True)

def coeff1(k, sk1, n0, n_s0, n_R0, g0, g_s0):
    # R1_k^1 = g' / n - g n' / n^2 with g' = g_s*sk1, n' = n_s*sk1 + n_R (R'=1)
    gp = g_s0*sk1
    np_ = n_s0*sk1 + n_R0
    return sp.expand(gp/n0 - g0*np_/n0**2)

# specialize at R=1, s=k*pi (symbolic a, b)
def specialize(expr, s0):
    ex = expr.subs({R: 1, s: s0})
    return ex

n0_1 = specialize(n_expr, pi); n_s1 = specialize(n_s, pi); n_R1 = specialize(n_R, pi)
g0_1 = specialize(g_expr, pi); g_s1 = specialize(g_s, pi)
n0_2 = specialize(n_expr, 2*pi); n_s2 = specialize(n_s, 2*pi); n_R2 = specialize(n_R, 2*pi)
g0_2 = specialize(g_expr, 2*pi); g_s2 = specialize(g_s, 2*pi)
print("specialized %.1fs" % (time.time()-t0), flush=True)

term1 = coeff1(1, s11, n0_1, n_s1, n_R1, g0_1, g_s1)
term2 = coeff1(2, s21, n0_2, n_s2, n_R2, g0_2, g_s2)
R11_expr = sp.expand(term1 - term2)
print("R11 built %.1fs, size=%d" % (time.time()-t0, len(str(R11_expr))), flush=True)
# simplify moderately
R11_s = sp.trigsimp(sp.expand_trig(R11_expr))
print("R11 trigsimp %.1fs, size=%d" % (time.time()-t0, len(str(R11_s))), flush=True)
with open("R11.pkl", "wb") as fh:
    pickle.dump({"R11": str(R11_s)}, fh)
print("saved R11.pkl")
print("R11 head:", str(R11_s)[:200])
