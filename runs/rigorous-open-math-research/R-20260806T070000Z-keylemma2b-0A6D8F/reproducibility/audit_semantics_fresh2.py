# -*- coding: utf-8 -*-
"""audit_semantics_fresh2.py -- fresh adversarial semantic audit (fixed alpha2).

Same checks as audit_semantics_fresh.py, but alpha2 is solved via gamma = pi - alpha2
in (0, pi/3) with f(g) = atan(q*tan g) - c*(pi - g) strictly increasing, hi = 1.05.
"""
import mpmath as mp
mp.mp.dps = 80
import random
random.seed(20260806)

def alpha1(c, q):
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
    lo, hi = mp.mpf(0), mp.mpf('1.05')
    for _ in range(400):
        mid = (lo + hi) / 2
        val = mp.atan(q * mp.tan(mid)) - c * (mp.pi - mid)
        if val > 0:
            hi = mid
        else:
            lo = mid
    return mp.pi - (lo + hi) / 2

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

# 1. sign(G2) == sign(IN)
for _ in range(400):
    q = 1 + 10**random.uniform(-6, 2.6)
    u = random.random() * mp.sqrt(2*q+1)
    c = mp.atan(u)/(mp.pi - mp.atan(u/q))
    a2 = alpha2(c, q)
    g2 = G(a2, c, q)
    in_ = IN(q, u)
    if mp.sign(g2) != mp.sign(in_) and abs(g2) > mp.mpf('1e-30') and abs(in_) > mp.mpf('1e-30'):
        check('sign_identity', False, 'q=%s u=%s g2=%s in=%s' % (q, u, g2, in_))
print('sign identity fails:', len(fails)); fails.clear()

# 2. u == q*tan(pi-alpha2) == tan(c*A)
for _ in range(300):
    q = 1 + 10**random.uniform(-6, 3)
    c = random.random()*0.5
    a2 = alpha2(c, q)
    u1 = q*mp.tan(mp.pi - a2)
    u2 = mp.tan(c*a2)
    if abs(u1 - u2) > mp.mpf('1e-45') or abs(u1 - mp.tan(c*(mp.pi - mp.atan(u1/q)))) > mp.mpf('1e-45'):
        check('u_identity', False, 'q=%s c=%s u1=%s u2=%s' % (q, c, u1, u2))
print('u identity fails:', len(fails)); fails.clear()

# 3. CORNER closed form vs direct
for q in [mp.mpf('2.0'), mp.mpf('2.01'), mp.mpf('3'), mp.mpf('10'), mp.mpf('1e3'), mp.mpf('1e6')]:
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    cf = 2*q*(q+1)*(mp.pi - x - 3*mp.sin(x))/(2*q+1)**mp.mpf('1.5')
    g2 = G(alpha2(mp.mpf('0.5'), q), mp.mpf('0.5'), q)
    if abs(cf - g2) > mp.mpf('1e-45'):
        check('corner_closed', False, 'q=%s cf=%s g2=%s' % (q, cf, g2))
print('corner closed-form fails:', len(fails)); fails.clear()

# 4. C4: IN == A*K(v)
vlo = mp.mpf('0.897597901025655210989326680937000824056334114107173091707127')
vhi = mp.mpf('1.25563706143591729538505735331180115367886775975004232838998')
for _ in range(300):
    v = vlo + random.random()*(vhi - vlo)
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    A = mp.mpf('2.5')*v
    in_ = IN(q, u)
    if abs(in_ - A*Kc4(v)) > mp.mpf('1e-40')*max(mp.mpf(1), abs(in_)):
        check('c4_identity', False, 'v=%s in=%s AK=%s' % (v, in_, A*Kc4(v)))
print('c4 identity fails:', len(fails)); fails.clear()

# 5. R1: G2 >= 0 for q>=2, c in (0,0.5)
bad_r1 = 0
for _ in range(600):
    q = 2 + random.random()*100
    c = random.random()*0.499
    if G(alpha2(c, q), c, q) < -mp.mpf('1e-12'):
        bad_r1 += 1
print('R1 negatives (should be 0):', bad_r1)

# 6. R2: G2 >= 0 for q>1, c in (0,0.4]
bad_r2 = 0
for _ in range(600):
    q = 1 + 10**random.uniform(-7, 4)
    c = random.random()*0.4
    if G(alpha2(c, q), c, q) < -mp.mpf('1e-12'):
        bad_r2 += 1
print('R2 negatives (should be 0):', bad_r2)

# 7. Box: H > 0, Fp < 0 on (1,2)x(0.4,0.5)
bad_h = 0; bad_f = 0
for _ in range(500):
    q = 1 + random.random()
    c = 0.4 + random.random()*0.1
    if Hval(c, q) < mp.mpf('1e-10'):
        bad_h += 1
    if Fp(c, q) > -mp.mpf('1e-10'):
        bad_f += 1
print('Box: H<=0 count:', bad_h, ' Fp>=0 count:', bad_f)

# 8. L4box H' < 0, L5box F~'' > 0 (direct FD)
bad_l4 = 0; bad_l5 = 0
for _ in range(300):
    q = 1 + random.random()
    c = 0.4 + random.random()*0.1
    a1 = alpha1(c, q); a2 = alpha2(c, q)
    Hp = dGdc_num(a2, c, q) - dGdc_num(a1, c, q)
    if Hp > -mp.mpf('1e-6'):
        bad_l4 += 1
    M1 = Mtilde(a1, c, q); M2 = Mtilde(a2, c, q)
    J1 = dGdc_num(a1, c, q) + G(a1, c, q)**2
    J2 = dGdc_num(a2, c, q) + G(a2, c, q)**2
    if M1*J1 - M2*J2 < mp.mpf('1e-6'):
        bad_l5 += 1
print('L4box Hp>=0 count:', bad_l4, ' L5box Fpp<=0 count:', bad_l5)

# 9. Extreme edge cases: q -> 1+, q large, c -> 0+, c -> 0.5-
for (q, c) in [('1.0000000001', '0.4'), ('1.0000000001', '0.499999999'), ('1e6', '1e-6'), ('1e6', '0.4'), ('1e6', '0.499'), ('2', '1e-7'), ('1e4', '0.25')]:
    qq = mp.mpf(q); cc = mp.mpf(c)
    g2 = G(alpha2(cc, qq), cc, qq)
    print('edge q=%s c=%s G2=%s' % (q, c, mp.nstr(g2, 12)))
    if g2 < -mp.mpf('1e-9'):
        check('edge_g2', False, 'q=%s c=%s g2=%s' % (q, c, g2))
print('edge fails:', len(fails)); fails.clear()
print('TOTAL FRESH AUDIT FAILS:', len(fails))
