# -*- coding: utf-8 -*-
"""Numeric verification of weak-contrast algebraic identities (evidence only)."""
import math, random

def data(mu, theta):
    s = math.sin(theta); S = math.sin(mu*theta)
    c = math.cos(theta); C = math.cos(mu*theta)
    F = S/s
    U = 1/s + mu/S
    Q = s + mu*S
    x = (F*c - mu*C)/(F+mu)
    rho = (mu*F + 1)/(F+mu)
    p = Q/U
    e = (mu**2-1)*F*(c+C)/(F+mu)**2
    kappa = 1 - x*x - p
    return x, rho, p, e, kappa, U

def check():
    for _ in range(1000):
        mu = random.uniform(1.05, 10)
        alpha = random.uniform(1e-6, math.pi/(mu+1)*0.9999)
        beta = random.uniform(math.pi/(mu+1)*1.0001, math.pi/mu*0.9999)
        r = random.uniform(1.001, 5)
        xp, rhop, pp, ep, kappap, Up = data(mu, alpha)
        xm, rhom, pm, em, kappam, Um = data(mu, beta)
        lam = Up/Um
        d = rhop - rhom
        eta = -em
        w = (ep - r*eta/lam)/d
        u = xp + w
        A0 = 1 - xp*u
        rB = lam*ep/(eta + d*xm)
        delta = r*r - 1
        Phi = (lam**2*w**2 + r*r*kappam + pm)*(A0 + delta*pp*u**2) - delta*pm*w*u**3
        Phi2 = pm*(A0 - delta*w*u**3) + (lam**2*w**2 + (1+delta)*kappam)*A0 + delta*pp*u**2*(lam**2*w**2 + (1+delta)*kappam + pm)
        if abs(Phi - Phi2) > 1e-7 * max(1.0, abs(Phi)):
            print('FAIL rearrangement', mu, alpha, beta, r, Phi, Phi2)
            return False
        expr = lam**2*A0*w**2 + delta*pp*pm*u**2 - delta*pm*w*u**3
        expr2 = lam**2*A0*(w - delta*pm*u**3/(2*lam**2*A0))**2 + delta*pm*u**2/(4*lam**2*A0)*(4*lam**2*pp*A0 - delta*pm*u**4)
        if abs(expr - expr2) > 1e-7 * max(1.0, abs(expr)):
            print('FAIL square', mu, alpha, beta, r, expr, expr2)
            return False
        # margin positive when physical domain
        margin = pp*(rhop-1) - xp*ep
        if margin <= 0:
            print('FAIL margin positive', mu, alpha, beta, margin)
            return False
        # A0 > kappa_+?
        if not (A0 > kappap):
            print('FAIL A0>kappa', mu, alpha, beta, A0, kappap)
            return False
    print('PASS all numeric checks (1000 random samples)')
    return True

check()
