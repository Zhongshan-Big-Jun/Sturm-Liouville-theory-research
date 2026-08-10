# -*- coding: utf-8 -*-
import math
from scipy.optimize import brentq
import numpy as np

def even_root(u, q):
    v = 0.5 - u
    f = lambda s: np.cos(s*u)*np.cos(s*q*v) - q*np.sin(s*u)*np.sin(s*q*v)
    xs = np.linspace(1e-9, math.pi, 20000)
    vals = f(xs)
    sg = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(sg)[0]
    return brentq(f, xs[idx[0]], xs[idx[0]+1])

def odd_root(u, q):
    v = 0.5 - u
    f = lambda s: q*np.sin(s*u)*np.cos(s*q*v) + np.cos(s*u)*np.sin(s*q*v)
    xs = np.linspace(1e-9, 2*math.pi, 30000)
    vals = f(xs)
    sg = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(sg)[0]
    return brentq(f, xs[idx[0]], xs[idx[0]+1])

q = 2.0  # R=4
u = 0.1
s1 = even_root(u, q); s2 = odd_root(u, q)
print("u=0.1: s1=%.10f lam1=%.8f | s2=%.10f lam2=%.8f" % (s1, s1**2, s2, s2**2))
for h in [1e-4, 1e-5, 1e-6]:
    u2 = u+h
    s1b = even_root(u2, q); s2b = odd_root(u2, q)
    print("h=%.0e: dlam1/du=%.6f  dlam2/du=%.6f  dD/du=%.6f" % (h, (s1b**2-s1**2)/h, (s2b**2-s2**2)/h, (s2b**2-s1b**2-s2**2+s1**2)/h))