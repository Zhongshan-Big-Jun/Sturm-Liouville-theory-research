import numpy as np

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

def nelder_mead(f, x0, steps, itmax=400, tol=1e-12):
    n = len(x0)
    pts = [np.array(x0, float)]
    for i in range(n):
        x = np.array(x0, float); x[i] += steps[i]; pts.append(x)
    vals = [f(p) for p in pts]
    for it in range(itmax):
        order = np.argsort(vals)
        pts = [pts[i] for i in order]; vals = [vals[i] for i in order]
        if vals[-1] - vals[0] < tol:
            break
        c = np.mean(pts[:-1], axis=0)
        r = 2*c - pts[-1]
        r = np.sort(np.clip(r, 0.005, 0.495))
        vr = f(r)
        if vals[0] <= vr < vals[-2]:
            pts[-1], vals[-1] = r, vr
            continue
        if vr > vals[-2]:
            e = c + 2*(r - c)
            e = np.sort(np.clip(e, 0.005, 0.495))
            ve = f(e)
            if ve > vr:
                pts[-1], vals[-1] = e, ve
            else:
                pts[-1], vals[-1] = r, vr
            continue
        # shrink
        ok = False
        for i in range(1, n+1):
            cand = pts[0] + 0.5*(pts[i] - pts[0])
            cand = np.sort(np.clip(cand, 0.005, 0.495))
            vc = f(cand)
            if vc > vals[i] or True:
                pts[i], vals[i] = cand, vc
                ok = True
        if not ok:
            break
    order = np.argsort(vals)
    return pts[order[0]], vals[order[0]]

import time
for R in [2.0, 4.0, 10.0, 100.0]:
    print(f"=== R={R} ===")
    for n in [1,2,3]:
        if n==1: x0=[0.4]
        elif n==2: x0=[0.25,0.38]
        else: x0=[0.18,0.28,0.40]
        steps = [0.02]*n
        t0=time.time()
        xs, val = nelder_mead(lambda x: F_ratio(x, R, n), x0, steps, itmax=300)
        print(f"  n={n}: M={val:.8f} at xs={np.round(xs,6)} ({(time.time()-t0):.0f}s)")
