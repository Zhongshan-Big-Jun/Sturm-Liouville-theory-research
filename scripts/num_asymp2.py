import numpy as np, time

def sym_eigs(c, R, k=4):
    if c < 1e-12:
        return np.array([(n*np.pi)**2 for n in range(1,k+1)])
    if c > 0.5-1e-12:
        return np.array([(n*np.pi)**2/R for n in range(1,k+1)])
    hw = 0.5 - c
    def even(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.cos(W*hw) - W*np.sin(w*c)*np.sin(W*hw)
    def odd(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.sin(W*hw) + W*np.sin(w*c)*np.cos(W*hw)
    def roots_of(f, nroot, lam_max):
        s = np.linspace(1e-9, np.sqrt(lam_max), 200000)
        d = f(s**2)
        out = []
        for i in range(len(s)-1):
            if d[i]*d[i+1] < 0:
                lo, hi = s[i], s[i+1]
                for _ in range(70):
                    m = 0.5*(lo+hi)
                    if f(lo**2)*f(m**2) <= 0: hi = m
                    else: lo = m
                out.append(((lo+hi)/2)**2)
                if len(out) >= nroot: break
        return out
    lam_max = R*((k+1)**2)*(np.pi**2)*2
    e = roots_of(even, (k+1)//2, lam_max)
    o = roots_of(odd, k//2, lam_max)
    res = []; i=j=0
    while len(res) < k:
        if i < len(e) and (j >= len(o) or e[i] < o[j]):
            res.append(e[i]); i+=1
        else:
            res.append(o[j]); j+=1
    return np.array(res[:k])

print("=== max lambda2/lambda1 over symmetric well (clean log scan) ===")
for R in [2.0, 4.0, 10.0, 100.0, 1e4, 1e6, 1e8]:
    ds = np.geomspace(1e-7, 0.4999, 400)
    best = (0.0, None)
    t0=time.time()
    for d in ds:
        r = sym_eigs(0.5-d/2, R, 2)[1]/sym_eigs(0.5-d/2, R, 2)[0]
        if r > best[0]: best = (r, d)
    gr = (np.sqrt(5)-1)/2
    a, b = best[1]*0.7, min(0.4999, best[1]*1.3)
    f = lambda d: sym_eigs(0.5-d/2, R, 2)[1]/sym_eigs(0.5-d/2, R, 2)[0]
    c = b - gr*(b-a); dd = a + gr*(b-a); fc, fd = f(c), f(d)
    for _ in range(90):
        if fc > fd:
            a, c, fd = c, dd, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, dd, fc = dd, c, fd
            dd = a + gr*(b-a); fd = f(dd)
    dopt = 0.5*(a+b)
    lam = sym_eigs(0.5-dopt/2, R, 2)
    print(f"R={R:9.0f}: max={f(dopt):.8f} delta*={dopt:.6e} lam1={lam[0]:.6f} lam2={lam[1]:.6f}  M/sqrt(R)={f(dopt)/np.sqrt(R):.6f}  ({time.time()-t0:.0f}s)")
