import mpmath as mp
import bisect
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def Psi(x, m, q):
    return x/mp.tan(x) + q*x*mp.sin(x)*mp.cos(x)/W(x,m)

def region2_pairs(R, tau, n=2000):
    m = mp.sqrt(mp.mpf(R)); q = R-1
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    pairs = []
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            for k in range(len(vx)):
                t = vx[k]
                if t <= lo or t >= hi: continue
                if vy[-1] > vy[0]:
                    idx = bisect.bisect_left(vy, t)
                else:
                    rvy = [-v for v in vy]
                    idx = bisect.bisect_left(rvy, -t)
                for j in (idx-1, idx):
                    if j < 0 or j >= len(yl)-1: continue
                    ya, yb = yl[j], yl[j+1]
                    fa = rtau(ya,m,tau)-rtau(xl[k],m,tau)
                    fb = rtau(yb,m,tau)-rtau(xl[k],m,tau)
                    if fa == 0: y = ya
                    elif fb == 0: y = yb
                    elif fa*fb < 0:
                        y = mp.findroot(lambda yy: rtau(yy,m,tau)-rtau(xl[k],m,tau), (ya,yb), solver='bisect')
                    else: continue
                    x = xl[k]
                    if xmid < x < y < xmax and abs(rtau(y,m,tau)-rtau(x,m,tau)) < 1e-16:
                        if not any(abs(x-p[0])<1e-8 and abs(y-p[1])<1e-8 for p in pairs):
                            pairs.append((x,y))
                        break
    return pairs

print("=== check: r strictly decreasing on (xmid, pi/2] ? ===")
ok_all = True
for R in [1.05, 1.5, 4, 100, 1000]:
    m = mp.sqrt(mp.mpf(R))
    for tau in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('1.9')]:
        xmid = mp.pi/(1+tau)
        xs = [xmid + (mp.pi/2-xmid)*i/2000 for i in range(1,2000)]
        v = [float(rtau(x,m,tau)) for x in xs]
        dec = all(v[i] > v[i+1] for i in range(len(v)-1))
        if not dec:
            ok_all = False
            print(f"  FAIL R={R} tau={tau}")
print("all decreasing on (xmid, pi/2]:", ok_all)

print()
print("=== global min x+y over (R,tau) grid, tau in (1,2) ===")
gmin = mp.inf; gbest=None; nfound=0
for R in [2,3,4,6,10,20,50,100,200,400,1000,10000]:
    for ti in range(11, 20):
        tau = mp.mpf(ti)/10
        pairs = region2_pairs(R, tau)
        if pairs:
            nfound += 1
            mxy = min(x+y for x,y in pairs)
            if mxy < gmin:
                gmin = mxy
                gbest=(R, tau, [p for p in pairs if abs(p[0]+p[1]-mxy)<1e-9][0], len(pairs))
print("configs with pairs:", nfound)
print("global min x+y =", mp.nstr(gmin,15), "vs pi =", mp.nstr(mp.pi,15), " margin:", mp.nstr(mp.pi-gmin,12))
print("at R=%s tau=%s; pair=(%s,%s); n_pairs=%s" % (gbest[0], mp.nstr(gbest[1],6), mp.nstr(gbest[2][0],12), mp.nstr(gbest[2][1],12), gbest[3]))
