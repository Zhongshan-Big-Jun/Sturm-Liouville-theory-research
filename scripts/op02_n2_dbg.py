# -*- coding: utf-8 -*-
import numpy as np
R = 4.0; s = np.sqrt(R); t = 1.0/(3*s+2)
a, b, c = s*t, t, s*t

def Thalf(omega, alpha, beta, gamma, R):
    def T(L, cc, w):
        wc = w*np.sqrt(cc)
        return np.array([[np.cos(wc*L), np.sin(wc*L)/wc], [-wc*np.sin(wc*L), np.cos(wc*L)]])
    M = T(alpha, 1.0, omega) @ T(beta, R, omega) @ T(gamma, 1.0, omega)
    return M

def shoot_mixed(w):
    u, up = 0.0, 1.0
    for L, cc in [(a,1.0),(b,R),(c/2.0,1.0)]:
        ww = w*np.sqrt(cc)
        u, up = u*np.cos(ww*L) + up*np.sin(ww*L)/ww, -u*ww*np.sin(ww*L) + up*np.cos(ww*L)
    return up

w = np.sqrt(4.79534735)
M = Thalf(w, a, b, c/2.0, R)
print("Thalf M =\n", M)
print("shoot up(0.5) =", shoot_mixed(w), " (should be ~0)")
print("Thalf[1,1] =", M[1,1], " Thalf[0,1] =", M[0,1])
# manual transfer on (u,up)
M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
for L, cc in [(a,1.0),(b,R),(c/2.0,1.0)]:
    ww = w*np.sqrt(cc); wL = ww*L
    cw = np.cos(wL); sw = np.sin(wL)/ww; sw2 = -ww*np.sin(wL)
    M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
print("manual M11 =", M11, " M01 =", M01)
