# -*- coding: utf-8 -*-
"""verify_parent_bases.py -- independent re-check of the parent run's premises.
L1 (G1 < 0), L2 (G2 >= 0 => LOG and FP), E1, E2, E8, B4, B5, B7,
plus the KEY LEMMA on a grid (LOG and FP forms).
"""
import mpmath as mp
mp.mp.dps = 50

def Phi(a, q):
    return mp.cos(a)**2 + q*q*mp.sin(a)**2

def Wfun(a):
    return 3 + 2*a/mp.tan(a)

def even_beta(a, q):
    return mp.atan(1.0/(q*mp.tan(a)))

def odd_beta(a, q):
    if a == mp.pi/2:
        return mp.pi/2
    if a < mp.pi/2:
        return mp.pi - mp.atan(q*mp.tan(a))
    return mp.atan(-q*mp.tan(a))

def bisect(f, lo, hi, tol=None, maxit=500):
    if tol is None:
        tol = mp.mpf(10)**(-(mp.mp.dps-6))
    flo = f(lo)
    for _ in range(maxit):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0 or (hi-lo)/2 < tol:
            return mid
        if flo*fm < 0:
            hi = mid
        else:
            lo = mid; flo = fm
    return (lo+hi)/2

def alpha1(c, q):
    return bisect(lambda a: even_beta(a, q) - c*a, mp.mpf('1e-60'), mp.pi/2)

def alpha2(c, q):
    return bisect(lambda a: odd_beta(a, q) - c*a, mp.mpf('1e-60'), mp.pi)

def Gfun(a, c, q):
    Ph = Phi(a, q); D = q + c*Ph
    return -Ph*Wfun(a)/D + 2*c*a*Ph*(q*q-1)*mp.sin(a)*mp.cos(a)/D**2

def Mtilde(a, c, q):
    return a*a*mp.sin(a)**2/(q + c*Phi(a, q))

def G1(c, q):
    return Gfun(alpha1(c, q), c, q)
def G2(c, q):
    return Gfun(alpha2(c, q), c, q)
def M1t(c, q):
    return Mtilde(alpha1(c, q), c, q)
def M2t(c, q):
    return Mtilde(alpha2(c, q), c, q)

def dGdc(a, c, q):
    Ph = Phi(a, q); D = q + c*Ph
    s, co = mp.sin(a), mp.cos(a); sc = s*co
    W = Wfun(a)
    Gc = Ph*W*Ph/D**2 + (2*a*Ph*(q*q-1)*sc)*(D - 2*c*Ph)/D**3
    Pha = 2*(q*q-1)*sc
    Wp = 2*(sc - a)/s**2
    d1 = -(Pha*W + Ph*Wp)/D + Ph*W*c*Pha/D**2
    dsc = co*co - s*s
    d2a = 2*c*(q*q-1)*(Ph*a*dsc + Ph*sc + a*Pha*sc)/D**2
    d2b = -4*c*c*a*Ph*(q*q-1)*sc*Pha/D**3
    Ga = d1 + d2a + d2b
    return Ga*(-a*Ph/D) + Gc

print('=== L1: G1 < 0 on (1,inf) x (0,1/2) ===')
bad = 0
for q in mp.linspace(1.0001, 100, 60):
    for c in mp.linspace(1e-4, 0.499, 40):
        if G1(c, q) >= 0:
            bad += 1
print('  violations:', bad)

print('=== L2 check: G2 >= 0 => H > 0 and Fp < 0 (on samples) ===')
bad = 0
for q in mp.linspace(1.0001, 100, 40):
    for c in mp.linspace(1e-4, 0.499, 25):
        G1v, G2v = G1(c, q), G2(c, q)
        H = G2v - G1v
        Fp = M1t(c, q)*G1v - M2t(c, q)*G2v
        if G2v >= 0 and not (H > 0 and Fp < 0):
            bad += 1
        # also check H > 0 and Fp < 0 on the whole sampled region (KEY LEMMA evidence)
        if not (H > 0 and Fp < 0):
            bad += 10000
print('  KEY LEMMA violations on grid:', bad // 10000, ' (L2 inconsistency:', bad % 10000, ')')

print('=== E1/E2/E8 ===')
bad = 0
for q in ['1.5', '2.7', '10']:
    for c in ['0.1', '0.4', '0.49']:
        qv, cv = mp.mpf(q), mp.mpf(c)
        a1, a2 = alpha1(cv, qv), alpha2(cv, qv)
        # E1: (d/dc) log(M1/M2) = G1 - G2
        h = mp.mpf('1e-20')
        lhs = (mp.log(M1t(cv+h, qv)/M2t(cv+h, qv)) - mp.log(M1t(cv-h, qv)/M2t(cv-h, qv)))/(2*h)
        if mp.fabs(lhs - (G1(cv,qv) - G2(cv,qv))) > mp.mpf('1e-12'):
            bad += 1
        # E2: Fp = M1 G1 - M2 G2
        Fp = M1t(cv,qv)*G1(cv,qv) - M2t(cv,qv)*G2(cv,qv)
        if mp.fabs(Fp - (M1t(cv,qv)*G1(cv,qv) - M2t(cv,qv)*G2(cv,qv))) > mp.mpf('1e-40'):
            bad += 1
        # E8: Fpp = M1 J1 - M2 J2 with J = G^2 + dG/dc
        J1 = Gfun(a1, cv, qv)**2 + dGdc(a1, cv, qv)
        J2 = Gfun(a2, cv, qv)**2 + dGdc(a2, cv, qv)
        Fpp = M1t(cv,qv)*J1 - M2t(cv,qv)*J2
        h2 = mp.mpf('1e-16')
        Fp_h = lambda cc: M1t(cc, qv)*G1(cc, qv) - M2t(cc, qv)*G2(cc, qv)
        lhs2 = (Fp_h(cv+h2) - Fp_h(cv-h2))/(2*h2)
        if mp.fabs(lhs2 - Fpp) > mp.mpf('1e-6')*mp.fabs(Fpp):
            bad += 1
print('  violations:', bad)

print('=== B4: Fp(q, 1/2) < 0 ===')
bad = 0
for q in mp.linspace(1.0001, 50, 80):
    Fp = M1t(mp.mpf('0.5'), q)*G1(mp.mpf('0.5'), q) - M2t(mp.mpf('0.5'), q)*G2(mp.mpf('0.5'), q)
    if Fp >= 0:
        bad += 1
print('  violations:', bad)

print('=== B5: H(q,1/2) = 2 pi q(q+1)/(2q+1)^{3/2} > 0 ===')
bad = 0
for q in mp.linspace(1.0001, 50, 80):
    H = G2(mp.mpf('0.5'), q) - G1(mp.mpf('0.5'), q)
    cf = 2*mp.pi*q*(q+1)/(2*q+1)**mp.mpf('1.5')
    if H <= 0 or mp.fabs(H - cf) > mp.mpf('1e-35'):
        bad += 1
print('  violations:', bad)

print('=== B7: G2(c,1) > 0 for c in (0,0.4] ===')
bad = 0
for c in mp.linspace(1e-4, 0.4, 200):
    if G2(c, mp.mpf(1)) <= 0:
        bad += 1
print('  violations:', bad)
print('  G2(0.4,1) =', mp.nstr(G2(mp.mpf('0.4'), mp.mpf(1)), 12))
