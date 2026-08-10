# -*- coding: utf-8 -*-
"""01_reproduce_claims.py
Reproduce the packet numerics at high precision (mpmath, 50 dps).
Inputs: none. Expected output: u*, mu1, mu2, Dbar at the claimed values
(24.94386613843234 etc). ASCII punctuation. Run: python 01_reproduce_claims.py
"""
import mpmath as mp
mp.mp.dps = 50

def a_of(u):
    # unique root of tan a = a(1 - 1/(2u)) on (pi/2, pi)
    f = lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    return mp.findroot(f, (mp.pi/2 + mp.mpf('0.7'), mp.pi - mp.mpf('0.7')))

def S(u):
    a = a_of(u)
    mu1 = mp.pi**2/(4*u**2)
    mu2 = (a/u)**2
    I2 = u/2 - mp.sin(2*a)*u/(4*a)
    return mu1*2/u - mu2*mp.sin(a)**2/I2

u_star = mp.findroot(S, mp.mpf('0.3299225'))
a_star = a_of(u_star)
mu1 = mp.pi**2/(4*u_star**2)
mu2 = (a_star/u_star)**2
Dbar = mu2 - mu1
print("u*    =", mp.nstr(u_star, 25))
print("a*    =", mp.nstr(a_star, 25))
print("mu1*  =", mp.nstr(mu1, 25))
print("mu2*  =", mp.nstr(mu2, 25))
print("Dbar* =", mp.nstr(Dbar, 25))
print("3pi^2 =", mp.nstr(3*mp.pi**2, 25))
print("ratio =", mp.nstr(Dbar/(3*mp.pi**2), 25))
print("claimed: u=0.32992251, mu1=22.668139, mu2=47.612005, D*R=24.943866")
assert abs(Dbar - mp.mpf('24.94386613843234')) < mp.mpf('1e-9')
assert abs(u_star - mp.mpf('0.3299225081196866')) < mp.mpf('1e-10')
print("PASS")
