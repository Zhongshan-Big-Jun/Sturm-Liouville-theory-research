# -*- coding: utf-8 -*-
"""verify_analytic_parts.py -- checks for the analytic proof building blocks.
1. B(q) upper-bounds dM2/dq for q>=20 on u in (0,sqrt(2q+1)).
2. direct bound: M2 < 0 on {q>20, sqrt(41)<u<sqrt(2q+1)} via M2/q^2 <= 4pi^2 tmax - 7(pi-atan tmax) + 2pi(1+t^2)/(1+41).
3. M2 < 0 on fine grid over D.
4. C4 tail identity: T^3 K = 5vu^3(1+T^2) - 3u^3T(1+T^2) + 2vu^2T(1+T^2) - 1.2u^2(1+u^2)T^2, and lower bound.
5. CORNER: closed form factorizations (symbolic + numeric).
"""
import mpmath as mp
mp.mp.dps = 60

def M2_formula(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u)
    return (4*A*A*u*q - 7*A*q*q - 9*A*u*u + 2*A*(q*q+u*u)/(1+u*u)
            + t*(4*A*u - 5*q - 9*q*u*u))

def dM2dq_formula(q, u):
    A = mp.pi - mp.atan(u/q); t = mp.atan(u)
    S = q*q + u*u
    return (4*A*A*u + 8*A*u*u*q/S - 7*q*q*u/S - 14*A*q - 9*u**3/S
            + 2*u/(1+u*u) + 4*A*q/(1+u*u) + t*(4*u*u/S - 5 - 9*u*u))

def Bq(q):
    return (4*mp.pi**2+14)*mp.sqrt(2*q+1) + 8*mp.pi*(2*q+1)/q + 1 + 2*mp.pi*(2*q+1)/(q*q) - 10*mp.pi*q

print('=== 1. dM2/dq <= B(q) for q>=20, u in (0,sqrt(2q+1)) ===')
bad = 0
worst_gap = None
for q in mp.linspace(20, 5000, 400):
    umax = mp.sqrt(2*q+1)
    for u in [umax*mp.mpf('0.01'), umax*mp.mpf('0.5'), umax*mp.mpf('0.99')]:
        v = dM2dq_formula(q, u)
        gap = Bq(q) - v
        if gap < 0:
            bad += 1
        if worst_gap is None or gap < worst_gap:
            worst_gap = gap
print('  violations:', bad, ' worst gap (B - dM2/dq):', mp.nstr(worst_gap, 6))

print('=== 2. direct bound M2/q^2 for q>20, u>sqrt(41) ===')
tmax = mp.sqrt(41)/mp.mpf(20)
Amin = mp.pi - mp.atan(tmax)
bound = 4*mp.pi**2*tmax - 7*Amin + 2*mp.pi*(1+tmax*tmax)/(1+41)
print('  tmax =', mp.nstr(tmax,10), ' Amax... Amin =', mp.nstr(Amin,10), ' bound M2/q^2 <=', mp.nstr(bound,10))
bad = 0
for q in mp.linspace(20.0001, 1e6, 300):
    u0 = mp.sqrt(41)*mp.mpf('1.0001')
    u1 = mp.sqrt(2*q+1)*mp.mpf('0.999')
    if u0 >= u1:
        continue
    for u in [u0, (u0+u1)/2, u1]:
        v = M2_formula(q, u)/q/q
        if v >= bound + mp.mpf('1e-30'):
            bad += 1
print('  violations of direct bound:', bad)

print('=== 3. M2 < 0 on D, fine grid ===')
bad = 0
worst = None
for q in mp.linspace(1.0001, 100, 500):
    umax = mp.sqrt(2*q+1)
    for u in mp.linspace(1e-6, umax*mp.mpf('0.99999'), 40):
        v = M2_formula(q, u)
        if v >= 0:
            bad += 1
        if worst is None or v < worst:
            worst = v
print('  nonneg violations:', bad, ' min M2:', mp.nstr(worst, 6))

print('=== 4. C4 tail identity and lower bound ===')
def K_v(v):
    u = mp.tan(v); w = mp.pi - mp.mpf('2.5')*v
    q = mp.sin(v)*mp.cos(w)/(mp.cos(v)*mp.sin(w))
    return (q*q+u*u)*(5*v*q - 3*u + 2*v) - mp.mpf('1.2')*u*q*(1+u*u)
def K_tail_identity(v):
    w = mp.pi - mp.mpf('2.5')*v
    T = mp.tan(w); u = mp.tan(v)
    return 5*v*u**3*(1+T*T) - 3*u**3*T*(1+T*T) + 2*v*u*u*T*(1+T*T) - mp.mpf('1.2')*u*u*(1+u*u)*T*T
bad = 0
for w in mp.linspace(mp.mpf('1e-6'), mp.mpf('2.5e-3'), 100):
    v = mp.mpf('0.4')*mp.pi - w/mp.mpf('2.5')
    T = mp.tan(w)
    lhs = T**3*K_v(v)
    rhs = K_tail_identity(v)
    if mp.fabs(lhs-rhs) > mp.mpf('1e-40')*mp.fabs(lhs):
        bad += 1
print('  identity violations:', bad)
# lower bound with clean constants
vmin = mp.mpf('1.25'); umin = mp.mpf('3.06'); umax = mp.mpf('3.08'); Tmax = mp.mpf('2.50002e-3')
lb = 5*vmin*umin**3 - 3*umax**3*Tmax*(1+Tmax*Tmax) - mp.mpf('1.2')*umax*umax*(1+umax*umax)*Tmax*Tmax
print('  clean lower bound for T^3 K:', mp.nstr(lb, 10))
# verify each ingredient
print('  v >= 1.25 on tail:', mp.mpf('0.4')*mp.pi - mp.mpf('2.5e-3')/mp.mpf('2.5') >= mp.mpf('1.25'))
print('  u_min = tan(2pi/5 - 1e-3) =', mp.nstr(mp.tan(mp.mpf('0.4')*mp.pi - mp.mpf('1e-3')), 10), ' >= 3.06:', mp.tan(mp.mpf('0.4')*mp.pi - mp.mpf('1e-3')) >= mp.mpf('3.06'))
print('  u_max = tan(2pi/5) =', mp.nstr(mp.tan(mp.mpf('0.4')*mp.pi), 10), ' <= 3.08:', mp.tan(mp.mpf('0.4')*mp.pi) <= mp.mpf('3.08'))

print('=== 5. CORNER: closed form checks ===')
# numeric: G2(1/2;q) vs 2q((pi-x)(q+1)-3sqrt(2q+1))/(2q+1)^{3/2} and vs 2q sqrt(1-cosx)(pi-x-3sinx)/(1+cosx)^{3/2}
def G2_half_num(q):
    a = mp.pi - 2*mp.asin(1/mp.sqrt(2*(q+1)))
    Ph = mp.cos(a)**2 + q*q*mp.sin(a)**2
    D = q + mp.mpf('0.5')*Ph
    W = 3 + 2*a/mp.tan(a)
    return -Ph*W/D + 2*mp.mpf('0.5')*a*Ph*(q*q-1)*mp.sin(a)*mp.cos(a)/D/D
def cf1(q):
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    return 2*q*((mp.pi-x)*(q+1) - 3*mp.sqrt(2*q+1))/(2*q+1)**mp.mpf('1.5')
def cf2(q):
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    return 2*q*mp.sqrt(1-mp.cos(x))*(mp.pi - x - 3*mp.sin(x))/(1+mp.cos(x))**mp.mpf('1.5')
bad = 0
for q in ['2','3','10','100','1000']:
    qv = mp.mpf(q)
    a = G2_half_num(qv); b = cf1(qv); c = cf2(qv)
    if mp.fabs(a-b) > mp.mpf('1e-50'): bad += 1
    if mp.fabs(a-c) > mp.mpf('1e-50'): bad += 1
    print('  q=%s G2(1/2;q)=%s  cf1=%s  cf2=%s  pi-x-3sinx=%s' % (q, mp.nstr(a,10), mp.nstr(b,10), mp.nstr(c,10), mp.nstr(mp.pi - 2*mp.asin(1/mp.sqrt(2*(qv+1))) - 3*mp.sin(2*mp.asin(1/mp.sqrt(2*(qv+1)))), 10)))
print('  closed-form mismatches:', bad)
print('  G2(1/2;2) =', mp.nstr(G2_half_num(2), 16), ' 12(pi - arccos(2/3) - sqrt5)/(5 sqrt5) =', mp.nstr(12*(mp.pi - mp.acos(mp.mpf(2)/3) - mp.sqrt(5))/(5*mp.sqrt(5)), 16))
