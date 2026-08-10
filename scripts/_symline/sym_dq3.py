# -*- coding: utf-8 -*-
# dFep/dq expanded; evaluate pieces numerically via lambdify-free approach: print expanded form
import sympy as sp

q, c = sp.symbols('q c', positive=True)
x1, x2 = sp.symbols('x1 x2', positive=True)

def Phi(x): return sp.cos(x)**2 + q**2*sp.sin(x)**2
def M(x): return x**2*sp.sin(x)**2/(q + c*Phi(x))
def G(x):
    Ph = Phi(x); D = q + c*Ph
    return -Ph*(3+2*x*sp.cot(x))/D + 2*c*x*Ph*(q**2-1)*sp.sin(x)*sp.cos(x)/D**2

x1q = -sp.sin(x1)*sp.cos(x1)/(q + c*Phi(x1))
x2q = -sp.sin(x2)*sp.cos(x2)/(q + c*Phi(x2))

Fep = M(x1)*G(x1) - M(x2)*G(x2)
dFdq = sp.diff(Fep, q) + sp.diff(Fep, x1)*x1q + sp.diff(Fep, x2)*x2q
# expand and group
ex = sp.expand(dFdq)
print('num terms:', len(sp.Add.make_args(ex)))
# count by structure
terms = sp.Add.make_args(ex)
from collections import Counter
cnt = Counter()
for t in terms:
    cnt[str(t.func)] += 1
print(cnt)
# Save expanded expression to file for inspection
with open('scripts/_symline/dFdq_expanded.txt','w') as f:
    f.write(sp.sstr(ex))
print('saved; length', len(sp.sstr(ex)))
