import sympy as sp

A, psi, B, m = sp.symbols('A psi B m', positive=True)
# piece 1: (A - sinA cosA)/(2m)
I1 = (A - sp.sin(A)*sp.cos(A))/(2*m)
# piece 2 (times s^3): W(A)/m^2 * [psi/2 - (sin2(alpha+psi)-sin2 alpha)/4]
# express via sin/cos directly: y=(1/s)[(sinA/m)cos th + cosA sin th]
# int_0^psi ((sinA/m)cos th + cosA sin th)^2 dth
y2_int = sp.integrate((sp.sin(A)/m*sp.cos(sp.symbols('th')) + sp.cos(A)*sp.sin(sp.symbols('th')))**2,
                      (sp.symbols('th'), 0, psi))
# piece 3 (times s^3): (1/m) int_0^B (u cos th + v sin th)^2 dth, u=sy(b), v=dyb/m
th = sp.symbols('th')
syb = sp.cos(psi)*sp.sin(A)/m + sp.sin(psi)*sp.cos(A)
dyb = -sp.sin(psi)*sp.sin(A)/m + sp.cos(psi)*sp.cos(A)
u = syb
v = dyb/m
I3 = sp.integrate((u*sp.cos(th) + v*sp.sin(th))**2, (th, 0, B))/m

Phi = sp.simplify(sp.expand_trig(I1 + y2_int + I3))
print("Phi (times s^3) simplified:")
print(Phi)
print()
print("expected: (mA*W(B)+mB*W(A)+psi*W(A)*W(B))/(2m^2*W(B))")
W = lambda x: sp.sin(x)**2 + m**2*sp.cos(x)**2
expected = (m*A*W(B) + m*B*W(A) + psi*W(A)*W(B))/(2*m**2*W(B))
print("diff:", sp.simplify(sp.expand_trig(Phi - expected)))
