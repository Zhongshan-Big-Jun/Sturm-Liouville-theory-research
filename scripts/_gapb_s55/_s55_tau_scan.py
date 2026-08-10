import mpmath as mp
mp.mp.dps = 30

def alpha(x, m):
    return mp.atan2(mp.sin(x)/m, mp.cos(x))

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def y_end(s, a, b, m):
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    sya = mp.sin(A)/m; dya = mp.cos(A)
    c, sn = mp.cos(psi), mp.sin(psi)
    syb = c*sya + sn*dya
    dyb = -sn*sya + c*dya
    return mp.cos(B)*(m*syb) + mp.sin(B)*dyb

def solve_modes(a, b, m, kmax=2):
    roots = []
    s = mp.mpf('0.01'); ds = mp.mpf('0.02')
    prev = y_end(s, a, b, m)
    while len(roots) < kmax and s < 200:
        s2 = s + ds
        v2 = y_end(s2, a, b, m)
        if prev == 0 or v2*prev < 0:
            lo, hi = s, s2; flo = prev
            for _ in range(300):
                mid = (lo+hi)/2
                fm = y_end(mid, a, b, m)
                if fm*flo <= 0: hi = mid
                else: lo, flo = mid, fm
            roots.append((lo+hi)/2)
            if len(roots) >= kmax: break
        s, prev = s2, v2
    return roots

print("=== tau at symmetric well good roots across R ===")
print("(symmetric well v* approx from session 13; solve exact modes at a=v*, b=1-v*)")
for R, v in [(1.05, 0.418),(1.1, 0.41813),(1.2, 0.414),(1.3,0.411),(1.5,0.409),(2,0.40),(3,0.39),(4,0.38259826),(10,0.361315),(100,0.33474),(400,0.33135),(1000,0.331),(1e4,0.331),(1e6,0.331)]:
    m = mp.sqrt(mp.mpf(R))
    a = mp.mpf(v); b = 1-a
    roots = solve_modes(a, b, m, kmax=2)
    if len(roots) < 2:
        print(f"R={R}: solve failed"); continue
    s1, s2 = roots
    tau = s2/s1
    A = m*s1*a
    print(f"R={R}: tau={mp.nstr(tau,10)}, s1={mp.nstr(s1,10)}, A={mp.nstr(A,10)}")

print("\n=== region II E=0 pairs for tau values incl > 2 ===")
def region2_pairs(R, tau, n=2000):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau)
    xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    # find all pairs (x<y) with r(x)=r(y) to high precision: scan level sets
    vals = [rtau(x, m, tau) for x in xs]
    # group by near-equal values
    pairs = []
    for i in range(len(xs)):
        for j in range(i+1, len(xs)):
            if abs(vals[i]-vals[j]) < 1e-9:
                pairs.append((xs[i], xs[j], vals[i]))
    return pairs

for R in [4, 100]:
    for tau in [mp.mpf('1.5'), mp.mpf('1.8'), mp.mpf('2.0'), mp.mpf('2.5'), mp.mpf('3.0')]:
        m = mp.sqrt(mp.mpf(R))
        xmid = mp.pi/(1+tau); xmax = mp.pi/tau
        # first check monotonic structure via critical points
        xs = [xmid + (xmax-xmid)*i/3000 for i in range(1,3000)]
        vals = [rtau(x,m,tau) for x in xs]
        crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
        # detect pairs: for each x, find y>x with same value via bisection on segments
        npairs = 0
        minxy = mp.inf
        # split into monotone segments
        segs = []
        start = 0
        for c in crit:
            segs.append((start, c+1)); start = c+1
        segs.append((start, len(xs)-1))
        for si in range(len(segs)):
            for sj in range(si+1, len(segs)):
                i0,i1 = segs[si]; j0,j1 = segs[sj]
                # for x in segment si (decreasing or increasing?), match level with y in sj
                xlist = xs[i0:i1+1]
                ylist = xs[j0:j1+1]
                vx = [rtau(x,m,tau) for x in xlist]
                vy = [rtau(y,m,tau) for y in ylist]
                # levels must overlap
                for k in range(len(xlist)):
                    lo, hi = 0, len(ylist)-1
                    # binary search assuming monotone y-segment
                    dy = vy[hi]-vy[lo]
                    target = vx[k]
                    # find via bisection on monotone segment
                    if (target-vy[0])*(target-vy[-1]) > 0: continue
                    l, h = 0, len(ylist)-1
                    for _ in range(80):
                        mid = (l+h)//2
                        if (vy[mid]-target)*(vy[0]-target) <= 0: h = mid
                        else: l = mid+1
                    # check
                    for idx in [l, l+1, l-1]:
                        if 0<=idx<len(ylist) and abs(vx[k]-vy[idx])<1e-10:
                            x,y = xlist[k], ylist[idx]
                            if x < y:
                                npairs += 1
                                if x+y < minxy: minxy = x+y
        print(f"R={R}, tau={mp.nstr(tau,4)}: regionII pairs~{npairs}, min x+y = {mp.nstr(minxy,8)} vs pi={mp.nstr(mp.pi,8)}, xmid={mp.nstr(xmid,6)}, pi/tau={mp.nstr(xmax,6)}")
