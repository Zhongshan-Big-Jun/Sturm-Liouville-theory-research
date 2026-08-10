# -*- coding: utf-8 -*-
"""t3_Gx_c12c.py: Gx(x,x/2) as rational fn of (s,b,x) via parity substitution."""
import sympy as sp
s, b, S, C, x = sp.symbols('s b S C x', positive=True)
th = x/2
N = (C**6*b**4*s**3*th**2 - C**6*b**3*s**4*th**2*x + C**6*b**3*s**2*th**2*x + C**6*b**2*s**5*th**2 - C**6*b*s**6*th**2*x
     + 2*C**5*S*b**3*s**2*th*x + C**5*S*b**2*s**3*th*x**2 + 2*C**5*S*b**2*s*th*x**2 - 2*C**5*S*b*s**4*th*x + 3*C**5*S*s**5*th*x**2
     + C**4*S**2*b**5*s**2*th**2*x + 2*C**4*S**2*b**4*s**3*th**2 + C**4*S**2*b**3*s**4*th**2*x + 3*C**4*S**2*b**3*s**2*th**2*x
     + 2*C**4*S**2*b**2*s**5*th**2 + C**4*S**2*b**2*s*x**2 + 2*C**4*S**2*b*s**2*x**3 + C**4*S**2*b*x**3 - 3*C**4*S**2*s**3*x**2
     - C**3*S**3*b**4*s*th*x**2 + 6*C**3*S**3*b**3*s**2*th*x - 4*C**3*S**3*b**2*s**3*th*x**2 + 4*C**3*S**3*b**2*s*th*x**2
     - 2*C**3*S**3*b*s**4*th*x + C**3*S**3*s**5*th*x**2
     + C**2*S**4*b**4*s**3*th**2 + C**2*S**4*b**3*s**4*th**2*x + 3*C**2*S**4*b**3*s**2*th**2*x - 2*C**2*S**4*b**3*x**3
     + C**2*S**4*b**2*s**5*th**2 + 4*C**2*S**4*b**2*s*x**2 + C**2*S**4*b*s**6*th**2*x + C**2*S**4*b*x**3
     + C*S**5*b**4*s*th*x**2 + 4*C*S**5*b**3*s**2*th*x - C*S**5*b**2*s**3*th*x**2 + 2*C*S**5*b**2*s*th*x**2
     - S**6*b**5*s**2*th**2*x - S**6*b**3*s**4*th**2*x + S**6*b**3*s**2*th**2*x)
# substitute parity-wise: even-even -> powers of S^2,C^2; odd-odd -> SC*(S^2)^k(C^2)^m
def parity_sub(expr):
    expr = sp.expand(expr)
    out = 0
    for term in sp.Add.make_args(expr):
        pS = sp.Poly(term, S).degree() if term.has(S) else 0
        pC = sp.Poly(term, C).degree() if term.has(C) else 0
        rest = term
        rest = rest.subs(S**pS, 1) if pS else rest
        rest = rest.subs(C**pC, 1) if pC else rest
        # now rest is the coefficient; but need to remove S^pS C^pC properly
        rest = term
        if pS or pC:
            # divide out
            rest = sp.expand(term / (S**pS * C**pC))
        sc = (pS % 2) * (pC % 2)  # 1 if both odd
        if sc:
            e = (s/2) * ( (1+b)/2 )**((pS-1)//2) * ( (1-b)/2 )**((pC-1)//2)
        else:
            e = ( (1+b)/2 )**(pS//2) * ( (1-b)/2 )**(pC//2)
        out += rest * e
    return sp.expand(out)

Np = parity_sub(N)
Np = sp.expand(Np)
print('N on c=1/2 curve:')
print(Np)
print('terms:', len(sp.Add.make_args(Np)))
Gx = 2*x*Np/(s*(x*s*(1+b)/2)**3)
Gx = sp.cancel(Gx)
print()
print('Gx(x,x/2) =')
print(sp.factor(sp.expand(sp.numer(Gx))))
print('/')
print(sp.factor(sp.expand(sp.denom(Gx))))
