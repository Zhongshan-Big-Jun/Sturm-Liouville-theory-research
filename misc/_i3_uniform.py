# -*- coding: utf-8 -*-
"""Uniform-grid certification for J2_2d<0 (and J1_2d>0) with corrected formulas."""
import sympy as sp
import mpmath as mp
iv = mp.iv
iv.dps = 50
def iv_atan(x, nterms=160):
    a, b = x.a, x.b
    if a < 0:
        if a > -mp.mpf('1e-40'): a = mp.mpf(0)
        else: raise ValueError('atan for x >= 0 only')
    def atan_series(xx, n):
        x2 = xx*xx; xp = xx; acc = iv.mpf(0); sign = 1
        for j in range(n+1):
            d = 2*j+1; term = xp/iv.mpf(d)
            acc = acc + term if sign > 0 else acc - term
            sign *= -1; xp = xp*x2
        R = xx.b**(2*n+3)/iv.mpf(2*n+3)
        return iv.mpf([acc.a - R, acc.b + R])
    def atan_endpoint(pt):
        if pt <= 1: return atan_series(iv.mpf([pt,pt]), nterms)
        inv = iv.mpf([1,1])/iv.mpf([pt,pt])
        return iv.pi/2 - atan_series(inv, nterms)
    return iv.mpf([atan_endpoint(a).a, atan_endpoint(b).b])
X, C, Q = sp.symbols('x c q', positive=True)
sx = sp.sin(X); cx = sp.cos(X)
Ph = cx**2 + Q**2*sx**2; D = Q + C*Ph
W = 3 + 2*X/sx*cx; sc = sx*cx
G = -Ph*W/D + 2*C*X*Ph*(Q**2-1)*sc/(D**2)
Gx_s = sp.simplify(sp.diff(G, X)); Gc_s = sp.simplify(sp.diff(G, C))
xp_s = -X*Ph/D; Gp_s = sp.simplify(Gx_s*xp_s + Gc_s)
J_s = sp.simplify(G**2 + Gp_s)
mods = {'sin': iv.sin, 'cos': iv.cos, 'tan': iv.tan, 'mpf': iv.mpf, 'pi': iv.pi}
Jf = sp.lambdify((X,C,Q), J_s, modules=mods)
def c1_iv(x, q): return iv_atan(1.0/(q*iv.tan(x)))/x
def c2_iv(g, q): return iv_atan(q*iv.tan(g))/(iv.pi - g)
def J1_2d_iv(x, q): return Jf(x, c1_iv(x,q), q)
def J2_2d_iv(g, q): return Jf(iv.pi-g, c2_iv(g,q), q)

def uniform(f, x0,x1,q0,q1,n, want_pos):
    worst = None
    for i in range(n):
        a = x0+(x1-x0)*i/n; b = x0+(x1-x0)*(i+1)/n
        for j in range(n):
            c = q0+(q1-q0)*j/n; d = q0+(q1-q0)*(j+1)/n
            r = f(iv.mpf([a,b]), iv.mpf([c,d]))
            if want_pos and r.a <= 0:
                if worst is None or (r.b-r.a) > (worst[1]-worst[0]): worst = (r.a, r.b, (a,b,c,d))
            if (not want_pos) and r.b >= 0:
                if worst is None or (r.b-r.a) > (worst[1]-worst[0]): worst = (r.a, r.b, (a,b,c,d))
    return worst

for n in [4, 8, 16]:
    w = uniform(J2_2d_iv, mp.mpf('0.6557'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2), n, False)
    print("J2_2d<0 uniform %dx%d: %s" % (n,n,("OK" if w is None else "FAIL worst=%s" % (w,))))
for n in [4, 8]:
    w = uniform(J1_2d_iv, mp.mpf('0.8411'), mp.mpf('1.1220'), mp.mpf(1), mp.mpf(2), n, True)
    print("J1_2d>0 uniform %dx%d: %s" % (n,n,("OK" if w is None else "FAIL worst=%s" % (w,))))
# strip single box for J2
r = J2_2d_iv(iv.mpf([mp.mpf('0.6557'),mp.mpf('0.695')]), iv.mpf([mp.mpf(1),mp.mpf(2)]))
print("J2 strip single box: [%.4f, %.4f]" % (r.a, r.b))
r = J2_2d_iv(iv.mpf([mp.mpf('0.695'),mp.mpf('1.0472')]), iv.mpf([mp.mpf(1),mp.mpf(2)]))
print("J2 regionA single box: [%.4f, %.4f]" % (r.a, r.b))
