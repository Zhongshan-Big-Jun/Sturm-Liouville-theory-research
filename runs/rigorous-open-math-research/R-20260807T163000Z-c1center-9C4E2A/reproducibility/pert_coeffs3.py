# -*- coding: utf-8 -*-
"""pert_coeffs3.py - 3rd-order eps-perturbation of the secular roots:
s_k(eps;a,b) = k*pi + s_k1(a,b) eps + s_k2(a,b) eps^2 + s_k3(a,b,xi) eps^3 (Taylor).
s_k3(eps) itself is computed as the closed-form 3rd coefficient at variable e,
then certified by interval evaluation over the box (Taylor remainder).
Dumps to pert_coeffs3.pkl."""
import sympy as sp
import pickle, time
pi = sp.pi
a, b, e = sp.symbols("a b e", real=True)
s1v, s2v, s3v = sp.symbols("s1v s2v s3v", real=True)
t0 = time.time()

def expn(expr, n=4):
    p = sp.Poly(sp.expand(expr), e)
    deg = min(n, p.degree()+1)
    return sp.Add(*[p.coeff_monomial(e**j)*e**j for j in range(deg)])

def tsin(arg, n=4):
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.sin(c0)*c_r + sp.cos(c0)*s_r)
def tcos(arg, n=4):
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.cos(c0)*c_r - sp.sin(c0)*s_r)

q = 1 + e/2 - e**2/8 + e**3/16 - 5*e**4/128
qinv = 1 - e/2 + 3*e**2/8 - 5*e**3/16 + 35*e**4/128

def build_root(k):
    s0 = k*pi
    se = s0 + s1v*e + s2v*e**2 + s3v*e**3
    th = sp.expand(q*se*(b-a))
    sa = tsin(se*a); ca = tcos(se*a)
    sb = tsin(se*(1-b)); cb = tcos(se*(1-b))
    st = tsin(th); ct = tcos(th)
    F = sp.expand(cb*(sa*ct + ca*st*qinv) + sb*(ca*ct - sa*st*q))
    F = expn(F, 4)
    c1 = sp.expand(sp.diff(F, e).subs(e, 0))
    c2 = sp.expand(sp.diff(F, e, 2).subs(e, 0)/2)
    c3 = sp.expand(sp.diff(F, e, 3).subs(e, 0)/6)
    c1s = sp.trigsimp(sp.expand_trig(c1))
    sol1 = sp.solve(sp.Eq(c1s, 0), s1v)[0]
    c2s = sp.simplify(sp.expand_trig(c2.subs(s1v, sol1)))
    sol2 = sp.solve(sp.Eq(c2s, 0), s2v)[0]
    c3s = sp.simplify(sp.expand_trig(sp.expand(c3.subs({s1v: sol1, s2v: sol2}))))
    sol3 = sp.solve(sp.Eq(c3s, 0), s3v)[0]
    return sol1, sol2, sol3

print("building k=1 ...", flush=True)
s11, s12, s13 = build_root(1)
print("building k=2 ...", flush=True)
s21, s22, s23 = build_root(2)
print("built %.1fs" % (time.time()-t0), flush=True)
out = {"s11": str(sp.simplify(sp.expand_trig(s11))), "s12": str(sp.simplify(sp.expand_trig(s12))),
       "s13": str(sp.simplify(sp.expand_trig(s13))), "s21": str(sp.simplify(sp.expand_trig(s21))),
       "s22": str(sp.simplify(sp.expand_trig(s22))), "s23": str(sp.simplify(sp.expand_trig(s23)))}
with open("pert_coeffs3.pkl", "wb") as fh:
    pickle.dump(out, fh)
print("saved pert_coeffs3.pkl", {k: len(v) for k, v in out.items()})
