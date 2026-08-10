# -*- coding: utf-8 -*-
"""Sign-classify with sign-adjusted variables (u=-cos2x>0, v=-sin4x>0) on B1."""
import sympy as sp
x, c, q = sp.symbols('x c q', positive=True)
sx = sp.sin(x); cx = sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x/sx*cx
Wp = 2*cx/sx - 2*x/sx**2
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
dPhi = 2*sc*(q**2-1); dD = c*dPhi; dsc = cx**2 - sx**2
term1 = -Ph*W/D; term2 = 2*c*x*Ph*(q**2-1)*sc/(D**2)
dt1 = -(dPhi*W + Ph*Wp)/D + Ph*W*dD/(D**2)
A = 2*c*(q**2-1)
num2 = A*(x*dPhi*sc + Ph*dsc + Ph*sc)
dt2 = num2/(D**2) - 2*c*x*Ph*(q**2-1)*sc*2*dD/(D**3)
Gx_expr = sp.simplify(dt1 + dt2)
dt1c = Ph*W*Ph/(D**2)
dt2c = 2*x*Ph*(q**2-1)*sc/(D**2) - 2*(2*c*x*Ph*(q**2-1)*sc)*Ph/(D**3)
Gc_expr = sp.simplify(dt1c + dt2c)
xp = -x*Ph/D
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)
num, den = sp.fraction(sp.together(J))
num = sp.expand(num)

s, C, S2, C2, S4 = sp.symbols('s C S2 C2 S4')
u, v = sp.symbols('u v', positive=True)
num_sub = num.subs(sp.sin(2*x), S2).subs(sp.cos(2*x), -u).subs(sp.sin(4*x), -v)
num_sub = num_sub.subs(sp.sin(x), s).subs(sp.cos(x), C)
num_sub = sp.expand(num_sub)
terms = sp.Add.make_args(num_sub)
from sympy import Mul, Pow, Symbol
pos_syms = {s, C, S2, x, c, q, u, v}
def rest_sign(expr):
    if isinstance(expr, Symbol):
        return 1 if expr in pos_syms else None
    if isinstance(expr, Pow):
        base, e = expr.as_base_exp()
        sg = rest_sign(base)
        return sg if sp.Integer(e).is_odd else 1
    if isinstance(expr, Mul):
        prod = 1
        for a_ in expr.args:
            sg = rest_sign(a_)
            if sg is None: return None
            prod *= sg
        return prod
    return None
pos_cnt = 0; neg_cnt = 0; mixed = []
for t in terms:
    numc, rest = t.as_coeff_Mul()
    if not numc.is_number:
        mixed.append((t,'non-numeric coeff')); continue
    csign = sp.sign(numc)
    rs = rest_sign(rest)
    if rs is None:
        mixed.append((t,'unknown')); continue
    if csign*rs > 0: pos_cnt += 1
    elif csign*rs < 0: neg_cnt += 1
    else: mixed.append((t,'zero'))
print("after sign adjustment: positive %d, negative %d, unknown %d" % (pos_cnt, neg_cnt, len(mixed)))
for t,why in mixed[:10]: print("  MIXED:", sp.sstr(t)[:150], "|", why)
# save negative terms
neg_terms = []
for t in terms:
    numc, rest = t.as_coeff_Mul()
    if not numc.is_number: continue
    csign = sp.sign(numc); rs = rest_sign(rest)
    if rs is not None and csign*rs < 0:
        neg_terms.append((csign, rest))
print("sample negative terms:")
for cs, rs in neg_terms[:12]:
    print("   coeff sign=%s rest=%s" % (cs, sp.sstr(rs)[:100]))
