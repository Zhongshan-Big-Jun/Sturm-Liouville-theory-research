# -*- coding: utf-8 -*-
# Thorough scan of dFep/dq over [q0,1] x (0,1/2). EVIDENCE.
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
print('=== dFep/dq over grid: min value ===')
q0 = mp.sqrt(mp.mpf(2)/3)
ql = [q0, mp.mpf('0.85'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('0.99'), mp.mpf('1.0')]
for q in ql:
    mn = mp.mpf('1e99'); mn_at = None
    for k in range(1, 250):
        c = mp.mpf(k)/500  # 0.002..0.498
        dq = (Fep(c,q+h)-Fep(c,q-h))/(2*h)
        if dq < mn: mn = dq; mn_at = c
    print('  q=%s: min dFep/dq = %s at c=%s' % (mp.nstr(q,5), mp.nstr(mn,8), mp.nstr(mn_at,5)))

print('=== dFep/dq near c->0 and c->1/2 ===')
for q in ql[:3]:
    for c0 in ['1e-3','5e-3','0.01','0.49','0.499']:
        c = mp.mpf(c0)
        dq = (Fep(c,q+h)-Fep(c,q-h))/(2*h)
        print('  q=%s c=%s: %s' % (mp.nstr(q,5), c0, mp.nstr(dq,8)))
