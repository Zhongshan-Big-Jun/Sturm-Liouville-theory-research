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

q = mp.mpf('0.5'); c = mp.mpf('0.5')
a1 = alpha1(c,q); a2 = alpha2(c,q)
x = mp.acos(q/(q+1))
print('a1 =', mp.nstr(a1,15), ' x =', mp.nstr(x,15), ' a1-x =', mp.nstr(a1-x,5))
print('a2 =', mp.nstr(a2,15), ' pi-x =', mp.nstr(pi-x,15), ' a2-(pi-x) =', mp.nstr(a2-(pi-x),5))
Ph = Phi(a1,q); D = q + c*Ph
print('Phi(a1) =', mp.nstr(Ph,12), ' 2q^2/(q+1) =', mp.nstr(mp.mpf(2)*q**2/(q+1),12))
print('D =', mp.nstr(D,12), ' q(2q+1)/(q+1) =', mp.nstr(q*(2*q+1)/(q+1),12))
print('M1 closed =', mp.nstr(a1**2/(q*(q+1)),12), ' Mf(a1) =', mp.nstr(Mf(a1,c,q),12))
print('M2 closed =', mp.nstr((pi-a1)**2/(q*(q+1)),12), ' Mf(a2) =', mp.nstr(Mf(a2,c,q),12))
print('G1 closed =', mp.nstr(-Ph*(3+2*a1*mp.cot(a1))/D + a1*Ph*(q**2-1)*mp.sin(a1)*mp.cos(a1)/D**2,12), ' Gval(a1) =', mp.nstr(Gval(a1,c,q),12))
print('G2 closed =', mp.nstr(-Ph*(3-2*(pi-a1)*mp.cot(a1))/D - a1*(pi-a1)*Ph*(q**2-1)*mp.sin(a1)*mp.cos(a1)/D**2,12), ' Gval(a2) =', mp.nstr(Gval(a2,c,q),12))
print('Fep closed =', mp.nstr((a1**2/(q*(q+1)))*(-Ph*(3+2*a1*mp.cot(a1))/D + a1*Ph*(q**2-1)*mp.sin(a1)*mp.cos(a1)/D**2) - ((pi-a1)**2/(q*(q+1)))*(-Ph*(3-2*(pi-a1)*mp.cot(a1))/D - a1*(pi-a1)*Ph*(q**2-1)*mp.sin(a1)*mp.cos(a1)/D**2),12))
print('Fep via Gval =', mp.nstr(Mf(a1,c,q)*Gval(a1,c,q)-Mf(a2,c,q)*Gval(a2,c,q),12))
