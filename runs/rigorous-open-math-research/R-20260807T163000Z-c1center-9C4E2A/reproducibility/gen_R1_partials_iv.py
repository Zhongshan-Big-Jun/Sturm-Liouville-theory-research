# -*- coding: utf-8 -*-
"""gen_R1_partials_iv.py v3 - R1, R1_a, R1_b for iv eval.  No expand (fast)."""
import sympy as sp
import pickle, time
pi = sp.pi
s, s1, s2, a, b, R = sp.symbols("s s1 s2 a b R", real=True)
t0 = time.time()
m = sp.sqrt(R); w = b - a
def Fexpr(sv):
    al = sv*a; be = sv*(1-b); th = sv*m*w
    ca, sa = sp.cos(al), sp.sin(al); cb, sb = sp.cos(be), sp.sin(be); ct, st = sp.cos(th), sp.sin(th)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca
def nexp(sv):
    al = sv*a; th = sv*m*w; L = w; be1 = 1-b
    I1 = a/2 - sp.sin(2*al)/(4*sv)
    Icc = L/2 + sp.sin(2*th)/(4*sv*m); Iss = L/2 - sp.sin(2*th)/(4*sv*m)
    Ics = sp.sin(th)**2/(2*sv*m)
    sa, ca = sp.sin(al), sp.cos(al)
    I2 = sa**2*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb = sa*sp.cos(th) + (ca/m)*sp.sin(th)
    ypb = -m*sp.sin(th)*sa + sp.cos(th)*ca
    Icc3 = be1/2 + sp.sin(2*sv*be1)/(4*sv); Iss3 = be1/2 - sp.sin(2*sv*be1)/(4*sv)
    Ics3 = sp.sin(sv*be1)**2/(2*sv)
    I3 = (yb**2*Icc3 + ypb**2*Iss3 + 2*yb*ypb*Ics3)/sv**2
    return (I1 + R*I2)/sv**2 + I3
Fs = sp.diff(Fexpr(s), s); Fa = sp.diff(Fexpr(s), a); Fb = sp.diff(Fexpr(s), b)
def d1da(sv): return -(Fa.subs(s, sv)/Fs.subs(s, sv))
def d1db(sv): return -(Fb.subs(s, sv)/Fs.subs(s, sv))
R1 = sp.sin(s1*a)**2/nexp(s1) - sp.sin(s2*a)**2/nexp(s2)
print("building R1_a ...", flush=True)
R1_a = sp.diff(R1, a) + sp.diff(R1, s1)*d1da(s1) + sp.diff(R1, s2)*d1da(s2)
print("building R1_b ...", flush=True)
R1_b = sp.diff(R1, b) + sp.diff(R1, s1)*d1db(s1) + sp.diff(R1, s2)*d1db(s2)
print("done %.1fs  sizes R1=%d R1_a=%d R1_b=%d" % (time.time()-t0, len(str(R1)), len(str(R1_a)), len(str(R1_b))), flush=True)
with open("R1_partials_exprs.pkl", "wb") as fh:
    pickle.dump({"R1": str(R1), "R1_a": str(R1_a), "R1_b": str(R1_b)}, fh)
print("saved")
