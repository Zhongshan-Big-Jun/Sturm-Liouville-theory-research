# -*- coding: utf-8 -*-
"""pert_coeffs.py - generate and save s11,s12,s21,s22 (eps-perturbation of the
secular roots s_k(eps) = k*pi + s_k1(a,b)*eps + s_k2(a,b)*eps^2 + O(eps^3)).
Reuses the machinery of sym_phi_secondorder2.py; dumps to pert_coeffs.pkl."""
import sympy as sp
import pickle, time
pi = sp.pi
a, b, e = sp.symbols("a b e", real=True)
s1v, s2v = sp.symbols("s1v s2v", real=True)
t0 = time.time()

def exp2(expr):
    p = sp.Poly(sp.expand(expr), e)
    return sp.Add(*[p.coeff_monomial(e**j)*e**j for j in range(min(3, p.degree()+1))])
def tsin(arg, n=3):
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.sin(c0)*c_r + sp.cos(c0)*s_r)
def tcos(arg, n=3):
    c0 = arg.subs(e, 0)
    rest = sp.expand(arg - c0)
    s_r = sp.series(sp.sin(rest), e, 0, n).removeO()
    c_r = sp.series(sp.cos(rest), e, 0, n).removeO()
    return sp.expand(sp.cos(c0)*c_r - sp.sin(c0)*s_r)
q2 = 1 + e/2 - e**2/8 + e**3/16
qinv2 = 1 - e/2 + 3*e**2/8
def build_root(k):
    s0 = k*pi
    se = s0 + s1v*e + s2v*e**2
    th = sp.expand(q2*se*(b-a))
    sa = tsin(se*a); ca = tcos(se*a)
    sb = tsin(se*(1-b)); cb = tcos(se*(1-b))
    st = tsin(th); ct = tcos(th)
    F = sp.expand(cb*(sa*ct + ca*st*qinv2) + sb*(ca*ct - sa*st*q2))
    F = exp2(F)
    c1 = sp.expand(sp.diff(F, e).subs(e, 0))
    c2 = sp.expand(sp.diff(F, e, 2).subs(e, 0)/2)
    c1s = sp.trigsimp(sp.expand_trig(c1))
    sol1 = sp.solve(sp.Eq(c1s, 0), s1v)[0]
    c2s = sp.simplify(sp.expand_trig(c2.subs(s1v, sol1)))
    sol2 = sp.solve(sp.Eq(c2s, 0), s2v)[0]
    return sol1, sol2
s11, s12 = build_root(1)
s21, s22 = build_root(2)
print("built %.1fs" % (time.time()-t0), flush=True)
out = {"s11": str(sp.simplify(sp.expand_trig(s11))),
       "s12": str(sp.simplify(sp.expand_trig(s12))),
       "s21": str(sp.simplify(sp.expand_trig(s21))),
       "s22": str(sp.simplify(sp.expand_trig(s22)))}
with open("pert_coeffs.pkl", "wb") as fh:
    pickle.dump(out, fh)
print("saved pert_coeffs.pkl, sizes:", {k: len(v) for k, v in out.items()})
