"""Exact replay for the finite-interior scale-entry lemma.

This file uses the unscaled phase displacement y=p3-pi/4.  It verifies the
first spectral IFT in (q,Cbr) before any boundedness of B=y/u**2 is assumed,
then computes the reduced (y,v) derivatives which force y=O(v).

All promoted identities use exact SymPy arithmetic.  The script reads but
does not modify the hash-bound closed residual source or prior proof files.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[6]
BOUND = {
    "scripts/_gapn2_largeR_closed.py":
        "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4",
    "research/artifacts/blueprint-rigorous-math/"
    "R-20260825T100044Z-b4-m3-blueprint/problem_contract.md":
        "6dc56880458e66119f66c2a16f33df65afa799e03bbc681db5809e127e585e19",
    "research/artifacts/blueprint-rigorous-math/"
    "R-20260825T100044Z-b4-m3-blueprint/round-001/"
    "route-001-finite-r-branch-certification/candidate_branch_proof.md":
        "0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8",
    "research/artifacts/blueprint-rigorous-math/"
    "R-20260825T100044Z-b4-m3-blueprint/round-001/"
    "route-002-noninteger-balance-classification/proof_package.md":
        "88be4d4c2a987729706aa8c7cf7860c9ede0a53f5bdd5732019fc683f7695008",
    "research/artifacts/blueprint-rigorous-math/"
    "R-20260825T100044Z-b4-m3-blueprint/round-001/"
    "route-002-noninteger-balance-classification/valuation_and_exhaustiveness.md":
        "4e6b45befa420b7b65f49a93fd3157946d53c50482e4c1262f225964df3122b4",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


observed = {rel: digest(ROOT / rel) for rel in BOUND}
if observed != BOUND:
    raise SystemExit(json.dumps({"expected": BOUND, "observed": observed}, indent=2))

u = sp.symbols("u", positive=True)
K = sp.symbols("K", positive=True)
q, C, y = sp.symbols("q C y", real=True)
eps = u**3
v = u**2

# The rate p1-pi/2=2v/K+O(v**2) and r-1=O(v**2) is established by the
# exact tangent identities in the accompanying proof.  q and C are their
# bounded blow-up variables; y is deliberately left unscaled.
p1 = sp.pi/2 + (2*v + q*v**2)/K
p3 = sp.pi/4 + y
r = 1 + C*v**2/K
k2 = K*u
k3 = r*k2
p2 = k2/2 - eps*(p1+p3)
p1t, p3t, p2t = sp.expand(r*p1), sp.expand(r*p3), sp.expand(r*p2)


def T(expr, order=9):
    return sp.series(expr, u, 0, order).removeO().expand()


def trig(expr, order=9):
    return T(sp.sin(expr), order), T(sp.cos(expr), order)


s1, c1 = trig(p1)
s2, c2 = trig(p2)
s3, c3 = trig(p3)
s1t, c1t = trig(p1t)
s2t, c2t = trig(p2t)
s3t, c3t = trig(p3t)
sin2p1, sin2p2, sin2p3 = T(sp.sin(2*p1)), T(sp.sin(2*p2)), T(sp.sin(2*p3))
sin2p1t = T(sp.sin(2*p1t))
sin2p2t = T(sp.sin(2*p2t))
sin2p3t = T(sp.sin(2*p3t))
cos2p2, cos2p2t = T(sp.cos(2*p2)), T(sp.cos(2*p2t))

E1 = T(c2*T(sp.sin(p1+p3)) + s2*c3*c1/eps - eps*s3*s2*s1, 6)
E2 = T(c2t*c1t*c3t - s3t*s2t*c1t/eps
       - s3t*c2t*s1t - eps*c3t*s2t*s1t, 6)
E6 = T(s1*(eps*c2t + s2t*T(c1t/s1t))
       + eps*c2*s1 + s2*c1, 9)

bcD = T(-(eps*c2*s1/k2 + s2*c1/k2)*T(1/sp.sin(p3)), 8)
m3D = T(bcD**2*T(p3-sin2p3/2)/(2*k2*eps), 8)
m1D = T((p1-sin2p1/2)*eps/(2*k2**3), 8)
aaD, bbD = T(eps*s1/k2), T(c1/k2)
mLD = T((aaD**2+bbD**2)*p2/(2*k2)
        +(aaD**2-bbD**2)*sin2p2/(4*k2)
        +aaD*bbD*(1-cos2p2)/(2*k2), 8)
ID = T(m1D+m3D+mLD, 8)

bcN = T((eps*c2t*s1t/k3 + s2t*c1t/k3)*T(1/sp.cos(p3t)), 8)
m3N = T(bcN**2*T(p3t+sin2p3t/2)/(2*k3*eps), 8)
m1N = T((p1t-sin2p1t/2)*eps/(2*k3**3), 8)
aaN, bbN = T(eps*s1t/k3), T(c1t/k3)
mLN = T((aaN**2+bbN**2)*p2t/(2*k3)
        +(aaN**2-bbN**2)*sin2p2t/(4*k3)
        +aaN*bbN*(1-cos2p2t)/(2*k3), 8)
IN = T(m1N+m3N+mLN, 8)
E5 = T(ID*T(s1t**2)-IN*T(s1**2), 8)

divisibility_checks = {
    "E1_below_u2": [sp.factor(E1.coeff(u, n)) for n in range(2)],
    "E2_below_u2": [sp.factor(E2.coeff(u, n)) for n in range(2)],
    "E6_below_u5": [sp.factor(E6.coeff(u, n)) for n in range(5)],
    "E5_below_u4": [sp.factor(E5.coeff(u, n)) for n in range(4)],
}
if any(value != 0 for values in divisibility_checks.values() for value in values):
    raise SystemExit(f"analytic divisibility failed: {divisibility_checks}")

# Coefficients of the analytic quotients F1=E1/v, F2=E2/v,
# L6=E6/u**5, and L5=E5/v**2.  The suffix 0 denotes v=0 and v denotes
# the partial derivative with respect to v at fixed (K,q,C,y).
F10, F1v = sp.factor(E1.coeff(u, 2)), sp.factor(E1.coeff(u, 4))
F20, F2v = sp.factor(E2.coeff(u, 2)), sp.factor(E2.coeff(u, 4))
L60, L6v = sp.factor(E6.coeff(u, 5)), sp.factor(E6.coeff(u, 7))
L50, L5v = sp.factor(E5.coeff(u, 4)), sp.factor(E5.coeff(u, 6))

q0 = (18*sp.pi-24-K**3)/(6*K)
C0 = 16/(sp.pi*K)
base = {y: 0, q: q0, C: C0}

Fbase = sp.Matrix([F10.subs(y, 0), F20.subs(y, 0)])
J = sp.simplify(Fbase.jacobian([q, C]).subs({q: q0, C: C0}))
Jy = sp.Matrix([sp.diff(F10, y), sp.diff(F20, y)]).subs(base)
Jv = sp.Matrix([F1v, F2v]).subs(base)
z_y = sp.simplify(-J.inv()*Jy)
z_v = sp.simplify(-J.inv()*Jv)


def reduced_derivatives(L0, Lv):
    dz = sp.Matrix([[sp.diff(L0, q), sp.diff(L0, C)]]).subs(base)
    dy = sp.factor((sp.diff(L0, y).subs(base) + (dz*z_y)[0]))
    dv = sp.factor((Lv.subs(base) + (dz*z_v)[0]))
    return dy, dv


S6y, S6v = reduced_derivatives(L60, L6v)
S5y, S5v = reduced_derivatives(L50, L5v)

expected = {
    "first_face_F1": -sp.sqrt(2)*(K**3+6*K*q-18*sp.pi+24)/(24*K),
    "first_face_F2": sp.sqrt(2)*(3*sp.pi*C*K+K**3+6*K*q-18*sp.pi-24)/(24*K),
    "first_jacobian": -sp.pi/16,
    "S6_y": 8/K,
    "S6_v": -8/K**2,
    "S5_y": 4*sp.pi/K**5,
    "S5_v": 2*(sp.pi*K**3-24*sp.pi**2+48)/(3*sp.pi*K**6),
}
actual = {
    "first_face_F1": sp.factor(F10.subs(y, 0)),
    "first_face_F2": sp.factor(F20.subs(y, 0)),
    "first_jacobian": sp.factor(J.det()),
    "S6_y": S6y,
    "S6_v": S6v,
    "S5_y": S5y,
    "S5_v": S5v,
}
for name, target in expected.items():
    if sp.simplify(actual[name]-target) != 0:
        raise SystemExit(f"identity failed: {name}: {actual[name]} != {target}")

H6 = sp.factor(S6y*sp.symbols("B", real=True) + S6v)
H5 = sp.factor(S5y*sp.symbols("B", real=True) + S5v)

print(json.dumps({"source_hashes": observed, "sympy": sp.__version__}, sort_keys=True))
for name, value in actual.items():
    print(f"{name}={sp.sstr(sp.factor(value))}")
print(f"q0={sp.sstr(q0)}")
print(f"C0={sp.sstr(C0)}")
print(f"z_y={sp.sstr(z_y)}")
print(f"z_v={sp.sstr(z_v)}")
print(f"H6={sp.sstr(H6)}")
print(f"H5={sp.sstr(H5)}")
print(f"divisibility_checks={divisibility_checks}")
print("validity_predicate=all exact identities passed")
