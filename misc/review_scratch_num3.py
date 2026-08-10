# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
pi = mp.pi

def dM2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return (4*A*A*w + 8*A*w*w*q/(q*q+w*w) - 7*w*q*q/(q*q+w*w) - 14*A*q - 9*w**3/(q*q+w*w)
            + 2*w/(1+w*w) + 4*A*q/(1+w*w) + t*(4*w*w/(q*q+w*w) - 5 - 9*w*w))
def intermediate(q):  # 4pi^2 sqrt + 8pi(2q+1)/q -14pi q +14 sqrt +4pi q +1
    return (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*(2*q+1)/q + 1 - 10*pi*q
def B(q):
    return (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*(2*q+1)/q + 1 + 2*pi*(2*q+1)/q**2 - 10*pi*q
worst = mp.mpf('-1e30')
for qq in [mp.mpf(20), mp.mpf(20.5), mp.mpf(30), mp.mpf(50), mp.mpf(100), mp.mpf(1000)]:
    for ww in [mp.mpf('1e-6'), mp.mpf('0.5'), mp.mpf(1), mp.mpf(3), mp.mpf(6), mp.mpf(10),
               mp.sqrt(2*qq+1)*mp.mpf('0.999999')]:
        if ww >= mp.sqrt(2*qq+1): continue
        s_i = intermediate(qq) - dM2(qq, ww)
        s_b = B(qq) - intermediate(qq)
        assert s_i > 0 and s_b > 0, (qq, ww, s_i, s_b)
        worst = max(worst, s_i)
print("Chain2(d): dM2 <= intermediate <= B on grid; min slack (interm-dM2) =", worst)
print("B(20) =", B(mp.mpf(20)))
print("B(20) < -232.723:", B(mp.mpf(20)) < mp.mpf('-232.723'))
Bp = lambda q: (4*pi**2+14)/mp.sqrt(2*q+1) - 12*pi/q**2 - 4*pi/q**3 - 10*pi
print("B'(q) <= (4pi^2+14)/sqrt41 - 10pi for q>=20:",
      all(Bp(mp.mpf(qq)) <= (4*pi**2+14)/mp.sqrt(41) - 10*pi for qq in [20,25,30,50,100,1000]))
print("(4pi^2+14)/sqrt41 - 10pi =", (4*pi**2+14)/mp.sqrt(41) - 10*pi)

# ---------- Chain 2(e) ----------
def M2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + t*(4*A*w-5*q-9*q*w*w)
ub = 4*pi**2*mp.mpf('0.33') - 7*(pi-mp.mpf('0.33')) + 2*pi*(1+mp.mpf('0.33')**2)/42
for qq in [mp.mpf(20.5), mp.mpf(25), mp.mpf(40), mp.mpf(100)]:
    for ww in [mp.sqrt(41)*mp.mpf('1.0001'), mp.mpf(7), mp.mpf(8), mp.sqrt(2*qq+1)*mp.mpf('0.9999')]:
        t = ww/qq
        if ww <= mp.sqrt(41) or ww >= mp.sqrt(2*qq+1): continue
        assert t <= mp.sqrt(41)/20 < mp.mpf('0.33')
        assert M2(qq,ww)/qq**2 <= ub and ub < 0, (qq, ww, M2(qq,ww)/qq**2, ub)
print("Chain2(e): bound holds on grid; bound value =", ub)

# ---------- Chain 4: endpoint closed form + F_e''>0 ----------
def phases(c, q):
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
def Fep(c, q):
    a1, a2 = phases(c, q)
    Mf = lambda x: x*x*mp.sin(x)**2/(q + c*(mp.cos(x)**2 + q*q*mp.sin(x)**2))
    G = lambda x: -(mp.cos(x)**2+q*q*mp.sin(x)**2)*(3+2*x*mp.cot(x))/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2)) \
                  + 2*c*x*(mp.cos(x)**2+q*q*mp.sin(x)**2)*(q*q-1)*mp.sin(x)*mp.cos(x)/(q+c*(mp.cos(x)**2+q*q*mp.sin(x)**2))**2
    return Mf(a1)*G(a1) - Mf(a2)*G(a2)
for qq in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('2.0')]:
    val = Fep(mp.mpf('0.5'), qq)
    x = 2*mp.asin(1/mp.sqrt(2*(qq+1)))
    P = (pi-3*x)**2 + 3*(x-mp.sin(x))*(pi-2*x)
    closed = 2*pi*(mp.cos(x)-1)**3/mp.sin(x)**3*P
    assert abs(val - closed) < mp.mpf('1e-40'), (qq, val, closed)
    assert 0 < x < pi/3 and P > 0
print("Chain4: closed form matches direct computation (1e-40); x in (0,pi/3); P>0: OK")
mn = mp.mpf('1e9')
for qq in [mp.mpf(1), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('1.8'), mp.mpf(2)]:
    for cc in [mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.5')]:
        v = mp.diff(lambda c: Fep(c, qq), cc)
        mn = min(mn, v)
        assert v > 0, (qq, cc, v)
print("Chain4: F_e''>0 on Q grid cross-check; min =", mn)
