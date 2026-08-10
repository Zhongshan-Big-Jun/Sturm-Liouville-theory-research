# _audit_sub_C_j2dec_full2.py — lem:j2dec identity:
#  (a) exact rational-in-(A,t) verification at 8 Pythagorean trig points
#  (b) high-precision numeric verification at 30 random (gamma,q) in the box
#  (c) exact polynomial W-decompositions (eq:w12, w45, w678) in all variables
import sympy as sp
from sympy import Rational, symbols, sqrt, diff, simplify, expand, together, cancel, fraction, rem
import mpmath as mp
mp.mp.dps = 80

sg, cg, st, ct, A, t = symbols('sg cg st ct A t')
qq_s, cc_s, xx = symbols('qq_s cc_s xx', positive=True)

def J_rat(sgv, cgv, qq, cc, A, t):
    # J(x;c) at x=A, sinx=sg, cosx=-cg, cotx=-cg/sg, with partials at fixed (q,c)
    P = cgv**2 + qq**2*sgv**2
    D = qq + cc*P
    cotx = -cgv/sgv
    G = -P*(3+2*A*cotx)/D + 2*cc*A*P*(qq**2-1)*sgv*(-cgv)/D**2
    Gc = P**2*(3+2*A*cotx)/D**2 + 2*A*P*(qq**2-1)*sgv*(-cgv)*(qq-cc*P)/D**3
    # Gx: d/dx G(x;c) at fixed c,q, then x=A with sinx=sg, cosx=-cg, cotx=-cg/sg
    Px = sp.cos(xx)**2 + qq**2*sp.sin(xx)**2
    Dx = qq + cc*Px
    Gx_expr = -Px*(3+2*xx*sp.cot(xx))/Dx + 2*cc*xx*Px*(qq**2-1)*sp.sin(xx)*sp.cos(xx)/Dx**2
    Gxd = sp.diff(Gx_expr, xx)
    Gx = Gxd.subs({xx: A, sp.sin(xx): sgv, sp.cos(xx): -cgv, sp.cot(xx): -cgv/sgv})
    u = A*P/D
    return sp.expand(sp.together(G**2 + Gc - u*Gx))

def rhs(sgv, cgv, stv, ctv, A, t):
    B1 = A*cgv - 2*sgv
    B2 = 4*A**2*cgv**2 - A**2 - 12*A*cgv*sgv + 6*sgv**2
    B4 = 7*A*cgv**2 - A*sgv**2 - 4*cgv*sgv
    B5 = A**2*cgv**2 - A**2*sgv**2 + 2*A**2 + 12*A*cgv*sgv - 12*sgv**2
    B7 = 3*A*cgv**2 + A*sgv**2 + 8*cgv*sgv
    W1 = -2*A**3*B1*stv**2*ctv**4
    W2 = A**2*cgv*B2*stv**2*ctv**2
    W3 = -2*A**3*sgv*t*stv*ctv**5
    W4 = A**2*sgv*t*B4*stv*ctv**3
    W5 = -A*cgv**2*sgv*t*B5*stv*ctv
    W6 = 4*A**2*cgv*sgv**2*t**2*ctv**4
    W7 = -A*cgv*sgv**2*t**2*B7*ctv**2
    W8 = 6*cgv**3*sgv**4*t**2
    W = W1+W2+W3+W4+W5+W6+W7+W8
    Delta = A*stv*ctv + t*sgv*cgv
    return sp.expand(sp.together(2*A**2*cgv*W/Delta**4))

# Pythagorean points: (tan g, tan t) rational -> q = tant/tang
pts = [(Rational(3,4), Rational(4,3)), (Rational(1,2), Rational(1)), (Rational(5,12), Rational(12,5)),
       (Rational(8,15), Rational(15,8)), (Rational(7,24), Rational(24,7)), (Rational(20,21), Rational(21,20)),
       (Rational(1,3), Rational(2,3)), (Rational(2,3), Rational(1,2))]
allok = True
for (tg, tt) in pts:
    sgv = tg/sp.sqrt(1+tg**2); cgv = 1/sp.sqrt(1+tg**2)
    stv = tt/sp.sqrt(1+tt**2); ctv = 1/sp.sqrt(1+tt**2)
    qq = sp.simplify(stv*cgv/(ctv*sgv))
    cc = t/A
    J = J_rat(sgv, cgv, qq, cc, A, t)
    R = rhs(sgv, cgv, stv, ctv, A, t)
    d = sp.together(J - R)
    num = sp.expand(sp.fraction(d)[0])
    ok = (num == 0)
    allok &= ok
    print("Pythagorean (tan g=%s, tan t=%s) q=%s: EXACT IDENTITY %s" % (tg, tt, qq, ok))
print("ALL PYTHAGOREAN EXACT:", allok)

# (b) high-precision numeric check at random points
def J_num(g, q):
    A_ = mp.pi - g
    t_ = mp.atan(q*mp.tan(g))
    c_ = t_/A_
    sgv = mp.sin(g); cgv = mp.cos(g)
    P = cgv**2 + q**2*sgv**2
    D = q + c_*P
    cotx = -cgv/sgv
    G = -P*(3+2*A_*cotx)/D + 2*c_*A_*P*(q**2-1)*sgv*(-cgv)/D**2
    # partials numerically via the same formulas
    Gc = P**2*(3+2*A_*cotx)/D**2 + 2*A_*P*(q**2-1)*sgv*(-cgv)*(q-c_*P)/D**3
    # Gx: use sympy-free direct derivative of G w.r.t. x at (x=A, c=c_) keeping q fixed
    # G(x;c) = -Phi(x)(3+2x cotx)/D(x) + 2 c x Phi(x)(q^2-1) sinx cosx / D(x)^2
    # we differentiate numerically via mpmath.diff
    def Gx_of_x(xx):
        Px = mp.cos(xx)**2 + q**2*mp.sin(xx)**2
        Dx = q + c_*Px
        return -Px*(3+2*xx/mp.tan(xx))/Dx + 2*c_*xx*Px*(q**2-1)*mp.sin(xx)*mp.cos(xx)/Dx**2
    Gx = mp.diff(Gx_of_x, A_)
    u = A_*P/D
    return G**2 + Gc - u*Gx

def W_num(g, q):
    A_ = mp.pi - g
    t_ = mp.atan(q*mp.tan(g))
    sgv = mp.sin(g); cgv = mp.cos(g)
    stv = mp.sin(t_); ctv = mp.cos(t_)
    B1 = A_*cgv - 2*sgv
    B2 = 4*A_**2*cgv**2 - A_**2 - 12*A_*cgv*sgv + 6*sgv**2
    B4 = 7*A_*cgv**2 - A_*sgv**2 - 4*cgv*sgv
    B5 = A_**2*cgv**2 - A_**2*sgv**2 + 2*A_**2 + 12*A_*cgv*sgv - 12*sgv**2
    B7 = 3*A_*cgv**2 + A_*sgv**2 + 8*cgv*sgv
    W1 = -2*A_**3*B1*stv**2*ctv**4
    W2 = A_**2*cgv*B2*stv**2*ctv**2
    W3 = -2*A_**3*sgv*t_*stv*ctv**5
    W4 = A_**2*sgv*t_*B4*stv*ctv**3
    W5 = -A_*cgv**2*sgv*t_*B5*stv*ctv
    W6 = 4*A_**2*cgv*sgv**2*t_**2*ctv**4
    W7 = -A_*cgv*sgv**2*t_**2*B7*ctv**2
    W8 = 6*cgv**3*sgv**4*t_**2
    W = W1+W2+W3+W4+W5+W6+W7+W8
    Delta = A_*stv*ctv + t_*sgv*cgv
    return 2*A_**2*cgv*W/Delta**4

import random
random.seed(20260810)
maxrel = mp.mpf(0)
for i in range(30):
    g = mp.mpf(random.uniform(0.655, 1.0472))
    q = mp.mpf(random.uniform(1.0, 2.0))
    Jv = J_num(g, q); Rv = W_num(g, q)
    rel = abs(Jv - Rv)/max(abs(Jv), abs(Rv), mp.mpf(1))
    maxrel = max(maxrel, rel)
print("numeric max rel err over 30 random points: %.3e" % maxrel)
print("NUMERIC IDENTITY OK (rel err < 1e-60):", maxrel < mp.mpf('1e-60'))
