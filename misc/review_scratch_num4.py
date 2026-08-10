# -*- coding: utf-8 -*-
import mpmath as mp
from fractions import Fraction as Fr
mp.mp.dps = 60
pi = mp.pi

def M2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + t*(4*A*w-5*q-9*q*w*w)
def dM2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return (4*A*A*w + 8*A*w*w*q/(q*q+w*w) - 7*w*q*q/(q*q+w*w) - 14*A*q - 9*w**3/(q*q+w*w)
            + 2*w/(1+w*w) + 4*A*q/(1+w*w) + t*(4*w*w/(q*q+w*w) - 5 - 9*w*w))

# lem:B1 : g(w)=d_q M2(1,w) < 0 on [0,sqrt3]
g = lambda w: dM2(mp.mpf(1), w)
print("lem:B1 cross-check: max g on [0,sqrt3] =",
      max(g(mp.mpf(w)*mp.sqrt(3)/200) for w in range(201)))
# lem:boundary: dM2(q,sqrt(2q+1))<0 and M2(q,sqrt(2q+1))<0, q in [1,2] and beyond
mn1 = mp.mpf('1e30'); mn2 = mp.mpf('1e30')
for qq in [mp.mpf(1)+mp.mpf(k)/100 for k in range(0,101)]:
    wb = mp.sqrt(2*qq+1)
    mn1 = min(mn1, dM2(qq, wb)); mn2 = min(mn2, M2(qq, wb))
print("lem:boundary cross-check: min d_qM2(q,w_b) =", mn1, "; min M2(q,w_b) =", mn2)
# part (a): M2(1,w)<0
print("part (a) cross-check: min M2(1,w) on [0,10] =", min(M2(mp.mpf(1), mp.mpf(w)*mp.mpf('0.05')) for w in range(201)))

# ---------- rational envelopes ----------
# B(20) = (4pi^2+14)*sqrt41 + 1 - 183.395*pi ; need < -232.723
# rearrange: (4pi^2+14)*sqrt41 + 233.723 < 183.395*pi
pi_hi = Fr(31416, 10000); pi_lo = Fr(31415, 10000)
s41_hi = Fr(64032, 10000); s41_lo = Fr(64031, 10000)
LHS_ub = (4*pi_hi**2 + 14)*s41_hi + Fr(233723, 1000)
RHS_lb = Fr(183395, 1000)*pi_lo
print("rational envelope B(20)<-232.723: LHS_ub =", LHS_ub, " RHS_lb =", RHS_lb, " LHS_ub < RHS_lb:", LHS_ub < RHS_lb)
print("   margin =", float(RHS_lb - LHS_ub))
# B'(q) < 0 : B'(q) <= (4pi^2+14)/sqrt41 - 10pi ; envelope with pi<=22/7, sqrt41>=64031/10000, 10pi>=10*157/50
env = (4*Fr(22,7)**2 + 14)*Fr(10000, 64031) - 10*Fr(157,50)
print("B'(q)<0 envelope (4pi^2+14)/sqrt41 - 10pi <= ", env, " < 0:", env < 0)

# ---------- Chain 3 cross-checks ----------
def G1f(q, c):
    lo, hi = mp.mpf('1e-12'), pi/2
    f = lambda x: mp.atan(1/(q*mp.tan(x))) - c*x
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    x=(lo+hi)/2
    Phi = mp.cos(x)**2+q*q*mp.sin(x)**2; D = q+c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
def G2f(q, c):
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    x=(lo+hi)/2
    Phi = mp.cos(x)**2+q*q*mp.sin(x)**2; D = q+c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
print("lem:G1 cross-check: max G1 over q in (1,2], c in (0,0.5] =",
      max(G1f(mp.mpf(1)+mp.mpf(qq)/50, mp.mpf(cc)/100) for qq in range(1,51) for cc in range(1,51)))
print("lem:G2m2 cross-check: min G2 over box [0.655,pi/3]x[1,2] via curve c=c2:",
      min(G2f(mp.mpf(1)+mp.mpf(qq)/50, mp.mpf('0.4')+mp.mpf(cc)/100) for qq in range(1,51) for cc in range(1,11)))
# G1 < -2 on T1-ish region: alpha1 range (0.841,1.1220), q in (1,2), c=c1 in (0.4,0.5)
print("thm:j1e1(iii) cross-check: max G1 over q in (1,2), c in (0.4,0.5):",
      max(G1f(mp.mpf(1)+mp.mpf(qq)/50, mp.mpf('0.4')+mp.mpf(cc)/100) for qq in range(1,51) for cc in range(1,11)))
