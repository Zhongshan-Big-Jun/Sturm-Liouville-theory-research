# -*- coding: utf-8 -*-
"""sym_phi2.py - derive phi_2(b): second-order coefficient of the sheet
A_eps(b) = a0 + eps*phi(b) + eps^2*phi_2(b) + O(eps^3), at a = a0.
R1(A_eps(b), b, eps) = 0 with R1 = sin^2(s1 a)/n1 - sin^2(s2 a)/n2,
s_k = k*pi + s_k1*e + s_k2*e^2 + ..., R = 1+e.
Formula: phi_2 = -[R1^2(a0,b) + phi*d_a R1^1(a0,b) + f_const''(a0)*phi^2/2]/f_const'(a0).
Outputs numeric tables for verification + pickle of evaluated b-samples."""
import sympy as sp
import time, pickle, os
pi = sp.pi
t0 = time.time()
e, b = sp.symbols("e b", real=True)

# exact trig values at a0
s15 = sp.sqrt(15)
a0v = sp.acos(sp.Rational(1,4))/pi
sin_pa0 = s15/4; cos_pa0 = sp.Rational(1,4)
sin_2pa0 = 2*sin_pa0*cos_pa0          # s15/8
cos_2pa0 = 2*cos_pa0**2 - 1           # 1/8
sin_4pa0 = 2*sin_2pa0*cos_2pa0        # s15/32
cos_4pa0 = 2*cos_2pa0**2 - 1          # -31/32

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

# load s_k1, s_k2 closed forms (depend on a, b); evaluate at a = a0
d = pickle.load(open("pert_coeffs.pkl", "rb"))
a_sym = sp.symbols("a", real=True)
def ev_at_a0(expr_str):
    ex = sp.sympify(expr_str)
    return sp.simplify(sp.expand_trig(ex.subs(a_sym, a0v)))

s11b = ev_at_a0(d["s11"]); s12b = ev_at_a0(d["s12"])
s21b = ev_at_a0(d["s21"]); s22b = ev_at_a0(d["s22"])
print("s11b/s12b/s21b/s22b built %.1fs" % (time.time()-t0), flush=True)

# norm n(s, a0, b, R): from norm_mp formula with a = a0
s, R = sp.symbols("s R", real=True)
m = sp.sqrt(R); Lw = b - a0v; be = 1 - b
al = s*a0v; th = s*m*Lw
I1 = a0v/2 - sp.sin(2*al)/(4*s)
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
print("n_expr built %.1fs" % (time.time()-t0), flush=True)

def expand_n(s0, s1c, s2c):
    # s = s0 + s1c*e + s2c*e^2 ; R = 1+e ; expand n to order 2 in e
    se = s0 + s1c*e + s2c*e**2
    nsub = n_expr.subs({s: se, R: 1+e})
    nsub = sp.expand(sp.together(nsub))
    # series in e
    nser = sp.series(nsub, e, 0, 3).removeO()
    return sp.expand(nser)

n1_ser = expand_n(pi, s11b, s12b)
n2_ser = expand_n(2*pi, s21b, s22b)
print("n1_ser, n2_ser built %.1fs" % (time.time()-t0), flush=True)

def sin2_sa(s0, s1c, s2c, a):
    se = s0 + s1c*e + s2c*e**2
    return sp.expand(tsin(se*a)**2)

g1 = sp.expand(tsin((pi + s11b*e + s12b*e**2)*a0v)**2)
g2 = sp.expand(tsin((2*pi + s21b*e + s22b*e**2)*a0v)**2)
print("g1,g2 built %.1fs" % (time.time()-t0), flush=True)

def inv_ser(nser):
    c0 = nser.subs(e, 0)
    return sp.expand(1/c0 * (1 - (nser-c0)/c0 + ((nser-c0)/c0)**2))
R1_ser = sp.expand(g1*inv_ser(n1_ser) - g2*inv_ser(n2_ser))
R1_ser = sp.expand(sp.series(R1_ser, e, 0, 3).removeO())
print("R1_ser built %.1fs" % (time.time()-t0), flush=True)
p = sp.Poly(sp.expand(R1_ser), e)
R11 = sp.simplify(sp.expand_trig(p.coeff_monomial(e)))
R12 = sp.simplify(sp.expand_trig(p.coeff_monomial(e**2)))
print("R11, R12 extracted %.1fs" % (time.time()-t0), flush=True)
print("R11 =", R11)
print()
print("R12 =", R12)
