# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq

def detfun(s, jumps, vals):
    xs = [0.0] + list(jumps) + [1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2; n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2; n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def lams_full(jumps, vals, k=6):
    A = max(vals)
    s = np.linspace(1e-8, np.sqrt(A*400), 150000)
    d = np.array([detfun(x, jumps, vals) for x in s])
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        root = brentq(detfun, s[i], s[i+1], args=(jumps, vals), xtol=1e-14, rtol=1e-14)
        out.append(root**2)
        if len(out) >= k: break
    return np.array(out)

R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
a, b, c = s*t, t, s*t
jumps = [a, a+b, a+b+c, a+b+c+b]
vals = [1, R, 1, R, 1]
lam = lams_full(jumps, vals, 6)
print("full 5-block eigenvalues:", np.array2string(lam, precision=6))
print("lambda2 =", lam[1], " lambda3 =", lam[2], " ratio =", lam[2]/lam[1])
print("half nu1^2 = 16.7556 (should be lambda2?)  half mu1^2 = 6.463 (should be lambda1?)")

# check symmetry: u2 node at 1/2?  build eigenfunction for lambda2
def eigfun(x, omega, jumps, vals):
    # integrate transfer from 0
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    pts = [0.0]+list(jumps)+[1.0]
    u = np.sin(0.0*omega)
    for i in range(len(pts)-1):
        if x < pts[i+1] - 1e-12:
            L = x - pts[i]; cc = vals[i]
            w = omega*np.sqrt(cc); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
            return M01  # u(x) = M01 (initial (0,1))
        else:
            L = pts[i+1]-pts[i]; cc = vals[i]
            w = omega*np.sqrt(cc); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M01

w2 = np.sqrt(lam[1]); w3 = np.sqrt(lam[2])
print("u2(1/2) =", eigfun(0.5, w2, jumps, vals), " (0 if antisym)")
print("u3(1/2) =", eigfun(0.5, w3, jumps, vals))
print("u1(1/2) =", eigfun(0.5, np.sqrt(lam[0]), jumps, vals))
# derivative at 1/2: use transfer M10/M11
def eigder(x, omega, jumps, vals):
    pts = [0.0]+list(jumps)+[1.0]
    M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
    for i in range(len(pts)-1):
        if x < pts[i+1] - 1e-12:
            L = x - pts[i]; cc = vals[i]
            w = omega*np.sqrt(cc); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            return M10*cw+M11*sw2
        else:
            L = pts[i+1]-pts[i]; cc = vals[i]
            w = omega*np.sqrt(cc); wL = w*L
            cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
            M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return M10*cw+M11*sw2
print("u1'(1/2) =", eigder(0.5, np.sqrt(lam[0]), jumps, vals), " (0 if symmetric)")
print("u3'(1/2) =", eigder(0.5, w3, jumps, vals))
