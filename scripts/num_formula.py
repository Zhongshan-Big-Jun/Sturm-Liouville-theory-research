import numpy as np, math

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

def eigs_fast(jumps, vals, k=8, npts0=60000, refine=5):
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    s = np.linspace(1e-6, np.sqrt(lam_hi), npts0)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(refine):
            sg = np.linspace(slo, shi, 1000)
            dg = _det_scan(jumps, vals, sg)
            jj = np.nonzero(np.signbit(dg[1:]) != np.signbit(dg[:-1]))[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def sup_config(R):
    sR = math.sqrt(R); t = 1.0/(2*sR + 1)
    return [sR*t, sR*t + t], [1.0, R, 1.0]  # a, A, a on [0,1]

def inf_config(R):
    sR = math.sqrt(R); t = 1.0/(2 + sR)
    return [t, t + sR*t], [R, 1.0, R]  # A, a, A on [0,1]

print("=== verify closed-form formulas: nu(R), mu(R) ===")
for R in [1.5, 2.0, 3.0, 4.0, 10.0, 100.0]:
    sR = math.sqrt(R)
    c1 = math.sqrt(sR/(2 + sR + 1.0/sR))
    nu_formula = (math.acos(-c1)/math.acos(c1))**2
    c2 = 1.0/(sR + 1)
    mu_formula = (math.acos(-c2)/math.acos(c2))**2
    jm, vm = sup_config(R); lam = eigs_fast(jm, vm, k=2)
    nu_num = lam[1]/lam[0]
    ji, vi = inf_config(R); lam2 = eigs_fast(ji, vi, k=2)
    mu_num = lam2[1]/lam2[0]
    print(f"R={R:6.1f}: nu_formula={nu_formula:.8f} nu_num={nu_num:.8f}  mu_formula={mu_formula:.8f} mu_num={mu_num:.8f}")
