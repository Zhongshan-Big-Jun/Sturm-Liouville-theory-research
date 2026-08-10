# -*- coding: utf-8 -*-
# Find threshold q where F~_e' first becomes positive; analyze G2 region. EVIDENCE.
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
def G2(c,q): return Gval(alpha2(c,q),c,q)
def G1(c,q): return Gval(alpha1(c,q),c,q)

print('=== F~_e max over c for q in (0.05..0.6) ===')
for q0 in ['0.05','0.1','0.15','0.2','0.25','0.3','0.35','0.4','0.45','0.5','0.55','0.6']:
    qq = mp.mpf(q0)
    best = mp.mpf('-1e99'); bestc = None
    for k in range(1,500):
        cc = mp.mpf(k)/1000
        v = Fep(cc,qq)
        if v > best: best = v; bestc = cc
    print('  q=%s: max Fep=%s at c=%s  %s' % (q0, mp.nstr(best,8), mp.nstr(bestc,5), 'POSITIVE!' if best>0 else ''))

print('=== G2 sign region (c where G2=0) ===')
for q0 in ['0.05','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8165','0.9','1.0']:
    qq = mp.mpf(q0)
    # find G2 zero in (0,0.5)
    prev = None; zc = None
    for k in range(1,501):
        cc = mp.mpf(k)/1000
        g = G2(cc,qq)
        if prev is not None and prev*g < 0:
            zc = mp.findroot(lambda c: G2(c,qq), (mp.mpf(k-1)/1000, cc), solver='bisect')
            break
        prev = g
    print('  q=%s: G2 zero at c=%s' % (q0, mp.nstr(zc,6) if zc is not None else 'none in (0,0.5)'))

print('=== F~_e'' components at q=0.8165, c=0.45 (G2<0 region) ===')
qq = mp.mpf('0.8165')
for cc in ['0.42','0.44','0.46','0.48','0.5']:
    ccc = mp.mpf(cc)
    a1=alpha1(ccc,qq); a2=alpha2(ccc,qq)
    M1=Mf(a1,ccc,qq); M2=Mf(a2,ccc,qq)
    g1=G1(ccc,qq); g2=G2(ccc,qq)
    print('  c=%s: M1=%s M2=%s G1=%s G2=%s  M1G1=%s M2G2=%s  Fep=%s' % (cc,
        mp.nstr(M1,6),mp.nstr(M2,6),mp.nstr(g1,6),mp.nstr(g2,6),mp.nstr(M1*g1,6),mp.nstr(M2*g2,6),mp.nstr(M1*g1-M2*g2,6)))
