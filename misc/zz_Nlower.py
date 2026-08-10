import mpmath as mp
mp.mp.dps = 40
t0, t1 = mp.tan(mp.mpf('0.655')), mp.tan(mp.mpf('1.0472'))
p = mp.pi
def P2(t): return 16*t**9 + 84*t**7 + 84*t**5 - 2*t**3 - 18*t
def P1(t): return -32*p*t**9 - 208*t**8 - 168*p*t**7 - 376*t**6 - 168*p*t**5 - 177*t**4 + 4*p*t**3 - 4*t**2 + 36*p*t + 5
def P0(t): return 16*p**2*t**9 + 208*p*t**8 + 160*t**7 + 84*p**2*t**7 + 376*p*t**6 + 312*t**5 + 84*p**2*t**5 + 177*p*t**4 - 2*p**2*t**3 + 102*t**3 + 4*p*t**2 - 18*p**2*t + 10*t - 5*p
def N(t):
    g = mp.atan(t)
    return g**2*P2(t) + g*P1(t) + P0(t)
Nn = 5000
for name, fn in [('P2', P2), ('P1', P1), ('P0', P0)]:
    mn = mp.mpf('1e40'); mx = mp.mpf('-1e40')
    for i in range(Nn+1):
        t = t0 + mp.mpf(i)*(t1-t0)/Nn
        v = fn(t)
        if v < mn: mn = v
        if v > mx: mx = v
    print('%s: [%.3f, %.3f]' % (name, mn, mx))
# L(t) = 0.429*P2 + 1.0472*P1 + P0  (rational approx of g^2, g)
def L(t): return mp.mpf('0.429')*P2(t) + mp.mpf('1.0472')*P1(t) + P0(t)
mn = mp.mpf('1e40'); mx = mp.mpf('-1e40')
for i in range(Nn+1):
    t = t0 + mp.mpf(i)*(t1-t0)/Nn
    v = L(t)
    if v < mn: mn = v
    if v > mx: mx = v
print('L = 0.429*P2 + 1.0472*P1 + P0: [%.3f, %.3f]' % (mn, mx))
# exact min of L via derivative? Just print L at endpoints and midpoint
for t in [t0, (t0+t1)/2, t1]:
    print('L(%.4f) = %.3f' % (t, L(t)))
