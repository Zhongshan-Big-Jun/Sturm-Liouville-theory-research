# -*- coding: utf-8 -*-
# Verify J1/J2 decomposition (O3a) for q<1 and compute their signs on well box. EVIDENCE.
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

# J^{(2)} along true curve: J = G^2 + G_c - u G_x, u = x Phi/(q+c Phi)
def J2_curve(c, q, which):
    # which=1: x=alpha1; which=2: x=alpha2
    x = alpha1(c,q) if which==1 else alpha2(c,q)
    Ph = Phi(x,q); D = q + c*Ph; u = x*Ph/D
    # G_c = partial c of G, G_x = partial x of G (holding q,c fixed)
    # G = -Ph*W/D + 2c x Ph (q^2-1) sinx cosx / D^2, W = 3+2x cotx
    W = 3+2*x*mp.cot(x)
    # partials of Ph: Ph_c = 0, Ph_x = 2(q^2-1) sinx cosx
    Phx = 2*(q**2-1)*mp.sin(x)*mp.cos(x)
    Dx = c*Phx
    # W_x = 2 cotx - 2x csc^2 x
    Wx = 2*mp.cot(x) - 2*x/mp.sin(x)**2
    # G_x = -[Phx*W + Ph*Wx]/D + Ph*W*Dx/D^2 + 2c(q^2-1)[(x Ph sinxcosx)_x D^2 - x Ph sinxcosx * 2D Dx]/D^4
    # let S = x*Ph*sinx*cosx; S_x = Ph*sinxcosx + x*Phx*sinxcosx + x*Ph*(cos^2x - sin^2x)
    S = x*Ph*mp.sin(x)*mp.cos(x)
    Sx = Ph*mp.sin(x)*mp.cos(x) + x*Phx*mp.sin(x)*mp.cos(x) + x*Ph*(mp.cos(x)**2-mp.sin(x)**2)
    Gx = -(Phx*W + Ph*Wx)/D + Ph*W*Dx/D**2 + 2*c*(q**2-1)*(Sx*D**2 - S*2*D*Dx)/D**4
    # G_c = Ph*W*Dc/D^2 + 2 x Ph (q^2-1) sinxcosx * (D^2 - c*2D*Dc)/D^4, Dc = Ph
    Dc = Ph
    Gc = Ph*W*Dc/D**2 + 2*x*Ph*(q**2-1)*mp.sin(x)*mp.cos(x)*(D**2 - c*2*D*Dc)/D**4
    return Gval(x,c,q)**2 + Gc - u*Gx

def Fep(c,q):
    a1=alpha1(c,q); a2=alpha2(c,q)
    return Mf(a1,c,q)*Gval(a1,c,q) - Mf(a2,c,q)*Gval(a2,c,q)

# verify: Fepp (numeric) == M1*J1 - M2*J2
h = mp.mpf('1e-5')
q0 = mp.sqrt(mp.mpf(2)/3)
print('=== Fepp vs M1*J1 - M2*J2 (q<1) ===')
for q0s in ['0.8165','0.9','1.0']:
    qq = mp.mpf(q0s)
    for c0 in ['0.43','0.46','0.49']:
        cc = mp.mpf(c0)
        Fepp_num = (Fep(cc+h,qq)-Fep(cc-h,qq))/(2*h)
        a1=alpha1(cc,qq); a2=alpha2(cc,qq)
        J1 = J2_curve(cc,qq,1); J2 = J2_curve(cc,qq,2)
        M1 = Mf(a1,cc,qq); M2 = Mf(a2,cc,qq)
        dec = M1*J1 - M2*J2
        print('  q=%s c=%s: Fepp_num=%s  M1J1-M2J2=%s  J1=%s J2=%s' % (q0s,c0,mp.nstr(Fepp_num,8),mp.nstr(dec,8),mp.nstr(J1,8),mp.nstr(J2,8)))

print('=== J1, J2 on well box [q0,1] x [0.42,0.5] ===')
for q0s in ['0.8165','0.85','0.9','0.95','1.0']:
    qq = mp.mpf(q0s)
    mnJ1 = mp.mpf('1e99'); mxJ2 = mp.mpf('-1e99')
    for k in range(0, 17):
        cc = mp.mpf('0.42') + mp.mpf(k)*mp.mpf('0.005')
        J1 = J2_curve(cc,qq,1); J2 = J2_curve(cc,qq,2)
        mnJ1 = min(mnJ1, J1); mxJ2 = max(mxJ2, J2)
    print('  q=%s: min J1=%s  max J2=%s' % (q0s, mp.nstr(mnJ1,8), mp.nstr(mxJ2,8)))
