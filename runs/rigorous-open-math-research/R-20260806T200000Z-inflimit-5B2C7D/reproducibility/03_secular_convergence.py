# -*- coding: utf-8 -*-
"""03_secular_convergence.py
Fixed-u convergence: for u fixed in (0,1/2), mu_k(R,u) = R lambda_k(R,u)
converge to the limiting values mu_1bar(u) = pi^2/(4u^2) and mu_2bar(u)
(unique root of tan(sqrt(mu) u) = sqrt(mu)(u - 1/2) with sqrt(mu) u in
(pi/2, pi)).  Computes the exact 3-block eigenvalues via the half-string
secular equations:
  even: E(mu) = cot(sqrt(mu) u) - (1/sqrt(R)) tan(sqrt(mu/R)(1/2-u)) = 0
  odd:  O(mu) = tan(sqrt(mu) u) + sqrt(R) tan(sqrt(mu/R)(1/2-u)) = 0
and checks (i) the roots converge, (ii) the convergence is locally uniform
in u on compact subintervals of (0,1/2), (iii) R*D_R(u) -> Dbar(u).
ASCII punctuation. Run: python 03_secular_convergence.py
"""
import numpy as np
from scipy.optimize import brentq
import mpmath as mp
mp.mp.dps = 30

def E(mu, u, R):
    return np.tan(np.pi/2 - np.sqrt(mu)*u) - (1/np.sqrt(R))*np.tan(np.sqrt(mu/R)*(0.5-u))
    # cot(x) = tan(pi/2 - x); same roots

def O(mu, u, R):
    return np.tan(np.sqrt(mu)*u) + np.sqrt(R)*np.tan(np.sqrt(mu/R)*(0.5-u))

def mu1_R(u, R):
    # unique root of E on (0, pi^2/(4u^2))
    return brentq(lambda m: E(m, u, R), 1e-12, np.pi**2/(4*u**2) - 1e-12)

def mu2_R(u, R):
    # for R large enough, unique root of O on (pi^2/(4u^2), pi^2/u^2)
    return brentq(lambda m: O(m, u, R), np.pi**2/(4*u**2) + 1e-12, np.pi**2/u**2 - 1e-12)

def mu1bar(u):
    return np.pi**2/(4*u**2)

def a_of(u):
    return brentq(lambda a: np.tan(a) - a*(1 - 1.0/(2*u)), np.pi/2 + 1e-9, np.pi - 1e-9)

def mu2bar(u):
    a = a_of(u)
    return (a/u)**2

print("(i) fixed-u convergence, u = 0.3")
for R in [1e2, 1e4, 1e6, 1e8]:
    m1, m2 = mu1_R(0.3, R), mu2_R(0.3, R)
    b1, b2 = mu1bar(0.3), mu2bar(0.3)
    print(f"R={R:8.0e}: mu1={m1:.9f} (lim {b1:.9f}) err={m1-b1:+.3e} | "
          f"mu2={m2:.9f} (lim {b2:.9f}) err={m2-b2:+.3e} | R*D={m2-m1:.9f} (lim {b2-b1:.9f})")

print("(ii) local uniformity on [0.2, 0.45]: max error vs R")
for R in [1e3, 1e5, 1e7]:
    us = np.linspace(0.2, 0.45, 40)
    err1 = max(abs(mu1_R(u, R) - mu1bar(u)) for u in us)
    err2 = max(abs(mu2_R(u, R) - mu2bar(u)) for u in us)
    errD = max(abs((mu2_R(u,R)-mu1_R(u,R)) - (mu2bar(u)-mu1bar(u))) for u in us)
    print(f"R={R:8.0e}: max|mu1-mu1bar|={err1:.3e} max|mu2-mu2bar|={err2:.3e} max|R*D-Dbar|={errD:.3e}")

print("(iii) scaling rates: error * R on [0.25, 0.4]")
us = np.linspace(0.25, 0.4, 10)
for R in [1e4, 1e8]:
    e1 = max(abs(mu1_R(u,R)-mu1bar(u)) for u in us)*R
    e2 = max(abs(mu2_R(u,R)-mu2bar(u)) for u in us)*R
    print(f"R={R:8.0e}: err1*R ~ {e1:.3f}, err2*R ~ {e2:.3f}  (O(1) expected for fixed u)")