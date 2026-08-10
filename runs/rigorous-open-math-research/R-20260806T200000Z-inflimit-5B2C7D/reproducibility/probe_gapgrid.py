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
def Dbar(u): return mu2bar(u) - mu1bar(u)

def bisect(f, lo, hi, tol=mp.mpf('1e-30')):
    flo, fhi = f(lo), f(hi)
    assert (flo < 0 < fhi) or (fhi < 0 < flo), (lo, hi, flo, fhi)
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

def gap_R(u, R, full=False):
    """gap via half-string secular equations (branches valid when u*sqrt(R)>=2),
    or full-string transfer matrix otherwise."""
    if not full and u*mp.sqrt(R) >= 2:
        sR = mp.sqrt(R)
        m1b = mu1bar(u); m2b = mu2bar(u)
        f1 = lambda m: mp.cot(mp.sqrt(m)*u) - (1/sR)*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
        f2 = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
        m1 = bisect(f1, mp.mpf('1e-15'), m1b)
        m2 = bisect(f2, m1b*(1+mp.mpf('1e-15')), m2b)
        return m2 - m1
    # full string: M = P(kR,u) P(k1,1-2u) P(kR,u); eigenvalues: M[0][1]=0
    def sec(m):
        kR = mp.sqrt(m); k1 = mp.sqrt(m/R)
        cR, sR = mp.cos(kR*u), mp.sin(kR*u)
        c1, s1 = mp.cos(k1*(1-2*u)), mp.sin(k1*(1-2*u))
        # P(k,L) = [[cos kL, sin kL/k],[-k sin kL, cos kL]]
        # M = P1 P2 P1 (P1 = heavy block, P2 = light block)
        a,b,c,d = cR, sR/kR, -kR*sR, cR
        e,f,g,h = c1, s1/k1, -k1*s1, c1
        # P1 P2
        a2 = a*e + b*g; b2 = a*f + b*h; c2 = c*e + d*g; d2 = c*f + d*h
        # (P1P2) P1
        a3 = a2*a + b2*c; b3 = a2*b + b2*d
        return b3
    # find first two roots of sec(m)=0
    lam_hi = mp.mpf('2000')
    N = 20000
    roots = []
    prev = None
    for k in range(1, N+1):
        m = lam_hi*k/N
        v = sec(m)
        if prev is not None and prev != 0 and v != 0 and (v < 0) != (prev < 0):
            r = bisect(sec, lam_hi*(k-1)/N, m)
            roots.append(r)
            if len(roots) == 2: break
        prev = v
    if len(roots) < 2:
        return None
    return roots[1]-roots[0]

print("== gap - Dbar on a wide grid ==")
bad = 0
for u in ['0.02','0.05','0.1','0.2','0.3','0.4','0.48']:
    uu = mp.mpf(u)
    for R in ['2','5','10','100','1000','1e6']:
        RR = mp.mpf(R)
        full = (uu*mp.sqrt(RR) < 2)
        g = gap_R(uu, RR, full=full)
        if g is None:
            print("  u=%s R=%s: FAIL" % (u,R)); continue
        d = Dbar(uu)
        diff = g - d
        if diff < -mp.mpf('1e-6'):
            bad += 1
            print("  u=%s R=%s: gap=%s Dbar=%s diff=%s <0 !!" % (u, R, mp.nstr(g,7), mp.nstr(d,7), mp.nstr(diff,4)))
print("total violations:", bad)