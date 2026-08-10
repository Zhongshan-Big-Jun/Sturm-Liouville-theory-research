# -*- coding: utf-8 -*-
"""Audit Part 3: high-precision verification of the core identities at good roots."""
import mpmath as mp
mp.mp.dps = 60

def y1_mp(a, b, q, s):
    y, dy = mp.mpf('0'), mp.mpf('1')
    om = s; t = a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s*q; t = b-a
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s; t = 1-b
    c, sn = mp.cos(om*t), mp.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    return y

def eigvals_mp(a, b, q, kmax=2):
    top = 2*mp.pi + mp.mpf('1e-3')
    N = 20000
    lo0 = mp.mpf('1e-9')
    prev = y1_mp(a, b, q, lo0)
    gprev = lo0
    signs = []
    for i in range(1, N+1):
        g = lo0 + (top-lo0)*i/N
        v = y1_mp(a, b, q, g)
        if prev*v < 0:
            lo, hi = gprev, g
            for _ in range(150):
                mid = (lo+hi)/2
                if y1_mp(a, b, q, mid)*y1_mp(a, b, q, lo) <= 0: hi = mid
                else: lo = mid
            signs.append((lo+hi)/2)
            if len(signs) >= kmax: break
        prev = v; gprev = g
    assert len(signs) >= kmax
    return signs[:kmax]

def mode_mp(a, b, q, s):
    om1 = s
    yA, dyA = mp.sin(om1*a)/om1, mp.cos(om1*a)
    om2 = s*q
    ya, dya = yA, dyA
    c, sn = mp.cos(om2*(b-a)), mp.sin(om2*(b-a))
    yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
    om3 = s
    n = (a/2 - mp.sin(2*s*a)/(4*s))/s**2
    amp2 = ya**2 + (dya/om2)**2
    cross = ya*dya/om2
    L = b-a
    n += q**2 * ( amp2*L/2 + (ya**2 - (dya/om2)**2)*mp.sin(2*om2*L)/(4*om2) + cross*(1-mp.cos(2*om2*L))/(2*om2) )
    amp2b = yb**2 + (dyb/om3)**2
    crossb = yb*dyb/om3
    L = 1-b
    n += amp2b*L/2 + (yb**2 - (dyb/om3)**2)*mp.sin(2*om3*L)/(4*om3) + crossb*(1-mp.cos(2*om3*L))/(2*om3)
    return ya, yb, n

def Jm(m, x):
    W = mp.cos(x)**2 + m*m*mp.sin(x)**2
    return mp.sin(x)**2/W

print("=== Part 3: identities at R=4 good root (a,b)=(0.451485465757,0.548514534243) ===")
R = 4.0; q = mp.sqrt(mp.mpf(R))
a = mp.mpf('0.451485465757'); b = 1 - a
s1, s2 = eigvals_mp(a, b, q)
print("s1 =", mp.nstr(s1, 25), " s2 =", mp.nstr(s2, 25))
ya1, yb1, n1 = mode_mp(a, b, q, s1)
ya2, yb2, n2 = mode_mp(a, b, q, s2)

# Lemma 3.1: 0 < s2*a < pi, 0 < s2*(1-b) < pi
print("s2*a =", mp.nstr(s2*a, 20), " pi =", mp.nstr(mp.pi, 20), " OK:", 0 < s2*a < mp.pi)
print("s2*(1-b) =", mp.nstr(s2*(1-b), 20), " OK:", 0 < s2*(1-b) < mp.pi)

# Identity (4): y(b)^2/y(a)^2 = Jm(s(1-b))/Jm(sa) for each mode
for k, (s, ya, yb) in enumerate([(s1, ya1, yb1), (s2, ya2, yb2)], 1):
    lhs = (yb/ya)**2
    rhs = Jm(q, s*(1-b))/Jm(q, s*a)
    print(f"mode {k}: (4) |lhs-rhs| = {mp.nstr(abs(lhs-rhs), 4)}")

# Identity (5): y1(b)^2/y1(a)^2 = y2(b)^2/y2(a)^2 (from R1=R2=0)
lhs5 = (yb1/ya1)**2; rhs5 = (yb2/ya2)**2
print("(5) |lhs-rhs| =", mp.nstr(abs(lhs5-rhs5), 4))

# Identity (6): r_tau(alpha) = r_tau(beta), alpha=s1*a, beta=s1*(1-b)
tau = s2/s1
alpha = s1*a; beta = s1*(1-b)
rt = lambda x: Jm(q, tau*x)/Jm(q, x)
print("(6) r(alpha)=", mp.nstr(rt(alpha), 25), " r(beta)=", mp.nstr(rt(beta), 25), " diff=", mp.nstr(abs(rt(alpha)-rt(beta)), 4))
print("alpha - beta =", mp.nstr(alpha - beta, 4))

# Residual check R1=R2=0 at high precision
l1, l2 = s1**2, s2**2
R1 = l1*ya1**2/n1 - l2*ya2**2/n2
R2 = l1*yb1**2/n1 - l2*yb2**2/n2
print("R1 =", mp.nstr(R1, 4), " R2 =", mp.nstr(R2, 4))

print("=== Part 3b: identity (14) SR(xi) = (2(c+q)/xi^2) F_tilde(c) on symmetric line ===")
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def Mf(q, c, x): return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))
def alpha1_of_c(q, c):
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    lo, hi = mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))
def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20')
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=mp.mpf('1e-55'))
def Fe(q, c): return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))

for Rv in [2.0, 4.0, 10.0]:
    qm = mp.sqrt(mp.mpf(Rv))
    for xi in [0.1, 0.25, 0.4, 0.45, 0.48]:
        a, b = mp.mpf(xi), 1-mp.mpf(xi)
        s1t, s2t = eigvals_mp(a, b, qm)
        ya1t, yb1t, n1t = mode_mp(a, b, qm, s1t)
        ya2t, yb2t, n2t = mode_mp(a, b, qm, s2t)
        SR = s1t**2*ya1t**2/n1t - s2t**2*ya2t**2/n2t
        c = qm*(mp.mpf('0.5')-xi)/xi
        Fe_val = Fe(qm, c)
        pred = 2*(c+qm)/xi**2 * Fe_val
        print(f"R={Rv} xi={xi}: |SR - pred| = {mp.nstr(abs(SR-pred), 4)}")
print("identity (14) verified")
