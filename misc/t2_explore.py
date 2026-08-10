# -*- coding: utf-8 -*-
"""T2-side reconnaissance for J2_2d < 0 (O3a I3 de-certification)."""
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

# 1) grid over the full box [0.655,1.0472]x[1,2]
g0, g1, q0, q1 = mp.mpf('0.655'), mp.mpf('1.0472'), mp.mpf(1), mp.mpf(2)
Ng, Nq = 120, 100
worst = None; worst_full = None
stats = dict(G=[mp.inf,-mp.inf], Gx=[mp.inf,-mp.inf], Gc=[mp.inf,-mp.inf], u=[mp.inf,-mp.inf], J=[mp.inf,-mp.inf])
onT2 = dict(G=[mp.inf,-mp.inf], Gx=[mp.inf,-mp.inf], Gc=[mp.inf,-mp.inf], u=[mp.inf,-mp.inf], J=[mp.inf,-mp.inf])
c2range = [mp.inf, -mp.inf]
cntT2 = 0
for i in range(Ng+1):
    for j in range(Nq+1):
        gv = g0 + (g1-g0)*i/Ng
        qv = q0 + (q1-q0)*j/Nq
        r = ev(gv, qv)
        for k in ['G','Gx','Gc','u','J']:
            v = r[k]
            if v < stats[k][0]: stats[k][0] = v
            if v > stats[k][1]: stats[k][1] = v
        if r['c'] < c2range[0]: c2range[0] = r['c']
        if r['c'] > c2range[1]: c2range[1] = r['c']
        if worst_full is None or r['J'] > worst_full[0]: worst_full = (r['J'], gv, qv, r['c'])
        if mp.mpf('0.4') < r['c'] < mp.mpf('0.5'):
            cntT2 += 1
            for k in ['G','Gx','Gc','u','J']:
                v = r[k]
                if v < onT2[k][0]: onT2[k][0] = v
                if v > onT2[k][1]: onT2[k][1] = v
            if worst is None or r['J'] > worst[0]: worst = (r['J'], gv, qv, r['c'])

print('=== full box [0.655,1.0472]x[1,2] grid (%dx%d) ===' % (Ng, Nq))
for k in ['G','Gx','Gc','u','J']:
    print('  %s in [%s, %s]' % (k, mp.nstr(stats[k][0], 8), mp.nstr(stats[k][1], 8)))
print('  c2 in [%s, %s]' % (mp.nstr(c2range[0], 8), mp.nstr(c2range[1], 8)))
print('  worst J (max) on full box:', mp.nstr(worst_full[0], 10), 'at g=', mp.nstr(worst_full[1],8), 'q=', mp.nstr(worst_full[2],8), 'c=', mp.nstr(worst_full[3],8))
print('=== T2 subset (c2 in (0.4,0.5)), %d/%d points ===' % (cntT2, (Ng+1)*(Nq+1)))
for k in ['G','Gx','Gc','u','J']:
    print('  %s in [%s, %s]' % (k, mp.nstr(onT2[k][0], 8), mp.nstr(onT2[k][1], 8)))
if worst:
    print('  worst J (max) on T2:', mp.nstr(worst[0], 10), 'at g=', mp.nstr(worst[1],8), 'q=', mp.nstr(worst[2],8), 'c=', mp.nstr(worst[3],8))
