# -*- coding: utf-8 -*-
"""Careful check of lambda1 FH."""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    return (np.sin(w1*t)/q1)*np.cos(w2*(1-t)) + np.cos(w1*t)*np.sin(w2*(1-t))/q2

def lam_k(t, k):
    # k=1,2 eigenvalue with high-precision bisection
    smax = 30.0
    s = np.linspace(1e-9, smax, 300000)
    M = M01_2block(t, 1.0, 4.0, s)
    sg = np.signbit(M)
    ch = sg[1:] != sg[:-1]
    idx = np.nonzero(ch)[0]
    lo, hi = s[idx[k-1]], s[idx[k-1]+1]
    return brentq(lambda x: M01_2block(t, 1.0, 4.0, x), lo, hi)**2

t = 0.4; h = 1e-6
lam1 = lam_k(t, 1)
dlam1 = (lam_k(t+h,1) - lam_k(t-h,1))/(2*h)

# eigenfunction: y on [0,t]: sin(sx)/q1; on (t,1]: matching
s1 = np.sqrt(lam1)
q1, q2 = 1.0, 2.0
w1 = s1*q1
def y(x):
    if x <= t:
        return np.sin(w1*x)/q1
    yt = np.sin(w1*t)/q1; ypt = np.cos(w1*t)
    w2 = s1*q2
    return yt*np.cos(w2*(x-t)) + (ypt/w2)*np.sin(w2*(x-t))
def rho(x):
    return 1.0 if x <= t else 4.0
nrm, _ = quad(lambda x: rho(x)*y(x)**2, 0, 1, points=[t], limit=200)
u_t = y(t)/np.sqrt(nrm)
print(f"lam1 = {lam1:.10f}, dlam1/dt = {dlam1:.10f}")
print(f"(R-1)*lam1*u1(t)^2 = {3*lam1*u_t**2:.10f}")
print(f"u1(t)^2 = {u_t**2:.10f}")
# also verify u1(0), u1(1)
print("y(1) =", y(1.0), "(should be 0)")
