import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
# candidate gamma-only lower bound for LB and upper bound for P2
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
def D(g):
    A, sg, cg, *_ = facts(g)
    return mp.sqrt(1+3*sg*sg)
def P2ub(g):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12 = facts(g)
    d = D(g)
    z_lo = cg*cg/(d*d)
    Qlo = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    tmax = mp.atan(2*mp.tan(g))
    return tmax*tmax*cg*sg*sg*Qlo
def Lcrude(g, mode):
    A, sg, cg, B1, M, B2, B4, B5, B7, G5, c12 = facts(g)
    d = D(g); tmax = mp.atan(2*mp.tan(g))
    TA = 4*c12*A*A*sg*sg*cg**3/d**4
    TB = 2*A**3*sg*sg*tmax*cg**5/d**5
    # m(gamma) = min over t in [gamma, tmax] of (t/2) sin 2t  (numeric)
    Ns = 200
    mm = mp.mpf('1e30')
    for i in range(Ns+1):
        t = mp.mpf(0.655) + mp.mpf(i)*(mp.mpf('1.289')-mp.mpf('0.655'))/Ns
        mm = min(mm, (t/2)*mp.sin(2*t))
    if mode == 'const_m':
        TC = G5*A*sg*cg*cg*mm
    elif mode == 't_gamma':
        TC = G5*A*sg*cg*cg*(0.655/2)*mp.sin(2*0.655)
    return TA+TB+TC
for mode in ['const_m','t_gamma']:
    mn = (mp.mpf('1e30'), None)
    N = 2000
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        v = Lcrude(g, mode) - P2ub(g)
        if v < mn[0]: mn = (v, float(g))
    print('%s: min of Lcrude - P2ub = %.5f at g=%.5f' % (mode, mn[0], mn[1]))
