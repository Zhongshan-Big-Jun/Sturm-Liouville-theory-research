import sympy as sp
A,B,psi,m,tau,s = sp.symbols('A B psi m tau s', positive=True)
# s1 = (A+m*psi+B)/m ; tau = s2/s1 free; mode-2 phases = tau*A etc.
# closed-form norm for wave number s with phases (msa->A etc.), normalized: n(s) with slope normalization
W = lambda t: sp.sin(t)**2 + m**2*sp.cos(t)**2
X0 = sp.sin(A)/m; Y0 = sp.cos(A)
# need a, 1-b in terms of phases: a = A/(m s), 1-b = B/(m s), b-a = psi/s
# nL = a/(2s^2) - sin(2A)/(4 m s^3)
# nM = (1/s^3)[ W(A) psi/(2 m^2) + (X0^2-Y0^2) sin(2 psi)/4 + X0 Y0 sin^2 psi ]
# nR = C^2 [(1-b)/(2s^2) - sin(2B)/(4 m s^3)], C^2 = W(A)/W(B)
C2 = W(A)/W(B)
nL = A/(m*s)/(2*s**2) - sp.sin(2*A)/(4*m*s**3)
nM = (1/s**3)*(W(A)*psi/(2*m**2) + (X0**2-Y0**2)*sp.sin(2*psi)/4 + X0*Y0*sp.sin(psi)**2)
nR = C2*(B/(m*s)/(2*s**2) - sp.sin(2*B)/(4*m*s**3))
n = sp.simplify(nL+nM+nR)
print("n(s) simplified:", sp.simplify(n))
# N1 = n(tau s)/n(s) - sin^2(tau A)/sin^2 A, with the SAME phases scaled by tau for mode 2:
# but A,B,psi are the MODE-1 phases; mode-2 phases are tau*A, tau*B, tau*psi and s2 = tau*s1.
n2 = n.subs({A:tau*A, B:tau*B, psi:tau*psi, s:tau*s})
N1 = sp.simplify(n2/n - sp.sin(tau*A)**2/sp.sin(A)**2)
print("N1 structure (unsimplified):")
print(N1)
# factor attempt
print("factor:", sp.factor(N1))
