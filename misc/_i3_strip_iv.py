# -*- coding: utf-8 -*-
"""Single-box iv certification of piece bounds on J2 strips."""
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
mods = {'sin': iv.sin, 'cos': iv.cos, 'tan': iv.tan, 'mpf': iv.mpf, 'pi': iv.pi}
Gf = sp.lambdify((X,C,Q), G, modules=mods)
Gxf = sp.lambdify((X,C,Q), Gx_s, modules=mods)
Gcf = sp.lambdify((X,C,Q), Gc_s, modules=mods)

def c2_iv(g, q): return iv_atan(q*iv.tan(g))/(iv.pi - g)
def pieces(g, q):
    x = iv.pi - g
    c = c2_iv(g,q)
    Phv = iv.cos(x)**2 + q*q*iv.sin(x)**2
    Dv = q + c*Phv
    return Gf(x,c,q), Gxf(x,c,q), Gcf(x,c,q), x*Phv/Dv

strips = [(mp.mpf('0.6557'),mp.mpf('0.75')),(mp.mpf('0.75'),mp.mpf('0.85')),(mp.mpf('0.85'),mp.mpf('0.95')),(mp.mpf('0.95'),mp.mpf('1.0472'))]
targets = {
    'G': [('max_abs', 2.75), ],  # need |G| <= 2.75 for G^2 <= 7.5625
}
# per strip, evaluate each piece over the strip box and report intervals
for (g0,g1) in strips:
    g = iv.mpf([g0,g1]); q = iv.mpf([mp.mpf(1),mp.mpf(2)])
    Gv, Gxv, Gcv, xp = pieces(g,q)
    print("strip [%.3f,%.3f]: G=[%.4f,%.4f] Gx=[%.4f,%.4f] Gc=[%.4f,%.4f] xPhi/D=[%.4f,%.4f]" % (
        g0,g1,Gv.a,Gv.b,Gxv.a,Gxv.b,Gcv.a,Gcv.b,xp.a,xp.b))
