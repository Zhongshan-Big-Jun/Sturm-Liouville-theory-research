import numpy as np
from scipy.integrate import quad
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
I2 = quad(lambda x: y_yp(x, s, base)[1]**2, 0, 1, epsabs=1e-13, limit=500)[0]
I0 = quad(lambda x: rho(x)*y_yp(x, s, base)[0]**2, 0, 1, epsabs=1e-13, limit=500)[0]
print("int y'^2 =", I2)
print("s^2 * int rho y^2 =", s*s*I0)
print("ratio:", I2/I0, " vs s^2 =", s*s)
