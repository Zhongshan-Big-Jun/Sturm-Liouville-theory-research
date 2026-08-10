# -*- coding: utf-8 -*-
"""Session 54n: reduced norm ntilde in alpha-coordinates; factor ntilde2-ntilde1.
EVIDENCE/symbolic exploration."""
import sympy as sp
A,B,m,s = sp.symbols('A B m s', positive=True)
W = sp.sin(A)**2 + m**2*sp.cos(A)**2
WB = sp.sin(B)**2 + m**2*sp.cos(B)**2
# X=alpha(A): sinX=sinA/sqrt(W), cosX=m cosA/sqrt(W); Y likewise
# sin(X+Y), cos(X+Y)
sX = sp.sin(A)/sp.sqrt(W); cX = m*sp.cos(A)/sp.sqrt(W)
sY = sp.sin(B)/sp.sqrt(WB); cY = m*sp.cos(B)/sp.sqrt(WB)
sXY = sp.expand(sX*cY + cX*sY)          # sin(X+Y)
cXY = sp.expand(cX*cY - sX*sY)          # cos(X+Y)
psi = sp.pi - sp.asin(sX)*0  # psi = pi - X - Y -> sin psi = sin(X+Y), cos psi = -cos(X+Y)
sp2 = sXY; cp2 = -cXY
# sin(2X), sin(2Y)
s2X = 2*sX*cX; s2Y = 2*sY*cY
C2 = W/WB
# n = nL + nM + nR with phases (A,psi,B) and s
nL = A/(m*s)/(2*s**2) - sp.sin(2*A)/(4*m*s**3)
X0 = sp.sin(A)/m; Y0 = sp.cos(A)
nM = (1/s**3)*(W*psi/(2*m**2) + (X0**2-Y0**2)*sp.sin(2*psi)/4 + X0*Y0*sp.sin(psi)**2)
nR = C2*(B/(m*s)/(2*s**2) - sp.sin(2*B)/(4*m*s**3))
n = sp.simplify(nL+nM+nR)
# substitute psi trigs
n = sp.simplify(n.subs({sp.sin(2*psi):2*sp2*cp2, sp.sin(psi)**2:sp2**2, sp.sin(psi):sp2, sp.cos(psi):cp2}))
n = sp.simplify(n.subs(sp.sin(2*psi), 2*sp2*cp2).subs(sp.sin(psi)**2, sp2**2).subs(sp.sin(psi),sp2).subs(sp.cos(psi),cp2))
# reduce sqrt: set sq = sqrt(W)*sqrt(WB)?? messy; instead substitute t = sqrt(W)
# try: multiply by sqrt(W)*sqrt(WB) denominators
print("n after substitution (may still contain sqrts):")
print(sp.simplify(n))
