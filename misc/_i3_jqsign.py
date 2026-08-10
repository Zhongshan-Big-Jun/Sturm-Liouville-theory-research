# -*- coding: utf-8 -*-
"""Locate Jq sign regions on B2."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
def Jq(x,c,q):
    h = mp.mpf('1e-6')
    return (J(x,c,q+h)-J(x,c,q-h))/(2*h)

# scan on B2 faces c=0.4, 0.45, 0.5: Jq sign by x,q
for cv in ['0.4','0.5']:
    c = mp.mpf(cv)
    print("c=%s: Jq sign map (x rows 0..10, q cols 0..10):" % cv)
    for i in range(11):
        x = mp.mpf('2.0944')+(mp.mpf('2.4859')-mp.mpf('2.0944'))*i/10
        row = []
        for j in range(11):
            q = 1+1*j/10
            v = Jq(x,c,q)
            row.append('+' if v>0 else ('-' if v<0 else '0'))
        print("  x=%.3f %s" % (x, ''.join(row)))
