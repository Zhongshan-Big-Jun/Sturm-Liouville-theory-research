# -*- coding: utf-8 -*-
"""cert_gap1r_constants.py - CERTIFIED constants for the R->1+ A10 estimates.
All constants come from interval evaluation (mpmath.iv, 200-bit, cell-wise) of
explicit closed forms.  Output: cert_gap1r_constants.json (ASCII)."""
import mpmath as mp
from mpmath import iv
iv.prec = 200
import json, os

piI = iv.pi
s15I = iv.sqrt(15)
a0I = iv.atan2(s15I/4, iv.mpf(1)/4)/piI
a0f = float(mp.mpf(a0I.a))

def fconst1_iv(x):  # f_const' = 2 pi^3 (sin(2 pi x) - 8 sin(4 pi x))
    return 2*piI**3*(iv.sin(2*piI*x) - 8*iv.sin(4*piI*x))
def fconst2_iv(x):
    return 4*piI**4*(iv.cos(2*piI*x) - 16*iv.cos(4*piI*x))
def fconst3_iv(x):
    return -8*piI**5*(iv.sin(2*piI*x) - 64*iv.sin(4*piI*x))

def phi_iv(b):
    # closed form: phi(b) = s15 * [...] / (57600 pi^2)
    br = 57600*piI**2
    num = (-1920*s15I*piI**2*a0I**2 + 1920*s15I*piI**2*a0I*b
           - 64*s15I*piI*a0I*iv.sin(2*piI*b) - 448*s15I*piI*a0I*iv.sin(4*piI*b)
           - 2700*piI*a0I + 1920*piI*b*iv.cos(2*piI*b)**2 - 960*piI*b*iv.cos(2*piI*b)
           - 960*piI*b - 960*iv.sin(2*piI*b) + 480*iv.sin(4*piI*b)
           - 1920*piI*iv.cos(2*piI*b)**2 + 960*piI*iv.cos(2*piI*b)
           + 225*s15I + 2310*piI)
    return s15I*num/br

def dphi_iv(b):
    u = iv.cos(2*piI*b); v = iv.sin(2*piI*b)
    N = (56*piI*a0I - 6*s15I)*u**2 + (2*piI*a0I + 3*s15I)*u + (3*s15I - 58*piI*a0I) \
        + 2*s15I*piI*(1-b)*(1-4*u)*v
    return -N/(60*piI)

def cell_max(fn, lo, hi, n):
    """max of upper bound over n cells."""
    m = iv.mpf('-inf')
    for i in range(n):
        B = iv.mpf([mp.mpf(lo + (hi-lo)*i/n), mp.mpf(lo + (hi-lo)*(i+1)/n)])
        v = fn(B)
        if v.b > m: m = v.b
    return m
def cell_min_abs(fn, lo, hi, n):
    m = iv.mpf('inf')
    for i in range(n):
        B = iv.mpf([mp.mpf(lo + (hi-lo)*i/n), mp.mpf(lo + (hi-lo)*(i+1)/n)])
        v = fn(B)
        va = iv.fabs(v)
        if va.a < m: m = va.a
    return m

Da = 0.03
# f_const derivatives on [a0-Da, a0+Da]
F0 = cell_min_abs(fconst1_iv, a0f-Da, a0f+Da, 400)
F2 = cell_max(lambda x: iv.fabs(fconst2_iv(x)), a0f-Da, a0f+Da, 400)
F3 = cell_max(lambda x: iv.fabs(fconst3_iv(x)), a0f-Da, a0f+Da, 400)
print("F0 = min|f_const'|  on [a0-0.03,a0+0.03] = %s" % mp.nstr(F0, 15))
print("F2 = max|f_const''| = %s" % mp.nstr(F2, 15))
print("F3 = max|f_const'''| = %s" % mp.nstr(F3, 15))

# phi / phi' on [a0, 1]
N = 4000
P = cell_max(lambda b: iv.fabs(phi_iv(b)), a0f, 1.0, N)
Phi_max = cell_max(lambda b: iv.fabs(dphi_iv(b)), a0f, 1.0-1e-12, N)
c_phi_099 = cell_min_abs(dphi_iv, a0f, 0.99, N)
# c_phi on [a0, 0.9999] for the main-box P0
c_phi_9999 = cell_min_abs(dphi_iv, a0f, 0.9999, N)
print("P = max|phi| on [a0,1) = %s" % mp.nstr(P, 15))
print("Phi_max = max|phi'| on [a0,1) = %s" % mp.nstr(Phi_max, 15))
print("c_phi[0.99] = min phi' on [a0,0.99] = %s" % mp.nstr(c_phi_099, 15))
print("c_phi[0.9999] = min phi' on [a0,0.9999] = %s" % mp.nstr(c_phi_9999, 15))

# point values
phi_b0 = phi_iv(iv.mpf([mp.mpf(1-a0f), mp.mpf(1-a0f)]))
phi_1 = phi_iv(iv.mpf([mp.mpf(0.999999), mp.mpf(0.999999)]))
dphi_b0 = dphi_iv(iv.mpf([mp.mpf(1-a0f), mp.mpf(1-a0f)]))
print("phi(b0) = %s" % mp.nstr(phi_b0, 15))
print("phi(0.999999) ~ phi(1) = %s" % mp.nstr(phi_1, 15))
print("phi'(b0) = %s" % mp.nstr(dphi_b0, 15))

# C_tail (recompute, strict): phi'(b)*60pi >= C_tail*e^2 on b=1-e, e in (0,1/1000]
d1I = iv.mpf((mp.pi/1000)**2/6)
d2I = iv.mpf((mp.pi/1000)**2/2)
mI = 56*piI*a0I - 6*s15I
nI = 2*piI*a0I + 3*s15I
Plb = 2*piI**2*(1-d1I)**2*(2*mI*(1-d2I)**2 + nI)
Tub = 12*s15I*piI**2
Ctail = (Plb - Tub)/(60*piI)
print("C_tail lower bound = %s" % mp.nstr(Ctail.a, 15))
# exact phi''(1)/2 = (pi/15)(114 pi a0 - 15 sqrt15)/2  -- compare
exact = (piI/15)*(114*piI*a0I - 15*s15I)/2
print("phi''(1)/2 (exact closed form) = %s" % mp.nstr(exact, 15))

out = dict(
    Da=Da,
    F0=mp.nstr(F0, 20), F2=mp.nstr(F2, 20), F3=mp.nstr(F3, 20),
    P=mp.nstr(P, 20), Phi_max=mp.nstr(Phi_max, 20),
    c_phi_099=mp.nstr(c_phi_099, 20), c_phi_09999=mp.nstr(c_phi_9999, 20),
    phi_b0=mp.nstr(phi_b0, 20), phi_1=mp.nstr(phi_1, 20), dphi_b0=mp.nstr(dphi_b0, 20),
    C_tail_lb=mp.nstr(Ctail.a, 20), phi2_at1_exact=mp.nstr(exact, 20),
    note="interval evaluation, 200-bit, cell-wise; soundness = mpmath.iv directed rounding",
    a0=mp.nstr(a0I, 25))
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "cert_gap1r_constants.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written cert_gap1r_constants.json")
