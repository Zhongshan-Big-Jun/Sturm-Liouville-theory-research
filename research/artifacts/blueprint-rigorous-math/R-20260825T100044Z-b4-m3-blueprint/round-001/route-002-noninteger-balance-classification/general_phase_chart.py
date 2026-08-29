"""Independent exact general-leading-p3 chart for route 002.

This is a direct SymPy transcription of the hash-bound closed equations; it
does not use the truncated P dictionary for the O(1) shift p3 -> theta.
"""

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
A = (2 + q*u**2)/K
eps = u**3
k2 = K*u
k3 = K*u + C*u**5
r = 1 + C*u**4/K
p1 = sp.pi/2 + A*u**2
p3 = th + B*u**2
p2 = k2/2 - eps*(p1 + p3)
p1t = r*p1
p3t = r*p3
p2t = r*p2

E1 = (sp.cos(p2)*sp.sin(p1 + p3)
      + sp.sin(p2)*sp.cos(p3)*sp.cos(p1)/eps
      - eps*sp.sin(p3)*sp.sin(p2)*sp.sin(p1))
E2 = (sp.cos(p2t)*sp.cos(p1t)*sp.cos(p3t)
      - sp.sin(p3t)*sp.sin(p2t)*sp.cos(p1t)/eps
      - sp.sin(p3t)*sp.cos(p2t)*sp.sin(p1t)
      - eps*sp.cos(p3t)*sp.sin(p2t)*sp.sin(p1t))
E6 = (sp.sin(p1)*(eps*sp.cos(p2t)
                  + sp.sin(p2t)*sp.cos(p1t)/sp.sin(p1t))
      + eps*sp.cos(p2)*sp.sin(p1) + sp.sin(p2)*sp.cos(p1))


def mass(k, x1, x2, x3, mode):
    if mode == "D":
        bc = -(eps*sp.cos(x2)*sp.sin(x1)/k
               + sp.sin(x2)*sp.cos(x1)/k)/sp.sin(x3)
        m3 = bc**2*(x3 - sp.sin(2*x3)/2)/(2*k*eps)
    else:
        bc = (eps*sp.cos(x2)*sp.sin(x1)/k
              + sp.sin(x2)*sp.cos(x1)/k)/sp.cos(x3)
        m3 = bc**2*(x3 + sp.sin(2*x3)/2)/(2*k*eps)
    m1 = (x1 - sp.sin(2*x1)/2)*eps/(2*k**3)
    aa = eps*sp.sin(x1)/k
    bb = sp.cos(x1)/k
    ml = ((aa**2 + bb**2)*x2/(2*k)
          + (aa**2 - bb**2)*sp.sin(2*x2)/(4*k)
          + aa*bb*(1 - sp.cos(2*x2))/(2*k))
    return m1 + m3 + ml


ID = mass(k2, p1, p2, p3, "D")
IN = mass(k3, p1t, p2t, p3t, "N")
E5 = ID*sp.sin(p1t)**2 - IN*sp.sin(p1)**2


def coeff(expr, n, order):
    return sp.factor(sp.series(expr, u, 0, order).removeO().expand().coeff(u, n))


print(f"sympy={sp.__version__}")
for name, expr, orders, stop in (
    ("E1", E1, (0, 2, 4), 6),
    ("E2", E2, (0, 2, 4), 6),
    ("E6", E6, (3, 5, 7), 9),
    ("E5", E5, (0, 2, 4, 5, 6), 7),
):
    series_expr = sp.series(expr, u, 0, stop).removeO().expand()
    print(f"{name}_SERIES={sp.factor(series_expr)}")
    for n in orders:
        print(f"{name}[{n}]={sp.factor(series_expr.coeff(u, n))}")
