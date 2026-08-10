import numpy as np, time

def transfer_prop(jumps, vals, lam, x):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.eye(2)
    i = 0
    while i < len(xs)-1 and x > xs[i+1] + 1e-12:
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(lam*c)
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        i += 1
    c = vals[i]
    w = np.sqrt(lam*c)
    L = x - xs[i]
    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
    M = M @ T
    v = M @ np.array([0.0, 1.0])
    return v[0], v[1]

def eigs_exact(jumps, vals, k=6, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    npts = 30000
    s = np.linspace(1e-5, np.sqrt(lam_hi), npts)
    M00 = np.ones(len(s)); M01 = np.zeros(len(s)); M10 = np.zeros(len(s)); M11 = np.ones(len(s))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    d = M01
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(60):
                m = 0.5*(lo+hi)
                dm = transfer_prop(jumps, vals, m**2, 1.0)[0]
                if transfer_prop(jumps, vals, lo**2, 1.0)[0]*dm <= 0:
                    hi = m
                else:
                    lo = m
            roots.append(((lo+hi)/2)**2)
    return np.array(sorted(roots)[:k])

def cfg_from_x(xs, R):
    n = len(xs)
    ints = []
    j = 0
    while j+1 < n:
        ints.append((xs[j], xs[j+1]))
        j += 2
    if n % 2 == 1:
        ints.append((xs[n-1], 1-xs[n-1]))
    m = len(ints)
    for i in range(m-1, -1, -1):
        a, b = ints[i]
        if not (abs((1-b) - a) < 1e-12 and abs((1-a) - b) < 1e-12):
            ints.append((1-b, 1-a))
    ints.sort()
    jumps = []
    for a,b in ints: jumps += [a,b]
    vals = [1.0]
    for p in jumps:
        v = R if any(a < p + 1e-12 <= b for (a,b) in ints) else 1.0
        vals.append(v)
    return jumps, vals

def F_ratio(xs, R, n):
    jumps, vals = cfg_from_x(xs, R)
    lam = eigs_exact(jumps, vals, k=n+1)
    return lam[n]/lam[n-1]

def golden_1d(f, a, b, tol=1e-12, itmax=80):
    gr = (np.sqrt(5)-1)/2
    c = b - gr*(b-a); d = a + gr*(b-a)
    fc, fd = f(c), f(d)
    for _ in range(itmax):
        if fc > fd:
            a, c, fd = c, d, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, d, fc = d, c, fd
            d = a + gr*(b-a); fd = f(d)
        if b-a < tol: break
    return 0.5*(a+b)

def coord_ascent_golden(xs0, R, n, itmax=30):
    xs = list(xs0)
    for it in range(itmax):
        improved = False
        for k in range(n):
            lo = (xs[k-1]+0.001) if k > 0 else 0.001
            hi = (xs[k+1]-0.001) if k < n-1 else 0.499
            if hi <= lo: continue
            fk = lambda t: F_ratio(xs[:k]+[t]+xs[k+1:], R, n)
            # coarse scan to avoid local maxima issues
            tgrid = np.linspace(lo, hi, 24)
            vg = np.array([fk(t) for t in tgrid])
            i = np.argmax(vg)
            a = tgrid[max(0,i-1)]; b = tgrid[min(len(tgrid)-1,i+1)]
            tb = golden_1d(fk, a, b)
            if fk(tb) > fk(xs[k]) + 1e-13:
                xs[k] = tb; improved = True
        if not improved: break
    return xs, F_ratio(xs, R, n)

t0=time.time()
for R in [2.0, 4.0, 10.0, 100.0]:
    print(f"=== R={R} ===")
    for n in [1,2,3]:
        # starts from damped-iteration configs (scaled guesses)
        if n==1: x0=[0.38]
        elif n==2: x0=[0.25,0.375]
        else: x0=[0.18,0.28,0.40]
        xs, val = coord_ascent_golden(x0, R, n, itmax=20)
        print(f"  n={n}: M={val:.8f} at xs={np.round(xs,6)}  ({(time.time()-t0):.0f}s)")
