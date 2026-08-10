import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
def parts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    c12 = cg*abs(B2) if B1 >= 0 else cg*abs(M)
    t = mp.atan(2*mp.tan(g)); st, ct = mp.sin(t), mp.cos(t)
    D = mp.sqrt(1+3*sg*sg)
    z_lo = cg*cg/(D*D)
    Qlo = 4*A*A*z_lo*z_lo - A*B7*z_lo + 6*cg*cg*sg*sg
    TA = c12*A*A*cg*st*st*ct*ct
    TB = 2*A**3*sg*sg*t*ct**5
    TC = G5*A*sg*t*st*ct*cg*cg
    TD = t*t*cg*sg*sg*Qlo
    return dict(TA=TA, TB=TB, TC=TC, TD=TD, G5=G5, c12=c12, t=t)
N = 300
names = ['TA','TB','TC','TD']
for name in names:
    vals = [parts(glo + mp.mpf(i)*(ghi-glo)/N)[name] for i in range(N+1)]
    print('%s: min %.5f max %.5f' % (name, min(vals), max(vals)))
print()
# monotonicity via derivative
h = mp.mpf('1e-8')
for name in names:
    d = [ (parts(g+h)[name]-parts(g-h)[name])/(2*h) for g in [glo + mp.mpf(i)*(ghi-glo)/N for i in range(1,N)] ]
    print('%s derivative: min %.4f max %.4f' % (name, min(d), max(d)))
# B1 zero location
def B1v(g):
    A = mp.pi-g; return A*mp.cos(g)-2*mp.sin(g)
lo, hi = mp.mpf('0.8'), mp.mpf('0.9')
for _ in range(80):
    mid = (lo+hi)/2
    if B1v(mid) > 0: lo = mid
    else: hi = mid
print('B1 zero ~ %.8f' % ((lo+hi)/2))
