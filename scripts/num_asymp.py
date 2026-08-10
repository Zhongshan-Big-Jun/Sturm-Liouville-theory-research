import numpy as np

def sym_ratio(c, R):
    """lambda2/lambda1 for symmetric well [c,1-c], rho=R inside. Exact via char eqs."""
    if c < 1e-12: return 4.0
    if c > 0.5-1e-12: return 4.0
    hw = 0.5 - c
    def even(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.cos(W*hw) - W*np.sin(w*c)*np.sin(W*hw)
    def odd(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.sin(W*hw) + W*np.sin(w*c)*np.cos(W*hw)
    def roots_of(f, nroot, lam_max):
        s = np.linspace(1e-9, np.sqrt(lam_max), 60000)
        d = f(s**2)
        out = []
        for i in range(len(s)-1):
            if d[i]*d[i+1] < 0:
                lo, hi = s[i], s[i+1]
                for _ in range(60):
                    m = 0.5*(lo+hi)
                    if f(lo**2)*f(m**2) <= 0: hi = m
                    else: lo = m
                out.append(((lo+hi)/2)**2)
                if len(out) >= nroot: break
        return out
    lam_max = R*9*(np.pi**2)*2
    e = roots_of(even, 1, lam_max)
    o = roots_of(odd, 1, lam_max)
    return o[0]/e[0]

import time
print("=== max lambda2/lambda1 over symmetric well, fine scan in delta = 1-2c ===")
for R in [4.0, 10.0, 100.0, 1e4, 1e6, 1e8]:
    # log scan in delta
    dmin = max(1e-6, 2.0/R)
    ds = np.geomspace(dmin, 0.5, 300)
    best = (0.0, None)
    t0 = time.time()
    for d in ds:
        r = sym_ratio(0.5 - d/2, R)
        if r > best[0]: best = (r, d)
    # refine with golden around best
    gr = (np.sqrt(5)-1)/2
    a, b = best[1]*0.8, best[1]*1.25
    f = lambda d: sym_ratio(0.5-d/2, R)
    c = b - gr*(b-a); dd = a + gr*(b-a); fc, fd = f(c), f(d)
    for _ in range(80):
        if fc > fd:
            a, c, fd = c, dd, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, dd, fc = dd, c, fd
            dd = a + gr*(b-a); fd = f(dd)
    dopt = 0.5*(a+b)
    print(f"R={R:9.0f}: max={f(dopt):.6f} delta*={dopt:.6e}  ratio/sqrt(R)={f(dopt)/np.sqrt(R):.5f}  pi^2/2={np.pi**2/2:.4f}  ({time.time()-t0:.0f}s)")
