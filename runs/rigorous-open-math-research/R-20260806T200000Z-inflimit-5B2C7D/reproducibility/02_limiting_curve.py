# -*- coding: utf-8 -*-
"""02_limiting_curve.py
Numerical verification of the Part I sign structure on a in (pi/2, pi):
  K~(a) = 3 sin^2 a + 3a sin a cos a - a^2        (sign of J')
  J(a)  = 6 a^2 + 4 a^3 cot a - pi^2              (sign of G')
  G(a)  = 8 a^3 sin^2 a - pi^2 (2a - sin 2a)      (sign of Dbar')
with u(a) = a/(2(a - tan a)).  Each function must have exactly one zero with
the sign pattern + then -.  Also verifies u'(a) > 0 and the endpoint limits
Dbar(0+) = +inf, Dbar(1/2-) = 3 pi^2.
ASCII punctuation. Run: python 02_limiting_curve.py
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 30

N = 200000
a = np.linspace(np.pi/2 + 1e-9, np.pi - 1e-9, N)

K = 3*np.sin(a)**2 + 3*a*np.sin(a)*np.cos(a) - a**2
J = 6*a**2 + 4*a**3/np.tan(a) - np.pi**2
G = 8*a**3*np.sin(a)**2 - np.pi**2*(2*a - np.sin(2*a))

def sign_changes(v):
    s = np.signbit(v)
    return int(np.sum(s[1:] != s[:-1]))

print("K~ sign changes (expect 1):", sign_changes(K))
print("J  sign changes (expect 1):", sign_changes(J))
print("G  sign changes (expect 1):", sign_changes(G))
print("K~ > 0 before its zero, < 0 after:",
      K[0] > 0, K[-1] < 0)
print("J  > 0 before its zero, < 0 after:",
      J[0] > 0, J[-1] < 0)
print("G  > 0 before its zero, < 0 after:",
      G[0] > 0, G[-1] < 0)

# u'(a) > 0
u = a/(2*(a - np.tan(a)))
du = np.diff(u)/np.diff(a)
print("u'(a) > 0 everywhere:", bool(np.all(du > 0)), " u(pi/2+)=", u[0], " u(pi-)=", u[-1])

# Dbar(a) = (a^2 - pi^2/4)/u^2 and endpoint limits
Dbar = (a**2 - np.pi**2/4)/u**2
print("Dbar(pi/2+) ~", Dbar[0], " (expect +inf)")
print("Dbar(pi-)  ~", Dbar[-1], " (expect 3 pi^2 =", 3*np.pi**2, ")")
print("min Dbar over grid =", Dbar.min(), " at a =", a[np.argmin(Dbar)], "(u =", u[np.argmin(Dbar)], ")")
print("claimed Dbar* = 24.94386613843234, u* = 0.3299225081196866")