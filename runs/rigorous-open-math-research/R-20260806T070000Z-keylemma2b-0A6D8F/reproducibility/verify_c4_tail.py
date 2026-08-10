import mpmath as mp
mp.mp.dps = 60
import random
random.seed(20260806)

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

print('=== 1 (fixed). IN == G2 * POS with POS = D^2 A (q^2+u^2) u / (Phi q) ===')
bad = 0
worst_rel = None
for _ in range(500):
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
    if mp.sign(IN) != mp.sign(G2v):
        bad += 1
        print('  SIGN MISMATCH q=%s c=%s IN=%s G2=%s' % (mp.nstr(q,8), mp.nstr(c,8), mp.nstr(IN,10), mp.nstr(G2v,10)))
    rel = mp.fabs(IN - G2v*POS)/mp.fabs(IN)
    if worst_rel is None or rel > worst_rel:
        worst_rel = rel
print('  bad:', bad, ' worst relative error IN vs G2*POS:', mp.nstr(worst_rel, 5))

print('=== C4 tail correspondence ===')
def K_of_v(v):
    u = mp.tan(v)
    w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u), q, u
v0 = mp.mpf('1.25563706143591729538505735331180115367886775975004232838998')  # 2pi/5 - 1e-3
K0, q0, u0 = K_of_v(v0)
print('  at v=2pi/5-1e-3: q =', mp.nstr(q0,10), ' K =', mp.nstr(K0,10))
# K' survey near both ends
def Kp_num(v):
    h = mp.mpf('1e-8')
    return (K_of_v(v+h)[0] - K_of_v(v-h)[0])/(2*h)
print('  Kp at 2pi/7:', mp.nstr(Kp_num(2*mp.pi/7), 8))
print('  Kp at 2pi/5-1e-3:', mp.nstr(Kp_num(v0), 8))
print('  Kp at 2pi/5-1e-4:', mp.nstr(Kp_num(mp.mpf('1.2566370614359172')-mp.mpf('1e-4')), 8))
# monotone increasing K' ?
prev = None
inc = True
v = mp.mpf('0.8975979010256552')
while v < v0:
    kp = Kp_num(v)
    if prev is not None and kp < prev - mp.mpf('1e-6'):
        inc = False
    prev = kp
    v += mp.mpf('1e-3')
print('  Kp increasing on [2pi/7, 2pi/5-1e-3] (sample):', inc)

print('=== Kp near limit: parametrize w = pi - 2.5v ===')
# q = tan v / tan w, w -> 0.  v = 0.4*pi - w/2.5
for w in ['1e-2','1e-3','1e-4','1e-5']:
    wv = mp.mpf(w)
    vv = mp.mpf('0.4')*mp.pi - wv/mp.mpf('2.5')
    K, q, u = K_of_v(vv)
    print('  w=%s: v=%s q=%s K=%s' % (w, mp.nstr(vv,10), mp.nstr(q,8), mp.nstr(K,10)))
