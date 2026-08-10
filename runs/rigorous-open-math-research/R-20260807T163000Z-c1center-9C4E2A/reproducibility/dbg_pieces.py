# -*- coding: utf-8 -*-
"""debug: compare closed-form pieces vs direct numeric integration at b=0.6, k=1,2."""
import sympy as sp
import numpy as np
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
a0 = float(np.arccos(0.25)/np.pi)
s1 = sp.sqrt(15)/4; c1 = sp.Rational(1,4)

def lam_prime(k):
    return -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))

# numeric reference (direct Simpson integration) of y_k^1(a0), n_k^1, Qint
def num_quantities(k, a, bb, N=200001):
    t = np.linspace(0,1,N); h = t[1]-t[0]
    lp = float(-k**2*np.pi**2*((bb-a) - (np.sin(2*k*np.pi*bb)-np.sin(2*k*np.pi*a))/(2*k*np.pi)))
    g = (lp + k**2*np.pi**2*((t>=a)&(t<=bb)))*np.sin(k*np.pi*t)/(k*np.pi)
    C = np.cumsum(np.cos(k*np.pi*t)*g)*h - 0.5*h*np.cos(k*np.pi*t)*g
    S = np.cumsum(np.sin(k*np.pi*t)*g)*h - 0.5*h*np.sin(k*np.pi*t)*g
    y1 = -(np.sin(k*np.pi*t)*C - np.cos(k*np.pi*t)*S)/(k*np.pi)
    yk0 = np.sin(k*np.pi*t)/(k*np.pi)
    ia = np.searchsorted(t, a)
    y1a = y1[ia]
    nk1 = 2*np.trapezoid(yk0*y1, t) + np.trapezoid(((t>=a)&(t<=bb))*yk0**2, t)
    nk0 = 1.0/(2*k**2*np.pi**2)
    w1 = y1a/np.sqrt(nk0) - np.sqrt(2)*np.sin(k*np.pi*a)*nk1/(2*nk0)
    lp2 = float(lp)
    R1k = lp2*(np.sqrt(2)*np.sin(k*np.pi*a))**2 + 2*(k*np.pi)**2*np.sqrt(2)*np.sin(k*np.pi*a)*w1
    return dict(lp=lp2, y1a=y1a, nk1=nk1, w1a=w1, R1k=R1k)

# symbolic pieces for given b value
def sym_pieces(k, bval):
    lp = lam_prime(k)
    Pk = sp.sin(k*pi*alpha)/(2*k*pi) - alpha*sp.cos(k*pi*alpha)/2
    y1a = -(1/(k*pi))*(lp/(k*pi))*Pk
    # Qint via direct symbolic integrate at fixed bval (numeric limits -> fast)
    bv = sp.Float(bval, 30)
    term2b = sp.Rational(1,4)*(sp.sin(k*pi*(x-2*alpha)) + sp.sin(k*pi*x)) - (k*pi/2)*(x-alpha)*sp.cos(k*pi*x)
    term2c = sp.Rational(1,4)*(sp.sin(k*pi*(x-2*alpha)) - sp.sin(k*pi*(x-2*bv))) - (k*pi/2)*(bv-alpha)*sp.cos(k*pi*x)
    J2b = sp.integrate(sp.sin(k*pi*x)*term2b, (x, alpha, bv))
    J2c = sp.integrate(sp.sin(k*pi*x)*term2c, (x, bv, 1))
    Qint = sp.expand(J2b + J2c)
    Pint = sp.Rational(3,8)/(k*pi)
    termA = -(2/(k**2*pi**2))*((lp/(k*pi))*Pint + (k*pi)*Qint)
    termB = (1/(k**2*pi**2))*(H(bv,k) - H(alpha,k))
    nk1 = sp.expand(termA + termB)
    nk0 = sp.Rational(1,2)/(k*pi)**2
    sk = sp.sin(k*pi*alpha)
    w1a = y1a*sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    R1k = sp.expand(lp*(sp.sqrt(2)*sk)**2 + 2*(k*pi)**2*sp.sqrt(2)*sk*w1a)
    # substitute alpha -> a0
    subs = {sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1, alpha: sp.Float(a0,30)}
    for e in (y1a, nk1, w1a, R1k, Qint):
        pass
    def ev(e):
        e2 = sp.expand_trig(e)
        e2 = e2.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
        e2 = sp.expand(e2).subs(alpha, sp.Float(a0,30))
        return float(sp.N(e2, 25))
    return dict(lp=ev(lp), y1a=ev(y1a), nk1=ev(nk1), w1a=ev(w1a), R1k=ev(R1k))

def H(xx, k):
    return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)

for k in (1,2):
    num = num_quantities(k, a0, 0.6)
    sym = sym_pieces(k, 0.6)
    print("k=%d at b=0.6:" % k)
    for key in ("lp","y1a","nk1","w1a","R1k"):
        print("  %-5s num=% .12e  sym=% .12e  diff=% .3e" % (key, num[key], sym[key], sym[key]-num[key]))
