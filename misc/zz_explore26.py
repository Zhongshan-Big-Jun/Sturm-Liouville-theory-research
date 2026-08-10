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
    c12 = cg*abs(B2) if B1 >= 0 else cg*abs(M)
    return A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12
mconst = mp.mpf('0.3164')
def comps(g):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12 = facts(g)
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    TA = 4*c12*A*A*sg*sg*cg**3/d**4
    TB = 2*A**3*sg*sg*tmax*cg**5/d**5
    TC = G5*A*sg*cg*cg*mconst
    return TA, TB, TC
print(' g       TA     TB     TC')
for i in range(0, 21):
    g = glo + mp.mpf(i)*(ghi-glo)/20
    TA, TB, TC = comps(g)
    print('%.4f  %.4f  %.4f  %.4f' % (g, TA, TB, TC))
# check monotonicity pieces of TA and TC: TA = 4 c12 A^2 sg^2 cg^3 / D^4
# c12 piecewise: cg|B2| on [0.655, g0], cg|M| on [g0, pi/3]
# check |B2| decreasing? B2 range [-6.78,-2.82], and d(B2)/dg?
h = mp.mpf('1e-9')
for name, fn in [('c12', lambda g: comps(g)[0]/(4*facts(g)[0]**2*facts(g)[1]**2*facts(g)[2]**3)* (1+3*facts(g)[1]**2)**2), ('M', lambda g: facts(g)[5]), ('B2', lambda g: facts(g)[6])]:
    pass
# just print c12*..., and |M|, |B2| samples
print()
for i in range(0, 21):
    g = glo + mp.mpf(i)*(ghi-glo)/20
    A, sg, cg, B1, M, B2, *_ = facts(g)
    print('%.4f  B1=%.3f  |B2|=%.3f  |M|=%.3f' % (g, B1, abs(B2), abs(M)))
