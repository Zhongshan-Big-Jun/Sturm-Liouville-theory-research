# -*- coding: utf-8 -*-
"""Session 54f: sympy closed-form for n2/n1 and N1 under secular constraints."""
import sympy as sp
A,B,tau,m,s = sp.symbols('A B tau m s', positive=True)
# alpha(x) = arctan(tan x / m); use tan-form: tan alpha = tan A / m  ->  cot alpha = m cot A
# W(x) = sin^2 x + m^2 cos^2 x
W = sp.sin(A)**2 + m**2*sp.cos(A)**2
# n(s) with phases (A,psi,B) and a=A/(ms), 1-b=B/(ms), b-a=psi/s
C2 = (sp.sin(A)**2+m**2*sp.cos(A)**2)/(sp.sin(B)**2+m**2*sp.cos(B)**2)
nL = A/(m*s)/(2*s**2) - sp.sin(2*A)/(4*m*s**3)
X0 = sp.sin(A)/m; Y0 = sp.cos(A)
nM = (1/s**3)*(W*psi/(2*m**2) + (X0**2-Y0**2)*sp.sin(2*psi)/4 + X0*Y0*sp.sin(psi)**2)
nR = C2*(B/(m*s)/(2*s**2) - sp.sin(2*B)/(4*m*s**3))
n = sp.simplify(nL+nM+nR)
print("n(s) =", sp.factor(n))
# mode 2: phases scaled by tau, s -> tau*s
n2e = n.subs({A:tau*A, B:tau*B, psi:tau*psi, s:tau*s})
n1e = n
N1 = sp.simplify(n2e/n1e - sp.sin(tau*A)**2/sp.sin(A)**2)
print()
print("N1 numerator (unsimplified):")
num = sp.factor(sp.together(N1).as_numer_denom()[0])
print(sp.factor(num))
