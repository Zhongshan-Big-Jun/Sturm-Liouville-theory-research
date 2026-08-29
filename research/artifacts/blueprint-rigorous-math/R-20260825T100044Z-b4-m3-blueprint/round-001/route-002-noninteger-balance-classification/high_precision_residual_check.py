"""High-precision original-residual scaling checks for route 002."""

from __future__ import annotations

import hashlib
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parents[6]
BOUND = REPO / "scripts/_gapn2_largeR_closed.py"
EXPECTED = "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4"
if hashlib.sha256(BOUND.read_bytes()).hexdigest() != EXPECTED:
    raise SystemExit("closed-equation source hash mismatch")

mp.mp.dps = 100


def mass(k, p1, p2, p3, eps, mode):
    if mode == "D":
        bc = -(eps*mp.cos(p2)*mp.sin(p1)/k
               + mp.sin(p2)*mp.cos(p1)/k)/mp.sin(p3)
        m3 = bc**2*(p3-mp.sin(2*p3)/2)/(2*k*eps)
    else:
        bc = (eps*mp.cos(p2)*mp.sin(p1)/k
              + mp.sin(p2)*mp.cos(p1)/k)/mp.cos(p3)
        m3 = bc**2*(p3+mp.sin(2*p3)/2)/(2*k*eps)
    m1 = (p1-mp.sin(2*p1)/2)*eps/(2*k**3)
    aa = eps*mp.sin(p1)/k
    bb = mp.cos(p1)/k
    ml = ((aa*aa+bb*bb)*p2/(2*k)
          + (aa*aa-bb*bb)*mp.sin(2*p2)/(4*k)
          + aa*bb*(1-mp.cos(2*p2))/(2*k))
    return m1+m3+ml


def residual(u, K, A, B, C):
    eps = u**3
    k2 = K*u
    k3 = K*u+C*u**5
    p1 = mp.pi/2+A*u**2
    p3 = mp.pi/4+B*u**2
    r = k3/k2
    p1t, p3t = r*p1, r*p3
    p2 = k2/2-eps*(p1+p3)
    p2t = r*p2
    e1 = (mp.cos(p2)*mp.sin(p1+p3)
          + mp.sin(p2)*mp.cos(p3)*mp.cos(p1)/eps
          - eps*mp.sin(p3)*mp.sin(p2)*mp.sin(p1))
    e2 = (mp.cos(p2t)*mp.cos(p1t)*mp.cos(p3t)
          - mp.sin(p3t)*mp.sin(p2t)*mp.cos(p1t)/eps
          - mp.sin(p3t)*mp.cos(p2t)*mp.sin(p1t)
          - eps*mp.cos(p3t)*mp.sin(p2t)*mp.sin(p1t))
    i_d = mass(k2,p1,p2,p3,eps,"D")
    i_n = mass(k3,p1t,p2t,p3t,eps,"N")
    e5 = i_d*mp.sin(p1t)**2-i_n*mp.sin(p1)**2
    e6 = (mp.sin(p1)*(eps*mp.cos(p2t)
                      + mp.sin(p2t)*mp.cos(p1t)/mp.sin(p1t))
          + eps*mp.cos(p2)*mp.sin(p1)+mp.sin(p2)*mp.cos(p1))
    return e1,e2,e5,e6


K = mp.mpf(3)
C = 16/(mp.pi*K)
q = (18*mp.pi-24-K**3)/(6*K)
B = mp.mpf("0.37")
target = -1/(6*K**2)
print(f"mpmath={mp.__version__} dps={mp.mp.dps}")
print(f"K={mp.nstr(K,30)} C={mp.nstr(C,30)} q={mp.nstr(q,30)} B={mp.nstr(B,30)}")
print(f"predicted_E5_over_u4={mp.nstr(target,50)}")
for exponent in (4,6,8,10,12,14):
    u = mp.mpf(10)**(-exponent)
    # AK-2=q*u^2, exactly the forced first blow-up.
    A = (2+q*u**2)/K
    e1,e2,e5,e6 = residual(u,K,A,B,C)
    print(" ".join((
        f"u=1e-{exponent}",
        f"E1/u2={mp.nstr(e1/u**2,30)}",
        f"E2/u2={mp.nstr(e2/u**2,30)}",
        f"E6/u5={mp.nstr(e6/u**5,30)}",
        f"E5/u4={mp.nstr(e5/u**4,50)}",
        f"error={mp.nstr(e5/u**4-target,20)}",
    )))

print("CORRECTED_SECONDARY_FACE")
K = (18*mp.pi-48/mp.pi)**(mp.mpf(1)/3)
B = 1/K
q0 = (18*mp.pi-24-K**3)/(6*K)
c0 = 16/(mp.pi*K)
q2 = -(1440*B*K+K**6-90*mp.pi*K**3+120*K**3
       -1620*mp.pi**2-4800+4320*mp.pi)/(360*K**2)
c2 = 4*(mp.pi*K**3-96+36*mp.pi**2)/(3*mp.pi**2*K**2)
print(" ".join((
    f"K0={mp.nstr(K,50)}", f"B0={mp.nstr(B,50)}",
    f"q0={mp.nstr(q0,50)}", f"C0={mp.nstr(c0,50)}",
    f"q2={mp.nstr(q2,50)}", f"C2={mp.nstr(c2,50)}",
)))
for exponent in (3,4,5,6,7,8):
    u = mp.mpf(10)**(-exponent)
    qv = q0+q2*u**2
    cv = c0+c2*u**2
    A = (2+qv*u**2)/K
    e1,e2,e5,e6 = residual(u,K,A,B,cv)
    print(" ".join((
        f"u=1e-{exponent}",
        f"E1/u4={mp.nstr(e1/u**4,25)}",
        f"E2/u4={mp.nstr(e2/u**4,25)}",
        f"E6/u7={mp.nstr(e6/u**7,25)}",
        f"E5/u6={mp.nstr(e5/u**6,25)}",
        f"E1/u6={mp.nstr(e1/u**6,25)}",
        f"E2/u6={mp.nstr(e2/u**6,25)}",
        f"E6/u9={mp.nstr(e6/u**9,25)}",
        f"E5/u8={mp.nstr(e5/u**8,25)}",
    )))

print("OFF_SEED_SECONDARY_COEFFICIENT_CHECK")
K=mp.mpf(3); B=mp.mpf("0.37")
q0=(18*mp.pi-24-K**3)/(6*K); c0=16/(mp.pi*K)
q2=-(1440*B*K+K**6-90*mp.pi*K**3+120*K**3
     -1620*mp.pi**2-4800+4320*mp.pi)/(360*K**2)
c2=4*(mp.pi*K**3-96+36*mp.pi**2)/(3*mp.pi**2*K**2)
h6=8*(B*K-1)/K**2
h5=2*(6*mp.pi**2*B*K+mp.pi*K**3-24*mp.pi**2+48)/(3*mp.pi*K**6)
print(f"predicted_H6={mp.nstr(h6,50)} predicted_H5={mp.nstr(h5,50)}")
for exponent in (3,5,7,9):
    u=mp.mpf(10)**(-exponent)
    A=(2+(q0+q2*u**2)*u**2)/K
    e1,e2,e5,e6=residual(u,K,A,B,c0+c2*u**2)
    print(" ".join((f"u=1e-{exponent}",f"E6/u7={mp.nstr(e6/u**7,50)}",
                    f"E5/u6={mp.nstr(e5/u**6,50)}")))
