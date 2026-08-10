# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 40
pi = mp.pi

def M2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + t*(4*A*w-5*q-9*q*w*w)
def dM2(q, w):
    A = pi - mp.atan(w/q); t = mp.atan(w)
    return (4*A*A*w + 8*A*w*w*q/(q*q+w*w) - 7*w*q*q/(q*q+w*w) - 14*A*q - 9*w**3/(q*q+w*w)
            + 2*w/(1+w*w) + 4*A*q/(1+w*w) + t*(4*w*w/(q*q+w*w) - 5 - 9*w*w))
# part (a) identity M2(1,w) = pi*h(w)
h = lambda w: 4*w*(pi-mp.atan(w)) - 5 - 9*w*w
print("part(a) identity: max |M2(1,w)-pi*h(w)| =",
      max(abs(M2(mp.mpf(1), mp.mpf(w)*mp.mpf('0.01')) - pi*h(mp.mpf(w)*mp.mpf('0.01'))) for w in range(1001)))
hp = lambda w: 4*(pi-mp.atan(w)) - 4*w/(1+w*w) - 18*w
print("h'(1/2) =", hp(mp.mpf('0.5')), " > 0.1016:", hp(mp.mpf('0.5')) > mp.mpf('0.1016'))
print("h'(0.53) =", hp(mp.mpf('0.53')), " < -0.52:", hp(mp.mpf('0.53')) < mp.mpf('-0.52'))

# CORNER and C4 used at lines 1046-1048
def G2(c, q):
    lo, hi = pi/2 + mp.mpf('1e-12'), pi - mp.mpf('1e-12')
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    for _ in range(200):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    x=(lo+hi)/2
    Phi = mp.cos(x)**2+q*q*mp.sin(x)**2; D = q+c*Phi
    return -Phi*(3+2*x*mp.cot(x))/D + 2*c*x*Phi*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
print("CORNER: min G2(1/2;q), q in [2,20] =", min(G2(mp.mpf('0.5'), mp.mpf(2)+mp.mpf(k)) for k in range(19)))
print("C4: min G2(0.4;q), q in (1,2] =", min(G2(mp.mpf('0.4'), mp.mpf('1.001')+mp.mpf('0.001')*k) for k in range(1000)))
print("C4: min G2(0.4;q), q in (2,20] =", min(G2(mp.mpf('0.4'), mp.mpf(2)+mp.mpf('0.01')*k) for k in range(1801)))
# IN decreasing in w (M2<0) + w increasing in c => IN decreasing in c => G2 sign check on grid
print("M2<0 check on D grid: min M2 =",
      min(M2(mp.mpf('1.01')+mp.mpf('0.2')*k, mp.mpf('0.05')+mp.mpf('0.15')*j)
          for k in range(11) for j in range(12)
          if mp.mpf('0.05')+mp.mpf('0.15')*j < mp.sqrt(2*(mp.mpf('1.01')+mp.mpf('0.2')*k)+1)))
