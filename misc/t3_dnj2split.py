# -*- coding: utf-8 -*-
"""t3_dnj2split: robust Q0/Q1 split of dNJ2dt = Q0(w) + sqrt(w(1-w))*Q1(w)."""
import sympy as sp, pickle

with open('misc/t3_dNJ2dt_parity.pkl','rb') as fh: d = pickle.load(fh)
E0e, E0o = d['E0e'], d['E0o']
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)
v, u = sp.symbols('v u', positive=True)
# substitute sqrt(w) -> v, sqrt(1-w) -> u, w -> v^2 in both
E0e2 = sp.expand(E0e.subs({w: v**2, sp.sqrt(w): v, sp.sqrt(1-w): u}))
E0o2 = sp.expand(E0o.subs({w: v**2, sp.sqrt(w): v, sp.sqrt(1-w): u}))
# E0e should be pure polynomial in w -> in v^2
E0e2 = sp.expand(E0e2)
print('E0e2 has u?', E0e2.has(u), ' has v-odd?', (lambda e: any(m[0]%2==1 for m in sp.Poly(e, v).monoms()))(E0e2) if False else 'n/a')
# E0o: split u^0/u^1 then v parity
O0 = sp.expand(E0o2.subs(u, 0))
O1 = sp.expand((E0o2 - O0)/u)
O0e = sp.expand(O0.subs(v, 0)); O0o = sp.expand((O0-O0e)/v)
O1e = sp.expand(O1.subs(v, 0)); O1o = sp.expand((O1-O1e)/v)
def to_w(e): return sp.expand(sp.expand(e).subs(v**2, w))
R1a, R1b, R2a, R2b = to_w(O0e), to_w(O0o), to_w(O1e), to_w(O1o)
print('R1a terms:', len(sp.Add.make_args(R1a)), ' R1b:', len(sp.Add.make_args(R1b)), ' R2a:', len(sp.Add.make_args(R2a)), ' R2b:', len(sp.Add.make_args(R2b)))
# dNJ2dt = E0e(w) + sqrt(w)*E0o = E0e + v*(O0 + u*O1) = E0e + v*O0e + v^2*O0o + v*u*O1e + v*u*v*O1o... 
# wait: v*O1 has v*O1e + v^2*O1o terms. So:
# dNJ2dt = E0e + v*O0e + v^2*O0o + v*u*O1e + v^2*u*O1o
#        = [E0e + w*O0o] + sqrt(w)*O0e + sqrt(w(1-w))*O1e + w*sqrt(w(1-w))*O1o
Q0 = sp.expand(E0e + w*O0o)
Q1 = sp.expand(O0e)          # coeff of sqrt(w) -- should be 0? since dNJ2dt has no sqrt(w) alone?
Q2 = sp.expand(O1e)          # coeff of sqrt(w(1-w))
Q3 = sp.expand(O1o)          # coeff of w*sqrt(w(1-w))
print('Q0 terms:', len(sp.Add.make_args(Q0)))
print('Q1 (=sqrt(w) coeff):', Q1)
print('Q3 (=w sqrt(w(1-w)) coeff):', Q3)
# verify
recon = Q0 + sp.sqrt(w)*Q1 + sp.sqrt(w*(1-w))*Q2 + w*sp.sqrt(w*(1-w))*Q3
dNJ2r = sp.expand(d['E0e']) + sp.sqrt(w)*sp.expand(d['E0o'])
diff = sp.expand(sp.expand(recon - dNJ2r))
print('recon-diff zero?', diff == 0)
print('Q2 =', sp.factor(Q2))
print('Q0 =', sp.factor(Q0))
