import sympy as sp
q = sp.symbols('q', positive=True)
x = sp.symbols('x')
# full substitution: cos x = q/(q+1), sin x = sqrt(2q+1)/(q+1), A = pi - x
cx = q/(q+1)
sx = sp.sqrt(2*q+1)/(q+1)
A = sp.pi - x
Ph = cx**2 + q**2*sx**2
D = q + sp.Rational(1,2)*Ph
W = 3 + 2*A*(sp.cos(A)/sp.sin(A))
G2 = -Ph*W/D + 2*sp.Rational(1,2)*A*Ph*(q**2-1)*sp.sin(A)*sp.cos(A)/D**2
# replace sin(A), cos(A) with +sx, -cx (A = pi - x)
G2b = sp.simplify(G2.subs({sp.sin(A): sx, sp.cos(A): -cx}))
# remove tan etc already gone; W uses cos(A)/sin(A) -> substitute cos(A), sin(A)
G2b = sp.simplify(G2b)
cf = 2*q*sp.sqrt(1-cx)*(sp.pi - x - 3*sx)/(1+cx)**sp.Rational(3,2)
diff = sp.simplify(G2b - cf)
print('G2b =', sp.factor(G2b))
print('cf  =', sp.factor(cf))
print('diff =', sp.simplify(diff))
# also express cf in (q,x) closed form
cfq = 2*q*((sp.pi-x)*(q+1)-3*sp.sqrt(2*q+1))/(2*q+1)**sp.Rational(3,2)
print('cfq - cf =', sp.simplify(cfq - cf))
