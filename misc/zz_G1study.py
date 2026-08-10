import mpmath as mp
mp.mp.dps = 50
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = None
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
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
    TD = tmax*tmax*cg*sg*sg*max(Qlo, mp.mpf(0))
    return TA+TB+TC-TD, TA, TB, TC, TD, Qlo
print('g        G1       TA      TB      TC      TD      Qlo')
N=25
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    G, TA, TB, TC, TD, Qlo = G1(g)
    print('%.4f  %.5f  %.5f  %.5f  %.5f  %.5f  %.5f' % (g, G, TA, TB, TC, TD, Qlo))
# B1 zero
def B1v(g):
    A = mp.pi-g; return A*mp.cos(g)-2*mp.sin(g)
lo, hi = mp.mpf('0.8'), mp.mpf('0.9')
for _ in range(100):
    mid=(lo+hi)/2
    if B1v(mid)>0: lo=mid
    else: hi=mid
print('B1 zero = %.10f' % ((lo+hi)/2))
# Qlo zero
def Qlov(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    d2 = 1+3*sg*sg; z = cg*cg/d2
    return 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
lo, hi = mp.mpf('0.99'), mp.mpf('1.02')
for _ in range(100):
    mid=(lo+hi)/2
    if Qlov(mid)>0: hi=mid
    else: lo=mid
print('Qlo zero = %.10f' % ((lo+hi)/2))
