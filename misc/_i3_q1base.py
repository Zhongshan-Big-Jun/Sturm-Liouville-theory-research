# -*- coding: utf-8 -*-
"""q=1 baseline: J1(1,c), J2(1,c) as 1D functions of c on [0.4,0.5]."""
import mpmath as mp
mp.mp.dps = 40

# alpha1 = pi/(2(1+c)), alpha2 = pi/(1+c)
# J1 = [W^2 + W + (pi/2)W']/(1+c)^2 at x=pi/(2(1+c))
# J2 = [W^2 + W + pi*W']/(1+c)^2 at x=pi/(1+c)   (check: Gx*xp + Gc with xp = -x/(1+c))
def W(x): return 3 + 2*x/mp.tan(x)
def Wp(x): return 2/mp.tan(x) - 2*x/mp.sin(x)**2

def J1_1(c):
    x = mp.pi/(2*(1+c))
    return (W(x)**2 + W(x) + (mp.pi/2)*Wp(x))/(1+c)**2
def J2_1(c):
    x = mp.pi/(1+c)
    return (W(x)**2 + W(x) + mp.pi*Wp(x))/(1+c)**2

mn1=mp.inf; mx1=-mp.inf; mn2=mp.inf; mx2=-mp.inf
for i in range(2001):
    c = mp.mpf('0.4')+mp.mpf('0.1')*i/2000
    j1 = J1_1(c); j2 = J2_1(c)
    mn1=min(mn1,j1); mx1=max(mx1,j1); mn2=min(mn2,j2); mx2=max(mx2,j2)
print("J1(1,c) on [0.4,0.5]: [%.6f, %.6f]" % (mn1,mx1))
print("J2(1,c) on [0.4,0.5]: [%.6f, %.6f]" % (mn2,mx2))

# verify against full curve computation at a few points
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W_ = 3 + 2*x/mp.tan(x)
    return -Ph*W_/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W_ = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W_*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
for c in [mp.mpf('0.4'),mp.mpf('0.45'),mp.mpf('0.5')]:
    a1 = mp.pi/(2*(1+c)); a2 = mp.pi/(1+c)
    print("c=%.2f: J1(1,c) direct %.6f vs curve %.6f | J2(1,c) direct %.6f vs curve %.6f" % (
        c, J1_1(c), J(a1,c,1), J2_1(c), J(a2,c,1)))
