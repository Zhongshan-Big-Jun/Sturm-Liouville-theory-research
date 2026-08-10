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

def rho_v(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < u, 1.0, np.where(x < 1-u, R, 1.0))

s = np.sqrt(3.12004426)
for npts in (10001, 100001, 1000001):
    xs = np.linspace(0, 1, npts)
    ys = np.array([y_yp(x, s, base) for x in xs])
    I2 = np.trapezoid(ys[:,1]**2, xs)
    I0 = np.trapezoid(rho_v(xs)*ys[:,0]**2, xs)
    print(f"npts={npts}: int y'^2={I2:.10f}  s^2 int rho y^2={s*s*I0:.10f}  ratio={I2/(s*s*I0):.8f}")
