# -*- coding: utf-8 -*-
"""Adaptive interval subdivision count for key claims (Jc<0 on B1, Jq>0 on B1, Jc>0 on B2, J<0 face B2)."""
import mpmath as mp
iv = mp.iv
iv.dps = 40

def Phi_iv(x, q): return iv.cos(x)**2 + q*q*iv.sin(x)**2

def G_iv(x, c, q):
    Ph = Phi_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    return -Ph*W/D + 2*c*x*Ph*(q*q-1)*iv.sin(x)*iv.cos(x)/(D*D)

def Gc_iv(x, c, q):
    Ph = Phi_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    sc = iv.sin(x)*iv.cos(x)
    return Ph*W*Ph/(D*D) + 2*x*Ph*(q*q-1)*sc/(D*D) - 2*(2*c*x*Ph*(q*q-1)*sc)*Ph/(D**3)

def Gx_iv(x, c, q):
    Ph = Phi_iv(x, q); D = q + c*Ph; W = 3 + 2*x/iv.tan(x)
    sx = iv.sin(x); cx = iv.cos(x); sc = sx*cx
    dPh = 2*sc*(q*q-1); dW = 2/iv.tan(x) - 2*x/(sx**2); dD = c*dPh; dsc = cx**2 - sx**2
    dt1 = -(dPh*W + Ph*dW)/D + Ph*W*dD/(D**2)
    A = 2*c*(q*q-1)
    num2 = A*(x*dPh*sc + Ph*dsc + Ph*sc)
    dt2 = num2/(D**2) - 2*c*x*Ph*(q*q-1)*sc*2*dD/(D**3)
    return dt1 + dt2

def J_iv(x, c, q):
    Ph = Phi_iv(x, q); D = q + c*Ph
    xp = -x*Ph/D
    Gv = G_iv(x, c, q)
    return Gv*Gv + Gx_iv(x, c, q)*xp + Gc_iv(x, c, q)

def Jc_iv(x, c, q):
    h = iv.mpf('1e-8')  # NOT valid for intervals; need symbolic Jc. fallback: skip
    raise NotImplementedError

# Instead: Jc via finite diff is not rigorous. We'll do symbolic derivative via mpmath? 
# mpmath.iv has no symbolic diff. Use centered difference with iv? Not rigorous.
# => For Jc, Jq we need explicit formulas. Let me derive Jc, Jq symbolically with sympy once and eval via lambdify with iv.
import sympy as sp
X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
Wp = 2*cx/sx - 2*X/sx**2
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
dPhi = 2*sc*(Q**2-1); dD = C*dPhi; dsc = cx**2 - sx**2
term1 = -Ph*W/D; term2 = 2*C*X*Ph*(Q**2-1)*sc/(D**2)
dt1 = -(dPhi*W + Ph*Wp)/D + Ph*W*dD/(D**2)
A = 2*C*(Q**2-1)
num2 = A*(X*dPhi*sc + Ph*dsc + Ph*sc)
dt2 = num2/(D**2) - 2*C*X*Ph*(Q**2-1)*sc*2*dD/(D**3)
Gx_expr = sp.simplify(dt1 + dt2)
dt1c = Ph*W*Ph/(D**2)
dt2c = 2*X*Ph*(Q**2-1)*sc/(D**2) - 2*(2*C*X*Ph*(Q**2-1)*sc)*Ph/(D**3)
Gc_expr = sp.simplify(dt1c + dt2c)
xp = -X*Ph/D
Gp = sp.simplify(Gx_expr*xp + Gc_expr)
J = sp.simplify(G**2 + Gp)
Jc = sp.simplify(sp.diff(J, C))
Jq = sp.simplify(sp.diff(J, Q))

from mpmath import iv as ivm
Jc_l = sp.lambdify((X,C,Q), Jc, modules='mpmath')
Jq_l = sp.lambdify((X,C,Q), Jq, modules='mpmath')
J_l = sp.lambdify((X,C,Q), J, modules='mpmath')

def box_eval(f, box):
    x, c, q = box
    try:
        r = f(x, c, q)
        return r
    except Exception as e:
        return None

def certify(f, box, want_pos, depth=0, maxdepth=14):
    r = box_eval(f, box)
    if r is None: return None, 1, 0
    if want_pos and r.a > 0: return True, 1, 0
    if (not want_pos) and r.b < 0: return True, 1, 0
    if depth >= maxdepth: return None, 1, 0
    x, c, q = box
    xm = (x.a+x.b)/2; cm = (c.a+c.b)/2; qm = (q.a+q.b)/2
    subs = [
        (iv.mpf([x.a,xm]), iv.mpf([c.a,cm]), iv.mpf([q.a,qm])),
        (iv.mpf([xm,x.b]), iv.mpf([c.a,cm]), iv.mpf([q.a,qm])),
        (iv.mpf([x.a,xm]), iv.mpf([cm,c.b]), iv.mpf([q.a,qm])),
        (iv.mpf([xm,x.b]), iv.mpf([cm,c.b]), iv.mpf([q.a,qm])),
        (iv.mpf([x.a,xm]), iv.mpf([c.a,cm]), iv.mpf([qm,q.b])),
        (iv.mpf([xm,x.b]), iv.mpf([c.a,cm]), iv.mpf([qm,q.b])),
        (iv.mpf([x.a,xm]), iv.mpf([cm,c.b]), iv.mpf([qm,q.b])),
        (iv.mpf([xm,x.b]), iv.mpf([cm,c.b]), iv.mpf([qm,q.b])),
    ]
    ok = True; total = 1; leaves = 0
    for sb in subs:
        st, n, lf = certify(f, sb, want_pos, depth+1, maxdepth)
        if st is None: ok = False
        total += n; leaves += lf
    if ok and leaves == 0: return True, total, 0
    return (True if ok else None), total, leaves+1

iv.dps = 40
B1 = (iv.mpf([mp.mpf('0.8411'), mp.mpf('1.1220')]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')]), iv.mpf([mp.mpf(1), mp.mpf(2)]))
B2 = (iv.mpf([mp.mpf('2.0944'), mp.mpf('2.4859')]), iv.mpf([mp.mpf('0.4'), mp.mpf('0.5')]), iv.mpf([mp.mpf(1), mp.mpf(2)]))
for name, box, f, want_pos in [
    ("Jc<0 on B1", B1, Jc_l, False),
    ("Jq>0 on B1", B1, Jq_l, True),
    ("Jc>0 on B2", B2, Jc_l, True),
]:
    st, n, lf = certify(f, box, want_pos, maxdepth=10)
    print("%s: status=%s boxes=%d unresolved_leaves=%d" % (name, st, n, lf))
