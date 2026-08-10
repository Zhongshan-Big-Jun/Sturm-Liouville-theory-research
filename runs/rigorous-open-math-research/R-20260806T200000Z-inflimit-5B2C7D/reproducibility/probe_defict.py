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
    assert flo < 0 < fhi or fhi < 0 < flo
    for _ in range(400):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0: return mid
        if (fm < 0) == (flo < 0):
            lo = mid; flo = fm
        else:
            hi = mid; fhi = fm
        if hi - lo < tol: return (lo+hi)/2
    return (lo+hi)/2

def mu1_R(u, R):
    sR = mp.sqrt(R)
    f = lambda m: mp.cot(mp.sqrt(m)*u) - (1/sR)*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    return bisect(f, mp.mpf('1e-12'), mu1bar(u))

def mu2_R(u, R):
    sR = mp.sqrt(R)
    f = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    return bisect(f, mu1bar(u)*(1+mp.mpf('1e-15')), mu2bar(u))

print("== monotonicity of gap in R, restricted to u*sqrt(R) >= 2 ==")
for u in ['0.1','0.2','0.3','0.4','0.48']:
    uu = mp.mpf(u)
    prev = None
    row = []
    for R in ['10','100','1000','1e4','1e6']:
        RR = mp.mpf(R)
        if uu*mp.sqrt(RR) < 2: continue
        g = mu2_R(uu, RR) - mu1_R(uu, RR)
        row.append((R, mp.nstr(g,8)))
        if prev is not None and g > prev + mp.mpf('1e-8'):
            print("  u=%s: NOT decreasing at R=%s" % (u, R))
        prev = g
    print("  u=%s: %s  Dbar=%s" % (u, " ".join("%s:%s" % (r,g) for r,g in row), mp.nstr(Dbar(uu),8)))

print()
print("== deficit Dbar(u) - gap(R,u), u*sqrt(R)>=2 ==")
for R in ['1600','1e4','1e6']:
    RR = mp.mpf(R)
    print(" R=%s:" % R)
    for u in ['0.05','0.07','0.1','0.15','0.2','0.25','0.3']:
        uu = mp.mpf(u)
        if uu*mp.sqrt(RR) < 2: continue
        g = mu2_R(uu,RR)-mu1_R(uu,RR)
        d = Dbar(uu) - g
        print("   u=%s: gap=%s Dbar=%s deficit=%s" % (u, mp.nstr(g,8), mp.nstr(Dbar(uu),8), mp.nstr(d,6)))