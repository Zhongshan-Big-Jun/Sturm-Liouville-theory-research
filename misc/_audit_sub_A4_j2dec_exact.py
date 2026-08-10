# _audit_sub_A4_j2dec_exact.py — exact rational verification of lem:j2dec at Pythagorean points
# J2 = N/(16 Delta^4) is rational in (A,t,sg,cg,st,ct) once sg^2+cg^2=1, st^2+ct^2=1.
from sympy import Rational, simplify, pi
from sympy import symbols

sg, cg, st, ct, A, t = symbols('sg cg st ct A t')

def Phi(qq, xx_cg, xx_sg):
    return xx_cg**2 + qq**2*xx_sg**2

def G_rat(sg, cg, qq, cc, A, t):
    # x = pi - gamma: sin x = sg, cos x = -cg, cot x = -cg/sg
    P = cg**2 + qq**2*sg**2
    D = qq + cc*P
    x = A  # x = pi - gamma = A
    cotx = -cg/sg
    return -P*(3+2*x*cotx)/D + 2*cc*x*P*(qq**2-1)*sg*(-cg)/D**2

def J_rat(sg, cg, qq, cc, A, t):
    # G as rational function; partials w.r.t. c and x at fixed q
    # We differentiate the expression treating sg,cg,A as functions of gamma? No: partial derivatives
    # at fixed q and c. G(x;c) with x = pi-gamma. We need dG/dc |_{x,q}, dG/dx |_{c,q}.
    # Compute symbolically with sympy first.
    from sympy import diff
    x = symbols('x', positive=True)
    cc_s, qq_s = symbols('cc_s qq_s', positive=True)
    P = cos2 = None
    # build G(x) generically
    import sympy as sp
    xx = sp.symbols('xx', positive=True)
    Px = sp.cos(xx)**2 + qq_s**2*sp.sin(xx)**2
    Dx = qq_s + cc_s*Px
    Gx = -Px*(3+2*xx*sp.cot(xx))/Dx + 2*cc_s*xx*Px*(qq_s**2-1)*sp.sin(xx)*sp.cos(xx)/Dx**2
    Gc = sp.diff(Gx, cc_s)
    Gxx = sp.diff(Gx, xx)
    # substitute xx = A, sin xx = sg, cos xx = -cg, cot xx = -cg/sg
    G_val = Gx.subs({xx: A, sp.sin(xx): sg, sp.cos(xx): -cg, sp.cot(xx): -cg/sg, qq_s: qq, cc_s: cc})
    Gc_val = Gc.subs({xx: A, sp.sin(xx): sg, sp.cos(xx): -cg, sp.cot(xx): -cg/sg, qq_s: qq, cc_s: cc})
    Gx_val = Gxx.subs({xx: A, sp.sin(xx): sg, sp.cos(xx): -cg, sp.cot(xx): -cg/sg, qq_s: qq, cc_s: cc})
    P = cg**2 + qq**2*sg**2
    D = qq + cc*P
    return sp.simplify(G_val**2 + Gc_val - A*P/D*Gx_val)

def rhs(sg, cg, st, ct, A, t):
    import sympy as sp
    B1 = A*cg - 2*sg
    B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
    B4 = 7*A*cg**2 - A*sg**2 - 4*cg*sg
    B5 = A**2*cg**2 - A**2*sg**2 + 2*A**2 + 12*A*cg*sg - 12*sg**2
    B7 = 3*A*cg**2 + A*sg**2 + 8*cg*sg
    W1 = -2*A**3*B1*st**2*ct**4
    W2 = A**2*cg*B2*st**2*ct**2
    W3 = -2*A**3*sg*t*st*ct**5
    W4 = A**2*sg*t*B4*st*ct**3
    W5 = -A*cg**2*sg*t*B5*st*ct
    W6 = 4*A**2*cg*sg**2*t**2*ct**4
    W7 = -A*cg*sg**2*t**2*B7*ct**2
    W8 = 6*cg**3*sg**4*t**2
    W = W1+W2+W3+W4+W5+W6+W7+W8
    Delta = A*st*ct + t*sg*cg
    return sp.simplify(32*A**2*cg*W/(16*Delta**4))

import sympy as sp
points = [
    (Rational(3,5), Rational(4,5), Rational(5,13), Rational(12,13), Rational(5,2), Rational(1,2)),
    (Rational(5,13), Rational(12,13), Rational(8,17), Rational(15,17), Rational(11,4), Rational(3,4)),
    (Rational(8,17), Rational(15,17), Rational(7,25), Rational(24,25), Rational(19,7), Rational(2,5)),
    (Rational(20,29), Rational(21,29), Rational(12,37), Rational(35,37), Rational(26,9), Rational(4,7)),
]
allok = True
for (sgv, cgv, stv, ctv, Av, tv) in points:
    qq = stv*cgv/(ctv*sgv)
    cc = tv/Av
    J = J_rat(sgv, cgv, qq, cc, Av, tv)
    R = rhs(sgv, cgv, stv, ctv, Av, tv)
    d = sp.simplify(J - R)
    ok = (d == 0)
    allok &= ok
    print("point", (sgv,cgv,stv,ctv,Av,tv), "J2==N/(16D^4):", ok)
print("ALL EXACT:", allok)
