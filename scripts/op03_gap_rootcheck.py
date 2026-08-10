import numpy as np
from op03_gap_precise import lams_precise

R = 4.0
u = 0.30
v0 = 1-2*u
base = [(u,1.0),(v0,R),(u,1.0)]

def M01(s):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    for L, c in base:
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M01

lam = lams_precise(base, 3)**2
print("lam:", lam)
for k in range(3):
    s = np.sqrt(lam[k])
    print(f"k={k}: s={s:.8f}, M01(s)={M01(s):.3e}")
# scan M01 sign near each root
for k in range(3):
    s = np.sqrt(lam[k])
    for d in (-1e-3, 1e-3):
        print(f"  M01({s+d:.6f}) = {M01(s+d):+.4e}")
# wide scan to see roots
ss = np.linspace(0.1, 8.0, 800)
vals = [M01(s) for s in ss]
# print sign changes
sc = np.signbit(np.array(vals[1:])) != np.signbit(np.array(vals[:-1]))
idx = np.nonzero(sc)[0]
print("sign changes at s ~", [f"{ss[i]:.4f}" for i in idx[:8]])
