# -*- coding: utf-8 -*-
# Symbolic: dFep/dq structure. Derive with implicit derivatives, then examine.
import sympy as sp

q, c = sp.symbols('q c', positive=True)
x1, x2 = sp.symbols('x1 x2', positive=True)  # alpha1, alpha2

def Phi(x): return sp.cos(x)**2 + q**2*sp.sin(x)**2
def Mf(x): return x**2*sp.sin(x)**2/(q + c*Phi(x))
def G(x):
    Ph = Phi(x); D = q + c*Ph
    return -Ph*(3+2*x*sp.cot(x))/D + 2*c*x*Ph*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2

# Fep = M(x1)G(x1) - M(x2)G(x2); x1, x2 functions of (q,c)
# implicit derivatives:
# even: E(x1) = c x1, E(x) = atan(1/(q tan x)): E_x = q/Phi(x) (check), E_q = tan(x)/(1+q^2 tan^2 x)
# actually E'(x) = -q/Phi(x); let me derive: E = atan(1/(q t)), t=tan x.
# dE/dx = 1/(1+(1/(q t))^2) * d/dx(1/(q t)) = (q^2 t^2/(q^2 t^2+1)) * (-sec^2 x/(q t^2)) = -q^2/(q^2 t^2+1) * sec^2 x / q = -q sec^2 x/(1+q^2 tan^2 x)
# = -q/cos^2 x / ((cos^2 x + q^2 sin^2 x)/cos^2 x) = -q/Phi(x). OK.
# dE/dq = 1/(1+(q t)^-2) * d/dq(1/(q t)) = (q^2 t^2/(1+q^2 t^2)) * (-1/(q^2 t)) = -t/(1+q^2 t^2)
# even eq: E(x1) - c x1 = 0: x1_q = -E_q/(E_x - c) = -(-t1/(1+q^2 t1^2))/(-q/Phi1 - c) = -t1/(1+q^2 t1^2)/(q/Phi1 + c)
# odd: O(x2) = c x2, O(x) for x>pi/2: O = atan(-q tan x)... complex branch. Use gamma = pi - x2:
# O(pi-gamma) = atan(q tan gamma); eq: atan(q tan gamma) - c(pi-gamma) = 0
# gamma_q = -(d/dq atan(q tan gamma))/(d/dgamma atan(q tan gamma) + c)
# d/dq atan(q t) = t/(1+q^2 t^2); d/dgamma atan(q tan gamma) = q sec^2 gamma/(1+q^2 tan^2 gamma) = q/Phi(gamma)
# gamma_q = -t_g/(1+q^2 t_g^2)/(q/Phi_g + c); x2_q = -gamma_q
t1 = sp.tan(x1); tg = sp.tan(sp.symbols('gamma', positive=True))
# Use gamma symbol
gamma = sp.symbols('gamma', positive=True)
Ph1 = Phi(x1); Phg = Phi(gamma)
x1q = -t1/(1+q**2*t1**2)/(q/Ph1 + c)
gammaq = -tg/(1+q**2*tg**2)/(q/Phg + c)
x2q = -gammaq

# x1_c, x2_c too (for completeness)
x1c = -x1/(q/Ph1 + c)   # from E_x x_c = x + ... : E_x x_c - x - c x_c = 0 -> (E_x - c)x_c = x -> x_c = x/(E_x - c) = -x/(q/Ph1+c)... check sign
# Actually: d/dc E(x1(c)) = d/dc(c x1): E_x x1_c = x1 + c x1_c -> (E_x - c) x1_c = x1 -> x1_c = x1/(E_x - c) = -x1/(q/Ph1 + c)
# hmm E_x = -q/Ph1, so E_x - c = -(q/Ph1 + c), x1_c = -x1/(q/Ph1+c). OK.
x2c = -x2/(q/Phg + c)   # alpha2 = pi - gamma, gamma_c: d/dc(atan(q tan g) - c(pi-g)) = 0: q/Phg g_c - (pi - g) + c g_c = 0 -> g_c (q/Phg + c) = pi - g -> g_c = (pi-g)/(q/Phg+c)
# x2_c = -g_c = -(pi-gamma)/(q/Phg + c). Let me just recompute below carefully with the right expression.

print('x1q =', sp.simplify(x1q))
print('gammaq =', sp.simplify(gammaq))
