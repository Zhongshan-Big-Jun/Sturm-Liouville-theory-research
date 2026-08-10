# -*- coding: utf-8 -*-
"""Study 1D functions M, B2, B4, B5, B7, G5=B5-A*B4 on gamma in [0.655, 1.0472]:
monotonicity, convexity, endpoints."""
import mpmath as mp
mp.mp.dps = 40
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def fns(g):
    A = mp.pi - g; sg, cg = mp.sin(g), mp.cos(g)
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    return dict(M=M, B2=B2, B4=B4, B5=B5, B7=B7, G5=G5)
h = mp.mpf('1e-7')
for name in ['M','B2','B4','B5','B7','G5']:
    lo = (mp.mpf('1e30'), None); hi = (mp.mpf('-1e30'), None)
    dmin = mp.mpf('1e30'); dmax = mp.mpf('-1e30')
    ddmin = mp.mpf('1e30'); ddmax = mp.mpf('-1e30')
    N = 400
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        v = fns(g)[name]
        if v < lo[0]: lo = (v, float(g))
        if v > hi[0]: hi = (v, float(g))
        if 0 < i < N:
            d = (fns(g+h)[name]-fns(g-h)[name])/(2*h)
            dd = (fns(g+2*h)[name]-2*fns(g)[name]+fns(g-2*h)[name])/(4*h*h)
            dmin = min(dmin, d); dmax = max(dmax, d)
            ddmin = min(ddmin, dd); ddmax = max(ddmax, dd)
    print('%s: [%.5f, %.5f]  d/dg: [%.3f, %.3f]  d2: [%.3f, %.3f]' % (name, lo[0], hi[0], dmin, dmax, ddmin, ddmax))
print()
print('endpoint values:')
for g in [glo, mp.mpf('0.7'), mp.mpf('0.8'), mp.mpf('0.9'), mp.mpf('1.0'), ghi]:
    r = fns(g)
    print('g=%.4f: M=%.5f B2=%.5f B4=%.5f B5=%.5f B7=%.5f G5=%.5f' % (g, r['M'], r['B2'], r['B4'], r['B5'], r['B7'], r['G5']))
