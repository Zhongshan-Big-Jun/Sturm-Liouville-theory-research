import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def dlogr(x, m, tau, h=mp.mpf('1e-12')):
    # derivative of log r via symmetric difference (for monotonicity detection)
    return (mp.log(rtau(x+h,m,tau)) - mp.log(rtau(x-h,m,tau)))/(2*h)

def region2_pairs_refined(R, tau, n=3000):
    """Find all E=0 pairs (x<y) in region II, refined with mpmath; return list of (x,y) mpf."""
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    pairs = []
    def refine(x0, y0):
        # solve r(y)=r(x0) near y0
        f = lambda y: rtau(y,m,tau) - rtau(x0,m,tau)
        y = mp.findroot(f, y0, solver='muller')
        return y
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            inc = vy[-1] > vy[0]
            for k in range(len(vx)):
                t = vx[k]
                if t < lo or t > hi: continue
                l,h = 0, len(yl)-1
                f = (lambda idx: vy[idx]-t) if inc else (lambda idx: t-vy[idx])
                if f(0)*f(len(yl)-1) > 0: continue
                l,h = 0, len(yl)-1
                for _ in range(40):
                    mid = (l+h)//2
                    if f(mid)<=0: h=mid
                    else: l=mid+1
                # refine around l
                for idx in [l, l+1, l-1]:
                    if 0<=idx<len(yl) and abs(vx[k]-vy[idx]) < 5e-6:
                        try:
                            y = refine(xl[k], yl[idx])
                        except Exception:
                            continue
                        x = xl[k]
                        if xmid < x < y < xmax and abs(rtau(y,m,tau)-rtau(x,m,tau)) < 1e-20:
                            # dedupe
                            if not any(abs(x-p[0])<1e-9 and abs(y-p[1])<1e-9 for p in pairs):
                                pairs.append((x,y))
                        break
    return pairs

# verify handoff case R=100, tau=1.22
pairs = region2_pairs_refined(100, mp.mpf('1.22'))
print("R=100 tau=1.22: num pairs:", len(pairs))
if pairs:
    s = [x+y for x,y in pairs]
    mxy = min(s)
    b = pairs[s.index(mxy)]
    print("min x+y =", mp.nstr(mxy,15), " pi =", mp.nstr(mp.pi,15))
    print("pair:", mp.nstr(b[0],15), mp.nstr(b[1],15))

print()
print("=== min x+y over (R,tau) grid with tau in (1,2) ===")
gmin = mp.inf; gbest=None; nfound=0
for R in [1.05,1.1,1.2,1.5,2,3,4,6,10,20,50,100,200,400,1000,10000]:
    for ti in range(11, 20):
        tau = mp.mpf(ti)/10
        pairs = region2_pairs_refined(R, tau)
        if pairs:
            nfound += 1
            mxy = min(x+y for x,y in pairs)
            if mxy < gmin:
                gmin = mxy; gbest=(R, tau, [p for p in pairs if abs(p[0]+p[1]-mxy)<1e-9][0])
print("configs with pairs:", nfound)
print("global min x+y =", mp.nstr(gmin,15), "vs pi =", mp.nstr(mp.pi,15))
print("at R=%s tau=%s pair=%s %s" % (gbest[0], mp.nstr(gbest[1],6), mp.nstr(gbest[2][0],12), mp.nstr(gbest[2][1],12)))
print("margin to pi:", mp.nstr(mp.pi-gmin,12))
