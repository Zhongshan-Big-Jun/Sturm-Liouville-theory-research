# _audit_sub_C_finalcross.py — E3-style cross-check of the theorem conclusions (not proof)
import mpmath as mp
mp.mp.dps = 50

def G(x, c, q):
    Phi = mp.cos(x)**2 + q**2*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x/mp.tan(x))/D + 2*c*x*Phi*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2

def J(x, c, q):
    Phi = mp.cos(x)**2 + q**2*mp.sin(x)**2
    D = q + c*Phi
    def Gx_of_xx(xx):
        Px = mp.cos(xx)**2 + q**2*mp.sin(xx)**2
        Dx = q + c*Px
        return -Px*(3+2*xx/mp.tan(xx))/Dx + 2*c*xx*Px*(q**2-1)*mp.sin(xx)*mp.cos(xx)/Dx**2
    Gval = G(x, c, q)
    P = Phi
    Gc = P**2*(3+2*x/mp.tan(x))/D**2 + 2*x*P*(q**2-1)*mp.sin(x)*mp.cos(x)*(q-c*P)/D**3
    Gx = mp.diff(Gx_of_xx, x)
    return Gval**2 + Gc - x*P/D*Gx

# J1^(2)(x,q) with c = c1(x,q) on T1
def c1(x, q): return mp.atan(1/(q*mp.tan(x)))/x
mn1 = None
for qv in [mp.mpf('1.0001'), mp.mpf(1.3), mp.mpf(1.7), mp.mpf('1.9999')]:
    for i in range(401):
        x = mp.mpf('0.841') + (5*mp.pi/14 - mp.mpf('0.841'))*mp.mpf(i)/400
        c = c1(x, qv)
        if not (mp.mpf('0.4') < c < mp.mpf('0.5')): continue
        v = J(x, c, qv)
        mn1 = v if mn1 is None else min(mn1, v)
print("min J1^(2) on T1 scan:", mn1, " >= 6499/7500 =", mp.mpf(6499)/7500, ":", mn1 >= mp.mpf(6499)/7500)

# J2^(2)(gamma,q) with c = c2 on the box
def c2(g, q): return mp.atan(q*mp.tan(g))/(mp.pi - g)
mx2 = None
for qv in [mp.mpf(1), mp.mpf(1.3), mp.mpf(1.7), mp.mpf(2)]:
    for i in range(401):
        g = mp.mpf('0.655') + (mp.mpf('1.0472')-mp.mpf('0.655'))*mp.mpf(i)/400
        c = c2(g, qv)
        x = mp.pi - g
        v = J(x, c, qv)
        mx2 = v if mx2 is None else max(mx2, v)
print("max J2^(2) on box scan:", mx2, " < 0:", mx2 < 0)

# F_tilde_e'(q,c) < 0 spot check on random (q,c)
def Fe(q, c):
    # F_e = Mf1 - Mf2 ratio; use the key-lemma raw form: Fe' = Mf1 G1 - Mf2 G2
    # directly compute G1, G2 at the true phases
    a1 = mp.findroot(lambda x: c*x - mp.atan(1/(q*mp.tan(x))), mp.mpf('1.0'))
    g2 = mp.findroot(lambda gg: c*(mp.pi-gg) - mp.atan(q*mp.tan(gg)), mp.mpf('0.8'))
    G1 = G(a1, c, q); G2 = G(mp.pi-g2, c, q)
    return G1 - G2   # sign of (1/Mf1 Mf2)*Fe'... actually Fe' = Mf1 G1 - Mf2 G2; the ratio log deriv is G1-G2
import random
random.seed(7)
ok = True
for _ in range(50):
    q = mp.mpf(random.uniform(1.01, 5))
    c = mp.mpf(random.uniform(0.001, 0.499))
    G1 = None
    try:
        a1 = mp.findroot(lambda x: c*x - mp.atan(1/(q*mp.tan(x))), mp.mpf('0.9'))
    except Exception:
        a1 = mp.findroot(lambda x: c*x - mp.atan(1/(q*mp.tan(x))), mp.mpf('0.5'))
    g2 = mp.findroot(lambda gg: c*(mp.pi-gg) - mp.atan(q*mp.tan(gg)), mp.mpf('0.7'))
    G1 = G(a1, c, q); G2 = G(mp.pi-g2, c, q)
    if not (G1 - G2 < 0): ok = False; print("LOG fail at", q, c, G1-G2)
print("LOG (G1-G2<0) random scan 50 pts:", ok)
