# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
def Psi(q0, x):
    W = 1 + q0*mp.sin(x)**2
    return x*mp.cot(x)/W

def check(q0, x):
    W = 1 + q0*mp.sin(x)**2
    dPsi = mp.diff(lambda t: Psi(q0, t), x, 1)
    lhs = W**2*mp.sin(x)**2*dPsi
    rhs = mp.sin(x)*mp.cos(x) - x + q0*mp.sin(x)**2*(mp.sin(x)*mp.cos(x) - x*(1+2*mp.cos(x)**2))
    return lhs, rhs

worst = 0
for q0 in [0, 1, 3, 10, 100]:
    for x in [0.001, 0.01, 0.1, 0.5, 1.0, 1.5, 2.5, 3.0, 3.13, 3.141]:
        l, r = check(mp.mpf(q0), mp.mpf(x))
        worst = max(worst, abs(l-r))
        assert mp.sign(l) == mp.sign(r) or abs(l-r) < mp.mpf('1e-30')
print("worst |lhs-rhs|:", worst)
# also verify sign of Psi' < 0 throughout (0,pi)
for q0 in [0, 0.5, 1, 3, 10, 100]:
    xs = [0.001, 0.01, 0.05, 0.1, 0.3, 0.7, 1.2, 1.8, 2.5, 2.9, 3.1, 3.14]
    for x in xs:
        d = mp.diff(lambda t: Psi(q0, t), x, 1)
        assert d < 0, (q0, x, d)
print("Psi' < 0 on (0,pi) sampled OK")
