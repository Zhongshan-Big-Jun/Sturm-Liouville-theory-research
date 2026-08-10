# -*- coding: utf-8 -*-
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

q0 = mp.sqrt(mp.mpf(2)/3)
print('=== Fep(c) at q=q0 ===')
for c0 in ['0.02','0.05','0.08','0.087','0.09','0.1','0.12','0.15','0.2','0.25','0.3','0.35','0.4','0.42','0.45','0.5']:
    print('  c=%s: Fep=%s' % (c0, mp.nstr(Fep(mp.mpf(c0),q0),8)))

# E1/E2 on the 2D box (not just the curve): E1 = G^2+G_c-u G_x evaluated freely on box
def E1_box(x,c,q):
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

print('=== E1 min over 2D box x in [pi/3,1.17], c in [0.40,0.5], q in [q0,1] ===')
mn = mp.mpf('1e99'); mx = mp.mpf('-1e99')
for xk in range(0, 27):
    x = mp.mpf(pi)/3 + mp.mpf(xk)*mp.mpf('0.005')
    for ck in range(0, 21):
        c = mp.mpf('0.40') + mp.mpf(ck)*mp.mpf('0.005')
        for qk in [0,1,2,3,4]:
            q = q0 + mp.mpf(qk)*mp.mpf('0.045875')
            v = E1_box(x,c,q)
            mn = min(mn,v); mx = max(mx,v)
print('  E1 on 2D box: min=%s max=%s' % (mp.nstr(mn,6), mp.nstr(mx,6)))

# E2 on 2D box for gamma: x2 = pi - gamma
def E2_box(g,c,q):
    x = pi - g
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
print('=== E2 min over 2D box g in [0.99,1.11], c in [0.40,0.5], q in [q0,1] ===')
mn = mp.mpf('1e99'); mx = mp.mpf('-1e99')
for gk in range(0, 25):
    g = mp.mpf('0.99') + mp.mpf(gk)*mp.mpf('0.005')
    for ck in range(0, 21):
        c = mp.mpf('0.40') + mp.mpf(ck)*mp.mpf('0.005')
        for qk in [0,1,2,3,4]:
            q = q0 + mp.mpf(qk)*mp.mpf('0.045875')
            v = E2_box(g,c,q)
            mn = min(mn,v); mx = max(mx,v)
print('  E2 on 2D box: min=%s max=%s' % (mp.nstr(mn,6), mp.nstr(mx,6)))
