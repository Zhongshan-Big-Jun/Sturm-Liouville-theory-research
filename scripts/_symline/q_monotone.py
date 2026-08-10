# -*- coding: utf-8 -*-
# Check pointwise monotonicity of Fep in q, and q=1 closed form. EVIDENCE.
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def alpha1(c,q):
    return mp.findroot(lambda A: mp.atan(1/(q*mp.tan(A))) - c*A, (mp.mpf('1e-30'), pi/2-mp.mpf('1e-30')), solver='bisect')
def alpha2(c,q):
    def O(x):
        if x < pi/2: return pi - mp.atan(q*mp.tan(x))
        elif x == pi/2: return pi/2
        else: return mp.atan(-q*mp.tan(x))
    return mp.findroot(lambda A: O(A) - c*A, (mp.mpf('1e-30'), pi-mp.mpf('1e-30')), solver='bisect')
def Phi(x,q): return mp.cos(x)**2 + q**2*mp.sin(x)**2
def Mf(x,c,q): return x**2*mp.sin(x)**2/(q + c*Phi(x,q))
def Fe(c,q): return Mf(alpha1(c,q),c,q) - Mf(alpha2(c,q),c,q)
def Gval(x,c,q):
    Ph = Phi(x,q); D = q + c*Ph
    return -Ph*(3+2*x*mp.cot(x))/D + 2*c*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def Fep(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mf(a1,c,q)*Gval(a1,c,q) - Mf(a2,c,q)*Gval(a2,c,q)

print('=== Fep(1,c) closed form check: alpha1=pi/(2(1+c)), alpha2=pi/(1+c) ===')
for c0 in ['0.1','0.3','0.5']:
    cc = mp.mpf(c0)
    a1c = pi/(2*(1+cc)); a2c = pi/(1+cc)
    a1 = alpha1(cc,mp.mpf(1)); a2 = alpha2(cc,mp.mpf(1))
    print('  c=%s: a1 err=%s a2 err=%s' % (c0, mp.nstr(abs(a1-a1c),4), mp.nstr(abs(a2-a2c),4)))

print('=== Fep(1,c) explicit: h(alpha)=alpha^3 sin^2 alpha (1-16 cos^2 alpha) ===')
# Fep(1,c) = (2/pi) * d/dc [alpha^3 sin^2 alpha (1-16cos^2 alpha)], alpha=pi/(2(1+c))
# = (2/pi)*alpha'(c)*h'(alpha) with alpha'(c) = -pi/(2(1+c)^2)
# so Fep(1,c) = -(1/(1+c)^2) * h'(alpha) = -(1/(1+c)^2)*alpha^2 sin^2 alpha [3(1-16c2)+2 alpha cot alpha (17-16c2)], c2=cos^2 alpha
for c0 in ['0.05','0.1','0.2','0.3','0.4','0.5']:
    cc = mp.mpf(c0)
    a = pi/(2*(1+cc)); c2 = mp.cos(a)**2
    hbracket = 3*(1-16*c2) + 2*a*mp.cot(a)*(17-16*c2)
    Fep1 = -(1/(1+cc)**2)*a**2*mp.sin(a)**2*hbracket
    Fep_num = Fep(cc, mp.mpf(1))
    print('  c=%s: Fep(1,c) closed=%s numeric=%s' % (c0, mp.nstr(Fep1,12), mp.nstr(Fep_num,12)))

print('=== pointwise monotonicity dFep/dq >= 0? ===')
for c0 in ['0.05','0.1','0.2','0.3','0.4','0.45','0.5']:
    cc = mp.mpf(c0)
    qq = mp.mpf('0.8165'); h = mp.mpf('1e-4')
    dq = (Fep(cc,qq+h)-Fep(cc,qq-h))/(2*h)
    print('  c=%s: dFep/dq at q=0.8165 = %s %s' % (c0, mp.nstr(dq,8), 'NEGATIVE!' if dq<0 else ''))
