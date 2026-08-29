"""Exact algebraic rank and uniqueness check for the corrected seed."""

import sympy as sp

K,B,q,C=sp.symbols("K B q C", positive=True)
F1=-sp.sqrt(2)*(K**3+6*K*q-18*sp.pi+24)/(24*K)
F2=sp.sqrt(2)*(3*sp.pi*C*K+K**3+6*K*q-18*sp.pi-24)/(24*K)
J1=sp.factor(sp.Matrix([F1,F2]).jacobian([q,C]).det())
H6=8*(B*K-1)/K**2
H5=2*(6*sp.pi**2*B*K+sp.pi*K**3-24*sp.pi**2+48)/(3*sp.pi*K**6)
J2=sp.factor(sp.Matrix([H6,H5]).jacobian([B,K]).det())
J2seed=sp.factor(J2.subs(B,1/K))
J2root=sp.factor(J2seed.subs(K**3,18*sp.pi-48/sp.pi))
seed_poly=sp.factor((sp.pi*K**3-18*sp.pi**2+48)/sp.pi)
print(f"FIRST_JACOBIAN={J1}")
print(f"SECOND_JACOBIAN={J2}")
print(f"SECOND_JACOBIAN_AT_BK1={J2seed}")
print(f"SECOND_JACOBIAN_AT_SEED={J2root}")
print(f"SEED_EQUATION={seed_poly}")
print(f"SEED_DERIVATIVE={sp.diff(seed_poly,K)}")
print(f"POSITIVE_RADICAND={sp.N(18*sp.pi-48/sp.pi,50)}")
print(f"K0={sp.N((18*sp.pi-48/sp.pi)**(sp.Rational(1,3)),50)}")
