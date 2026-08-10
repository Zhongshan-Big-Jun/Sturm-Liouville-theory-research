# -*- coding: utf-8 -*-
# sym_endpoint_fixed.py — CORRECTED closed form of Fep(q,1/2) and T(x) analysis.
# Fix: sym_endpoint.py had G2 second term with an extra factor t (buggy for q<1).
# Correct identity: Fep(q,1/2) = -2*pi*(1-cos x)^3 * T(x) / sin(x)^3,
#   x = arccos(q/(q+1)) in (pi/3, pi/2), T(x) = pi^2 - 3x(pi-x) - 3(pi-2x) sin x.
# Verified to 1e-29 for q in (0,1] (mpmath 50 digits).
import mpmath as mp
mp.mp.dps = 50
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
def T(x): return pi**2 - 3*x*(pi-x) - 3*(pi-2*x)*mp.sin(x)
def closed(q):
    x = mp.acos(q/(q+1))
    return -2*pi*(1-mp.cos(x))**3*T(x)/mp.sin(x)**3

print('=== CORRECTED closed form check: Fep(q,1/2) vs -2pi(1-cosx)^3 T(x)/sin^3 x ===')
for q0s in ['0.1','0.3','0.5','0.7','0.8165','0.9','0.99','1.0']:
    q = mp.mpf(q0s)
    err = abs(Fep(mp.mpf('0.5'),q)-closed(q))
    print('  q=%s: err=%s' % (q0s, mp.nstr(err,3)))
print('=== T(x) positivity on (pi/3, pi/2) ===')
print('  T(pi/3)=%s, T\'(pi/3)=%s, T\'\'(x)=6+12cosx+3(pi-2x)sinx>0, e.g. T\'\'(pi/3)=%s' % (
    mp.nstr(T(pi/3),10), mp.nstr(3*mp.sqrt(3)-3*pi/2,10), mp.nstr(6+12*mp.cos(pi/3)+3*(pi/3)*mp.sin(pi/3),10)))
print('  min T on [pi/3, pi/2] = %s (at pi/3) => Fep(q,1/2) < 0 for all q in (0,1]' % mp.nstr(T(pi/3),10))
