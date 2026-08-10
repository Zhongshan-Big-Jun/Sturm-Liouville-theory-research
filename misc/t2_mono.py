# -*- coding: utf-8 -*-
"""Check composed monotonicity (M1')-(M3') on T2 with exact derivatives."""
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

c2 = sp.atan(q*sp.tan(g))/(sp.pi - g)
# composed functions: x -> pi - g
def compose(f):
    return sp.simplify(f.subs({x: sp.pi - g, c: c2}))
G2  = compose(G)
Gc2 = compose(Gc)
Gx2 = compose(Gx)
u2  = compose(u)

dG2_dg  = sp.simplify(sp.diff(G2, g));  dG2_dq  = sp.simplify(sp.diff(G2, q))
dGc2_dg = sp.simplify(sp.diff(Gc2, g)); dGc2_dq = sp.simplify(sp.diff(Gc2, q))
dGx2_dg = sp.simplify(sp.diff(Gx2, g))
du2_dg  = sp.simplify(sp.diff(u2, g));  du2_dq  = sp.simplify(sp.diff(u2, q))

fn = dict()
for name, expr in [('dG2_dg',dG2_dg),('dG2_dq',dG2_dq),('dGc2_dg',dGc2_dg),('dGc2_dq',dGc2_dq),
                   ('dGx2_dg',dGx2_dg),('du2_dg',du2_dg),('du2_dq',du2_dq)]:
    fn[name] = sp.lambdify((g, q), expr, modules='mpmath')

g0, g1, q0, q1 = mp.mpf('0.655'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2)
def c2v(gv, qv): return mp.atan(qv*mp.tan(gv))/(mp.pi-gv)
Ng, Nq = 160, 120
res = {k: (mp.inf, -mp.inf) for k in fn}
cnt = 0
viol = {k: 0 for k in fn}
for i in range(Ng+1):
    for j in range(Nq+1):
        gv = g0 + (g1-g0)*i/Ng
        qv = q0 + (q1-q0)*j/Nq
        cv = c2v(gv, qv)
        if not (mp.mpf('0.4') < cv < mp.mpf('0.5')):
            continue
        cnt += 1
        for k, f in fn.items():
            v = f(gv, qv)
            if v < res[k][0]: res[k] = (v, gv, qv)
            if v > res[k][1]: res[k] = (v, gv, qv)
print('T2 points:', cnt)
expect = {'dG2_dg': '<0', 'dG2_dq': '<0', 'dGc2_dg': '>0', 'dGc2_dq': '<0', 'dGx2_dg': '<0', 'du2_dg': '?', 'du2_dq': '?'}
for k in fn:
    mn, mg, mq = res[k][0], res[k][1], res[k][2]
    mx = res[k][3]
    print('%s: min=%s at (g=%s,q=%s)  max=%s at (g=%s,q=%s)  expect %s' % (
        k, mp.nstr(mn,7), mp.nstr(mg,7), mp.nstr(mq,7), mp.nstr(mx,7), mp.nstr(res[k][4],7), mp.nstr(res[k][5],7), expect[k]))
