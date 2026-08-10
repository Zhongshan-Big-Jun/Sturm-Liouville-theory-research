import sympy as sp
g, q = sp.symbols('g q', positive=True)
A = sp.pi - g
t = sp.atan(q*sp.tan(g))
sg, cg = sp.sin(g), sp.cos(g)
st, ct = sp.sin(t), sp.cos(t)
D = A*st*ct + t*sg*cg
Phi = cg*cg + q*q*sg*sg
c = t/A
# J = G^2 + Gc - u*Gx with doc's G (x=A):
x = A
Gx0 = -Phi*(3 + 2*x*sp.cot(x))/(q + c*Phi) + 2*c*x*Phi*(q*q-1)*sp.sin(x)*sp.cos(x)/(q+c*Phi)**2
u = x*Phi/(q + c*Phi)
Gc0 = sp.diff(Gx0, c)
Gx_x = sp.diff(Gx0, x)
J = sp.simplify(Gx0**2 + Gc0 - u*Gx_x)
print('J (simplified):')
print(J)
