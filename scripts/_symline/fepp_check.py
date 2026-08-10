# -*- coding: utf-8 -*-
# Check second derivative of Fe on [q0,1]x[0.42,0.5]. EVIDENCE.
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

h = mp.mpf('1e-4')
print('=== second derivative on box ===')
for q0 in ['0.7','0.8165','0.9','1.0']:
    qq = mp.mpf(q0)
    for c0 in ['0.42','0.44','0.46','0.48','0.495']:
        cc = mp.mpf(c0)
        fpp = (Fep(cc+h,qq) - 2*Fep(cc,qq) + Fep(cc-h,qq))/h**2
        fp = (Fep(cc+h,qq)-Fep(cc-h,qq))/(2*h)
        print('  q=%s c=%s: Fep=%s Fepp=%s' % (q0,c0,mp.nstr(fp,7),mp.nstr(fpp,7)))
