import numpy as np

def sym_eigs(c, R, k=6):
    """Symmetric two-step: rho=R on [c,1-c], 1 outside. Returns lam1..lamk (alternating even/odd)."""
    if c < 1e-12:  # constant 1
        return np.array([(n*np.pi)**2 for n in range(1,k+1)])
    if c > 0.5-1e-12:  # constant R
        return np.array([(n*np.pi)**2/R for n in range(1,k+1)])
    hw = 0.5 - c  # half-width of well
    def even(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.cos(W*hw) - W*np.sin(w*c)*np.sin(W*hw)  # w cot(wc) = W tan(Whw) => w cos(wc)cos(Whw) - W sin(wc)sin(Whw)=0
    def odd(lam):
        w = np.sqrt(lam); W = np.sqrt(lam*R)
        return w*np.cos(w*c)*np.sin(W*hw) + W*np.sin(w*c)*np.cos(W*hw)  # w cot(wc) = -W cot(Whw) => w cos(wc)sin(Whw) + W sin(wc)cos(Whw)=0
    # find roots: even roots: 1st,3rd,... ; odd: 2nd,4th,...
    def roots_of(f, nroot, lam_max):
        s = np.linspace(1e-9, np.sqrt(lam_max), 200000)
        d = f(s**2)
        out = []
        for i in range(len(s)-1):
            if d[i]*d[i+1] < 0:
                lo, hi = s[i], s[i+1]
                for _ in range(90):
                    m = 0.5*(lo+hi)
                    if f(lo**2)*f(m**2) <= 0: hi = m
                    else: lo = m
                out.append(((lo+hi)/2)**2)
                if len(out) >= nroot: break
        return out
    lam_max = R*((k+1)**2)*(np.pi**2)*2
    e = roots_of(even, (k+1)//2, lam_max)
    o = roots_of(odd, k//2, lam_max)
    # merge alternating
    res = []
    i = j = 0
    while len(res) < k:
        if i < len(e) and (j >= len(o) or e[i] < o[j]):
            res.append(e[i]); i+=1
        else:
            res.append(o[j]); j+=1
    return np.array(res[:k])

# verify vs transfer: c=0.404, R=4
print("sym_eigs c=0.404 R=4:", np.round(sym_eigs(0.404,4.0,4),6))
print("expect ~ [4.51315, 33.73544, 61.68591, ?]")

import time
t0=time.time()
for R in [2.0,4.0,10.0,100.0,1e4,1e6,1e8,1e10]:
    gr = (np.sqrt(5)-1)/2
    # grid scan coarse
    cs = np.linspace(0.0, 0.5, 200)
    vals = np.array([sym_eigs(c,R,3)[1]/sym_eigs(c,R,3)[0] for c in cs])
    i = np.argmax(vals)
    a, b = max(1e-10, cs[max(0,i-1)]), min(0.5, cs[min(len(cs)-1,i+1)])
    f = lambda c: sym_eigs(c,R,3)[1]/sym_eigs(c,R,3)[0]
    c = b - gr*(b-a); d = a + gr*(b-a); fc, fd = f(c), f(d)
    for _ in range(80):
        if fc > fd:
            a, c, fd = c, d, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            b, d, fc = d, c, fd
            d = a + gr*(b-a); fd = f(d)
    cb = 0.5*(a+b)
    lam = sym_eigs(cb, R, 3)
    print(f"R={R:10.0f}: max lam2/lam1={lam[1]/lam[0]:.8f}  c*={cb:.8f} delta={1-2*cb:.6e}  lam1={lam[0]:.4f} lam2={lam[1]:.4f}  4sqrt(R)={4*np.sqrt(R):.2f}")
print("elapsed %.0fs" % (time.time()-t0))
