import mpmath as mp
mp.mp.dps = 40
Cbar = mp.mpf('0.45'); q0 = mp.mpf('0.20'); R0 = mp.mpf('1500')

def a_of(u):
    f = lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    lo = mp.pi/2 + mp.mpf('1e-30'); hi = mp.pi - mp.mpf('1e-30')
    al, ah = lo, hi
    for k in range(1, 30000):
        x = lo + (hi-lo)*k/30000
        if f(x) > 0:
            ah = x; break
        al = x
    return mp.findroot(f, (al, ah))
def mu1bar(u): return mp.pi**2/(4*u**2)
def mu2bar(u):
    a = a_of(u); return (a/u)**2
def Dbar(u): return mu2bar(u) - mu1bar(u)
def bisect(f, lo, hi, tol=mp.mpf('1e-28')):
    flo, fhi = f(lo), f(hi)
    assert (flo < 0 < fhi) or (fhi < 0 < flo)
    for _ in range(300):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0: return mid
        if (fm < 0) == (flo < 0):
            lo = mid; flo = fm
        else:
            hi = mid; fhi = fm
        if hi - lo < tol: return (lo+hi)/2
    return (lo+hi)/2
def gap_half(u, R):
    sR = mp.sqrt(R)
    m1b = mu1bar(u); m2b = mu2bar(u)
    f1 = lambda m: mp.cot(mp.sqrt(m)*u) - (1/sR)*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    f2 = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    m1 = bisect(f1, mp.mpf('1e-15'), m1b)
    m2 = bisect(f2, m1b*(1+mp.mpf('1e-15')), m2b)
    return m2 - m1
def E_bound(u, R):
    a = a_of(u); th = a
    delta = Cbar*th**3*(mp.mpf(1)/2-u)**3/(u**3*R*(1+th**2*(mp.mpf(1)/2-u)**2/u**2)*(1-q0))
    return 2*th*delta/u**2

print("u, gap_exact, Dbar(u), Dbar-E_bound, slack (gap >= Dbar-E ?)")
bad = 0
for u in ['0.052','0.06','0.08','0.1','0.2','0.3','0.4','0.475']:
    uu = mp.mpf(u)
    g = gap_half(uu, R0)
    d = Dbar(uu)
    E = E_bound(uu, R0)
    ok = g >= d - E
    if not ok: bad += 1
    print("%s: gap=%.4f Dbar=%.4f D-E=%.4f ok=%s" % (u, g, d, d-E, ok))
print("violations:", bad)
print()
print("Reference values:")
print("  u*     =", mp.nstr(mp.mpf('0.3299225081200665495928080550119348196095'), 30))
print("  a*     =", mp.nstr(mp.mpf('2.276513239026433075016554939167376365'), 30))
print("  Dbar*  =", mp.nstr(mp.mpf('24.943866138432476902584342900'), 30))
print("  3pi^2  =", mp.nstr(3*mp.pi**2, 30))
print("  margin =", mp.nstr(3*mp.pi**2 - mp.mpf('24.943866138432476902584342900'), 30))
print("  Dbar(0.1) =", mp.nstr(Dbar(mp.mpf('0.1')), 20))
print("  Dbar(0.475) =", mp.nstr(Dbar(mp.mpf('0.475')), 20))
print("  Dbar(0.052) =", mp.nstr(Dbar(mp.mpf('0.052')), 20))