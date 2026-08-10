# -*- coding: utf-8 -*-
import mpmath as mp
from fractions import Fraction as Fr
mp.mp.dps = 60
pi = mp.pi

# ---------- Chain 1: w(c) solves atan w = c(pi - atan(w/q)); check w<sqrt(2q+1), monotone ----------
def w_of_c(c, q):
    # solve atan w = c*(pi - atan(w/q)); bisection
    lo, hi = mp.mpf(0), mp.mpf(20)
    f = lambda w: mp.atan(w) - c*(pi - mp.atan(w/q))
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo+hi)/2
ok = True
prev = None
for qq in [mp.mpf(1.01), mp.mpf(2), mp.mpf(5), mp.mpf(20), mp.mpf(100)]:
    prev = None
    for cc in [mp.mpf('0.001'), mp.mpf(0.1), mp.mpf(0.25), mp.mpf(0.4), mp.mpf(0.49)]:
        w = w_of_c(cc, qq)
        assert w < mp.sqrt(2*qq+1), (qq, cc, w)
        assert w > 0
        if prev is not None: assert w > prev, ("mono fail", qq, cc)
        prev = w
    # check tan(c*A)=w, A=pi-atan(w/q)
    w = w_of_c(mp.mpf('0.37'), qq)
    A = pi - mp.atan(w/qq)
    assert abs(mp.atan(w) - mp.mpf('0.37')*A) < mp.mpf('1e-50')
print("Chain1: w<sqrt(2q+1) and strict monotonicity in c: OK (grid)")

# ---------- Chain 2: bound chain for d_q M2, q>=20 ----------
def dM2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return (4*A*A*w + 8*A*w*w*q/(q*q+w*w) - 7*w*q*q/(q*q+w*w) - 14*A*q - 9*w**3/(q*q+w*w)
            + 2*w/(1+w*w) + 4*A*q/(1+w*w) + t*(4*w*w/(q*q+w*w) - 5 - 9*w*w))
def intermediate(q):
    return (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*(2*q+1)/q - 14*pi*q + 14*mp.sqrt(2*q+1) + 4*pi*q + 1
def B(q):
    return (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*(2*q+1)/q + 1 + 2*pi*(2*q+1)/q**2 - 10*pi*q
worst = mp.mpf(-mp.inf)
for qq in [mp.mpf(20), mp.mpf(20.5), mp.mpf(30), mp.mpf(50), mp.mpf(100), mp.mpf(1000)]:
    for ww in [mp.mpf('1e-6'), mp.mpf('0.5'), mp.mpf(1), mp.mpf(3), mp.mpf(6), mp.mpf(10),
               mp.sqrt(2*qq+1)*mp.mpf('0.999999')]:
        if ww >= mp.sqrt(2*qq+1): continue
        slack_i = intermediate(qq) - dM2(qq, ww)
        slack_b = B(qq) - intermediate(qq)
        assert slack_i > 0 and slack_b > 0, (qq, ww, slack_i, slack_b)
        worst = max(worst, slack_i)
print("Chain2(d): dM2 <= intermediate <= B holds on grid; min slack (interm-dM2) =", worst)
print("B(20) =", B(mp.mpf(20)))
print("B(20) < -232.723:", B(mp.mpf(20)) < mp.mpf('-232.723'))
Bp = lambda q: (4*pi**2+14)/mp.sqrt(2*q+1) - 12*pi/q**2 - 4*pi/q**3 - 10*pi
print("B'(q) <= (4pi^2+14)/sqrt41 - 10pi for q>=20:",
      all(Bp(mp.mpf(qq)) <= (4*pi**2+14)/mp.sqrt(41) - 10*pi for qq in [20,25,30,50,100,1000]))
print("(4pi^2+14)/sqrt41 - 10pi =", (4*pi**2+14)/mp.sqrt(41) - 10*pi)

# ---------- Chain 2(e): M2/q^2 bound, w>sqrt41 ----------
def M2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + t*(4*A*w-5*q-9*q*w*w)
for qq in [mp.mpf(20.5), mp.mpf(25), mp.mpf(40), mp.mpf(100)]:
    for ww in [mp.sqrt(41)*mp.mpf('1.0001'), mp.mpf(7), mp.mpf(8), mp.sqrt(2*qq+1)*mp.mpf('0.9999')]:
        t = ww/qq
        if ww <= mp.sqrt(41) or ww >= mp.sqrt(2*qq+1): continue
        assert t <= mp.sqrt(41)/20 < mp.mpf('0.33')
        ub = 4*pi**2*mp.mpf('0.33') - 7*(pi-mp.mpf('0.33')) + 2*pi*(1+mp.mpf('0.33')**2)/42
        assert M2(qq,ww)/qq**2 <= ub and ub < 0, (qq, ww, M2(qq,ww)/qq**2, ub)
print("Chain2(e): M2/q^2 <= 4pi^2(0.33)-7(pi-0.33)+2pi(1+0.33^2)/42 < 0: OK")
print("value of the bound:", 4*pi**2*mp.mpf('0.33') - 7*(pi-mp.mpf('0.33')) + 2*pi*(1+mp.mpf('0.33')**2)/42)

# ---------- Chain 4: endpoint closed form ----------
def Fep(q, c):
    # M_f1*G1 - M_f2*G2 at the real phases
    def alpha1(q,c):
        lo, hi = mp.mpf('1e-12'), pi/2
        f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
        for _ in range(200):
            mid = (lo+hi)/2
            if f(mid) > 0: hi = mid
            else: lo = mid
        return (lo+hi)/2
    a1 = alpha1(q,c)
    # alpha2 in (pi/2, pi): O(x)=atan(-q tan x) for x in (pi/2,pi); solve O(x)=c x
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    a2 = (lo+hi)/2
    Mf = lambda x: x*x*mp.sin(x)**2/(q + c*(mp.cos(x)**2 + q*q*mp.sin(x)**2))
    G = lambda x: -(mp.cos(x)**2+q*q*mp.sin(x)**2)*(3+2*x*mp.cot(x))/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2)) \
                  + 2*c*x*(mp.cos(x)**2+q*q*mp.sin(x)**2)*(q*q-1)*mp.sin(x)*mp.cos(x)/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2))**2
    return Mf(a1)*G(a1) - Mf(a2)*G(a2), a1, a2
for qq in [mp.mpf(1.1), mp.mpf(1.5), mp.mpf(2.0)]:
    val, a1, a2 = Fep(qq, mp.mpf('0.5'))
    x = 2*mp.asin(1/mp.sqrt(2*(qq+1)))
    P = (pi-3*x)**2 + 3*(x-mp.sin(x))*(pi-2*x)
    closed = 2*pi*(mp.cos(x)-1)**3/mp.sin(x)**3*P
    assert abs(val - closed) < mp.mpf('1e-40'), (qq, val, closed)
    assert 0 < x < pi/3 and P > 0
print("Chain4: closed form F_e'(q,1/2) matches direct computation; x in (0,pi/3); P>0: OK")

# F_e'' > 0 cross-check on Q grid
def Fep2(q, c):
    def alpha1(q,c):
        lo, hi = mp.mpf('1e-12'), pi/2
        f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
        for _ in range(100):
            mid=(lo+hi)/2
            if f(mid)>0: hi=mid
            else: lo=mid
        return (lo+hi)/2
    a1 = alpha1(q,c)
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(100):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    a2=(lo+hi)/2
    Mf = lambda x: x*x*mp.sin(x)**2/(q + c*(mp.cos(x)**2 + q*q*mp.sin(x)**2))
    G = lambda x: -(mp.cos(x)**2+q*q*mp.sin(x)**2)*(3+2*x*mp.cot(x))/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2)) \
                  + 2*c*x*(mp.cos(x)**2+q*q*mp.sin(x)**2)*(q*q-1)*mp.sin(x)*mp.cos(x)/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2))**2
    # d/dc F_e' numerically via mp.diff on F_e'
    Fe = lambda cc: (lambda a1,a2: Mf(a1)*G(a1)-Mf(a2)*G(a2))(* (lambda aa1,aa2:(aa1,aa2))(*phase_of(cc,q)))
    return mp.diff(lambda cc: Fe(cc), c), a1, a2
def phase_of(c, q):
    lo, hi = mp.mpf('1e-12'), pi/2
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    for _ in range(100):
        mid=(lo+hi)/2
        if f(mid)>0: hi=mid
        else: lo=mid
    a1=(lo+hi)/2
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(100):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    return a1, (lo+hi)/2
mn = mp.mpf('1e9')
for qq in [mp.mpf(1), mp.mpf(1.2), mp.mpf(1.5), mp.mpf(1.8), mp.mpf(2)]:
    for cc in [mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.5')]:
        v = Fep2(qq, cc)[0]
        mn = min(mn, v)
        assert v > 0, (qq, cc, v)
print("Chain4: F_e''>0 on Q grid cross-check, min =", mn)
