import mpmath as mp
mp.mp.dps = 40
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    return A, sg, cg, B1, M, B2, B7
def c12(g):
    A, sg, cg, B1, M, B2, B7 = facts(g)
    return cg*abs(B2) if B1 >= 0 else cg*abs(M)
def F1(g):
    A, sg, cg, B1, M, B2, B7 = facts(g)
    t = mp.atan(2*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    LB = c12(g)*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
    z_hi = cg*cg; z_lo = cg*cg/(cg*cg+4*sg*sg)
    Qh = 4*A*A*z_hi*z_hi - A*B7*z_hi + 6*cg*cg*sg*sg
    Ql = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    P2ub = t*t*cg*sg*sg*max(Qh, Ql)
    return LB - P2ub
mn = (mp.mpf('1e30'), None); mx = (mp.mpf('-1e30'), None)
N = 2000
prev = None
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    v = F1(g)
    if v < mn[0]: mn = (v, float(g))
    if v > mx[0]: mx = (v, float(g))
print('F1(g) = LB(g,2) - P2ub(g) on [0.655, 1.0472]: min %.6f at g=%.6f ; max %.6f at g=%.6f' % (mn[0], mn[1], mx[0], mx[1]))
# derivative
h = mp.mpf('1e-8')
dmn = (mp.mpf('1e30'), None); dmx = (mp.mpf('-1e30'), None)
for i in range(1, N):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    d = (F1(g+h)-F1(g-h))/(2*h)
    if d < dmn[0]: dmn = (d, float(g))
    if d > dmx[0]: dmx = (d, float(g))
print('F1 derivative: min %.4f at g=%.5f ; max %.4f at g=%.5f' % (dmn[0], dmn[1], dmx[0], dmx[1]))
