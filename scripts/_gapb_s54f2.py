# -*- coding: utf-8 -*-
"""Session 54f: sympy closed-form for n2/n1 and N1 under secular constraints."""
import sympy as sp
A,B,tau,m,s,psi = sp.symbols('A B tau m s psi', positive=True)
W = sp.sin(A)**2 + m**2*sp.cos(A)**2
C2 = (sp.sin(A)**2+m**2*sp.cos(A)**2)/(sp.sin(B)**2+m**2*sp.cos(B)**2)
nL = A/(m*s)/(2*s**2) - sp.sin(2*A)/(4*m*s**3)
X0 = sp.sin(A)/m; Y0 = sp.cos(A)
nM = (1/s**3)*(W*psi/(2*m**2) + (X0**2-Y0**2)*sp.sin(2*psi)/4 + X0*Y0*sp.sin(psi)**2)
nR = C2*(B/(m*s)/(2*s**2) - sp.sin(2*B)/(4*m*s**3))
n = sp.simplify(nL+nM+nR)
n2e = n.subs({A:tau*A, B:tau*B, psi:tau*psi, s:tau*s})
N1 = sp.together(n2e/n - sp.sin(tau*A)**2/sp.sin(A)**2)
num = sp.factor(sp.together(N1).as_numer_denom()[0])
print("N1 numerator factors:")
print(sp.factor(num))
# substitute psi = pi - alpha(A) - alpha(B); tan alpha = tan A/m: express via cot alpha = m cot A
# alpha in (0,pi): sin alpha = sin A/sqrt(W(A)), cos alpha = m cos A/sqrt(W(A))
# psi = pi - alphaA - alphaB: sin psi = sin(alphaA+alphaB)? no: sin(pi-x-y)=sin(x+y)
#   sin psi = sin(alphaA+alphaB) = sinA cosB m cosB/sqrt(WA WB)*... messy. Instead substitute cot psi via cot(alphaA+alphaB) with sign.
# Let's substitute tan(psi/2) using tan((pi-aA-aB)/2) = cot((aA+aB)/2) via tan-half-angle.
# Try simpler: substitute numerically later; first check if N1 factors under E=0 (r(A)=r(B)) via elimination.
print()
print("=== Now impose E=0: sin^2(alpha(tauA))/sin^2(alpha(A)) = sin^2(alpha(tauB))/sin^2(alpha(B)) ===")
print("(will handle numerically / via elimination in a separate pass)")
