import sympy as sp
A, psi, B, m, th = sp.symbols('A psi B m th', positive=True)
# piece1 * s^3
I1 = (A - sp.sin(A)*sp.cos(A))/(2*m)
# piece2 * s^3
I2 = sp.integrate((sp.sin(A)/m*sp.cos(th) + sp.cos(A)*sp.sin(th))**2, (th, 0, psi))
# piece3 * s^3 via lambda-parametrization with Dirichlet constraint
syb = sp.cos(psi)*sp.sin(A)/m + sp.sin(psi)*sp.cos(A)
dyb = -sp.sin(psi)*sp.sin(A)/m + sp.cos(psi)*sp.cos(A)
u = syb; v = dyb/m
lam2 = sp.simplify(sp.expand(u**2 + v**2))
I3 = (1/m)*(B - sp.sin(B)*sp.cos(B))/2*lam2
Phi = sp.simplify(sp.expand_trig(I1 + I2 + I3))
W = lambda x: sp.sin(x)**2 + m**2*sp.cos(x)**2
expected = (m*A*W(B) + m*B*W(A) + psi*W(A)*W(B))/(2*m**2*W(B))
diff = sp.simplify(sp.expand_trig(Phi - expected))
print("diff (should be 0):", diff)
# also verify lam2 closed form
print("lam2:", sp.simplify(sp.expand_trig(lam2)))
