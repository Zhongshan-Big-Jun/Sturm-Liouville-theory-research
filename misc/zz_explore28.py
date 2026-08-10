import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def P2(g, q):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    t = mp.atan(q*mp.tan(g)); ct = mp.cos(t)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    z = ct*ct
    Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
    return t*t*cg*sg*sg*Q
N = 150
bad = 0; mxq2 = mp.mpf('-1e30')
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        if P2(g,q) > P2(g,2) + mp.mpf('1e-9'): bad += 1
        if P2(g,q) > mxq2: mxq2 = P2(g,q)
print('points with P2(g,q) > P2(g,2): %d ; global max %.6f' % (bad, mxq2))
# is P2(g,2) <= P2(pi/3,2)?
mx = mp.mpf('-1e30'); loc = None
for i in range(2000+1):
    g = glo + mp.mpf(i)*(ghi-glo)/2000
    v = P2(g, 2)
    if v > mx: mx, loc = v, float(g)
print('P2(g,2) max %.6f at g=%.5f ; P2(pi/3,2)=%.6f' % (mx, loc, P2(ghi,2)))
# Q(z_lo) max and Q(z_hi) max
def Qlo(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    D2 = 1+3*sg*sg
    z_lo = cg*cg/D2
    return 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
def Qhi(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    z = cg*cg
    return 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
mxl = mp.mpf('-1e30'); mxh = mp.mpf('-1e30'); locl = None; loch = None
for i in range(2000+1):
    g = glo + mp.mpf(i)*(ghi-glo)/2000
    v1, v2 = Qlo(g), Qhi(g)
    if v1 > mxl: mxl, locl = v1, float(g)
    if v2 > mxh: mxh, loch = v2, float(g)
print('Q(z_lo) max %.6f at g=%.5f ; Q(z_hi) max %.6f at g=%.5f' % (mxl, locl, mxh, loch))
