# _audit_sub_C_tail_q1.py — tail bound B(q), q=1 closed forms, lem:inclusion endpoints
import mpmath as mp
mp.mp.dps = 40

def M2(q, w):
    A = mp.pi - mp.atan(w/q)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + mp.atan(w)*(4*A*w - 5*q - 9*q*w**2)

def dqM2(q, w, h=mp.mpf('1e-10')):
    return (M2(q+h, w) - M2(q-h, w))/(2*h)

def B(q):
    pi = mp.pi
    return (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*(2*q+1)/q + 1 + 2*pi*(2*q+1)/q**2 - 10*pi*q

mx = mp.mpf(0)
for qv in [20, 21, 25, 30, 40, 50, 80, 100, 200, 500, 1000, 5000, 20000]:
    qv = mp.mpf(qv)
    for wf in [mp.mpf('0.999'), mp.mpf('0.5'), mp.mpf('0.0')]:
        w = mp.sqrt(2*qv+1)*wf
        if w == 0: continue
        d = dqM2(qv, w) - B(qv)
        mx = max(mx, d)
print("tail: max(dqM2 - B) over q>=20 grid:", mx, " (<=0 required)")
print("TAIL BOUND OK:", mx <= 0)
print("B(20) =", B(mp.mpf(20)), " < -232.723:", B(mp.mpf(20)) < mp.mpf('-232.723'))

# q=1 closed forms
def J1_q1(x):
    N = 12 + 16*x/mp.tan(x) + 2*x**2/mp.tan(x)**2 - 2*x**2
    return (2*x/mp.pi)**2*N
def J2_q1(x):  # x = pi - gamma
    N = 12 + 16*x/mp.tan(x) + 2*x**2/mp.tan(x)**2 - 2*x**2
    return x**2/mp.pi**2*N
print("J1(pi/3,1) =", J1_q1(mp.pi/3))
print("J2(pi/3,1) =", J2_q1(2*mp.pi/3))
# lem:inclusion endpoints
print("arccos(2/3) =", mp.acos(mp.mpf(2)/3), " > 0.841:", mp.acos(mp.mpf(2)/3) > mp.mpf('0.841'))
print("5pi/14 =", 5*mp.pi/14, " < 1.1220:", 5*mp.pi/14 < mp.mpf('1.1220'))
print("pi/3 =", mp.pi/3, " < 1.0472:", mp.pi/3 < mp.mpf('1.0472'))
# gamma(2,2/5): root of (2/5)(pi-gamma) = arctan(2 tan gamma)
def h(g): return mp.mpf(2)/5*(mp.pi - g) - mp.atan(2*mp.tan(g))
g1 = mp.findroot(h, mp.mpf('0.66'))
print("gamma(2,2/5) =", g1, " > 0.655:", g1 > mp.mpf('0.655'))
print("h(0.655) =", h(mp.mpf('0.655')), " > 0:", h(mp.mpf('0.655')) > 0)
# tau(1.0472) < 13/10, alpha1(2,1/2) in (0.841,1.1220)
print("tau(1.0472) =", mp.atan(2*mp.tan(mp.mpf('1.0472'))), " < 1.3:", mp.atan(2*mp.tan(mp.mpf('1.0472'))) < mp.mpf('1.3'))
