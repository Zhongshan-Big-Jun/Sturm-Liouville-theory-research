# -*- coding: utf-8 -*-
"""Verify algebraic identities in the weak-contrast chapter (general mu, n=2)."""
import sympy as sp

mu, alpha, beta = sp.symbols('mu alpha beta', positive=True)
r = sp.symbols('r', positive=True)

def data(theta):
    s = sp.sin(theta)
    S = sp.sin(mu*theta)
    c = sp.cos(theta)
    C = sp.cos(mu*theta)
    F = S/s
    U = 1/s + mu/S
    Q = s + mu*S
    x = (F*c - mu*C)/(F+mu)
    rho = (mu*F + 1)/(F+mu)
    p = Q/U
    e = (mu**2-1)*F*(c+C)/(F+mu)**2
    kappa = 1 - x**2 - p
    return sp.simplify(x), sp.simplify(rho), sp.simplify(p), sp.simplify(e), sp.simplify(kappa), sp.simplify(U)

xp, rhop, pp, ep, kappap, Up = data(alpha)
xm, rhom, pm, em, kappam, Um = data(beta)
lam = sp.simplify(Up/Um)
d = sp.simplify(rhop - rhom)
eta = sp.simplify(-em)
w = sp.simplify((ep - r*eta/lam)/d)
u = sp.simplify(xp + w)
A0 = sp.simplify(1 - xp*u)
rB = sp.simplify(lam*ep/(eta + d*xm))
delta = r**2 - 1

Phi = (lam**2*w**2 + r**2*kappam + pm)*(A0 + delta*pp*u**2) - delta*pm*w*u**3
# Rearrangement
Phi2 = pm*(A0 - delta*w*u**3) + (lam**2*w**2 + (1+delta)*kappam)*A0 + delta*pp*u**2*(lam**2*w**2 + (1+delta)*kappam + pm)
print('Phi rearrangement holds:', sp.simplify(sp.expand(Phi - Phi2)) == 0)

# Square completion identity
expr = lam**2*A0*w**2 + delta*pp*pm*u**2 - delta*pm*w*u**3
expr2 = lam**2*A0*(w - delta*pm*u**3/(2*lam**2*A0))**2 + delta*pm*u**2/(4*lam**2*A0)*(4*lam**2*pp*A0 - delta*pm*u**4)
print('square completion holds:', sp.simplify(sp.expand(expr - expr2)) == 0)

# Positive margin key bracket: p_+(rho_+-1)-x_+ e_+ > 0
margin = sp.simplify(pp*(rhop-1) - xp*ep)
print('margin expression simplified:')
print(sp.factor(margin))
# The tex says the key bracket equals positive factor times q tan A - tan B(cos^2 B + q^2 sin^2 B)
# Let A=(mu+1)alpha/2, B=(mu-1)alpha/2, q=B/A.
A = (mu+1)*alpha/2
B = (mu-1)*alpha/2
q = B/A
key = q*sp.tan(A) - sp.tan(B)*(sp.cos(B)**2 + q**2*sp.sin(B)**2)
# Check if margin / (some positive factor) simplifies to key. We'll attempt to find ratio.
# Just print margin and key numeric for sample.
print('margin factor attempt (ratio):', sp.simplify(margin/key) if key != 0 else 'key zero')
# Numeric sample positivity
import random
for _ in range(5):
    muval = random.uniform(1.1, 5)
    # choose alpha < pi/(mu+1)
    al = random.uniform(0.01, 3.14159/(muval+1)*0.99)
    sub = {mu: muval, alpha: al}
    mv = float(margin.subs(sub))
    kv = float(key.subs(sub))
    print('sample', muval, al, 'margin', mv, 'key', kv)
