# -*- coding: utf-8 -*-
# key_lemma_verify.py — comprehensive EVIDENCE checks for gap (a) KEY LEMMA components.
# All results are numeric cross-checks (EVIDENCE); the proof itself is analytic (STRICT).
import mpmath as mp
mp.mp.dps = 50
pi = mp.pi

def Efun(x, q):
    return mp.atan(1/(q*mp.tan(x)))
def Ofun(x, q):
    if x < pi/2: return pi - mp.atan(q*mp.tan(x))
    elif x == pi/2: return pi/2
    else: return mp.atan(-q*mp.tan(x))
def alpha1(c, q):
    return mp.findroot(lambda A: Efun(A, q) - c*A, (mp.mpf('1e-40'), pi/2-mp.mpf('1e-40')), solver='bisect')
def alpha2(c, q):
    return mp.findroot(lambda A: Ofun(A, q) - c*A, (mp.mpf('1e-40'), pi-mp.mpf('1e-40')), solver='bisect')
def Phi(x, q): return mp.cos(x)**2 + q**2*mp.sin(x)**2
def Mf(x, c, q): return x**2*mp.sin(x)**2/(q + c*Phi(x, q))
def Gval(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph
    return -Ph*(3+2*x*mp.cot(x))/D + 2*c*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def G1(c, q): return Gval(alpha1(c, q), c, q)
def G2(c, q): return Gval(alpha2(c, q), c, q)
def M1(c, q): return Mf(alpha1(c, q), c, q)
def M2(c, q): return Mf(alpha2(c, q), c, q)
def Fe(c, q): return M1(c, q) - M2(c, q)
def Fep_num(c, q, h=mp.mpf('1e-7')):
    return (Fe(c+h, q)-Fe(c-h, q))/(2*h)
def W0(g): return 3 - 2*(pi-g)*mp.cot(g)

q0 = mp.sqrt(mp.mpf(2)/3)
Gamma = mp.acos(q0/(1+q0))

print('q0 =', mp.nstr(q0, 12), ' Gamma =', mp.nstr(Gamma, 12), ' (4/3)q0 =', mp.nstr(4*q0/3, 12))
print('W0(Gamma) =', mp.nstr(W0(Gamma), 12), ' < (4/3)q0 ?', W0(Gamma) < 4*q0/3)

print()
print('=== P1: G1 bound.  Want G1 <= -3/(1/q0+1/2) ~ -1.7394 < -4/3 ===')
mx = mp.mpf('-1e99'); at = None
for qi in range(0, 21):
    q = q0 + (1-q0)*qi/20
    for ci in range(1, 50):
        c = mp.mpf(ci)/100
        g = G1(c, q)
        if g > mx: mx = g; at = (c, q)
print('  max G1 over (0,1/2)x[q0,1] grid =', mp.nstr(mx, 10), 'at', mp.nstr(at[0],6), mp.nstr(at[1],6))
print('  bound 3/(1/q0+1/2) =', mp.nstr(3/(1/q0+mp.mpf('0.5')), 10))

print()
print('=== P2: G2 bound.  Want G2 > -4/3 (we prove >= -W0/q >= -1/q0) ===')
mn = mp.mpf('1e99'); at = None
for qi in range(0, 21):
    q = q0 + (1-q0)*qi/20
    for ci in range(1, 50):
        c = mp.mpf(ci)/100
        g = G2(c, q)
        if g < mn: mn = g; at = (c, q)
print('  min G2 over grid =', mp.nstr(mn, 10), 'at', mp.nstr(at[0],6), mp.nstr(at[1],6), ' (should be > -1.225 = -1/q0)')

print()
print('=== W0 monotone + range on (0, Gamma] ===')
d = (W0(Gamma+mp.mpf('1e-6'))-W0(Gamma-mp.mpf('1e-6')))/mp.mpf('2e-6')
print('  W0\'(Gamma) ~', mp.nstr(d, 8), '>0; W0(0.001)=', mp.nstr(W0(mp.mpf('0.001')),8))
print('  W0 min on [0.0001,Gamma] =', mp.nstr(min(W0(Gamma*g) for g in [mp.mpf('1e-4')] + [mp.mpf(k)/1000 for k in range(1,1000)]), 8))
print('  W0 max on [0.0001,Gamma] =', mp.nstr(max(W0(Gamma*g) for g in [mp.mpf('1e-4')] + [mp.mpf(k)/1000 for k in range(1,1000)]), 8))

print()
print('=== G1-G2 < 0 on grid ===')
mx = mp.mpf('-1e99'); at = None
for qi in range(0, 21):
    q = q0 + (1-q0)*qi/20
    for ci in range(1, 50):
        c = mp.mpf(ci)/100
        v = G1(c,q)-G2(c,q)
        if v > mx: mx = v; at = (c, q)
print('  max(G1-G2) =', mp.nstr(mx, 10), 'at', mp.nstr(at[0],6), mp.nstr(at[1],6))

print()
print('=== Endpoints ===')
for qs in ['0.8165','0.85','0.9','0.95','1.0']:
    q = mp.mpf(qs)
    print('  q=%s: Fe(1e-6)=%s, Fe(0.5)=%s, Fe(0.5)/(pi sin^2 a1 (2a1-pi)/(q+Phi/2)) ratio=%s' % (
        qs, mp.nstr(Fe(mp.mpf('1e-6'),q),8), mp.nstr(Fe(mp.mpf('0.5'),q),8),
        mp.nstr(Fe(mp.mpf('0.5'),q)/(pi*mp.sin(alpha1(mp.mpf('0.5'),q))**2*(2*alpha1(mp.mpf('0.5'),q)-pi)/(q+Phi(alpha1(mp.mpf('0.5'),q),q)/2)), 8)))
print('  pi^2/(4q0) =', mp.nstr(pi**2/(4*q0), 8))

print()
print('=== Unique zero c* of Fe on (0,1/2), and Fe\' sign where Fe>=0 ===')
for qs in ['0.8165','0.9','1.0']:
    q = mp.mpf(qs)
    # locate zero
    c1, c2 = mp.mpf('1e-4'), mp.mpf('0.499')
    while c2-c1 > mp.mpf('1e-14'):
        mid = (c1+c2)/2
        if Fe(mid,q) > 0: c1 = mid
        else: c2 = mid
    cstar = (c1+c2)/2
    # check Fep < 0 on grid where Fe >= 0
    bad = 0; worst = mp.mpf('-1e99')
    for ci in range(1, 499):
        c = mp.mpf(ci)/1000
        if Fe(c,q) >= 0:
            fp = Fep_num(c,q)
            worst = max(worst, fp)
            if fp >= 0: bad += 1
    print('  q=%s: c*=%s, Fe>0 on (0,c*), Fe<0 on (c*,0.5)? check: Fe(c*+1e-4)=%s; Fe(c*-1e-4)=%s; max Fe\' on {Fe>=0} = %s (bad count %d)' % (
        qs, mp.nstr(cstar,10), mp.nstr(Fe(cstar+mp.mpf('1e-4'),q),6), mp.nstr(Fe(cstar-mp.mpf('1e-4'),q),6), mp.nstr(worst,6), bad))

print()
print('=== Easy region c>=1/2: Fe<0 ===')
mx = mp.mpf('-1e99'); at=None
for qs in ['0.8165','0.9','1.0']:
    q = mp.mpf(qs)
    for ci in range(50, 201):
        c = mp.mpf(ci)/100
        if Fe(c,q) > mx: mx = Fe(c,q); at=(c,q)
print('  max Fe on [0.5,2.0]x{q0,0.9,1} =', mp.nstr(mx,10), 'at', mp.nstr(at[0],6), mp.nstr(at[1],6))

print()
print('=== D(c) and D(v) structure ===')
def Dc_val(c, q):
    # D(c) = 4(c+q)^2*(a2^2-a1^2)
    return 4*(c+q)**2*(alpha2(c,q)**2-alpha1(c,q)**2)
def Dc_deriv_num(c, q, h=mp.mpf('1e-7')):
    return (Dc_val(c+h,q)-Dc_val(c-h,q))/(2*h)
q = mp.mpf('0.8165'); m = 1/q
# D_c sign vs -Fe
bad = 0
for ci in range(1, 200):
    c = mp.mpf(ci)/200
    dD = Dc_deriv_num(c,q)
    if (dD > 0) != (Fe(c,q) < 0): bad += 1
print('  D_c sign = -sign(Fe) violations:', bad)
print('  D(0+) limit (c=1e-6):', mp.nstr(Dc_val(mp.mpf('1e-6'),q),8), ' vs 3pi^2/R =', mp.nstr(3*pi**2*q**2,8))
print('  D(inf) limit (c=100):', mp.nstr(Dc_val(mp.mpf('100'),q),8), ' vs 3pi^2 =', mp.nstr(3*pi**2,8))
print('  D(c*):')
for qs in ['0.8165','0.9','1.0']:
    qq = mp.mpf(qs); mm = 1/qq
    c1, c2 = mp.mpf('1e-4'), mp.mpf('0.499')
    while c2-c1 > mp.mpf('1e-13'):
        mid=(c1+c2)/2
        if Fe(mid,qq)>0: c1=mid
        else: c2=mid
    cs=(c1+c2)/2
    print('    q=%s: c*=%s D(c*)=%s < 3pi^2/R=%s ? %s' % (qs, mp.nstr(cs,8), mp.nstr(Dc_val(cs,qq),8), mp.nstr(3*pi**2*qq**2,8), Dc_val(cs,qq) < 3*pi**2*qq**2))

print()
print('=== S_R identity: S_R(xi) = -8 q^2 (c+q)^3 Fe(c) ===')
# compute S_R(xi) = f(xi) via FH: dD/dxi = -2(R-1) S_R, so S_R = -dD/dxi/(2(R-1))
for R0 in ['1.2','1.5']:
    Rv = mp.mpf(R0); mm = mp.sqrt(Rv); qq = 1/mm
    for v in ['0.2','0.3','0.35','0.4','0.45']:
        vv = mp.mpf(v)
        cc = (1-2*vv)/(2*mm*vv)
        h = mp.mpf('1e-6')
        dD = (Dc_val(cc+h,qq)-Dc_val(cc-h,qq))/(2*h)  # D_c
        # c'(v) = d/dv [(1-2v)/(2mv)] = (-2*(2mv) - (1-2v)*2m)/(4 m^2 v^2) = (-4mv - 2m + 4mv)/(4m^2v^2) = -2m/(4m^2v^2) = -1/(2 m v^2)
        dc = -1/(2*mm*vv**2)
        dDdv = dD*dc
        SR = -dDdv/(2*(Rv-1))
        rhs = -8*qq**2*(cc+qq)**3*Fe(cc,qq)
        print('    R=%s v=%s: S_R=%s, rhs=%s, rel err=%s' % (R0, v, mp.nstr(SR,10), mp.nstr(rhs,10), mp.nstr(abs(SR-rhs)/abs(rhs),4)))
