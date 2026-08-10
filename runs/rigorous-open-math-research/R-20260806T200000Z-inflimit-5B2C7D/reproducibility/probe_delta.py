import mpmath as mp
mp.mp.dps = 40

def a_of(u):
    f = lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    lo = mp.pi/2 + mp.mpf('1e-25'); hi = mp.pi - mp.mpf('1e-25')
    al, ah = lo, hi
    for k in range(1, 100000):
        x = lo + (hi-lo)*k/100000
        if f(x) > 0:
            ah = x; break
        al = x
    return mp.findroot(f, (al, ah))

def mu1bar(u): return mp.pi**2/(4*u**2)
def mu2bar(u):
    a = a_of(u); return (a/u)**2

def bisect(f, lo, hi, tol=mp.mpf('1e-30')):
    flo, fhi = f(lo), f(hi)
    assert (flo < 0 < fhi) or (fhi < 0 < flo)
    for _ in range(500):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0: return mid
        if (fm < 0) == (flo < 0):
            lo = mid; flo = fm
        else:
            hi = mid; fhi = fm
        if hi - lo < tol: return (lo+hi)/2
    return (lo+hi)/2

Cbar = mp.mpf('0.4434')  # sup (tan z - z)/z^3 on [0, pi/4], upper bound

print("u, R, |psi-psibar| actual, delta_bound, E_bound, gap-Dbar actual, Dbar(u)-E")
for u in ['0.04','0.06','0.1','0.2','0.3']:
    uu = mp.mpf(u)
    for R in ['750','1000','1e4','1e6']:
        RR = mp.mpf(R)
        if uu*mp.sqrt(RR) < 2: continue
        sR = mp.sqrt(RR)
        # psibar
        f = lambda p: mp.tan(p) - (mp.pi-p)*(mp.mpf(1)/2-uu)/uu
        psibar = bisect(f, mp.mpf('1e-9'), mp.pi/2 - mp.mpf('1e-9'))
        thetabar = mp.pi - psibar
        # actual psi: solve tan(psi) = sR*tan((pi-psi)*(1/2-u)/(u sR))
        g = lambda p: mp.tan(p) - sR*mp.tan((mp.pi-p)*(mp.mpf(1)/2-uu)/(uu*sR))
        psi = bisect(g, mp.mpf('1e-9'), mp.pi/2 - mp.mpf('1e-9'))
        delta_act = abs(psi - psibar)
        # analytic bound: delta <= Cbar * thetabar^3*(1/2-u)^3/(u^3 R) / (1+thetabar^2*(1/2-u)^2/u^2) / (1-q)
        num = Cbar*thetabar**3*(mp.mpf(1)/2-uu)**3/(uu**3*RR)
        den = 1 + thetabar**2*(mp.mpf(1)/2-uu)**2/uu**2
        q = (mp.mpf(1)/2-uu)/(uu*sR) * 2  # crude |F'| <= (1/2-u)/u * sec^2 z/(1+R tan^2 z) <= (1/2-u)/u * 2/(R z^2)... use crude
        # better q bound: (1/2-u)/u * (1/R + 4 u^2/(pi^2 (1/2-u)^2))
        q2 = (mp.mpf(1)/2-uu)/uu*(1/RR + 4*uu**2/(mp.pi**2*(mp.mpf(1)/2-uu)**2))
        delta_b = num/den/(1-q2)
        E = 2*thetabar*delta_b/uu**2
        # actual gap - Dbar
        m1b = mu1bar(uu); m2b = mu2bar(uu)
        f1 = lambda m: mp.cot(mp.sqrt(m)*uu) - (1/sR)*mp.tan(mp.sqrt(m/RR)*(mp.mpf(1)/2-uu))
        f2 = lambda m: mp.tan(mp.sqrt(m)*uu) + sR*mp.tan(mp.sqrt(m/RR)*(mp.mpf(1)/2-uu))
        m1 = bisect(f1, mp.mpf('1e-15'), m1b)
        m2 = bisect(f2, m1b*(1+mp.mpf('1e-15')), m2b)
        gap = m2-m1
        D = m2b - m1b
        print("u=%s R=%s: |psi-psibar|=%.3e delta_b=%.3e E_b=%.4f gap-Dbar=%.4f D-E=%.3f  q2=%.3f" % (
            u, R, delta_act, delta_b, E, gap-D, D-E, q2))