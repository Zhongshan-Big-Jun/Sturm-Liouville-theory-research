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
def G1(g):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12 = facts(g)
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    TA = 4*c12*A*A*sg*sg*cg**3/d**4
    TB = 2*A**3*sg*sg*tmax*cg**5/d**5
    TC = G5*A*sg*cg*cg*mconst
    z_lo = cg*cg/(d*d)
    Qlo = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    TD = tmax*tmax*cg*sg*sg*Qlo
    return TA+TB+TC-TD
N = 3000
mn = (mp.mpf('1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    v = G1(g)
    if v < mn[0]: mn = (v, float(g))
print('G1 min = %.6f at g=%.6f' % (mn[0], mn[1]))
h = mp.mpf('1e-9')
dmn = (mp.mpf('1e30'), None); dmx = (mp.mpf('-1e30'), None)
for i in range(1, N):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    d = (G1(g+h)-G1(g-h))/(2*h)
    if d < dmn[0]: dmn = (d, float(g))
    if d > dmx[0]: dmx = (d, float(g))
print('G1 derivative: min %.4f at g=%.5f ; max %.4f at g=%.5f' % (dmn[0], dmn[1], dmx[0], dmx[1]))
# components monotonicity
def comps(g):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12 = facts(g)
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    return dict(TA=4*c12*A*A*sg*sg*cg**3/d**4, TB=2*A**3*sg*sg*tmax*cg**5/d**5, TC=G5*A*sg*cg*cg*mconst, TD=tmax*tmax*cg*sg*sg*(4*A*A*(cg*cg/d**2)**2 - A*B7*cg*cg/d**2 + 6*cg*cg*sg*sg))
for name in ['TA','TB','TC','TD']:
    vals = [comps(glo+mp.mpf(i)*(ghi-glo)/N)[name] for i in range(N+1)]
    print('%s: [%.5f, %.5f]' % (name, min(vals), max(vals)))
