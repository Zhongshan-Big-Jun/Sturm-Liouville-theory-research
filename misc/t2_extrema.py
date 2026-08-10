# -*- coding: utf-8 -*-
"""Locate extrema of G, Gc, Gx, u on T2 and check composed monotonicity."""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

x, c, q = sp.symbols('x c q', positive=True)
g = sp.symbols('gamma', positive=True)

sx, cx = sp.sin(x), sp.cos(x)
Ph = cx**2 + q**2*sx**2
D = q + c*Ph
W = 3 + 2*x*cx/sx
sc = sx*cx
G = -Ph*W/D + 2*c*x*Ph*(q**2-1)*sc/(D**2)
Gx = sp.simplify(sp.diff(G, x))
Gc = sp.simplify(sp.diff(G, c))
u = x*Ph/D
J = sp.simplify(G**2 - u*Gx + Gc)
c2 = sp.atan(q*sp.tan(g))/(sp.pi - g)

fn_G  = sp.lambdify((x, c, q), G,  modules='mpmath')
fn_Gx = sp.lambdify((x, c, q), Gx, modules='mpmath')
fn_Gc = sp.lambdify((x, c, q), Gc, modules='mpmath')
fn_u  = sp.lambdify((x, c, q), u,  modules='mpmath')
fn_J  = sp.lambdify((x, c, q), J,  modules='mpmath')
fn_c2 = sp.lambdify((g, q), c2, modules='mpmath')

def ev(gv, qv):
    xv = mp.pi - gv
    cv = fn_c2(gv, qv)
    return dict(g=gv, q=qv, x=xv, c=cv,
                G=fn_G(xv, cv, qv), Gx=fn_Gx(xv, cv, qv), Gc=fn_Gc(xv, cv, qv),
                u=fn_u(xv, cv, qv), J=fn_J(xv, cv, qv))

g0, g1, q0, q1 = mp.mpf('0.655'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2)
Ng, Nq = 200, 160
ext = dict(G=dict(mx=(None,None,None), mn=(None,None,None)),
           Gx=dict(mx=(None,None,None), mn=(None,None,None)),
           Gc=dict(mx=(None,None,None), mn=(None,None,None)),
           u=dict(mx=(None,None,None), mn=(None,None,None)))
cnt = 0
for i in range(Ng+1):
    for j in range(Nq+1):
        gv = g0 + (g1-g0)*i/Ng
        qv = q0 + (q1-q0)*j/Nq
        r = ev(gv, qv)
        if not (mp.mpf('0.4') < r['c'] < mp.mpf('0.5')):
            continue
        cnt += 1
        for k in ['G','Gx','Gc','u']:
            v = r[k]
            e = ext[k]
            if e['mx'][0] is None or v > e['mx'][0]:
                e['mx'] = (v, gv, qv)
            if e['mn'][0] is None or v < e['mn'][0]:
                e['mn'] = (v, gv, qv)
print('T2 points:', cnt)
for k in ['G','Gx','Gc','u']:
    mx, mg, mq = ext[k]['mx']; mn, ng_, nq = ext[k]['mn']
    print('%s: max=%s at (g=%s, q=%s, c=%s) | min=%s at (g=%s, q=%s, c=%s)' % (
        k, mp.nstr(mx,8), mp.nstr(mg,8), mp.nstr(mq,8), mp.nstr(ev(mg,mq)['c'],8),
           mp.nstr(mn,8), mp.nstr(ng_,8), mp.nstr(nq,8), mp.nstr(ev(ng_,nq)['c'],8)))
