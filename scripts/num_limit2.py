import numpy as np

def _det_scan(jumps, vals, s_grid):
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigs_fast(jumps, vals, k=8):
    xs = [0.0] + list(jumps) + [1.0]
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
            sg_signs = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nonzero(sg_signs)[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def nperiodic_cell(n, cell_jumps, cell_vals):
    # replicate cell n times on [0,1]: cell on [0,1/n] scaled
    jumps = []; vals = []
    for i in range(n):
        for j in range(len(cell_jumps)):
            jumps.append((i + cell_jumps[j])/n)
        # interval values: between consecutive cell jumps, plus edges
        pts = [0.0] + list(cell_jumps) + [1.0]
        iv = [cell_vals[j] for j in range(len(pts)-1)]
        for j in range(len(iv)):
            vals.append(iv[j])
    # drop duplicate boundary jumps at i/n for i=1..n-1 (same value on both sides -> keep as jump only if values differ)
    jumps = [j for j in jumps if 0.0 < j < 1.0]
    jumps = sorted(jumps)
    return jumps, vals

# cell a(2/3)|A(1/3): jumps [2/3], vals [1,4]
cell_jumps = [2.0/3.0]
cell_vals = [1.0, 4.0]
print("=== n-periodic cell a(2/3)|A(1/3): lam_{n+1}/lam_n (R=4) ===")
for n in [5, 10, 20, 30, 50]:
    jumps, vals = nperiodic_cell(n, cell_jumps, cell_vals)
    lam = eigs_fast(jumps, vals, k=n+3)
    print(f"n={n}: ratio={lam[n]/lam[n-1]:.8f}")

# also conjectured config c_n vs n-periodic cell: compare
print()
print("=== conjectured config c_n (R=4) vs periodic-cell ratio ===")
for n in [5, 10, 20]:
    sR = 2.0
    t = 1.0/((n+1)*sR + n)
    jumps = []
    x = 0.0
    while True:
        x += 2*t
        if x < 1.0: jumps.append(x)
        x += t
        if x < 1.0: jumps.append(x)
        if x >= 1.0: break
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = [4.0 if i%2==1 else 1.0 for i in range(len(pts)-1)]
    lam = eigs_fast(jumps, vals, k=n+3)
    print(f"n={n}: conj ratio={lam[n]/lam[n-1]:.8f}")

# limit estimate: c_inf via n=50 periodic cell
jumps, vals = nperiodic_cell(50, cell_jumps, cell_vals)
lam = eigs_fast(jumps, vals, k=53)
print(f"\nlimit estimate (n=50 periodic cell): {lam[50]/lam[49]:.8f}")
