# -*- coding: utf-8 -*-
# Check Fe''(c) = d/dc Fep over FULL (0,1/2) for q in [q0,1]. EVIDENCE.
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
print('=== Fepp = d/dc Fep over (0, 1/2): min ===')
q0 = mp.sqrt(mp.mpf(2)/3)
for q in [q0, mp.mpf('0.85'), mp.mpf('0.9'), mp.mpf('1.0')]:
    mn = mp.mpf('1e99'); mn_at=None
    for k in range(1, 249):
        c = mp.mpf(k)/500
        fp2 = (Fep(c+h,q)-Fep(c-h,q))/(2*h)
        if fp2 < mn: mn = fp2; mn_at = c
    print('  q=%s: min Fepp = %s at c=%s %s' % (mp.nstr(q,5), mp.nstr(mn,8), mp.nstr(mn_at,5), 'NEGATIVE!' if mn<0 else ''))

print('=== Fepp at selected c (q=q0) ===')
q = q0
for k in [1,2,5,10,20,40,80,120,160,200,240]:
    c = mp.mpf(k)/500
    fp2 = (Fep(c+h,q)-Fep(c-h,q))/(2*h)
    print('  c=%s: Fepp=%s' % (mp.nstr(c,4), mp.nstr(fp2,8)))
