# -*- coding: utf-8 -*-
"""Full certification counts with corrected formulas."""
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 50

def iv_atan(x, nterms=160):
    a, b = x.a, x.b
    if a < 0:
        if a > -mp.mpf('1e-40'):
            a = mp.mpf(0)
        else:
            raise ValueError('atan for x >= 0 only')
    def atan_series(xx, n):
        x2 = xx*xx; xp = xx; acc = iv.mpf(0); sign = 1
        for j in range(n+1):
            d = 2*j+1
            term = xp/iv.mpf(d)
            acc = acc + term if sign > 0 else acc - term
            sign *= -1
            xp = xp*x2
        R = xx.b**(2*n+3)/iv.mpf(2*n+3)
        return iv.mpf([acc.a - R, acc.b + R])
    def atan_endpoint(pt):
        if pt <= 1:
            return atan_series(iv.mpf([pt,pt]), nterms)
        inv = iv.mpf([1,1])/iv.mpf([pt,pt])
        return iv.pi/2 - atan_series(inv, nterms)
    return iv.mpf([atan_endpoint(a).a, atan_endpoint(b).b])

X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2
D = Q + C*Ph
W = 3 + 2*X/sx*cx
sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
Gx_s = sp.simplify(sp.diff(G, X))
Gc_s = sp.simplify(sp.diff(G, C))
xp_s = -X*Ph/D
Gp_s = sp.simplify(Gx_s*xp_s + Gc_s)
J_s = sp.simplify(G**2 + Gp_s)
Jx_s = sp.simplify(sp.diff(J_s, X))
Jc_s = sp.simplify(sp.diff(J_s, C))
mods = {'sin': iv.sin, 'cos': iv.cos, 'tan': iv.tan, 'mpf': iv.mpf, 'pi': iv.pi}
Jf = sp.lambdify((X,C,Q), J_s, modules=mods)
Jxf = sp.lambdify((X,C,Q), Jx_s, modules=mods)
Jcf = sp.lambdify((X,C,Q), Jc_s, modules=mods)

def c1_iv(x, q):
    return iv_atan(1.0/(q*iv.tan(x)))/x
def c2_iv(g, q):
    return iv_atan(q*iv.tan(g))/(iv.pi - g)
def J1_2d_iv(x, q): return Jf(x, c1_iv(x,q), q)
def J2_2d_iv(g, q): return Jf(iv.pi-g, c2_iv(g,q), q)
# dJ1_2d/dx = Jx + Jc * dc1/dx ; dc1/dx = (x*dE - E)/x^2, dE = -q/Phi
def dJ1dx_iv(x, q):
    c = c1_iv(x,q)
    Phv = Ph.subs({X:x, Q:q, C:c}) if False else (iv.cos(x)**2 + q*q*iv.sin(x)**2)
    E = c*x
    dEdx = -q/Phv
    dcdx = (x*dEdx - E)/(x*x)
    return Jxf(x,c,q) + Jcf(x,c,q)*dcdx
def dJ1dq_iv(x, q):
    c = c1_iv(x,q)
    Phv = iv.cos(x)**2 + q*q*iv.sin(x)**2
    # dc1/dq = dE/dq / x ; E = atan(1/(q tan x)); dE/dq = -sin x cos x / Phi
    dEdq = -iv.sin(x)*iv.cos(x)/Phv
    dcdq = dEdq/x
    return Jf(x,c,q) # placeholder wrong; need Jq partial
# need Jq partial: dJ/dq with c fixed
Jq_s = sp.simplify(sp.diff(J_s, Q))
Jqf = sp.lambdify((X,C,Q), Jq_s, modules=mods)
def dJ1dq_iv(x, q):
    c = c1_iv(x,q)
    Phv = iv.cos(x)**2 + q*q*iv.sin(x)**2
    dEdq = -iv.sin(x)*iv.cos(x)/Phv
    dcdq = dEdq/x
    return Jqf(x,c,q) + Jcf(x,c,q)*dcdq
# dJ2_2d/dg: x = pi - g, dx/dg = -1; c2 = atan(q tan g)/(pi-g)
# dc2/dg: compute symbolically? E2(g) = atan(q tan g); c = E2/(pi-g)
# dE2/dg = q (1+tan^2 g)/(1+q^2 tan^2 g)
def dJ2dg_iv(g, q):
    x = iv.pi - g
    c = c2_iv(g,q)
    tg = iv.tan(g)
    dE2dg = q*(1+tg*tg)/(1+q*q*tg*tg)
    dc2dg = (dE2dg*(iv.pi-g) + c)/(iv.pi-g)  # d/dg [E2/(pi-g)] = (E2'(pi-g) + E2)/(pi-g)^2; E2 = c(pi-g)
    # c = E2/(pi-g) => E2 = c*(pi-g); d/dg = (E2'*(pi-g) + E2)/(pi-g)^2 = (dE2dg*(pi-g) + c*(pi-g))/(pi-g)^2
    dc2dg = (dE2dg*(iv.pi-g) + c*(iv.pi-g))/((iv.pi-g)**2)
    return Jxf(x,c,q)*(-1) + Jcf(x,c,q)*dc2dg

def certify2(f, x0, x1, q0, q1, want_pos, depth=0, maxdepth=14):
    x = iv.mpf([x0, x1]); q = iv.mpf([q0, q1])
    try:
        r = f(x, q)
    except Exception as e:
        return None, 1, 0, str(e)[:60]
    if want_pos and r.a > 0: return True, 1, 0, ''
    if (not want_pos) and r.b < 0: return True, 1, 0, ''
    if depth >= maxdepth: return None, 1, 0, 'depth'
    xm = (x0+x1)/2; qm = (q0+q1)/2
    subs = [(x0,xm,q0,qm),(xm,x1,q0,qm),(x0,xm,qm,q1),(xm,x1,qm,q1)]
    ok = True; total = 1; leaves = 0; err = ''
    for (a,b,c,d) in subs:
        st, n, lf, e = certify2(f, a, b, c, d, want_pos, depth+1, maxdepth)
        if st is None: ok = False
        if e and not err: err = e
        total += n; leaves += lf
    return (True if ok else None), total, leaves, err

tests = [
    ("J1_2d>0", lambda x,q: J1_2d_iv(x,q), mp.mpf('0.8411'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), True),
    ("J2_2d<0", lambda g,q: J2_2d_iv(g,q), mp.mpf('0.6557'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2), False),
    ("dJ1_2d/dx>0", dJ1dx_iv, mp.mpf('0.8411'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), True),
    ("dJ1_2d/dq>0", dJ1dq_iv, mp.mpf('0.8411'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), True),
    ("dJ2_2d/dg>0 [0.695,pi/3]", dJ2dg_iv, mp.mpf('0.695'), mp.pi/3, mp.mpf(1), mp.mpf(2), True),
]
for name, f, x0, x1, q0, q1, wp in tests:
    st, n, lf, e = certify2(f, x0, x1, q0, q1, wp, maxdepth=12)
    print("%s: status=%s boxes=%d leaves=%d err=%s" % (name, st, n, lf, e))
