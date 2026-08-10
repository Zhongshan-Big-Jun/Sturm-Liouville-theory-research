# -*- coding: utf-8 -*-
# Symbolic: Fep(q,1/2) closed form; numeric verification. EVIDENCE.
import mpmath as mp
import sympy as sp
mp.mp.dps = 40
pi = mp.pi

# ---- numeric Fep(q,1/2) via G-decomposition ----
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

# ---- closed form at c=1/2 ----
def Fep_half_closed(q):
    t = mp.acos(q/(q+1))
    Ph = mp.mpf(2)*q**2/(q+1)
    D = q + Ph/2
    M1 = t**2/(q*(q+1)); M2 = (pi-t)**2/(q*(q+1))
    G1 = -Ph*(3+2*t*mp.cot(t))/D + t*Ph*(q**2-1)*mp.sin(t)*mp.cos(t)/D**2
    G2 = -Ph*(3-2*(pi-t)*mp.cot(t))/D - t*(pi-t)*Ph*(q**2-1)*mp.sin(t)*mp.cos(t)/D**2
    return M1*G1 - M2*G2

print('=== Fep(q,1/2): closed vs numeric ===')
for q0 in ['0.1','0.3','0.5','0.7','0.8165','0.9','1.0','2.0','5.0']:
    qq = mp.mpf(q0)
    print('  q=%s: closed=%s numeric=%s' % (q0, mp.nstr(Fep_half_closed(qq),10), mp.nstr(Fep(mp.mpf('0.5'),qq),10)))

# ---- sign over q>0 ----
print('=== Fep(q,1/2) sign for q in (0, 100] ===')
mn = mp.mpf('1e99'); mnq=None
for k in range(1, 200):
    qq = mp.mpf(k)*mp.mpf('0.5')
    v = Fep_half_closed(qq)
    if v < mn: mn = v; mnq = qq
print('  min over q in (0.5,100): %s at q=%s' % (mp.nstr(mn,8), mp.nstr(mnq,4)))
# near 0
for q0 in ['0.01','0.02','0.05','0.1','0.2','0.3']:
    print('  q=%s: %s' % (q0, mp.nstr(Fep_half_closed(mp.mpf(q0)),10)))
