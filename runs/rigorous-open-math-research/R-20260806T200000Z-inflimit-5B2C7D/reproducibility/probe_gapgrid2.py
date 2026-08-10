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

def gap_half(u, R):
    sR = mp.sqrt(R)
    m1b = mu1bar(u); m2b = mu2bar(u)
    f1 = lambda m: mp.cot(mp.sqrt(m)*u) - (1/sR)*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    f2 = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    m1 = bisect(f1, mp.mpf('1e-15'), m1b)
    m2 = bisect(f2, m1b*(1+mp.mpf('1e-15')), m2b)
    return m2 - m1

def gap_full(u, R):
    def sec(m):
        kR = mp.sqrt(m); k1 = mp.sqrt(m/R)
        cR, sR = mp.cos(kR*u), mp.sin(kR*u)
        c1, s1 = mp.cos(k1*(1-2*u)), mp.sin(k1*(1-2*u))
        a,b,c,d = cR, sR/kR, -kR*sR, cR
        e,f,g,h = c1, s1/k1, -k1*s1, c1
        a2 = a*e + b*g; b2 = a*f + b*h; c2 = c*e + d*g; d2 = c*f + d*h
        a3 = a2*a + b2*c; b3 = a2*b + b2*d
        return b3
    lam_hi = mp.mpf('2.5')*max(mu2bar(u), mp.mpf('40'))  # adaptive
    N = 40000
    roots = []
    prev = None
    for k in range(1, N+1):
        m = lam_hi*k/N
        v = sec(m)
        if prev is not None and v != 0 and prev != 0 and (v < 0) != (prev < 0):
            r = bisect(sec, lam_hi*(k-1)/N, m)
            roots.append(r)
            if len(roots) == 2: break
        prev = v
    return (roots[1]-roots[0]) if len(roots)==2 else None

print("== mid-sliver: gap - Dbar for u*sqrt(R) >= 2 ==")
viol = 0
for u in ['0.05','0.06','0.07','0.08','0.09','0.1','0.12','0.15','0.2','0.3']:
    uu = mp.mpf(u)
    for R in ['100','1000','1e4','1e6']:
        RR = mp.mpf(R)
        if uu*mp.sqrt(RR) < 2: continue
        g = gap_half(uu, RR); d = Dbar(uu)
        if g - d < -mp.mpf('1e-8'):
            viol += 1
            print("  u=%s R=%s: gap-Dbar = %s <0 !!" % (u,R,mp.nstr(g-d,4)))
print("violations:", viol)

print()
print("== deep-sliver boundary u = 1/sqrt(R): gap vs Dbar (full matrix) ==")
for R in ['100','1000','1e4']:
    RR = mp.mpf(R)
    uu = 1/mp.sqrt(RR)
    g = gap_full(uu, RR)
    d = Dbar(uu)
    print("  R=%s u=%s: gap=%s Dbar=%s diff=%s" % (R, mp.nstr(uu,4), mp.nstr(g,7), mp.nstr(d,7), mp.nstr(g-d,4)))

print()
print("== B2 bound at u=1/sqrt(R) vs 24.95 ==")
for R in ['100','1000','1e4']:
    RR = mp.mpf(R)
    c = (RR-1)/(2*RR)
    b = 3*mp.pi**2*RR/((1+4*mp.pi**2*c)*(1+mp.pi**2*c))
    print("  R=%s: B2 bound = %s" % (R, mp.nstr(b,7)))