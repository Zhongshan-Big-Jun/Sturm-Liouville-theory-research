# -*- coding: utf-8 -*-
# key_lemma_verify2.py — remaining EVIDENCE checks: S_R identity, gamma range, W0 cases,
# easy region over wide c, alpha1+alpha2=pi at c=1/2, Fep closed-form comparison.
import mpmath as mp
mp.mp.dps = 50
pi = mp.pi

def Efun(x, q): return mp.atan(1/(q*mp.tan(x)))
def Ofun(x, q):
    if x < pi/2: return pi - mp.atan(q*mp.tan(x))
    elif x == pi/2: return pi/2
    else: return mp.atan(-q*mp.tan(x))
def alpha1(c, q): return mp.findroot(lambda A: Efun(A,q)-c*A, (mp.mpf('1e-40'), pi/2-mp.mpf('1e-40')), solver='bisect')
def alpha2(c, q): return mp.findroot(lambda A: Ofun(A,q)-c*A, (mp.mpf('1e-40'), pi-mp.mpf('1e-40')), solver='bisect')
def Phi(x, q): return mp.cos(x)**2 + q**2*mp.sin(x)**2
def Mf(x, c, q): return x**2*mp.sin(x)**2/(q + c*Phi(x,q))
def Gval(x, c, q):
    Ph = Phi(x,q); D = q + c*Ph
    return -Ph*(3+2*x*mp.cot(x))/D + 2*c*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def G1(c,q): return Gval(alpha1(c,q),c,q)
def G2(c,q): return Gval(alpha2(c,q),c,q)
def M1(c,q): return Mf(alpha1(c,q),c,q)
def M2(c,q): return Mf(alpha2(c,q),c,q)
def Fe(c,q): return M1(c,q)-M2(c,q)
def Dc_val(c,q): return 4*(c+q)**2*(alpha2(c,q)**2-alpha1(c,q)**2)
def W0(g): return 3 - 2*(pi-g)*mp.cot(g)

q0 = mp.sqrt(mp.mpf(2)/3)
Gamma = mp.acos(q0/(1+q0))

print('=== gamma range: gamma = pi - alpha2 in (0, gamma0(q)] subset (0, Gamma] ===')
ok = True
for qs in ['0.8165','0.85','0.9','0.95','1.0']:
    q = mp.mpf(qs)
    gmax = 0
    for ci in range(1, 50):
        c = mp.mpf(ci)/100
        g = pi - alpha2(c,q)
        gmax = max(gmax, g)
    print('  q=%s: max gamma on c in (0,0.5] = %s ; gamma0(q)=%s ; <= Gamma=%s ? %s' % (
        qs, mp.nstr(gmax,8), mp.nstr(mp.acos(q/(1+q)),8), mp.nstr(Gamma,8), gmax <= Gamma))
    ok = ok and gmax <= Gamma
print('  all ok:', ok)

print()
print('=== W0 case analysis: if W0<=0 then G2>=0; if 0<W0 then G2 >= -W0/q > -4/3 ===')
mn_viol = mp.mpf('1e99'); ncase = [0,0]; worst_ratio = mp.mpf('1e99')
for qi in range(0, 21):
    q = q0 + (1-q0)*qi/20
    for ci in range(1, 50):
        c = mp.mpf(ci)/100
        g = pi - alpha2(c,q)
        w = W0(g)
        g2 = G2(c,q)
        if w <= 0:
            ncase[0] += 1
            if g2 < 0: mn_viol = min(mn_viol, g2)
        else:
            ncase[1] += 1
            # G2 >= -Phi*W0/D >= -W0/q ; check direct
            bound = -w/q
            if g2 < bound - mp.mpf('1e-30'): mn_viol = min(mn_viol, g2-bound)
            worst_ratio = min(worst_ratio, w/(4*q0/3))
print('  cases W0<=0:', ncase[0], ' W0>0:', ncase[1])
print('  min violation (should stay ~0) =', mp.nstr(mn_viol, 6))
print('  max W0/((4/3)q0) ratio =', mp.nstr(worst_ratio, 8), ' (<1 means W0 < (4/3)q0)')

print()
print('=== alpha1+alpha2 = pi at c=1/2 ===')
for qs in ['0.8165','0.9','1.0']:
    q = mp.mpf(qs)
    a1 = alpha1(mp.mpf('0.5'),q); a2 = alpha2(mp.mpf('0.5'),q)
    print('  q=%s: a1+a2-pi = %s ; tan(a1/2) = %s, 1/sqrt(2q+1)=%s' % (
        qs, mp.nstr(a1+a2-pi, 8), mp.nstr(mp.tan(a1/2),8), mp.nstr(1/mp.sqrt(2*q+1),8)))

print()
print('=== closed form T(x) value vs simple formula ===')
def T(x): return pi**2 - 3*x*(pi-x) - 3*(pi-2*x)*mp.sin(x)
for qs in ['0.8165','0.9','1.0']:
    q = mp.mpf(qs)
    x = mp.acos(q/(1+q))
    cf = -2*pi*(1-mp.cos(x))**3*T(x)/mp.sin(x)**3
    a1 = alpha1(mp.mpf('0.5'),q)
    simple = pi*mp.sin(a1)**2*(2*a1-pi)/(q+Phi(a1,q)/2)
    print('  q=%s: closed=%s, simple=%s, rel diff=%s' % (qs, mp.nstr(cf,10), mp.nstr(simple,10), mp.nstr(abs(cf-simple)/abs(simple),4)))

print()
print('=== easy region c>=1/2 over wide range ===')
mx = mp.mpf('-1e99'); at=None
for qs in ['0.8165','0.9','1.0']:
    q = mp.mpf(qs)
    for ci in range(50, 5001):
        c = mp.mpf(ci)/100
        v = Fe(c,q)
        if v > mx: mx = v; at=(c,q)
print('  max Fe on [0.5,50] =', mp.nstr(mx,8), 'at c=%s q=%s' % (mp.nstr(at[0],5), mp.nstr(at[1],5)))

print()
print('=== S_R identity: S_R(xi) = -8 q^2 (c+q)^3 Fe(c) ===')
for R0 in ['1.2','1.5']:
    Rv = mp.mpf(R0); mm = mp.sqrt(Rv); qq = 1/mm
    for v in ['0.2','0.3','0.35','0.4','0.45']:
        vv = mp.mpf(v)
        cc = (1-2*vv)/(2*mm*vv)
        h = mp.mpf('1e-6')
        dDdc = (Dc_val(cc+h,qq)-Dc_val(cc-h,qq))/(2*h)
        dcdv = -1/(2*mm*vv**2)
        dDdv = dDdc*dcdv
        SR = -dDdv/(2*(Rv-1))
        rhs = -8*qq**2*(cc+qq)**3*Fe(cc,qq)
        print('    R=%s v=%s: S_R=%s rhs=%s rel err=%s' % (R0, v, mp.nstr(SR,10), mp.nstr(rhs,10), mp.nstr(abs(SR-rhs)/abs(rhs),4)))

print()
print('=== D(v) monotone structure on symmetric line (v-grid) ===')
for R0 in ['1.2','1.5']:
    Rv = mp.mpf(R0); mm = mp.sqrt(Rv); qq = 1/mm
    prev = None; monotone = True
    vstar = None; dmin = mp.mpf('1e99')
    for vi in range(1, 500):
        v = mp.mpf(vi)/1000
        cc = (1-2*v)/(2*mm*v)
        Dv = Dc_val(cc,qq)
        if Dv < dmin: dmin = Dv; vstar = v
        if prev is not None:
            # expected: decreasing until v*, increasing after
            pass
        prev = Dv
    # check decreasing on (0,vstar), increasing on (vstar,1/2)
    ok1 = ok2 = True
    prev = None
    for vi in range(1, 499):
        v = mp.mpf(vi)/1000
        cc = (1-2*v)/(2*mm*v)
        Dv = Dc_val(cc,qq)
        if prev is not None:
            if v < vstar and Dv > prev + mp.mpf('1e-30'): ok1 = False
            if v > vstar and Dv < prev - mp.mpf('1e-30'): ok2 = False
        prev = Dv
    print('  R=%s: v*=%s D*=%s ; decreasing on (0,v*)? %s ; increasing on (v*,1/2)? %s ; D(0.001)=%s D(0.499)=%s' % (
        R0, mp.nstr(vstar,6), mp.nstr(dmin,8), ok1, ok2, mp.nstr(Dc_val((1-2*mp.mpf('0.001'))/(2*mm*mp.mpf('0.001')),qq),8), mp.nstr(Dc_val((1-2*mp.mpf('0.499'))/(2*mm*mp.mpf('0.499')),qq),8)))
