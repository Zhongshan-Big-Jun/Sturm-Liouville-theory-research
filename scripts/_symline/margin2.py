# -*- coding: utf-8 -*-
# Margins for 3-region split: Fepp<0 on (0,c1), J1/J2 on [c1,0.5]. EVIDENCE.
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

q0 = mp.sqrt(mp.mpf(2)/3)
h = mp.mpf('1e-4')

print('=== Fepp on (0,0.09] - margin at c1 (max Fepp over q) ===')
for c0 in ['0.02','0.04','0.06','0.07','0.08','0.085','0.09']:
    cc = mp.mpf(c0)
    mx = mp.mpf('-1e99')
    for qs in [q0, mp.mpf('0.9'), mp.mpf('1.0')]:
        fp2 = (Fep(cc+h,qs)-Fep(cc-h,qs))/(2*h)
        mx = max(mx, fp2)
    print('  c=%s: max Fepp over q in [q0,1] = %s %s' % (c0, mp.nstr(mx,8), 'POSITIVE!' if mx>0 else ''))

print('=== J1/J2 on [0.09,0.5]x[q0,1] ===')
mnJ1 = mp.mpf('1e99'); mxJ2 = mp.mpf('-1e99')
mnJ1_at=None; mxJ2_at=None
for qs in [q0, mp.mpf('0.85'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('1.0')]:
    for k in range(0, 83):
        cc = mp.mpf('0.09') + mp.mpf(k)*mp.mpf('0.005')
        J1 = J2_curve(cc,qs,1); J2 = J2_curve(cc,qs,2)
        if J1 < mnJ1: mnJ1=J1; mnJ1_at=(cc,qs)
        if J2 > mxJ2: mxJ2=J2; mxJ2_at=(cc,qs)
print('  min J1 =', mp.nstr(mnJ1,8), 'at', mp.nstr(mnJ1_at[0],4), mp.nstr(mnJ1_at[1],4))
print('  max J2 =', mp.nstr(mxJ2,8), 'at', mp.nstr(mxJ2_at[0],4), mp.nstr(mxJ2_at[1],4))

print('=== Fepp limit near 0 (q=q0): c=1e-6..1e-3 ===')
for e in ['1e-6','1e-5','1e-4','1e-3','5e-3']:
    cc = mp.mpf(e)
    fp2 = (Fep(cc+h,q0)-Fep(cc-h,q0))/(2*h)
    print('  c=%s: Fepp=%s' % (e, mp.nstr(fp2,10)))
