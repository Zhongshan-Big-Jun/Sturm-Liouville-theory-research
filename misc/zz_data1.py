import mpmath as mp
mp.mp.dps = 40
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    return dict(A=A, sg=sg, cg=cg, B1=B1, M=M, B2=B2, B4=B4, B5=B5, B7=B7, G5=G5)
# monotonicity & extrema of key functions via fine scan
N = 20000
names = ['B1','M','B2','B4','B5','B7','G5']
for name in names:
    lo=(mp.mpf('1e40'),None); hi=(mp.mpf('-1e40'),None)
    dmin=mp.mpf('1e40'); dmax=mp.mpf('-1e40')
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        v = facts(g)[name]
        if v<lo[0]: lo=(v,g)
        if v>hi[0]: hi=(v,g)
    h = mp.mpf('1e-6')
    # derivative scan
    dmin=mp.mpf('1e40'); dmax=mp.mpf('-1e40')
    for i in range(1,N):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        d = (facts(g+h)[name]-facts(g-h)[name])/(2*h)
        if d<dmin: dmin=d
        if d>dmax: dmax=d
    print('%s: min %.6f@%.5f  max %.6f@%.5f  d: [%.3f, %.3f]' % (name, lo[0],lo[1], hi[0],hi[1], dmin, dmax))
# P = A*sg*cg^2, H = G5*P
def P(g): return facts(g)['A']*facts(g)['sg']*facts(g)['cg']**2
def H(g): return facts(g)['G5']*P(g)
dmin=mp.mpf('1e40'); dmax=mp.mpf('-1e40')
for i in range(1,N):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    d = (P(g+h)-P(g-h))/(2*h)
    if d<dmin: dmin=d
    if d>dmax: dmax=d
print('P: [%.5f, %.5f] dP: [%.4f, %.4f]' % (P(glo), P(ghi), dmin, dmax))
dmin=mp.mpf('1e40'); dmax=mp.mpf('-1e40'); hlo=(mp.mpf('1e40'),None); hhi=(mp.mpf('-1e40'),None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    v = H(g)
    if v<hlo[0]: hlo=(v,g)
    if v>hhi[0]: hhi=(v,g)
for i in range(1,N):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    d = (H(g+h)-H(g-h))/(2*h)
    if d<dmin: dmin=d
    if d>dmax: dmax=d
print('H: min %.6f@%.5f  max %.6f@%.5f  dH: [%.4f, %.4f]' % (hlo[0],hlo[1], hhi[0],hhi[1], dmin, dmax))
# H at selected points
for g in [mp.mpf('0.655'), mp.mpf('0.7'), mp.mpf('0.75'), mp.mpf('0.8'), mp.mpf('0.85'), mp.mpf('0.9'), mp.mpf('0.95'), mp.mpf('1.0'), mp.mpf('1.0472')]:
    print('H(%.4f) = %.6f' % (g, H(g)))
# G5 monotonicity: find sign changes of G5'
prev = None
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    d = (facts(g+h)['G5']-facts(g-h)['G5'])/(2*h)
    s = 1 if d>0 else (-1 if d<0 else 0)
    if prev is not None and s != prev[0]:
        print('G5 d sign change at g=%.6f (%s -> %s)' % (g, prev[0], s))
    prev = (s, g)
