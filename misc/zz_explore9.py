import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def QloQhi(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    z_hi = cg*cg
    z_lo = cg*cg/(cg*cg+4*sg*sg)
    Qh = 4*A*A*z_hi*z_hi - A*B7*z_hi + 6*cg*cg*sg*sg
    Ql = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    return max(Qh, Ql), Qh, Ql
# G5 min
def G5v(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    return B5 - A*B4
N = 300
worst = (mp.mpf('-1e30'), None)
G5mn = mp.mpf('1e30')
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    G5mn = min(G5mn, G5v(g))
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
        z = ct*ct
        # actual P2
        B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
        Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
        P2 = t*t*cg*sg*sg*Q
        # proposed negative bound
        LB = 4.948*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
        # upper bound for P2 via 1D max
        Qm, _, _ = QloQhi(g)
        tmax = mp.atan(2*mp.tan(g))
        P2ub = tmax*tmax*cg*sg*sg*Qm
        margin = LB - P2ub  # need >0
        if margin < worst[0]: worst = (margin, (float(g), float(q)))
print('G5 min = %.5f' % G5mn)
print('worst margin (LB - P2ub): %.5f at %s' % (worst[0], worst[1]))
# also check the tight version: LB - actual P2
worst2 = (mp.mpf('1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
        z = ct*ct
        B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
        Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
        P2 = t*t*cg*sg*sg*Q
        LB = 4.948*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
        m = LB - P2
        if m < worst2[0]: worst2 = (m, (float(g), float(q)))
print('worst tight margin (LB - P2): %.5f at %s' % (worst2[0], worst2[1]))
