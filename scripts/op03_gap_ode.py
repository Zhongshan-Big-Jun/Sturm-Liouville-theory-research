import numpy as np
from op03_gap_precise import lams_precise

R = 4.0
u = 0.30
v0 = 1-2*u
base = [(u,1.0),(v0,R),(u,1.0)]

def y_yp(x, ss, blocks):
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

def rho(x):
    if x < u: return 1.0
    if x < 1-u: return R
    return 1.0

s = np.sqrt(3.12004426)
for x in (0.15, 0.45, 0.75):
    y, yp = y_yp(x, s, base)
    h = 1e-6
    ypp = (y_yp(x+h, s, base)[0] - 2*y + y_yp(x-h, s, base)[0])/h**2
    print(f"x={x}: y={y:.8f}  y''={ypp:.6f}  -s^2 rho y={-s*s*rho(x)*y:.6f}  y'={yp:.6f}")
# also check y'(u) continuity
yL, ypL = y_yp(u, s, base)
yR, ypR = y_yp(u+1e-9, s, base)
print(f"junction u: y={yL:.8f}/{yR:.8f}, y'={ypL:.8f}/{ypR:.8f}")
