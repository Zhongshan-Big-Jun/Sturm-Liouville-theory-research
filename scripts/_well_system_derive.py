# -*- coding: utf-8 -*-
"""Derive the full good-root system for the well family in phase variables (sympy).
Equations: S1 (secular lam1), S2 (secular lam2), N1 (norm ratio), N2 (C-ratio).
Goal: look for a factor (A-B) or sign-definite structure."""
import sympy as sp

A, psi, B, tau, m = sp.symbols('A psi B tau m', positive=True)
s1 = (A + m*psi + B)/m  # exact geometric identity

def block_phase(k):
    """phases for eigenfunction k: (A_k, psi_k, B_k)."""
    return (tau**k * A, tau**k * psi, tau**k * B)

def sec_value(Ak, psik, Bk):
    """Secular function G(A,psi,B) = (cos psi sin A + m sin psi cos A)cos B
       + (-sin psi sin A/m + cos psi cos A) sin B."""
    X = sp.cos(psik)*sp.sin(Ak)/m + sp.sin(psik)*sp.cos(Ak)
    Y = -sp.sin(psik)*sp.sin(Ak)/m + sp.cos(psik)*sp.cos(Ak)
    return sp.cos(Bk)*X + (sp.sin(Bk)/m)*Y

def C_amp(Ak, psik, Bk):
    """C = m sinB X - cosB Y (right-side amplitude, y=C sin(ms(1-x))/(ms))."""
    X = sp.cos(psik)*sp.sin(Ak)/m + sp.sin(psik)*sp.cos(Ak)
    Y = -sp.sin(psik)*sp.sin(Ak)/m + sp.cos(psik)*sp.cos(Ak)
    return m*sp.sin(Bk)*X - sp.cos(Bk)*Y

def norm_block(Ak, psik, Bk, sk):
    """n_k = int rho y^2 in phases. s_k = tau^k * s1."""
    # left block
    I_left = (Ak/2 - sp.sin(2*Ak)/4)/(m*sk**3)
    # middle block: y = P cos(s xi) + Q sin(s xi), P = sinA/(m s), Q = cosA/s
    P = sp.sin(Ak)/(m*sk); Q = sp.cos(Ak)/sk
    L = psik/sk
    I_mid = P**2*(L/2 + sp.sin(2*psik)/(4*sk)) + Q**2*(L/2 - sp.sin(2*psik)/(4*sk)) \
            + 2*P*Q*sp.sin(psik)**2/(2*sk)
    # right block
    Ck = C_amp(Ak, psik, Bk)
    I_right = Ck**2*(Bk/2 - sp.sin(2*Bk)/4)/(m*sk**3)
    return sp.simplify(I_left + I_mid + I_right)

# check n1, n2
n1 = norm_block(A, psi, B, s1)
n2 = norm_block(tau*A, tau*psi, tau*B, tau*s1)
C1 = C_amp(A, psi, B)
C2 = C_amp(tau*A, tau*psi, tau*B)

print("=== S1 (secular lam1) ===")
print(sp.simplify(sp.trigsimp(sp.expand_trig(sec_value(A, psi, B)))))
print("=== S2 (secular lam2) ===")
print(sp.simplify(sp.trigsimp(sp.expand_trig(sec_value(tau*A, tau*psi, tau*B)))))
print("=== N1: n2/n1 - sin^2(tau A)/sin^2 A ===")
N1 = sp.simplify(sp.trigsimp(sp.expand_trig(n2/n1 - sp.sin(tau*A)**2/sp.sin(A)**2)))
print(sp.simplify(N1))
print("=== N2: (C2^2/C1^2) sin^2(tau B)/sin^2 B - sin^2(tau A)/sin^2 A ===")
N2 = sp.simplify(sp.trigsimp(sp.expand_trig(C2**2/C1**2*sp.sin(tau*B)**2/sp.sin(B)**2 - sp.sin(tau*A)**2/sp.sin(A)**2)))
print(sp.simplify(N2))
