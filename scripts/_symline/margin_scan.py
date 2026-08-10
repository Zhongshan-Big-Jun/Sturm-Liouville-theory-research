# -*- coding: utf-8 -*-
# Margins for candidate splits. EVIDENCE.
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

q0 = mp.sqrt(mp.mpf(2)/3)
h = mp.mpf('1e-4')

print('=== (B) G2 on (0,0.42]x[q0,1]: min (tight at corner?) ===')
mn = mp.mpf('1e99'); mn_at=None
for qs in [q0, mp.mpf('0.9'), mp.mpf('1.0')]:
    for k in range(1, 211):
        c = mp.mpf(k)*mp.mpf('0.002')  # up to 0.42
        g = G2(c,qs)
        if g < mn: mn = g; mn_at=(c,qs)
print('  min G2 =', mp.nstr(mn,8), 'at (c,q)=', mp.nstr(mn_at[0],5), mp.nstr(mn_at[1],5))
# G2 at the corner (0.42, q0)
print('  G2(0.42,q0) =', mp.nstr(G2(mp.mpf('0.42'),q0),8))
print('  G2(0.40,q0) =', mp.nstr(G2(mp.mpf('0.40'),q0),8))
print('  G2(0.38,q0) =', mp.nstr(G2(mp.mpf('0.38'),q0),8))

print('=== (E1) Fepp < 0 on (0,0.12]x[q0,1]? ===')
for c0 in ['0.02','0.04','0.06','0.08','0.10','0.12']:
    cc = mp.mpf(c0)
    fp2 = (Fep(cc+h,q0)-Fep(cc-h,q0))/(2*h)
    print('  q=q0 c=%s: Fepp=%s' % (c0, mp.nstr(fp2,8)))
print('  Fepp(q0, 0) limit: compute at c=1e-4:', mp.nstr((Fep(mp.mpf('1e-4')+h,q0)-Fep(mp.mpf('1e-4')-h,q0))/(2*h),8))

print('=== (E2) J1/J2 on [0.12,0.5]x[q0,1] ===')
# quick J2_curve
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
mnJ1 = mp.mpf('1e99'); mxJ2 = mp.mpf('-1e99')
for qs in [q0, mp.mpf('1.0')]:
    for k in range(0, 77):
        cc = mp.mpf('0.12') + mp.mpf(k)*mp.mpf('0.005')
        J1 = J2_curve(cc,qs,1); J2 = J2_curve(cc,qs,2)
        mnJ1 = min(mnJ1,J1); mxJ2 = max(mxJ2,J2)
print('  [0.12,0.5]: min J1 =', mp.nstr(mnJ1,8), ' max J2 =', mp.nstr(mxJ2,8))
