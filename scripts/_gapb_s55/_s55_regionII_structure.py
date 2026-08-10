import mpmath as mp
mp.mp.dps = 30

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def rtau_num(x, m, tau):
    return float(rtau(x,m,tau))

# Structure of r_tau on region II for R=100, tau=1.22
R = 100.0; m = mp.sqrt(mp.mpf(R)); tau = mp.mpf('1.22')
xmid = mp.pi/(1+tau); xmax = mp.pi/tau
print("R=100, tau=1.22: xmid=", mp.nstr(xmid,6), "pi/tau=", mp.nstr(xmax,6))

xs = [xmid + (xmax-xmid)*i/4000 for i in range(1,4000)]
vals = [rtau_num(x,m,tau) for x in xs]
# critical points
crit = []
for i in range(1,len(xs)-1):
    if (vals[i]-vals[i-1])*(vals[i+1]-vals[i]) < 0:
        crit.append(xs[i])
print("critical points in region II:", [round(c,5) for c in crit])

# find pairs: level sets. use segments between critical points (monotone pieces)
import bisect
segs_idx = [0] + [int(xs.index(c)) for c in crit] + [len(xs)-1]
# dedupe segments
segs = []
for i in range(len(segs_idx)-1):
    a0,a1 = segs_idx[i], segs_idx[i+1]
    if a1>a0: segs.append((a0,a1))

pairs = []
for si in range(len(segs)):
    for sj in range(si, len(segs)):
        i0,i1 = segs[si]; j0,j1 = segs[sj]
        if si==sj:
            # within same segment (monotone): only diagonal
            continue
        xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
        vx = [rtau_num(x,m,tau) for x in xl]; vy = [rtau_num(y,m,tau) for y in yl]
        lo_v, hi_v = min(vy), max(vy)
        for k in range(len(xl)):
            t = vx[k]
            if t < lo_v - 1e-12 or t > hi_v + 1e-12: continue
            # bisection on monotone y-segment
            l,h = 0, len(yl)-1
            if vy[0] < vy[-1]:
                f = lambda idx: vy[idx]-t
            else:
                f = lambda idx: t-vy[idx]
            if f(0)*f(len(yl)-1) > 0: continue
            l,h = 0, len(yl)-1
            for _ in range(60):
                mid = (l+h)//2
                if f(mid)<=0: h=mid
                else: l=mid+1
            for idx in [l,l+1,l-1]:
                if 0<=idx<len(yl) and abs(vx[k]-vy[idx])<1e-9:
                    x,y = xl[k], yl[idx]
                    if x < y-1e-9:
                        pairs.append((x,y))
                        break

print("num pairs found (approx grid):", len(pairs))
if pairs:
    mxy = min(x+y for x,y in pairs)
    print("min x+y =", round(mxy,6), "vs pi =", round(float(mp.pi),6))
    # refine best pair
    bx,by = min(pairs, key=lambda p: p[0]+p[1])
    print("best pair:", round(bx,6), round(by,6), "sum:", round(bx+by,8))
