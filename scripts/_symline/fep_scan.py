# -*- coding: utf-8 -*-
# Scan F~_e'(c) and its components for q in (0,1). EVIDENCE.
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
def Fep(c,q,h=mp.mpf('1e-6')):
    return (Fe(c+h,q)-Fe(c-h,q))/(2*h)
def Fep_analytic(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mf(a1,c,q)*Gval(a1,c,q) - Mf(a2,c,q)*Gval(a2,c,q)

# 1) verify G-decomposition identity for q<1
print('=== G-decomposition check (Fep_analytic vs numeric) ===')
for q in ['0.3','0.5','0.8165','0.9','0.99']:
    qq = mp.mpf(q)
    for c in ['0.1','0.3','0.45']:
        cc = mp.mpf(c)
        diff = abs(Fep_analytic(cc,qq)-Fep(cc,qq))
        print('  q=%s c=%s: |analytic-numeric|=%s' % (q,c,mp.nstr(diff,4)))

# 2) F~_e' sign over grid; find max
print('=== F~_e max over (q,c) grid ===')
qmax = mp.mpf('-1e99'); qmax_at = None
for q in ['0.7','0.8','0.8165','0.5','0.7','0.8','0.8165','0.85','0.9','0.95','0.99','0.999']:
    qq = mp.mpf(q)
    best = mp.mpf('-1e99'); bestc = None
    for k in range(1,200):
        cc = mp.mpf(k)/400  # c in (0.0025, 0.5)
        v = Fep_analytic(cc,qq)
        if v > best: best = v; bestc = cc
    print('  q=%s: max Fep=%s at c=%s' % (q, mp.nstr(best,8), mp.nstr(bestc,5)))
