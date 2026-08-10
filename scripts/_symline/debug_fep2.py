# -*- coding: utf-8 -*-
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
def Gval(x,c,q):
    Ph = Phi(x,q); D = q + c*Ph
    return -Ph*(3+2*x*mp.cot(x))/D + 2*c*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def Fep(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mf(a1,c,q)*Gval(a1,c,q) - Mf(a2,c,q)*Gval(a2,c,q)

q = mp.mpf('0.8165')
c = mp.mpf('0.42')
h = mp.mpf('1e-4')
v0 = Fep(c,q); vp = Fep(c+h,q); vm = Fep(c-h,q)
print('Fep(c-h) =', mp.nstr(vm,12))
print('Fep(c)   =', mp.nstr(v0,12))
print('Fep(c+h) =', mp.nstr(vp,12))
print('fp =', mp.nstr((vp-vm)/(2*h),12))
print('fpp =', mp.nstr((vp-2*v0+vm)/h**2,12))
# also check alpha values at the three points
for cc in [c-h, c, c+h]:
    a1=alpha1(cc,q); a2=alpha2(cc,q)
    print('  c=%s: a1=%s a2=%s' % (mp.nstr(cc,6), mp.nstr(a1,8), mp.nstr(a2,8)))
