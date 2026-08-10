# -*- coding: utf-8 -*-
"""#2 n=2 structure: for symmetric [1,R,1,R,1], lambda2 = nu1 (Dirichlet half), lambda3 = mu2 (mixed half).
Half-string [1,R,1] widths (a,b,c/2).  Verify + derive balanced-phase secular eqs symbolically."""
import numpy as np
from scipy.optimize import brentq

def Thalf(omega, alpha, beta, gamma, R):
    def T(L, cc, w):
        wc = w*np.sqrt(cc)
        return np.array([[np.cos(wc*L), np.sin(wc*L)/wc], [-wc*np.sin(wc*L), np.cos(wc*L)]])
    M = T(alpha, 1.0, omega) @ T(beta, R, omega) @ T(gamma, 1.0, omega)
    return M

def solve_sec(fun, k, lo=1e-9, hi=200.0, npts=40000):
    w = np.linspace(lo, hi, npts)
    d = np.array([fun(x) for x in w])
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        root = brentq(fun, w[i], w[i+1], xtol=1e-14, rtol=1e-14)
        out.append(root)
        if len(out) >= k: break
    return np.array(out)

R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
a, b, c = s*t, t, s*t
alpha, beta, gamma = a, b, c/2.0

# half-string Dirichlet: M01(w) = 0  -> nu_k;  mixed (u'(L)=0): M11(w) = 0 -> mu_k
nu = solve_sec(lambda w: Thalf(w, alpha, beta, gamma, R)[0,1], 3)
mu = solve_sec(lambda w: Thalf(w, alpha, beta, gamma, R)[1,1], 3)
print("half Dirichlet nu_1,nu_2,nu_3:", np.array2string(nu**2, precision=8))
print("half mixed     mu_1,mu_2,mu_3:", np.array2string(mu**2, precision=8))
print("lambda2 = nu1^2 =", nu[0]**2)
print("lambda3 = mu2^2 =", mu[1]**2)
print("ratio mu2^2/nu1^2 =", (mu[1]/nu[0])**2, " vs conjectured 4.2846614708")

# balanced-phase relations?  try: w2*a vs w3*a etc.
w2 = nu[0]; w3 = mu[1]
print("\nw2*a =", w2*alpha, " w2*b =", w2*beta, " w2*gamma =", w2*gamma)
print("w3*a =", w3*alpha, " w3*b =", w3*beta, " w3*gamma =", w3*gamma)
print("pi - w3*a =", np.pi - w3*alpha)
print("w2*a + w3*a =", w2*alpha + w3*alpha, " (pi?)")
print("w2*beta + w3*beta =", (w2+w3)*beta)
