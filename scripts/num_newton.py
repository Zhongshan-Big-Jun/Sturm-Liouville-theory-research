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

def eigs_exact(jumps, vals, k=8, lam_hi=None):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    if lam_hi is None:
        lam_hi = (A/a)*((k+1)**2)*(np.pi**2)*4 + 1.0
    npts = 60000
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
            for _ in range(70):
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

jumps, vals = cfg_from_x([0.39909], 4.0)
print("n=1 jumps:", jumps, "vals:", vals)
lam = eigs_exact(jumps, vals, k=3)
print("lam:", np.round(lam,6), "ratio:", lam[1]/lam[0])

def residual(xs, R, n):
    jumps, vals = cfg_from_x(xs, R)
    lam = eigs_exact(jumps, vals, k=n+1)
    g = np.zeros(len(xs))
    for j, xj in enumerate(xs):
        y_n = transfer_prop(jumps, vals, lam[n-1], xj)[0]
        y_np = transfer_prop(jumps, vals, lam[n], xj)[0]
        g[j] = y_n**2 - y_np**2
    return g, lam

def newton(R, n, xs0, itmax=25, damp=0.7):
    xs = np.array(xs0, float)
    for it in range(itmax):
        g, lam = residual(xs, R, n)
        if np.max(np.abs(g)) < 1e-11: break
        J = np.zeros((n,n))
        for j in range(n):
            for k in range(n):
                xp = xs.copy(); xp[k] += 1e-6
                xm = xs.copy(); xm[k] -= 1e-6
                gp, _ = residual(xp, R, n)
                gm, _ = residual(xm, R, n)
                J[j,k] = (gp[j]-gm[j])/(2e-6)
        step = np.linalg.solve(J, g)
        xs = xs - damp*step
        xs = np.sort(np.clip(xs, 0.001, 0.499))
    g, lam = residual(xs, R, n)
    return xs, g, lam

R=4.0
for n in [1,2,3,4]:
    if n==1: xs0=[0.4]
    elif n==2: xs0=[0.25,0.375]
    elif n==3: xs0=[0.18,0.27,0.40]
    else: xs0=[0.14,0.21,0.30,0.40]
    xs, g, lam = newton(R, n, xs0)
    print(f"n={n}: xs={np.round(xs,9)} |g|max={np.max(np.abs(g)):.2e} ratio={lam[n]/lam[n-1]:.10f}")
