# -*- coding: utf-8 -*-
"""t3_NJ2_terms: term structure of NJ2 over the loose region D."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
terms = [coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms)]

Amin, Amax = 2*math.pi/3, math.pi-0.655
def ev(term, Av, cv):
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, t: tv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    return float(term.subs(sv).evalf(20))

# scan ranges of each term and NJ2 total
rng = {}
for k, term in enumerate(terms):
    rng[k] = [1e30, -1e30]
NJ = [0.0, 0.0]
argN = [None, None]
N = 60
for i in range(N+1):
    for j in range(N+1):
        Av = Amin + i*(Amax-Amin)/N
        cv = 0.4 + j*0.1/N
        if Av*(1+cv) < math.pi: continue
        tot = 0.0
        for k, term in enumerate(terms):
            v = ev(term, Av, cv)
            tot += v
            if v < rng[k][0]: rng[k][0] = v
            if v > rng[k][1]: rng[k][1] = v
        if tot < NJ[0]: NJ[0] = tot; argN[0] = (Av, cv)
        if tot > NJ[1]: NJ[1] = tot; argN[1] = (Av, cv)
print('NJ2 over D: [%.1f, %.1f] at %s' % (NJ[0], NJ[1], argN))
print()
print('term ranges:')
for k, term in enumerate(terms):
    print('  %-55s coeff=%5d  range [%9.1f, %9.1f]' % (str(term)[:55], int(coeffs[k]), rng[k][0], rng[k][1]))
# sum of always-positive and always-negative terms
pos_sum_rng = [0.0, 0.0]; neg_sum_rng = [0.0, 0.0]
for i in range(N+1):
    for j in range(N+1):
        Av = Amin + i*(Amax-Amin)/N
        cv = 0.4 + j*0.1/N
        if Av*(1+cv) < math.pi: continue
        ps = sum(ev(term, Av, cv) for term in terms if int(str(term).split("*")[0]) > 0)
        ns = sum(ev(term, Av, cv) for term in terms if int(str(term).split("*")[0]) < 0)
        pos_sum_rng[0] = min(pos_sum_rng[0], ps); pos_sum_rng[1] = max(pos_sum_rng[1], ps)
        neg_sum_rng[0] = min(neg_sum_rng[0], ns); neg_sum_rng[1] = max(neg_sum_rng[1], ns)
print('positive terms sum: [%.1f, %.1f]; negative terms sum: [%.1f, %.1f]' % (pos_sum_rng[0], pos_sum_rng[1], neg_sum_rng[0], neg_sum_rng[1]))
