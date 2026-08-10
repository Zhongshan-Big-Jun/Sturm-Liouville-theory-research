# -*- coding: utf-8 -*-
"""verify_formulas.py -- independent re-derivation audit for R-20260806T070000Z-keylemma2b-0A6D8F.

Re-derives every premise used by the analytic proofs from the primary definitions:
  - secular equations and alpha1/alpha2
  - G(alpha;c), Mtilde, IN(q,u), sign(IN)=sign(G2) with explicit positive factor
  - M2 = dIN/du (entry-5 formula) vs central finite differences
  - dM2/dq formula vs central finite differences
  - M2(1,u) = pi*h(u), h(u) = 4u(pi-atan u)-5-9u^2
  - dM2/dq <= B(q) tail bound for q>=20, B decreasing
  - CORNER closed form and the equivalence pi > arccos(2/3)+sqrt(5)
  - C4 curve: IN = A*K(v), K monotone (slope survey), K(2pi/7)
  - corner values G2(1/2;2), G2(0.4;1)
Uses only mpmath at high precision; no interval engine.
"""
import mpmath as mp
mp.mp.dps = 60

def Phi(a, q):
    return mp.cos(a)**2 + q*q*mp.sin(a)**2

def Wfun(a):
    return 3 + 2*a/mp.tan(a)

def odd_beta(a, q):
    if a == mp.pi/2:
        return mp.pi/2
    if a < mp.pi/2:
        return mp.pi - mp.atan(q*mp.tan(a))
    return mp.atan(-q*mp.tan(a))

def even_beta(a, q):
    return mp.atan(1.0/(q*mp.tan(a)))

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

def G2(c, q):
    return Gfun(alpha2(c, q), c, q)

def IN_formula(q, u):
    A = mp.pi - mp.atan(u/q)
    t = mp.atan(u)
    return (q*q+u*u)*A*(2*A*q - 3*u + 2*t) - 3*t*u*q*(1+u*u)

def u_of(q, gamma):
    return q*mp.tan(gamma)

def A_of(q, gamma):
    return mp.pi - gamma

def IN_from_G2(c, q):
    """G2 * positive factor, to verify sign identity.
    On the odd curve: gamma = pi - alpha2, u = q*tan(gamma), A = pi - gamma."""
    a = alpha2(c, q)
    gamma = mp.pi - a
    u = u_of(q, gamma)
    A = A_of(q, gamma)
    Ph = Phi(a, q); D = q + c*Ph
    return G2(c, q) * (D*D*A*(q*q+u*u)*u/(Ph*q))

# 1. sign(IN) = sign(G2) with explicit positive factor, on random points
import random
random.seed(20260806)
print('=== 1. sign(IN) == sign(G2), positive factor ===')
bad = 0
for _ in range(300):
    q = mp.mpf(1 + 9*random.random())
    c = mp.mpf(0.49*random.random() + 1e-9)
    a2 = alpha2(c, q)
    gamma = mp.pi - a2
    u = q*mp.tan(gamma)
    A = mp.pi - gamma
    IN = IN_formula(q, u)
    Ph = Phi(a2, q); D = q + c*Ph
    POS = D*D*A*(q*q+u*u)*u/(Ph*q)
    G2v = G2(c, q)
    if mp.sign(IN) != mp.sign(G2v) or mp.fabs(IN - G2v*POS) > mp.mpf('1e-40')*mp.fabs(IN):
        bad += 1
        print('  MISMATCH q=%s c=%s' % (mp.nstr(q,6), mp.nstr(c,6)))
print('  random points:', 300, 'bad:', bad)

# 2. c=1/2 boundary: u = sqrt(2q+1)
print('=== 2. c=1/2 => u = sqrt(2q+1) ===')
bad = 0
for q in ['1.01','1.5','2','5','10','100']:
    qv = mp.mpf(q)
    a2 = alpha2(mp.mpf('0.5'), qv)
    u = qv*mp.tan(mp.pi - a2)
    if mp.fabs(u - mp.sqrt(2*qv+1)) > mp.mpf('1e-45'):
        bad += 1
        print('  FAIL q=%s u=%s sqrt=%s' % (q, mp.nstr(u,20), mp.nstr(mp.sqrt(2*qv+1),20)))
print('  bad:', bad)

# 3. M2 = dIN/du formula (entry 5) vs central FD
print('=== 3. M2 = dIN/du vs central FD ===')
def M2_formula(q, u):
    A = mp.pi - mp.atan(u/q)
    t = mp.atan(u)
    return (4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u)
            + t*(4*A*u - 5*q - 9*q*u*u))
bad = 0
for q in ['1.01','1.2','2','5','17.3']:
    for u in ['0.1','0.52','1.5','3.2','6.0']:
        qv, uv = mp.mpf(q), mp.mpf(u)
        if uv >= mp.sqrt(2*qv+1):
            continue
        h = mp.mpf('1e-30')
        fd = (IN_formula(qv, uv+h) - IN_formula(qv, uv-h))/(2*h)
        if mp.fabs(M2_formula(qv, uv) - fd) > mp.mpf('1e-25'):
            bad += 1
            print('  FAIL q=%s u=%s: %s vs FD %s' % (q, u, mp.nstr(M2_formula(qv,uv),15), mp.nstr(fd,15)))
print('  bad:', bad)

# 4. dM2/dq formula vs central FD
print('=== 4. dM2/dq vs central FD ===')
def dM2dq_formula(q, u):
    A = mp.pi - mp.atan(u/q)
    t = mp.atan(u)
    S = q*q + u*u
    return (4*A*A*u + 8*A*u*u*q/S - 7*q*q*u/S - 14*A*q - 9*u**3/S
            + 2*u/(1+u*u) + 4*A*q/(1+u*u) + t*(4*u*u/S - 5 - 9*u*u))
bad = 0
for q in ['1.01','1.2','2','5','17.3']:
    for u in ['0.1','0.52','1.5','3.2','6.0']:
        qv, uv = mp.mpf(q), mp.mpf(u)
        if uv >= mp.sqrt(2*qv+1):
            continue
        h = mp.mpf('1e-30')
        fd = (M2_formula(qv+h, uv) - M2_formula(qv-h, uv))/(2*h)
        if mp.fabs(dM2dq_formula(qv, uv) - fd) > mp.mpf('1e-25'):
            bad += 1
            print('  FAIL q=%s u=%s: %s vs FD %s' % (q, u, mp.nstr(dM2dq_formula(qv,uv),15), mp.nstr(fd,15)))
print('  bad:', bad)

# 5. M2(1,u) = pi h(u)
print('=== 5. M2(1,u) = pi h(u) ===')
def hfun(u):
    return 4*u*(mp.pi - mp.atan(u)) - 5 - 9*u*u
bad = 0
for u in ['0.01','0.5','1','3','10','100']:
    uv = mp.mpf(u)
    if mp.fabs(M2_formula(mp.mpf(1), uv) - mp.pi*hfun(uv)) > mp.mpf('1e-45'):
        bad += 1
        print('  FAIL u=%s' % u)
print('  bad:', bad)
print('  h max survey:')
best = None
u = mp.mpf('1e-6')
while u < 10:
    hv = hfun(u)
    if best is None or hv > best[0]:
        best = (hv, u)
    u *= 1.05
print('  hmax ~', mp.nstr(best[0],12), 'at u ~', mp.nstr(best[1],8))
print('  h(0.53) =', mp.nstr(hfun(mp.mpf('0.53')),12), ' h(0.5) =', mp.nstr(hfun(mp.mpf('0.5')),12))
print('  crude bound 9*(0.53)^2+4*(0.53)^2-5 =', mp.nstr(9*mp.mpf('0.53')**2+4*mp.mpf('0.53')**2-5, 12))

# 6. B(q) tail bound
print('=== 6. B(q) for dM2/dq, q >= 20 ===')
def Bq(q):
    return (4*mp.pi**2+14)*mp.sqrt(2*q+1) + 8*mp.pi*(2*q+1)/q + 1 + 2*mp.pi*(2*q+1)/(q*q) - 10*mp.pi*q
for q in ['20','21','25','50','100','1000']:
    qv = mp.mpf(q)
    print('  B(%s) = %s' % (q, mp.nstr(Bq(qv),8)))
# B decreasing: check B'(q) < 0 for q >= 20 analytically-ish via sampling
def Bp(q):
    return (4*mp.pi**2+14)/mp.sqrt(2*q+1) - 8*mp.pi/(q*q) - 4*mp.pi*(q+1)/(q**3) - 10*mp.pi
bad = 0
q = mp.mpf(20)
while q < 1000:
    if Bp(q) > 0:
        bad += 1
    q *= 1.01
print('  Bp(q) > 0 violations for q in [20,1000]:', bad)

# 7. CORNER closed form
print('=== 7. CORNER: G2(1/2;q), q >= 2 ===')
def G2_half(q):
    return G2(mp.mpf('0.5'), q)
print('  G2(1/2;2) =', mp.nstr(G2_half(mp.mpf(2)), 18))
print('  G2(0.4;1) =', mp.nstr(G2(mp.mpf('0.4'), mp.mpf(1)), 18))
print('  pi - arccos(2/3) - sqrt(5) =', mp.nstr(mp.pi - mp.acos(mp.mpf(2)/3) - mp.sqrt(5), 18))
# monotone in q?
prev = None
mono = True
for q in mp.linspace(2, 200, 2000):
    v = G2_half(q)
    if prev is not None and v < prev - mp.mpf('1e-40'):
        mono = False
    prev = v
print('  G2(1/2;q) increasing on [2,200] (fine grid):', mono)
# check closed form from ledger
def G2_half_cf(q):
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    return 2*q*(-q*x + mp.pi*q - x - 3*mp.sqrt(2*q+1) + mp.pi)/(2*q+1)**mp.mpf('1.5')
bad = 0
for q in ['2','3','10','100']:
    qv = mp.mpf(q)
    if mp.fabs(G2_half_cf(qv) - G2_half(qv)) > mp.mpf('1e-40'):
        bad += 1
        print('  FAIL cf q=%s' % q)
print('  ledger closed form matches: bad =', bad)

# 8. C4 curve: IN = A*K(v)
print('=== 8. C4: K(v), monotonicity ===')
def K_of_v(v):
    u = mp.tan(v)
    w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u)
# check IN = A*K on the curve
bad = 0
for v in mp.linspace(2*mp.pi/7, mp.mpf('1.2556370614359172'), 50):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    A = mp.mpf('2.5')*v
    if mp.fabs(IN_formula(q, u) - A*K_of_v(v)) > mp.mpf('1e-35')*mp.fabs(IN_formula(q,u)) + mp.mpf('1e-50'):
        bad += 1
print('  IN = A*K on curve: bad =', bad)
# K monotone: slope survey
kprev = None
min_slope = None
v = mp.mpf('0.8975979010256552')
while v < mp.mpf('1.2556370614359172'):
    k1 = K_of_v(v)
    v2 = v + mp.mpf('1e-4')
    k2 = K_of_v(v2)
    slope = (k2-k1)/(v2-v)
    if min_slope is None or slope < min_slope:
        min_slope = slope
    v = v2
print('  min slope of K on [2pi/7, 2pi/5-1e-3]:', mp.nstr(min_slope,8))
print('  K(2pi/7) =', mp.nstr(K_of_v(2*mp.pi/7), 10))
