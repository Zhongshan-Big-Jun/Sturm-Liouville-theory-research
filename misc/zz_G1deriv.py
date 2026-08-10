# -*- coding: utf-8 -*-
"""Derivative structure of G1 components on [0.655, 1.0472]."""
import mpmath as mp
mp.mp.dps = 50
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')

def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
    G5 = B5 - A*B4
    return dict(A=A, sg=sg, cg=cg, B1=B1, M=M, B2=B2, B4=B4, B5=B5, B7=B7, G5=G5)

def comps(g):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    c12 = cg*abs(f['B2']) if f['B1'] >= 0 else cg*abs(f['M'])
    TA = 4*c12*A*A*sg*sg*cg**3/d**4
    TB = 2*A**3*sg*sg*tmax*cg**5/d**5
    H = f['G5']*A*sg*cg*cg
    TC = H*mp.mpf('0.3164')
    z_lo = cg*cg/(d*d)
    Qlo = 4*A*A*z_lo*z_lo - A*f['B7']*z_lo + 6*cg*cg*sg*sg
    TD = tmax*tmax*cg*sg*sg*max(Qlo, mp.mpf(0))
    return dict(TA=TA, TB=TB, TC=TC, TD=TD, H=H, G1=TA+TB+TC-TD, Qlo=Qlo, P=A*sg*cg*cg, tmax=tmax, d=d)

h = mp.mpf('1e-8')
N = 2000
names = ['TA','TB','TC','TD','H','G1','Qlo','P']
dmin = {k: mp.mpf('1e30') for k in names}; dmax = {k: -mp.mpf('1e30') for k in names}
vmin = {k: mp.mpf('1e30') for k in names}; vmax = {k: -mp.mpf('1e30') for k in names}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    c = comps(g)
    for k in names:
        vmin[k] = min(vmin[k], c[k]); vmax[k] = max(vmax[k], c[k])
    if 0 < i < N:
        cp = comps(g+h); cm = comps(g-h)
        for k in names:
            dv = (cp[k]-cm[k])/(2*h)
            dmin[k] = min(dmin[k], dv); dmax[k] = max(dmax[k], dv)
for k in names:
    print('%-4s: val [%.5f, %.5f]   d/dg [%9.3f, %9.3f]' % (k, vmin[k], vmax[k], dmin[k], dmax[k]))
print()
# locate mins/maxs of G1 and H
def find_extremum(k, name):
    bestmin = (mp.mpf('1e30'), None); bestmax = (-mp.mpf('1e30'), None)
    for i in range(N+1):
        g = glo + mp.mpf(i)*(ghi-glo)/N
        v = comps(g)[k]
        if v < bestmin[0]: bestmin = (v, g)
        if v > bestmax[0]: bestmax = (v, g)
    print('%s: min %.6f @ %.5f ; max %.6f @ %.5f' % (name, bestmin[0], bestmin[1], bestmax[0], bestmax[1]))
find_extremum('G1','G1'); find_extremum('H','H'); find_extremum('TA','TA'); find_extremum('TD','TD')
# derivative sign regions for G1
print()
print('G1 derivative sign regions (sample every 0.01):')
prev = None
for i in range(0, 500):
    g = glo + mp.mpf(i)*mp.mpf('0.001')
    if g > ghi: break
    cp = comps(min(g+h,ghi)); cm = comps(max(g-h,glo))
    dv = (cp['G1']-cm['G1'])/(2*h)
    s = '+' if dv > 0 else '-'
    if s != prev:
        if prev is not None: print('  at g=%.4f: %s -> %s' % (g, prev, s))
        prev = s
print('  final sign: %s' % prev)
