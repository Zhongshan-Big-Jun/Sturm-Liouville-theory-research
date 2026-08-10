# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50
# 1) M2 == d_w IN  (numeric)
def vals(q,w):
    A = mp.pi - mp.atan(w/q)
    IN = (q*q+w*w)*A*(2*A*q-3*w+2*mp.atan(w)) - 3*w*q*(1+w*w)*mp.atan(w)
    M2 = 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + mp.atan(w)*(4*A*w-5*q-9*q*w*w)
    dIN = mp.diff(lambda ww: (q*q+ww*ww)*A*(2*A*q-3*ww+2*mp.atan(ww)) - 3*ww*q*(1+ww*ww)*mp.atan(ww), w)
    return M2, dIN
for (q,w) in [(2.0,1.0),(5.0,3.0),(1.5,0.7),(20.0,6.0)]:
    M2,dIN = vals(q,w)
    print("q,w=",q,w," M2-dIN=", M2-dIN)
# 2) d_q M2 manual vs numeric diff
def dM2_manual(q,w):
    A = mp.pi - mp.atan(w/q); t = mp.atan(w)
    return (4*A*A*w + 8*A*w*w*q/(q*q+w*w) - 7*w*q*q/(q*q+w*w) - 14*A*q - 9*w**3/(q*q+w*w)
            + 2*w/(1+w*w) + 4*A*q/(1+w*w) + t*(4*w*w/(q*q+w*w) - 5 - 9*w*w))
def M2f(q,w):
    A = mp.pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + t*(4*A*w-5*q-9*q*w*w)
for (q,w) in [(2.0,1.0),(5.0,3.0),(1.5,0.7),(20.0,6.0),(1.2,2.1)]:
    dnum = mp.diff(lambda qq: M2f(qq,w), q)
    print("q,w=",q,w," dqM2 manual-num=", dM2_manual(q,w)-dnum)
# 3) IN == G2*POS numeric, correct Phi
def G(x,c,q):
    Phi = mp.cos(x)**2 + q*q*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
for (q,w) in [(2.0,1.0),(5.0,3.0),(1.5,0.7),(20.0,6.0)]:
    A = mp.pi - mp.atan(w/q); c = mp.atan(w)/A
    Phi = (q*q*(1+w*w))/(q*q+w*w)
    D = q + c*Phi
    G2 = -Phi*(3+2*A*(-q/w))/D + 2*c*A*Phi*(q*q-1)*(-q*w/(q*q+w*w))/D**2
    POS = D*D*A*(q*q+w*w)*w/(Phi*q)
    IN = (q*q+w*w)*A*(2*A*q-3*w+2*mp.atan(w)) - 3*w*q*(1+w*w)*mp.atan(w)
    print("q,w=",q,w," IN - G2*POS =", IN - G2*POS)
