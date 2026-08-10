import numpy as np

def sym_ratio(c, R):
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
    lam_max = R*9*(np.pi**2)*2
    e = roots_of(even, 1, lam_max)
    o = roots_of(odd, 1, lam_max)
    return o[0]/e[0], e, o

for (c,R) in [(0.399,4.0),(0.4778,100.0),(0.4978,1e4)]:
    r, e, o = sym_ratio(c,R)
    print(f"c={c}, R={R}: ratio={r:.6f}, lam1={e[0]:.6f}, lam2={o[0]:.6f}")
# expected: c=0.399 R=4 -> 7.4812; c=0.4778 R=100 -> 39.5; c=0.4978 R=1e4 -> 424
