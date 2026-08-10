# -*- coding: utf-8 -*-
"""Adversarial review scratch: verify chains 1-4 in SL_gap_n1_O3a_phase_rigidity_proof.tex"""
import sympy as sp

pi = sp.pi
q, w, A = sp.symbols('q w A', positive=True)

# ---------- Symbolic: M2 = d_w IN, d_q M2 ----------
IN = (q**2+w**2)*A*(2*A*q-3*w+2*sp.atan(w)) - 3*w*q*(1+w**2)*sp.atan(w)
dIN_dw = sp.simplify(sp.diff(IN, w))
M2 = 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + sp.atan(w)*(4*A*w-5*q-9*q*w**2)
print("M2 == d_w IN :", sp.simplify(dIN_dw - M2) == 0)

Aq = sp.simplify(sp.diff(sp.pi - sp.atan(w/q), q))  # = w/(q^2+w^2)
print("A_q =", Aq)
# d_q M2 with chain rule dA/dq = w/(q^2+w^2)
t = sp.atan(w)
M2sym = 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + t*(4*A*w-5*q-9*q*w**2)
dM2_dq = sp.simplify(sp.diff(M2sym, q).subs(sp.Derivative(A,q), Aq))
# manual decomposition
manual = (4*A**2*w + 8*A*w**2*q/(q**2+w**2) - 7*w*q**2/(q**2+w**2) - 14*A*q - 9*w**3/(q**2+w**2)
          + 2*w/(1+w**2) + 4*A*q/(1+w**2) + t*(4*w**2/(q**2+w**2) - 5 - 9*w**2))
print("d_q M2 manual == sympy:", sp.simplify(dM2_dq - manual) == 0)

# ---------- Symbolic: IN = G2 * POS ----------
# G(x;c) with x=A=pi-gamma, c=atan(w)/A, Phi_q(pi-gamma) in terms of q,w:
# tan(gamma)=w/q -> sin^2 gamma = w^2/(q^2+w^2), cos^2 gamma = q^2/(q^2+w^2)
Phi = sp.simplify((q**2+q**2*w**2 + w**2)/(q**2+w**2))  # cos^2 + q^2 sin^2 with cos^2=q^2/(q^2+w^2)
x = A
c = sp.atan(w)/A
D = q + c*Phi
# cot x = -cot gamma = -q/w ; sin x cos x = -sin gamma cos gamma = -q w/(q^2+w^2)
G2 = -Phi*(3 + 2*x*(-q/w))/D + 2*c*x*Phi*(q**2-1)*(-q*w/(q**2+w**2))/D**2
POS = (q + c*Phi)**2*A*(q**2+w**2)*w/(Phi*q)
print("IN == G2*POS (sympy simplify zero):", sp.simplify(IN - G2*POS) == 0)

# ---------- P(x) identity ----------
x = sp.symbols('x', positive=True)
P1 = 3*x**2 + 6*x*sp.sin(x) - 3*pi*x - 3*pi*sp.sin(x) + pi**2
P2 = (pi-3*x)**2 + 3*(x-sp.sin(x))*(pi-2*x)
print("P identity:", sp.simplify(P1-P2) == 0)

# ---------- B(q) and B'(q) exact expressions ----------
q = sp.symbols('q', positive=True)
B = (4*pi**2+14)*sp.sqrt(2*q+1) + 8*pi*(2*q+1)/q + 1 + 2*pi*(2*q+1)/q**2 - 10*pi*q
Bp = sp.simplify(sp.diff(B, q))
print("B' =", sp.simplify(Bp))
print("B'(20) exact-ish:", sp.N(Bp.subs(q,20), 40))
print("(4pi^2+14)/sqrt(41) - 10pi =", sp.N((4*pi**2+14)/sp.sqrt(41) - 10*pi, 40))
print("B(20) =", sp.N(B.subs(q,20), 40))
