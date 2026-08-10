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
def Fe(c,q):
    return Mf(alpha1(c,q),c,q) - Mf(alpha2(c,q),c,q)

q = mp.mpf('0.8165')
c = mp.mpf('0.42')
a1 = alpha1(c,q); a2 = alpha2(c,q)
print('a1 =', mp.nstr(a1,15))
print('a2 =', mp.nstr(a2,15))
print('cot(a1) =', mp.nstr(mp.cot(a1),10), ' cot(a2) =', mp.nstr(mp.cot(a2),10))
print('M1 =', mp.nstr(Mf(a1,c,q),10), ' M2 =', mp.nstr(Mf(a2,c,q),10))
print('G1 =', mp.nstr(Gval(a1,c,q),10), ' G2 =', mp.nstr(Gval(a2,c,q),10))
print('M1G1 =', mp.nstr(Mf(a1,c,q)*Gval(a1,c,q),10))
print('M2G2 =', mp.nstr(Mf(a2,c,q)*Gval(a2,c,q),10))
print('Fep analytic =', mp.nstr(Fep(c,q),10))
h = mp.mpf('1e-6')
print('Fep numeric  =', mp.nstr((Fe(c+h,q)-Fe(c-h,q))/(2*h),10))
print('Fe at c-1e-6, c, c+1e-6:', mp.nstr(Fe(c-h,q),10), mp.nstr(Fe(c,q),10), mp.nstr(Fe(c+h,q),10))
