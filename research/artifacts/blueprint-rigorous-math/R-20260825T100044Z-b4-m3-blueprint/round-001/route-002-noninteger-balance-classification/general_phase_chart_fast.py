"""Truncated-algebra replay of the exact O(1) p3-shift chart."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[6]
BOUND = REPO / "scripts/_gapn2_largeR_closed.py"
EXPECTED = "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4"
if hashlib.sha256(BOUND.read_bytes()).hexdigest() != EXPECTED:
    raise SystemExit("closed-equation source hash mismatch")

u = sp.symbols("u", positive=True)
K, q, B, C, th = sp.symbols("K q B C th", real=True)
eps = u**3
k2 = K*u
k3 = K*u + C*u**5
r = 1 + C*u**4/K
p1 = sp.pi/2 + (2*u**2 + q*u**4)/K
p3 = th + B*u**2
p2 = K*u/2 - eps*(p1 + p3)
p1t = sp.expand(r*p1)
p3t = sp.expand(r*p3)
p2t = sp.expand(r*p2)


def S(expr, n=9):
    return sp.series(expr, u, 0, n).removeO().expand()


def trig(x):
    return S(sp.sin(x), 11), S(sp.cos(x), 11)


s1, c1 = trig(p1)
s3, c3 = trig(p3)
s2, c2 = trig(p2)
s1t, c1t = trig(p1t)
s3t, c3t = trig(p3t)
s2t, c2t = trig(p2t)
sin2p1, sin2p3, sin2p2 = S(sp.sin(2*p1), 11), S(sp.sin(2*p3), 11), S(sp.sin(2*p2), 11)
sin2p1t, sin2p3t, sin2p2t = S(sp.sin(2*p1t), 11), S(sp.sin(2*p3t), 11), S(sp.sin(2*p2t), 11)
cos2p2, cos2p2t = S(sp.cos(2*p2), 11), S(sp.cos(2*p2t), 11)
inv_s3, inv_c3t = S(1/sp.sin(p3), 11), S(1/sp.cos(p3t), 11)

E1 = S(c2*S(sp.sin(p1+p3), 11) + s2*c3*c1/eps - eps*s3*s2*s1, 7)
E2 = S(c2t*c1t*c3t - s3t*s2t*c1t/eps - s3t*c2t*s1t - eps*c3t*s2t*s1t, 7)
cot1t = S(c1t/s1t, 11)
E6 = S(s1*(eps*c2t + s2t*cot1t) + eps*c2*s1 + s2*c1, 9)

bcD = S(-(eps*c2*s1/k2 + s2*c1/k2)*inv_s3, 8)
m3D = S(bcD**2*S(p3-sin2p3/2, 11)/(2*k2*eps), 7)
m1D = S((p1-sin2p1/2)*eps/(2*k2**3), 7)
aaD, bbD = S(eps*s1/k2, 9), S(c1/k2, 9)
mLD = S((aaD**2+bbD**2)*p2/(2*k2)
         + (aaD**2-bbD**2)*sin2p2/(4*k2)
         + aaD*bbD*(1-cos2p2)/(2*k2), 7)
ID = S(m1D+m3D+mLD, 7)

bcN = S((eps*c2t*s1t/k3 + s2t*c1t/k3)*inv_c3t, 8)
m3N = S(bcN**2*S(p3t+sin2p3t/2, 11)/(2*k3*eps), 7)
m1N = S((p1t-sin2p1t/2)*eps/(2*k3**3), 7)
aaN, bbN = S(eps*s1t/k3, 9), S(c1t/k3, 9)
mLN = S((aaN**2+bbN**2)*p2t/(2*k3)
         + (aaN**2-bbN**2)*sin2p2t/(4*k3)
         + aaN*bbN*(1-cos2p2t)/(2*k3), 7)
IN = S(m1N+m3N+mLN, 7)
E5 = S(ID*S(s1t**2, 9)-IN*S(s1**2, 9), 7)

print(f"sympy={sp.__version__}")
for name, expr, orders in (
    ("E1", E1, (2, 4, 6)),
    ("E2", E2, (2, 4, 6)),
    ("E6", E6, (5, 7)),
    ("E5", E5, (4, 5, 6)),
):
    for n in orders:
        print(f"{name}[{n}]={sp.factor(expr.coeff(u, n))}")

