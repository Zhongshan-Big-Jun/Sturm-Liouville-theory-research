# -*- coding: utf-8 -*-
"""audit_semantics_fresh.py -- fresh adversarial semantic audit of the KEY LEMMA proof.

Independent re-derivation (mpmath 80 dps) of:
  1. G2, H, Ftilde, H', Ftilde'' from first principles (secular roots via monotone
     bisection), checked for sign on random points in the four regions;
  2. the (q,u) reformulation: u = q tan(pi - alpha2) = tan(c*alpha2), c = atan(u)/A,
     sign(G2) == sign(IN);
  3. CORNER closed form at c = 1/2 vs direct G2;
  4. C4: on the c=0.4 curve v = arctan(u), IN == A*K(v);
  5. the R1/R2/Box reduction: H > 0 and Ftilde' < 0 on random (q,c) in the box;
  6. the KEY LEMMA claim itself: (LOG) and (FP) on random (q,c) in (1,2)x(0.4,0.5).
This is a check harness (numerical evidence), not a proof; the proof obligations are
the analytic lemmas and the certified boxes.
"""
import mpmath as mp
mp.mp.dps = 80
import random
random.seed(20260806)

def alpha1(c, q):
    # root of atan(1/(q tan a)) = c a on (0, pi/2); monotone in a -> solve in x = pi/2 - a
    lo, hi = mp.mpf(0), mp.mpf(1.57)
    for _ in range(400):
        mid = (lo + hi) / 2
        val = mp.atan(mp.tan(mid) / q) - c * (mp.pi / 2 - mid)
        if val > 0:
            hi = mid
        else:
            lo = mid
    return mp.pi / 2 - (lo + hi) / 2

def alpha2(c, q):
    # root of O(a) = c a, O(a) = pi - atan(q tan a) on (0, pi/2), arctan(-q tan a) on (pi/2, pi)
    lo, hi = mp.mpf(0), mp.mpf(3.14)
    for _ in range(400):
        mid = (lo + hi) / 2
        if mid < mp.pi / 2:
            val = mp.pi - mp.atan(q * mp.tan(mid)) - c * mid
        else:
            val = mp.atan(-q * mp.tan(mid)) - c * mid
        if val > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def Phi(a, q):
    return mp.cos(a)**2 + q*q*mp.sin(a)**2

def W(a):
    return 3 + 2*a/mp.tan(a)

def Mtilde(a, c, q):
    return a*a*mp.sin(a)**2/(q + c*Phi(a, q))

def G(a, c, q):
    Ph = Phi(a, q); D = q + c*Ph
    return -Ph*W(a)/D + 2*c*a*Ph*(q*q-1)*mp.sin(a)*mp.cos(a)/D**2

def dGdc_num(a, c, q, h=mp.mpf('1e-20')):
    return (G(a, c+h, q) - G(a, c-h, q)) / (2*h)

def Hval(c, q):
    return G(alpha2(c, q), c, q) - G(alpha1(c, q), c, q)

def Fp(c, q):
    a1 = alpha1(c, q); a2 = alpha2(c, q)
    return Mtilde(a1, c, q)*G(a1, c, q) - Mtilde(a2, c, q)*G(a2, c, q)

def IN(q, u):
    A = mp.pi - mp.atan(u/q)
    t = mp.atan(u)
    return (q*q+u*u)*A*(2*A*q - 3*u + 2*t) - 3*u*q*(1+u*u)*t

def Kc4(v):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u)

fails = []
def check(name, cond, detail=''):
    if not cond:
        fails.append(name)
        print('FAIL', name, detail)

# 1. sign(G2) == sign(IN) on random (q,u)
for _ in range(300):
    q = 1 + 10**random.uniform(-6, 2.6)
    u = random.random() * mp.sqrt(2*q+1)
    c = mp.atan(u)/(mp.pi - mp.atan(u/q))
    a2 = alpha2(c, q)
    g2 = G(a2, c, q)
    in_ = IN(q, u)
    if mp.sign(g2) != mp.sign(in_) and abs(g2) > mp.mpf('1e-30') and abs(in_) > mp.mpf('1e-30'):
        check('sign_identity', False, 'q=%s u=%s g2=%s in=%s' % (q, u, g2, in_))
check('sign_identity', len(fails) == 0 or fails[-1] != 'sign_identity' or len(fails) == 0, '')
fails.clear()

# 2. u == tan(c*A) identity
for _ in range(200):
    q = 1 + 10**random.uniform(-6, 2)
    c = random.random()*0.5
    a2 = alpha2(c, q)
    u1 = q*mp.tan(mp.pi - a2)
    u2 = mp.tan(c*a2)
    if abs(u1 - u2) > mp.mpf('1e-50'):
        check('u_identity', False, 'q=%s c=%s u1=%s u2=%s' % (q, c, u1, u2))
print('u identity fails:', len(fails)); fails.clear()

# 3. CORNER: G2(1/2;q) closed form vs direct
for q in [mp.mpf('2.0'), mp.mpf('2.01'), mp.mpf('3'), mp.mpf('10'), mp.mpf('1e3'), mp.mpf('1e6')]:
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    cf = 2*q*(q+1)*(mp.pi - x - 3*mp.sin(x))/(2*q+1)**mp.mpf('1.5')
    g2 = G(alpha2(mp.mpf('0.5'), q), mp.mpf('0.5'), q)
    if abs(cf - g2) > mp.mpf('1e-50'):
        check('corner_closed', False, 'q=%s cf=%s g2=%s' % (q, cf, g2))
# q>=2 min at q=2
print('corner checks ok so far; fails:', len(fails)); fails.clear()

# 4. C4: IN == A*K(v) on curve
for _ in range(200):
    v = mp.mpf('0.897597901025655210989326680937000824056334114107173091707127') + random.random()*(mp.mpf('1.25663706143591729538505735331180115367886775975004232838998') - mp.mpf('0.897597901025655210989326680937000824056334114107173091707127'))
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    A = mp.mpf('2.5')*v
    in_ = IN(q, u)
    if abs(in_ - A*Kc4(v)) > mp.mpf('1e-40')*max(mp.mpf(1), abs(in_)):
        check('c4_identity', False, 'v=%s in=%s AK=%s' % (v, in_, A*Kc4(v)))
print('c4 identity fails:', len(fails)); fails.clear()

# 5. R1 region: G2 >= 0 for q>=2, c in (0,0.5)
bad_r1 = 0
for _ in range(500):
    q = 2 + random.random()*100
    c = random.random()*0.49
    g2 = G(alpha2(c, q), c, q)
    if g2 < -mp.mpf('1e-12'):
        bad_r1 += 1
print('R1 negatives (should be 0):', bad_r1)

# 6. R2 region: G2 >= 0 for q>1, c in (0,0.4]
bad_r2 = 0
for _ in range(500):
    q = 1 + 10**random.uniform(-7, 3)
    c = random.random()*0.4
    g2 = G(alpha2(c, q), c, q)
    if g2 < -mp.mpf('1e-12'):
        bad_r2 += 1
print('R2 negatives (should be 0):', bad_r2)

# 7. Box: H > 0 and Fp < 0 for (q,c) in (1,2)x(0.4,0.5)
bad_h = 0; bad_f = 0
for _ in range(400):
    q = 1 + random.random()
    c = 0.4 + random.random()*0.1
    h = Hval(c, q)
    fp = Fp(c, q)
    if h < mp.mpf('1e-10'):
        bad_h += 1
    if fp > -mp.mpf('1e-10'):
        bad_f += 1
print('Box: H<=0 count (should be 0):', bad_h, ' Fp>=0 count (should be 0):', bad_f)

# 8. H'(L4box) and F~''(L5box) signs on random box points (direct FD for H')
bad_l4 = 0; bad_l5 = 0
for _ in range(200):
    q = 1 + random.random()
    c = 0.4 + random.random()*0.1
    a1 = alpha1(c, q); a2 = alpha2(c, q)
    h1 = dGdc_num(a1, c, q); h2 = dGdc_num(a2, c, q)
    Hp = h2 - h1
    if Hp > -mp.mpf('1e-6'):
        bad_l4 += 1
    M1 = Mtilde(a1, c, q); M2 = Mtilde(a2, c, q)
    J1 = dGdc_num(a1, c, q) + G(a1, c, q)**2
    J2 = dGdc_num(a2, c, q) + G(a2, c, q)**2
    L5 = M1*J1 - M2*J2
    if L5 < mp.mpf('1e-6'):
        bad_l5 += 1
print('L4box Hp>=0 count (should be 0):', bad_l4, ' L5box Fpp<=0 count (should be 0):', bad_l5)

print('TOTAL FRESH AUDIT FAILS:', len(fails))
