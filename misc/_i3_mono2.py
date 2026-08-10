# -*- coding: utf-8 -*-
"""Track max location on B2; check q-monotonicity on face c=0.5."""
import mpmath as mp
mp.mp.dps = 40

def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def Gc(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    sc = mp.sin(x)*mp.cos(x)
    return Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
def Gx(x, c, q):
    h = mp.mpf('1e-6')
    return (G(x+h, c, q) - G(x-h, c, q))/(2*h)
def J(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    Gv = G(x, c, q)
    return Gv*Gv + Gx(x, c, q)*xp + Gc(x, c, q)

# max location on B2
x0,x1,q0,q1,c0,c1 = mp.mpf('2.0944'),mp.mpf('2.4859'),mp.mpf(1),mp.mpf(2),mp.mpf('0.4'),mp.mpf('0.5')
mx = -mp.inf; arg = None
for i in range(30+1):
    x = x0 + (x1-x0)*i/30
    for j in range(30+1):
        q = q0 + (q1-q0)*j/30
        for k in range(30+1):
            c = c0 + (c1-c0)*k/30
            v = J(x,c,q)
            if v > mx: mx = v; arg = (x,c,q)
print("B2 max J = %.6f at (x,c,q)=%s" % (mx, arg))

# q-monotonicity of J at c=0.5 on B2
def Jq(x,c,q):
    h = mp.mpf('1e-6')
    return (J(x,c,q+h)-J(x,c,q-h))/(2*h)
mn = mp.inf; mx = -mp.inf
for i in range(12+1):
    x = x0 + (x1-x0)*i/12
    for j in range(12+1):
        q = q0 + (q1-q0)*j/12
        v = Jq(x, mp.mpf('0.5'), q)
        mn = min(mn, v); mx = max(mx, v)
print("B2 face c=0.5: Jq in [%.4f, %.4f]" % (mn, mx))

# q-monotonicity of J at c=0.4 on B2
mn = mp.inf; mx = -mp.inf
for i in range(12+1):
    x = x0 + (x1-x0)*i/12
    for j in range(12+1):
        q = q0 + (q1-q0)*j/12
        v = Jq(x, mp.mpf('0.4'), q)
        mn = min(mn, v); mx = max(mx, v)
print("B2 face c=0.4: Jq in [%.4f, %.4f]" % (mn, mx))
