import numpy as np

def _det_scan(jumps, vals, s_grid):
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0)); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2; n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2; n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigs_fast(jumps, vals, k=8):
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    s = np.linspace(1e-6, np.sqrt(lam_hi), 30000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(slo, shi, 400)
            dg = _det_scan(jumps, vals, sg)
            jj = np.nonzero(np.signbit(dg[1:]) != np.signbit(dg[:-1]))[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

# ---- Test 1: pointwise statement lambda3/lambda2 <= lambda2/lambda1 ? ----
# rho = R on [c-eps, c+eps] around x=1/4 (localized bump), a elsewhere, R=4
print("=== Test 1: localized bump at x=1/4, R=4: lambda3/lambda2 vs lambda2/lambda1 ===")
R = 4.0
for eps in [0.005, 0.01, 0.02, 0.04, 0.08, 0.12]:
    jumps = sorted([max(0.0, 0.25-eps), min(1.0, 0.25+eps)])
    # values: a=1 outside bump, R inside
    pts = [0.0]+jumps+[1.0]
    vals = []
    for i in range(len(pts)-1):
        mid = 0.5*(pts[i]+pts[i+1])
        vals.append(R if abs(mid-0.25) < eps else 1.0)
    lam = eigs_fast(jumps, vals, k=4)
    print(f"eps={eps:.3f}: lambda2/l1={lam[1]/lam[0]:.6f}  lambda3/l2={lam[2]/lam[1]:.6f}  ratio3>2: {lam[2]/lam[1] > lam[1]/lam[0]}")
print()

# ---- Test 2: adversarial random search, bang-bang with many jumps, n=2 and n=3, R=4 ----
print("=== Test 2: random bang-bang search for lambda3/lambda2 and lambda4/lambda3 (R=4) ===")
rng = np.random.default_rng(20260801)
best3 = (0.0, None); best4 = (0.0, None)
worst3 = (1e9, None)
for trial in range(4000):
    nj = rng.integers(2, 12)
    jumps = np.sort(rng.uniform(0.01, 0.99, nj))
    # random values: alternate or random; try both patterns
    for pattern in range(2):
        vals = []
        pts = [0.0]+list(jumps)+[1.0]
        if pattern == 0:
            start = rng.choice([1.0, R])
            vals = [start if i%2==0 else R/start for i in range(len(pts)-1)]
        else:
            vals = rng.choice([1.0, R], len(pts)-1)
        lam = eigs_fast(list(jumps), vals, k=5)
        r3 = lam[2]/lam[1]; r4 = lam[3]/lam[2]
        if r3 > best3[0]: best3 = (r3, (jumps, vals))
        if r4 > best4[0]: best4 = (r4, (jumps, vals))
        if r3 < worst3[0]: worst3 = (r3, (jumps, vals))
print(f"best lambda3/lambda2 = {best3[0]:.6f} (conjectured extremizer gives 4.2847)")
print(f"best lambda4/lambda3 = {best4[0]:.6f}")
print(f"worst lambda3/lambda2 = {worst3[0]:.6f}")

# ---- Test 3: the n=1 extremizer config: check lambda3/l2, lambda4/l3, lambda5/l4 (periodic double well) ----
print()
print("=== Test 3: MW extremizer c=0.4 R=4: all adjacent ratios ===")
jumps = [0.4, 0.6]; vals = [1.0, 4.0, 1.0]
lam = eigs_fast(jumps, vals, k=7)
for n in range(1, 6):
    print(f"n={n}: lambda_{n+1}/lambda_{n} = {lam[n]/lam[n-1]:.6f}")
print("nu(4) should be 7.4815 for n=1")
