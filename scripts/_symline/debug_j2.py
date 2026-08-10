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
def J2_curve(c, q, which):
    x = alpha1(c,q) if which==1 else alpha2(c,q)
    Ph = Phi(x,q); D = q + c*Ph; u = x*Ph/D
    W = 3+2*x*mp.cot(x)
    Phx = 2*(q**2-1)*mp.sin(x)*mp.cos(x)
    Dx = c*Phx
    Wx = 2*mp.cot(x) - 2*x/mp.sin(x)**2
    S = x*Ph*mp.sin(x)*mp.cos(x)
    Sx = Ph*mp.sin(x)*mp.cos(x) + x*Phx*mp.sin(x)*mp.cos(x) + x*Ph*(mp.cos(x)**2-mp.sin(x)**2)
    Gx = -(Phx*W + Ph*Wx)/D + Ph*W*Dx/D**2 + 2*c*(q**2-1)*(Sx*D**2 - S*2*D*Dx)/D**4
    Dc = Ph
    Gc = Ph*W*Dc/D**2 + 2*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)*(D**2 - c*2*D*Dc)/D**4
    return Gval(x,c,q)**2 + Gc - u*Gx

for c0 in ['0.1','0.15','0.2','0.25','0.3','0.35']:
    cc = mp.mpf(c0)
    q = mp.mpf(1)
    J1 = J2_curve(cc,q,1); J2 = J2_curve(cc,q,2)
    a1=alpha1(cc,q); a2=alpha2(cc,q)
    M1=Mf(a1,cc,q); M2=Mf(a2,cc,q)
    h = mp.mpf('1e-5')
    Fepp = (Fep(cc+h,q)-Fep(cc-h,q))/(2*h)
    dec = M1*J1 - M2*J2
    print('c=%s: J1=%s J2=%s M1J1-M2J2=%s Fepp=%s  diff=%s' % (c0, mp.nstr(J1,8), mp.nstr(J2,8), mp.nstr(dec,8), mp.nstr(Fepp,8), mp.nstr(abs(dec-Fepp),6)))
