import sympy as sp
A, psi, B, m = sp.symbols('A psi B m', positive=True)
# pieces form
I1 = (A - sp.sin(A)*sp.cos(A))/(2*m)
syb = sp.cos(psi)*sp.sin(A)/m + sp.sin(psi)*sp.cos(A)
dyb = -sp.sin(psi)*sp.sin(A)/m + sp.cos(psi)*sp.cos(A)
lam2 = sp.simplify(sp.expand(syb**2 + (dyb/m)**2))
I3 = m*(B - sp.sin(B)*sp.cos(B))/2*lam2
th = sp.symbols('th')
I2 = sp.integrate((sp.sin(A)/m*sp.cos(th) + sp.cos(A)*sp.sin(th))**2, (th, 0, psi))
Phi_p = sp.expand_trig(I1 + I2 + I3)
W = lambda x: sp.sin(x)**2 + m**2*sp.cos(x)**2
Phi_c = (m*A*W(B) + m*B*W(A) + psi*W(A)*W(B))/(2*m**2*W(B))
D = sp.simplify(sp.expand_trig(Phi_p - Phi_c))
print("D numerator factors:")
num = sp.factor(sp.together(D).as_numer_denom()[0])
print(num)
# secular expression: cos(psi)*sin(A+B) + sin(psi)*(m cosA cosB - sinA sinB/m)
sec = sp.expand_trig(sp.cos(psi)*sp.sin(A+B) + sp.sin(psi)*(m*sp.cos(A)*sp.cos(B) - sp.sin(A)*sp.sin(B)/m))
print()
print("secular:", sp.factor(sec))
# check D * something = secular^2 or similar
