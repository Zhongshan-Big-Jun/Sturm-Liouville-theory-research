import numpy as np
from scipy.integrate import quad
from op03_gap_precise import lams_precise

def y_fn(x, ss, blocks):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in blocks:
        x1 = x0 + L
        if x <= x1:
            w = ss*np.sqrt(c); d = x - x0
            y = M01*np.cos(w*d) + M11*np.sin(w*d)/w
            yp = -M01*w*np.sin(w*d) + M11*np.cos(w*d)
            return y, yp
        w = ss*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
    raise ValueError

def rho_of(blocks):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    def rho(x):
        for i in range(len(xs)-1):
            if xs[i] <= x <= xs[i+1]: return blocks[i][1]
        return 1.0
    return rho

for blocks, label in [ ([(1.0,1.0)], "const rho=1"), ([(0.5,2.0),(0.5,1.0)], "two-block") ]:
    lam = lams_precise(blocks, 2)**2
    rho = rho_of(blocks)
    for k in range(2):
        s = np.sqrt(lam[k])
        nrm = quad(lambda x: rho(x)*y_fn(x, s, blocks)[0]**2, 0, 1, epsabs=1e-13, limit=500)[0]
        K = quad(lambda x: y_fn(x, s, blocks)[1]**2, 0, 1, epsabs=1e-13, limit=500)[0]
        print(f"{label} k={k}: lam={lam[k]:.6f}  RQ={K/nrm:.6f}  y(1)={y_fn(1,s,blocks)[0]:.2e}")
