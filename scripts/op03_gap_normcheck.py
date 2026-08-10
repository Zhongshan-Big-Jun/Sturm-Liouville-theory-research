import numpy as np
from scipy.integrate import quad
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
v0 = 1-2*u
blocks = [(u,1.0),(v0,R),(u,1.0)]
xs = [0.0, u, u+v0, 1.0]
s = lams_precise(blocks, 3)
lam = s**2

def y(x, ss):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for bi, (L, c) in enumerate(blocks):
        x1 = x0 + L
        if x <= x1:
            w = ss*np.sqrt(c); d = x - x0
            return M01*np.cos(w*d) + M11*np.sin(w*d)/w
        w = ss*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
    raise ValueError

def rho(x):
    if x < u: return 1.0
    if x < 1-u: return R
    return 1.0

for k in range(2):
    nrm, err = quad(lambda x: rho(x)*y(x, s[k])**2, 0, 1, epsabs=1e-13, limit=500)
    print(f"k={k}: int rho y^2 = {nrm:.12f} (should be 1 if normalized correctly)")
# what eigfuns_precise thinks the norm is: u(u)^2 vs y(u)^2
vp = eigfuns_precise(blocks, s[:2], np.array([u]))
for k in range(2):
    yu = y(u, s[k])
    print(f"k={k}: y(u)^2={yu**2:.8f}, precise u(u)^2={vp[k,0]**2:.8f}, implied norm={yu**2/vp[k,0]**2:.8f}")
