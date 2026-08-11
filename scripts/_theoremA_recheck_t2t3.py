
# -*- coding: utf-8 -*-
# Independent re-verification of Theorem A (docs/SL_gap_n1_inf_limit_proof.tex)
# Gap (c): INF R->inf limit.  All numerics = EVIDENCE cross-checks; the doc's
# analytical claims are re-checked pointwise at high precision.
import mpmath as mp
mp.mp.dps = 50

def Dbar(u):
    # u in (0,1/2): theta-bar2 = a solves tan a = a(1 - 1/(2u)), a in (pi/2, pi)
    def F(a): return mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    a = mp.findroot(F, (mp.pi/2 + 1e-9, mp.pi - 1e-12), solver='anderson')
    mu1 = (mp.pi/2)**2/u**2
    mu2 = a**2/u**2
    return mu2 - mu1, a

def Sfun(u):
    # S(u) := mu1*(2/u) - mu2*sin^2(a)/I2(u);  should equal Dbar'(u)
    mu1 = (mp.pi/2)**2/u**2
    _, a = Dbar(u)
    mu2 = a**2/u**2
    I2 = u/2 - u*mp.sin(2*a)/(4*a)
    return mu1*(2/u) - mu2*mp.sin(a)**2/I2

def Ktilde(a): return -a**2 + 3*mp.sin(a)**2 + mp.mpf(3)/2*a*mp.sin(2*a)
def Jfun(a): return 4*a**3*mp.cot(a) + 6*a**2 - mp.pi**2
def Gfun(a): return 8*a**3*mp.sin(a)**2 - mp.pi**2*(2*a - mp.sin(2*a))

# ---- T2: sign chain checks ----
print("== T2: u(a), K~, J, G, S chain ==")
# (a) u(a) = a/(2(a-tan a)), endpoints and monotonicity
def ua(a): return a/(2*(a - mp.tan(a)))
for a in [mp.pi/2 + mp.mpf('1e-6'), mp.mpf('1.8'), mp.mpf('2.2'), mp.mpf('2.5'), mp.mpf('3.0'), mp.pi - mp.mpf('1e-6')]:
    print("  ua(%s) = %s" % (mp.nstr(a, 8), mp.nstr(ua(a), 14)))
print("  ua(pi/2+) ->", mp.nstr(ua(mp.pi/2 + mp.mpf('1e-9')), 14), "(should go to 0+)")
print("  ua(pi-)   ->", mp.nstr(ua(mp.pi - mp.mpf('1e-9')), 14), "(should go to 1/2-)")
# derivative u'(a) formula positive
da = mp.mpf('1e-6')
for a in [mp.mpf('1.6'), mp.mpf('1.9'), mp.mpf('2.3'), mp.mpf('2.7'), mp.mpf('3.1')]:
    num = (ua(a+da) - ua(a-da))/(2*da)
    formula = (a - mp.sin(2*a)/2)/(2*mp.cos(a)**2*(a - mp.tan(a))**2)
    print("  u'(%s) num=%s formula=%s match=%s" % (mp.nstr(a,6), mp.nstr(num,10), mp.nstr(formula,10), mp.almosteq(num, formula, rel_eps=1e-10)))

# (b) h'(a)*sin^3 a = 3 cos a sin^2 a - 5 a sin a + 2 a^2 cos a < 0 on (pi/2, pi)
ok = True
for a in mp.linspace(mp.pi/2 + mp.mpf('1e-4'), mp.pi - mp.mpf('1e-4'), 2001):
    v = 3*mp.cos(a)*mp.sin(a)**2 - 5*a*mp.sin(a) + 2*a**2*mp.cos(a)
    if v >= 0:
        ok = False; print("  h' FAIL at", a); break
print("  h'*sin^3 < 0 on (pi/2,pi):", ok)

# (c) J' = 4a K~/sin^2 a ; G' = 4 sin^2 a J  (finite differences)
okJ = okG = True
for a in [mp.mpf('1.6'), mp.mpf('1.9'), mp.mpf('2.3'), mp.mpf('2.7'), mp.mpf('3.1')]:
    dJ = (Jfun(a+da)-Jfun(a-da))/(2*da); fJ = 4*a*Ktilde(a)/mp.sin(a)**2
    dG = (Gfun(a+da)-Gfun(a-da))/(2*da); fG = 4*mp.sin(a)**2*Jfun(a)
    okJ &= mp.almosteq(dJ, fJ, rel_eps=1e-10)
    okG &= mp.almosteq(dG, fG, rel_eps=1e-10)
print("  J'=4aK~/sin^2a:", okJ, "| G'=4sin^2a J:", okG)

# (d) roots and sign pattern
a1 = mp.findroot(lambda a: Ktilde(a), (1.6, 1.7))
astar = mp.findroot(lambda a: Jfun(a), (1.9, 2.1))
aG = mp.findroot(lambda a: Gfun(a), (2.2, 2.4))
print("  a1 =", mp.nstr(a1, 15), " a* =", mp.nstr(astar, 15), " aG =", mp.nstr(aG, 15))
print("  (doc says approx 1.6351, 1.9856, 2.2766)")
uG = ua(aG)
print("  u* = u(aG) =", mp.nstr(uG, 20))
# signs
checks = {"K>0 on (pi/2,a1)": all(Ktilde(a) > 0 for a in mp.linspace(mp.pi/2+mp.mpf('1e-3'), a1-mp.mpf('1e-4'), 50)),
          "K<0 on (a1,pi)": all(Ktilde(a) < 0 for a in mp.linspace(a1+mp.mpf('1e-4'), mp.pi-mp.mpf('1e-3'), 50)),
          "J>0 on (pi/2,a*)": all(Jfun(a) > 0 for a in mp.linspace(mp.pi/2+mp.mpf('1e-3'), astar-mp.mpf('1e-4'), 50)),
          "J<0 on (a*,pi)": all(Jfun(a) < 0 for a in mp.linspace(astar+mp.mpf('1e-4'), mp.pi-mp.mpf('1e-3'), 50)),
          "G>0 on (pi/2,aG)": all(Gfun(a) > 0 for a in mp.linspace(mp.pi/2+mp.mpf('1e-4'), aG-mp.mpf('1e-4'), 50)),
          "G<0 on (aG,pi)": all(Gfun(a) < 0 for a in mp.linspace(aG+mp.mpf('1e-4'), mp.pi-mp.mpf('1e-3'), 50))}
for k, v in checks.items(): print("  ", k, ":", v)

# (e) S(u(a)) = -(4(a-tan a)^3)/(a^3(2a-sin2a)) G(a);  Dbar'(u(a)) = S(u(a))
okS = okD = True
for a in [mp.mpf('1.7'), mp.mpf('2.0'), aG, mp.mpf('2.5'), mp.mpf('3.0')]:
    u = ua(a)
    lhs = Sfun(u)
    rhs = -mp.mpf(4)*(a-mp.tan(a))**3/(a**3*(2*a-mp.sin(2*a)))*Gfun(a)
    dD = (Dbar(u+mp.mpf('1e-8'))[0] - Dbar(u-mp.mpf('1e-8'))[0])/mp.mpf('2e-8')
    okS &= mp.almosteq(lhs, rhs, rel_eps=1e-20)
    okD &= mp.almosteq(dD, lhs, rel_eps=1e-8)
print("  S(u(a)) identity:", okS, "| Dbar'=S (FD):", okD)
# sign of S: S<0 on (0,u*), S>0 on (u*,1/2)
print("  S<0 left:", all(Sfun(u) < 0 for u in [mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('0.2'), uG-mp.mpf('1e-6')]))
print("  S>0 right:", all(Sfun(u) > 0 for u in [uG+mp.mpf('1e-6'), mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.49')]))

# (f) endpoints
print("  Dbar(1e-5) =", mp.nstr(Dbar(mp.mpf('1e-5'))[0], 10), "(-> +inf)")
print("  Dbar(0.499999) =", mp.nstr(Dbar(mp.mpf('0.499999'))[0], 12), "(-> 3pi^2 =", mp.nstr(3*mp.pi**2, 12), ")")

# ---- T3: constants ----
print("== T3 ==")
Dstar, astar_ = Dbar(uG)
print("  u* =", mp.nstr(uG, 30))
print("  Dbar(u*) =", mp.nstr(Dstar, 30))
print("  doc: u* in [0.32992250812006654958, 0.32992250812006654960]")
print("  doc: Dbar in [24.9438661384324768968, 24.9438661384324769084]")
lo, hi = mp.mpf('0.32992250812006654958'), mp.mpf('0.32992250812006654960')
print("  u* in doc interval:", lo <= uG <= hi)
Dlo, Dhi = mp.mpf('24.9438661384324768968'), mp.mpf('24.9438661384324769084')
print("  Dbar in doc interval:", Dlo <= Dstar <= Dhi)
print("  margin 3pi^2 - Dbar =", mp.nstr(3*mp.pi**2 - Dstar, 12), ">= 4.664947:", 3*mp.pi**2 - Dstar >= mp.mpf('4.664947'))
print("  margin 25 - Dbar =", mp.nstr(25 - Dstar, 12), "> 0.0561:", 25 - Dstar > mp.mpf('0.0561'))
print("  Dbar(0.2) =", mp.nstr(Dbar(mp.mpf('0.2'))[0], 10), "(doc 29.2398)")
print("  Dbar(0.1) =", mp.nstr(Dbar(mp.mpf('0.1'))[0], 10), "(doc 47.556)")
print("  Dbar(1e-4) =", mp.nstr(Dbar(mp.mpf('1e-4'))[0], 10), "(doc ~40006)")
