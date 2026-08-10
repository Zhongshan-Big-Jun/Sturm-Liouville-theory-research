import mpmath as mp
mp.mp.dps = 40
t0, t1 = mp.tan(mp.mpf('0.655')), mp.tan(mp.mpf('1.0472'))
def N(t):
    g = mp.atan(t); p = mp.pi
    return (16*t**9*g**2 - 32*p*t**9*g - 384*t**9 + 16*p**2*t**9 - 208*t**8*g + 208*p*t**8
        + 84*t**7*g**2 - 168*p*t**7*g + 160*t**7 + 84*p**2*t**7 - 376*t**6*g + 376*p*t**6
        + 84*t**5*g**2 - 168*p*t**5*g + 312*t**5 + 84*p**2*t**5 - 177*t**4*g + 177*p*t**4
        - 2*t**3*g**2 + 4*p*t**3*g - 2*p**2*t**3 + 102*t**3 - 4*t**2*g + 4*p*t**2
        - 18*t*g**2 + 36*p*t*g - 18*p**2*t + 10*t + 5*g - 5*p)
print('t0 = %.6f, t1 = %.6f' % (t0, t1))
mn = (mp.mpf('1e40'), None); mx = (mp.mpf('-1e40'), None)
Nn = 4000
for i in range(Nn+1):
    t = t0 + mp.mpf(i)*(t1-t0)/Nn
    v = N(t)
    if v < mn[0]: mn = (v, t)
    if v > mx[0]: mx = (v, t)
print('N(t): min %.4f @ t=%.5f ; max %.4f @ t=%.5f' % (mn[0], mn[1], mx[0], mx[1]))
h = mp.mpf('1e-7')
dmn = mp.mpf('1e40'); dmx = mp.mpf('-1e40')
for i in range(1, Nn):
    t = t0 + mp.mpf(i)*(t1-t0)/Nn
    d = (N(t+h)-N(t-h))/(2*h)
    if d < dmn: dmn = d
    if d > dmx: dmx = d
print('dN/dt: [%.3f, %.3f]' % (dmn, dmx))
# Qlo values at endpoints and midpoint
def Qlo(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    D2 = 1+3*sg*sg; z = cg*cg/D2
    return 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
for g in [mp.mpf('0.655'), mp.mpf('1.0'), mp.mpf('1.001'), mp.mpf('1.002'), mp.mpf('1.0472')]:
    print('Qlo(%.4f) = %.6f' % (g, Qlo(g)))
# Qhi
def Qhi(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    z = cg*cg
    return 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
mnq = (mp.mpf('1e40'),None); mxq = (mp.mpf('-1e40'),None)
for i in range(Nn+1):
    g = mp.mpf('0.655') + mp.mpf(i)*(mp.mpf('1.0472')-mp.mpf('0.655'))/Nn
    v = Qhi(g)
    if v < mnq[0]: mnq = (v, g)
    if v > mxq[0]: mxq = (v, g)
print('Qhi: [%.5f, %.5f]' % (mnq[0], mxq[0]))
