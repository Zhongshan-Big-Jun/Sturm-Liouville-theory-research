import sympy as sp
from sympy import symbols, expand
A, sg, cg, st, ct, t = symbols('A sg cg st ct t')
B1 = A*cg - 2*sg
B2 = 4*A**2*cg**2 - A**2 - 12*A*cg*sg + 6*sg**2
W1 = -2*A**3*B1*st**2*ct**4
W2 = A**2*cg*B2*st**2*ct**2
z_ = symbols('z_')
d12 = expand(W1 + W2 - z_*(1-z_)*(A**2*cg*B2 - 2*A**3*B1*z_))
print('d12 (before subs):', d12)
d12s = expand(d12.subs(z_, ct**2))
print('d12 after subs:', d12s)
print('is zero:', d12s == 0)
