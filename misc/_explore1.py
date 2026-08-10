# -*- coding: utf-8 -*-
# Deep exploration of KEY LEMMA structure: A-C, B-D, sum, G1, G2, M1, M2 over (q, c)
import math, numpy as np

def solve_phases(q, c):
    """Return alpha1 in (0,pi/2) solving tan(c a)=1/(q tan a), and gamma in (0,pi/2)
    solving tan(c (pi-g)) = q tan g. Bisection."""
    # alpha1: f(a) = q tan(a) tan(c a) - 1 = 0, on (alpha0, pi/2)
    # monotone? q tan(a) tan(ca) increasing in a on (0,pi/2) for c in (0,1/2)? check numerically.
    def f1(a): return q*math.tan(a)*math.tan(c*a) - 1.0
    lo, hi = 1e-12, math.pi/2 - 1e-12
    # f1 -> -1 at 0; at pi/2 -> +inf; single crossing assumed
    for _ in range(200):
        m = 0.5*(lo+hi)
        if f1(lo)*f1(m) <= 0: hi = m
        else: lo = m
    a1 = 0.5*(lo+hi)
    # gamma: f2(g) = q tan(g) tan(c (pi - g)) - 1 = 0? check: tan(c(pi-g)) = q tan g
    # at g=0: 0*... -1 = -1; at g=pi/2: q*inf*... hmm. Use form: g2(g) = q tan g - tan(c(pi-g))
    def f2(g): return q*math.tan(g) - math.tan(c*(math.pi - g))
    lo, hi = 1e-12, math.pi/2 - 1e-12
    # f2(0+) = 0 - tan(c*pi) ; for c<1/2, c*pi < pi/2 so tan>0 => f2(0)<0. f2(pi/2-)=+inf>0.
    for _ in range(200):
        m = 0.5*(lo+hi)
        if f2(lo)*f2(m) <= 0: hi = m
        else: lo = m
    g = 0.5*(lo+hi)
    return a1, g

def Phi(a, q): return math.cos(a)**2 + q*q*math.sin(a)**2
def Wf(a): return 3 + 2*a/math.tan(a) if abs(math.tan(a)) > 1e-12 else 3.0

def components(q, c):
    a1, g = solve_phases(q, c)
    a2 = math.pi - g
    P1, P2 = Phi(a1, q), Phi(g, q)
    W1, W2 = Wf(a1), Wf(a2)
    q1 = q + c*P1; q2 = q + c*P2
    AC = P1*W1/q1 - 2*c*(q*q-1)*a1*P1*math.sin(a1)*math.cos(a1)/q1**2
    BD = -P2*W2/q2 + 2*c*(q*q-1)*a2*P2*abs(math.sin(a2)*math.cos(a2))/q2**2
    return a1, g, AC, BD, AC+BD

# sanity: corner limit q->1+, c->1/2-
for q, c in [(1.0001, 0.4999), (1.001, 0.499), (1.01, 0.49), (1.05, 0.47), (1.1, 0.45)]:
    a1, g, AC, BD, S = components(q, c)
    print("q=%.4f c=%.4f: a1=%.4f g=%.4f A-C=%.5f B-D=%.5f sum=%.5f" % (q, c, a1, g, AC, BD, S))
print("corner limit: 4pi/(3sqrt3) =", 4*math.pi/(3*math.sqrt(3)))