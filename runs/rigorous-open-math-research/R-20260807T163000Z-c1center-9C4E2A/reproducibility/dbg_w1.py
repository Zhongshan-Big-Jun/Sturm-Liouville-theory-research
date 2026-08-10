import sympy as sp
import numpy as np
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
a0 = float(np.arccos(0.25)/np.pi)
s1 = sp.sqrt(15)/4; c1 = sp.Rational(1,4)
A0 = sp.Float(a0, 35)
k=1; bval=0.6
B = sp.Float(bval, 35)
def H(xx, k): return xx/2 - sp.sin(2*k*pi*xx)/(4*k*pi)
def F(xx, k, c): return sp.Rational(1,2)*(xx*sp.cos(2*k*pi*c) - sp.sin(2*k*pi*xx-2*k*pi*c)/(2*k*pi))
def G(xx, k): return sp.sin(k*pi*xx)**2/(2*k*pi)
def M(xx, k): return sp.Rational(1,2)*(-xx*sp.cos(2*k*pi*xx)/(2*k*pi) + sp.sin(2*k*pi*xx)/(4*k**2*pi**2) + alpha*sp.cos(2*k*pi*xx)/(2*k*pi))
def subnum(e):
    e = e.subs(b, B)
    e = sp.expand_trig(e)
    e = e.subs({sp.sin(pi*alpha): s1, sp.cos(pi*alpha): c1})
    e = sp.expand(e).subs(alpha, A0)
    return sp.N(e, 30)
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
print("sqrt(nk0) =", sp.sqrt(nk0))
print("y1a*sqrt(nk0) =", subnum(y1a*sp.sqrt(nk0)))
print("sqrt(2)*sk*nk1/(2 nk0) =", subnum(sp.sqrt(2)*sk*nk1/(2*nk0)))
print("w1a =", subnum(w1a))
# reference numbers
t = np.linspace(0,1,200001); h=t[1]-t[0]
lpv = float(subnum(lp))
g = (lpv + k**2*np.pi**2*((t>=a0)&(t<=bval)))*np.sin(k*np.pi*t)/(k*np.pi)
C = np.cumsum(np.cos(k*np.pi*t)*g)*h - 0.5*h*np.cos(k*np.pi*t)*g
S = np.cumsum(np.sin(k*np.pi*t)*g)*h - 0.5*h*np.sin(k*np.pi*t)*g
y1 = -(np.sin(k*np.pi*t)*C - np.cos(k*np.pi*t)*S)/(k*np.pi)
ia = np.searchsorted(t, a0)
y1a_num = y1[ia]
print("ref y1a =", y1a_num)
print("ref y1a/sqrt(nk0) =", y1a_num/np.sqrt(float(subnum(nk0))))
# compute reference nk1 via trapezoid
yk0 = np.sin(k*np.pi*t)/(k*np.pi)
nk1_num = 2*np.trapezoid(yk0*y1, t) + np.trapezoid(((t>=a0)&(t<=bval))*yk0**2, t)
print("ref nk1 =", nk1_num)
print("ref sqrt(2) sin nk1/(2nk0) =", np.sqrt(2)*np.sin(k*np.pi*a0)*nk1_num/(2*float(subnum(nk0))))
print("ref w1a =", y1a_num/np.sqrt(float(subnum(nk0))) - np.sqrt(2)*np.sin(k*np.pi*a0)*nk1_num/(2*float(subnum(nk0))))
