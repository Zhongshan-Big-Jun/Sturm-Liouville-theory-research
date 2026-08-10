# -*- coding: utf-8 -*-
"""J2_2d derivative sign structure on box."""
import mpmath as mp
mp.mp.dps = 40
def Phi(x, q): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; W = 3 + 2*x/mp.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*mp.sin(x)*mp.cos(x)/(D*D)
def Jfull(x, c, q):
    Ph = Phi(x, q); D = q + c*Ph; xp = -x*Ph/D
    W = 3 + 2*x/mp.tan(x)
    Gv = G(x, c, q)
    h = mp.mpf('1e-6')
    Gpv = ((G(x+h,c,q)-G(x-h,c,q))/(2*h))*xp
    sc = mp.sin(x)*mp.cos(x)
    Gc_ = Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)
    return Gv*Gv + Gpv + Gc_
def J2_2d(g,q):
    return Jfull(mp.pi-g, mp.atan(q*mp.tan(g))/(mp.pi-g), q)
def d1(f, var, a, b):
    h=mp.mpf('1e-6')
    if var=='g': return (f(a+h,b)-f(a-h,b))/(2*h)
    if var=='q': return (f(a,b+h)-f(a,b-h))/(2*h)

print("J2_2d d/dg sign map (g rows 0..10, q cols 0..10):")
for i in range(11):
    g = mp.mpf('0.6557')+(mp.mpf('1.0472')-mp.mpf('0.6557'))*i/10
    row=[]
    for j in range(11):
        q = 1+1*j/10
        v = d1(J2_2d,'g',g,q)
        row.append('+' if v>0 else ('-' if v<0 else '0'))
    print("  g=%.3f %s" % (g,''.join(row)))
print("J2_2d d/dq sign map (g rows 0..10, q cols 0..10):")
for i in range(11):
    g = mp.mpf('0.6557')+(mp.mpf('1.0472')-mp.mpf('0.6557'))*i/10
    row=[]
    for j in range(11):
        q = 1+1*j/10
        v = d1(J2_2d,'q',g,q)
        row.append('+' if v>0 else ('-' if v<0 else '0'))
    print("  g=%.3f %s" % (g,''.join(row)))
