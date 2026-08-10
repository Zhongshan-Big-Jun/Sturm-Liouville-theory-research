import mpmath as mp
mp.mp.dps = 30
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
    return A, sg, cg, B1, M, B2, B7, G5
# piecewise coefficient for T1+T2
def coef12(g):
    A, sg, cg, B1, M, B2, B7, G5 = facts(g)
    return (cg*abs(B2), cg*abs(M))[B1 < 0]
def Qmax(g):
    A, sg, cg, B1, M, B2, B7, G5 = facts(g)
    z_hi = cg*cg; z_lo = cg*cg/(cg*cg+4*sg*sg)
    Qh = 4*A*A*z_hi*z_hi - A*B7*z_hi + 6*cg*cg*sg*sg
    Ql = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    return max(Qh, Ql)
def P2ub(g):
    A, sg, cg, B1, M, B2, B7, G5 = facts(g)
    tmax = mp.atan(2*mp.tan(g))
    return tmax*tmax*cg*sg*sg*Qmax(g)
N = 400
worst = (mp.mpf('1e30'), None)
worst_tight = (mp.mpf('1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A, sg, cg, B1, M, B2, B7, G5 = facts(g)
    c12 = coef12(g)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
        LB = c12*A*A*cg*st*st*ct*ct + 2*A**3*sg*sg*t*ct**5 + 3.8*A*sg*t*st*ct*cg*cg
        m = LB - P2ub(g)
        if m < worst[0]: worst = (m, (float(g), float(q)))
        # tight check with actual P2
        z = ct*ct
        Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
        P2 = t*t*cg*sg*sg*Q
        m2 = LB - P2
        if m2 < worst_tight[0]: worst_tight = (m2, (float(g), float(q)))
print('worst margin LB - P2ub: %.5f at %s' % (worst[0], worst[1]))
print('worst tight margin LB - P2: %.5f at %s' % (worst_tight[0], worst_tight[1]))
# also check the pointwise Qmax vs actual Q ratio
worstr = (mp.mpf('1e30'), None)
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A, sg, cg, B1, M, B2, B7, G5 = facts(g)
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g)); ct = mp.cos(t)
        z = ct*ct
        Q = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
        if Q > 0:
            r = (t*t*Q)/(P2ub(g))
            if r < worstr[0]: worstr = (r, (float(g), float(q)))
print('min ratio t^2 Q / P2ub over Q>0: %.5f at %s' % (worstr[0], worstr[1]))
