# -*- coding: utf-8 -*-
"""Classify sign of each monomial of J numerator on B1 (x in (pi/4, pi/2): sin>0, cos>0, sin2>0, cos2<0, sin4<0)."""
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

# Substitute sin(x)=s, cos(x)=C, sin(2x)=S2, cos(2x)=C2, sin(4x)=S4 but keep track.
# Rewrite using these as symbols with sign info.
s, C, S2, C2, S4 = sp.symbols('s C S2 C2 S4', positive=True)
num_sub = num.subs(sp.sin(2*x), S2).subs(sp.cos(2*x), C2).subs(sp.sin(4*x), S4).subs(sp.sin(x), s).subs(sp.cos(x), C)
num_sub = sp.expand(num_sub)
terms = sp.Add.make_args(num_sub)
# sign facts on B1: s>0, C>0, S2>0, C2<0, S4<0, x>0, c>0, q>0 (q>=1)
pos_syms = {s, C, S2, x, c, q}
neg_syms = {C2, S4}
pos_cnt = 0; neg_cnt = 0; mixed = []
for t in terms:
    coeff = sp.Mul(*[a for a in t.as_coeff_Mul()]) if False else None
    # get numeric coefficient
    numc, rest = t.as_coeff_Mul()
    # sign of numc
    if numc.is_number:
        csign = sp.sign(numc)
    else:
        mixed.append((t, 'coeff not numeric'))
        continue
    # sign of rest (product of symbols with signs)
    rsign = 1
    ok = True
    for a in sp.preorder_traversal(rest):
        pass
    # instead: factor rest into powers
    rest_f = sp.factor(rest)
    # determine sign: rest is product of symbol powers
    from sympy import Mul, Pow, Symbol
    def rest_sign(expr):
        if isinstance(expr, Symbol):
            if expr in pos_syms: return 1
            if expr in neg_syms: return -1
            return None
        if isinstance(expr, Pow):
            base, e = expr.as_base_exp()
            sg = rest_sign(base)
            if sg is None: return None
            return sg if sp.Integer(e).is_odd else 1
        if isinstance(expr, Mul):
            prod = 1
            for a_ in expr.args:
                sg = rest_sign(a_)
                if sg is None: return None
                prod *= sg
            return prod
        return None
    rs = rest_sign(rest)
    if rs is None:
        mixed.append((t, 'rest sign unknown'))
        continue
    total = csign*rs
    if total > 0: pos_cnt += 1
    elif total < 0: neg_cnt += 1
    else: mixed.append((t, 'zero?'))
print("positive-sign monomials: %d, negative-sign: %d, unknown: %d" % (pos_cnt, neg_cnt, len(mixed)))
for t, why in mixed[:15]:
    print("  MIXED:", sp.sstr(t)[:120], "|", why)
