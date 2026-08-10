# -*- coding: utf-8 -*-
"""Derivative ranges on the two G1 monotonicity regions."""
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
    return dict(TA=TA, TB=TB, TC=TC, TD=TD, H=H, G1=TA+TB+TC-TD, Qlo=Qlo)
h = mp.mpf('1e-8')
def deriv_ranges(a, b, names, label):
    N = 600
    dmin = {k: mp.mpf('1e30') for k in names}; dmax = {k: -mp.mpf('1e30') for k in names}
    for i in range(N+1):
        g = a + mp.mpf(i)*(b-a)/N
        if i == 0 or i == N: continue
        cp = comps(g+h); cm = comps(g-h)
        for k in names:
            dv = (cp[k]-cm[k])/(2*h)
            dmin[k] = min(dmin[k], dv); dmax[k] = max(dmax[k], dv)
    print('--- %s on [%.4f, %.4f] ---' % (label, a, b))
    for k in names:
        print('%-4s d/dg [%9.4f, %9.4f]' % (k, dmin[k], dmax[k]))
deriv_ranges(mp.mpf('0.655'), mp.mpf('0.743'), ['TA','TB','TC','TD','G1'], 'inc region')
deriv_ranges(mp.mpf('0.743'), mp.mpf('1.0472'), ['TA','TB','TC','TD','G1'], 'dec region')
# G1 endpoint values
for g in [mp.mpf('0.655'), mp.mpf('0.743'), mp.mpf('1.0472')]:
    c = comps(g)
    print('g=%.4f: TA=%.5f TB=%.5f TC=%.5f TD=%.5f G1=%.5f Qlo=%.5f' % (g, c['TA'], c['TB'], c['TC'], c['TD'], c['G1'], c['Qlo']))
