# -*- coding: utf-8 -*-
# Symbolic simplification of Fep(q,1/2). EVIDENCE.
import sympy as sp

q, x = sp.symbols('q x', positive=True)
c = sp.Rational(1,2)
# cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1)
Phi = sp.Rational(2)*q**2/(q+1)
D = q*(2*q+1)/(q+1)
M1 = x**2/(q*(q+1))
M2 = (sp.pi-x)**2/(q*(q+1))
G1 = -Phi*(3+2*x*sp.cot(x))/D + x*Phi*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2
G2 = -Phi*(3-2*(sp.pi-x)*sp.cot(x))/D - (sp.pi-x)*Phi*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2
Fep = M1*G1 - M2*G2

# substitute sin x, cos x, cot x in terms of q
sx = sp.sqrt(2*q+1)/(q+1)
cx = q/(q+1)
Fep2 = Fep.subs({sp.sin(x): sx, sp.cos(x): cx})
Fep2 = sp.simplify(Fep2)
print('Fep(q,1/2) simplified:')
print(Fep2)
print()
Fep3 = sp.factor(Fep2)
print('Fep factored:')
print(Fep3)
