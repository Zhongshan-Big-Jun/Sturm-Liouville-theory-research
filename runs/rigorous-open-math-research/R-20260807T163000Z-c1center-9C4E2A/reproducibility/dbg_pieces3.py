# -*- coding: utf-8 -*-
"""debug pieces v3."""
import sympy as sp
import numpy as np
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
a0 = float(np.arccos(0.25)/np.pi)
s1 = sp.sqrt(15)/4; c1 = sp.Rational(1,4)
A0 = sp.Float(a0, 35)

def H(xx, k): return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)
def F(xx, k, c): return sp.Rational(1,2)*(xx*sp.cos(2*k*pi*c) - sp.sin(2*k*pi*xx-2*k*pi*c)/(2*k*pi))
def G(xx, k): return sp.sin(k*pi*xx)**2/(2*k*pi)
def M(xx, k): return sp.Rational(1,2)*(-xx*sp.cos(2*k*pi*xx)/(2*k*pi) + sp.sin(2*k*pi*xx)/(4*k**2*pi**2) + alpha*sp.cos(2*k*pi*xx)/(2*k*pi))

def subnum(e, bval):
    B = sp.Float(bval, 35)
    e = e.subs(b, B)
    e = sp.expand_trig(e)
    e = e.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
    e = sp.expand(e)
    e = e.subs(alpha, A0)
    return float(sp.N(e, 30))

def closed_pieces(k, bv):
    B = sp.Float(bv, 35)
    lp = -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))
    Pk = sp.sin(k*pi*alpha)/(2*k*pi) - alpha*sp.cos(k*pi*alpha)/2
    y1a = -(1/(k*pi))*(lp/(k*pi))*Pk
    ant1 = (1/(4*k*pi))*(F(x,k,alpha) + H(x,k)) - sp.Rational(1,2)*M(x,k)
    p1 = sp.expand(ant1.subs(x, B) - ant1.subs(x, alpha))
    ant2 = (1/(4*k*pi))*(F(x,k,alpha) - F(x,k,b)) - sp.Rational(1,2)*(b-alpha)*G(x,k)
    p2 = sp.expand(ant2.subs(x, 1) - ant2.subs(x, B))
    Qint = sp.expand(p1 + p2)
    Pint = sp.Rational(3,8)/(k*pi)
    termA = -(2/(k**2*pi**2))*((lp/(k*pi))*Pint + (k*pi)*Qint)
    termB = (1/(k**2*pi**2))*(H(B,k) - H(alpha,k))
    nk1 = sp.expand(termA + termB)
    nk0 = sp.Rational(1,2)/(k*pi)**2
    sk = sp.sin(k*pi*alpha)
    w1a = y1a*sp.sqrt(nk0) - sp.sqrt(2)*sk*nk1/(2*nk0)
    uk0 = sp.sqrt(2)*sk
    R1k = sp.expand(lp*uk0**2 + 2*(k*pi)**2*uk0*w1a)
    return dict(lp=lp, y1a=y1a, Qint=Qint, nk1=nk1, w1a=w1a, R1k=R1k)

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
    w1a = y1a/np.sqrt(nk0) - np.sqrt(2)*np.sin(k*np.pi*a)*nk1/(2*nk0)
    R1k = lp*(np.sqrt(2)*np.sin(k*np.pi*a))**2 + 2*(k*np.pi)**2*np.sqrt(2)*np.sin(k*np.pi*a)*w1a
    return dict(lp=lp, y1a=y1a, nk1=nk1, w1a=w1a, R1k=R1k)

for bval in (0.45, 0.6, 0.77, 0.95):
    print("=== b =", bval, "===")
    for k in (1,2):
        num = num_quantities(k, a0, bval)
        sym = closed_pieces(k, bval)
        print(" k=%d" % k)
        for key in ("lp","y1a","nk1","w1a","R1k"):
            sv = subnum(sym[key], bval)
            print("   %-5s num=% .12e  sym=% .12e  diff=% .3e" % (key, num[key], sv, sv-num[key]))
