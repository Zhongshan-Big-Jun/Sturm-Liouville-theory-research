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
    s = np.linspace(1e-6, np.sqrt(lam_hi), 50000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(5):
            sg = np.linspace(slo, shi, 800)
            dg = _det_scan(jumps, vals, sg)
            jj = np.nonzero(np.signbit(dg[1:]) != np.signbit(dg[:-1]))[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def alt(n, R, wr, start):
    """alternating symmetric config; start = 'a' or 'A'; width ratio wr = (start-width)/(other-width)"""
    t = 1.0/((n+1)*(wr if start=='a' else 1.0) + n*(1.0 if start=='a' else wr))
    w1 = wr*t; w2 = t
    if start == 'A': w1, w2 = t, wr*t
    jumps = []; x = 0.0
    while True:
        x += w1
        if x < 1.0: jumps.append(x)
        x += w2
        if x < 1.0: jumps.append(x)
        if x >= 1.0: break
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = []
    for i in range(len(pts)-1):
        base = 1.0 if (start=='a') == (i%2==0) else 4.0
        vals.append(base)
    return jumps, vals

print("=== inf direction: alternating symmetric family, R=4 ===")
print("--- n=1 (min lambda2/l1): known Keller min = 2.40922 at [0.2512,0.7488] (A,a,A pattern, A-width = sqrt(R)*a-width? check) ---")
for start in ['a', 'A']:
    best = (1e9, None)
    for wr in np.linspace(0.2, 6.0, 117):
        jumps, vals = alt(1, 4.0, wr, start)
        lam = eigs_fast(jumps, vals, k=2)
        r = lam[1]/lam[0]
        if r < best[0]: best = (r, wr, jumps)
    print(f"start={start}: min={best[0]:.6f} at wr={best[1]:.3f}  jumps={np.round(best[2],4)}")
print()
print("--- n=2 (min lambda3/l2): summary claims 1.424 at [1/7,3/7,4/7,6/7] (a,A,a,A,a, A-wider) ---")
for start in ['a', 'A']:
    best = (1e9, None)
    for wr in np.linspace(0.2, 6.0, 117):
        jumps, vals = alt(2, 4.0, wr, start)
        lam = eigs_fast(jumps, vals, k=3)
        r = lam[2]/lam[1]
        if r < best[0]: best = (r, wr, jumps)
    print(f"start={start}: min={best[0]:.6f} at wr={best[1]:.3f}  jumps={np.round(best[2],4)}")
print()
print("--- n=3,4 (min lambda_{n+1}/lambda_n) ---")
for n in [3,4]:
    for start in ['a', 'A']:
        best = (1e9, None)
        for wr in np.linspace(0.2, 6.0, 117):
            jumps, vals = alt(n, 4.0, wr, start)
            lam = eigs_fast(jumps, vals, k=n+1)
            r = lam[n]/lam[n-1]
            if r < best[0]: best = (r, wr, jumps)
        print(f"n={n} start={start}: min={best[0]:.6f} at wr={best[1]:.3f}")
