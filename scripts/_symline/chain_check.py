# -*- coding: utf-8 -*-
# Verify all pieces of the proof chain. EVIDENCE.
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
def Fep(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mf(a1,c,q)*Gval(a1,c,q) - Mf(a2,c,q)*Gval(a2,c,q)
def G2(c,q): return Gval(alpha2(c,q),c,q)

print('=== A) Fe(1/2) sign for q in [q0,1] ===')
for q0 in ['0.8165','0.85','0.9','0.95','0.99','1.0']:
    qq = mp.mpf(q0)
    print('  q=%s: Fe(1/2)=%s' % (q0, mp.nstr(Fe(mp.mpf('0.5'),qq),10)))

print('=== B) phi_c monotonicity for q<1 (d/dx log phi_c at sample points) ===')
for q0 in ['0.5','0.8165','0.9']:
    qq = mp.mpf(q0)
    for c0 in ['0.3','0.5','1.0','2.0']:
        cc = mp.mpf(c0)
        # d/dx log phi_c = 2/x + 2cot x - 2c(q^2-1) sin x cos x / (q + c Phi)
        for x0 in ['0.3','0.7','1.2','1.5']:
            xx = mp.mpf(x0)
            val = 2/xx + 2*mp.cot(xx) - 2*cc*(qq**2-1)*mp.sin(xx)*mp.cos(xx)/(qq + cc*Phi(xx,qq))
            if val <= 0:
                print('  q=%s c=%s x=%s: dlog=%s NEGATIVE!' % (q0,c0,x0,mp.nstr(val,6)))
    print('  (q=%s checked, only negatives printed)' % q0)

print('=== C) G2 zeros in (0,1/2) - count ===')
for q0 in ['0.5','0.7','0.8165','0.9','1.0']:
    qq = mp.mpf(q0)
    prev=None; zeros=[]
    for k in range(1,501):
        cc = mp.mpf(k)/1000
        g = G2(cc,qq)
        if prev is not None and prev*g<0:
            z = mp.findroot(lambda c: G2(c,qq), (mp.mpf(k-1)/1000, cc), solver='bisect')
            zeros.append(z)
        prev = g
    print('  q=%s: G2 zeros in (0,0.5): %s' % (q0, [mp.nstr(z,5) for z in zeros]))

print('=== D) ratio |G1|/|G2| vs M2/M1 in G2<0 region ===')
for q0 in ['0.8165','1.0']:
    qq = mp.mpf(q0)
    for c0 in ['0.43','0.45','0.47','0.49','0.5']:
        cc = mp.mpf(c0)
        a1=alpha1(cc,qq); a2=alpha2(cc,qq)
        M1=Mf(a1,cc,qq); M2=Mf(a2,cc,qq)
        g1=Gval(a1,cc,qq); g2=Gval(a2,cc,qq)
        if g2 < 0:
            print('  q=%s c=%s: |G1|/|G2|=%s  M2/M1=%s  margin=%s' % (q0,c0,
                mp.nstr(abs(g1)/abs(g2),7), mp.nstr(M2/M1,7), mp.nstr((abs(g1)/abs(g2))/(M2/M1),7)))
