# -*- coding: utf-8 -*-
# Symbolic dFep/dq in terms of alpha1, alpha2, q, c.
import sympy as sp

q, c = sp.symbols('q c', positive=True)
x1, x2 = sp.symbols('x1 x2', positive=True)

def Phi(x): return sp.cos(x)**2 + q**2*sp.sin(x)**2
def M(x): return x**2*sp.sin(x)**2/(q + c*Phi(x))
def G(x):
    Ph = Phi(x); D = q + c*Ph
    return -Ph*(3+2*x*sp.cot(x))/D + 2*c*x*Ph*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2

# implicit derivatives (clean forms)
x1q = -sp.sin(x1)*sp.cos(x1)/(q + c*Phi(x1))
x2q = -sp.sin(x2)*sp.cos(x2)/(q + c*Phi(x2))   # = -sin x2 cos x2 / D2 (positive since sin x2 cos x2 < 0)

def total_q(f):
    # d/dq f(x1(q,c), x2(q,c), q, c) holding c fixed
    return sp.diff(f, q) + sp.diff(f, x1)*x1q + sp.diff(f, x2)*x2q

Fep = M(x1)*G(x1) - M(x2)*G(x2)
dFdq = total_q(Fep)
print('dFdq expression length:', len(str(sp.simplify(dFdq))))

# Substitute phase relations to simplify: tan(x1)tan(c x1) = 1/q, q tan x2 + tan(c x2) = 0
# We can substitute sin^2 and cos^2 via the phase equations? Try expressing c in terms of x1: c = atan(1/(q tan x1))/x1
# and in terms of x2: c = atan(-q tan x2)/x2 (with branch care).  Instead, substitute:
# sin^2(x1) = 1/(1 + cot^2(c x1)/q^2 ... messy.

# Try: substitute t1 = tan(x1), t2 = tan(x2), and use phase equations to eliminate c.
# Phase 1: tan(x1) tan(c x1) = 1/q.  Phase 2: q tan(x2) + tan(c x2) = 0.
# These link c to x1 and x2, but c is transcendental in them.  Hard to eliminate fully.

# Alternative: numerically test a factorization ansatz.  First print simplified form.
s = sp.simplify(dFdq)
print(s)
