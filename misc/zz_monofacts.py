# -*- coding: utf-8 -*-
"""Verify monotonicity facts on chosen subintervals (with margin) + endpoint values."""
import mpmath as mp
mp.mp.dps = 50
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
    return dict(TA=TA, TB=TB, TC=TC, TD=TD, H=H, G1=TA+TB+TC-TD, Qlo=Qlo, P=A*sg*cg*cg, tmax=tmax, F=tmax*tmax*cg*sg*sg)
h = mp.mpf('1e-8')
def dsign(fn, a, b, N=800):
    lo = mp.mpf('1e30'); hi = -mp.mpf('1e30')
    for i in range(N+1):
        g = a + mp.mpf(i)*(b-a)/N
        if i in (0, N): continue
        v = (fn(g+h)-fn(g-h))/(2*h)
        lo = min(lo, v); hi = max(hi, v)
    return lo, hi
print('TA derivative on [0.655, 0.73]: ', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TA'], mp.mpf('0.655'), mp.mpf('0.73'))))
print('TA derivative on [0.73, 1.0472]:', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TA'], mp.mpf('0.73'), mp.mpf('1.0472'))))
print('TC derivative on [0.655, 0.83]: ', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TC'], mp.mpf('0.655'), mp.mpf('0.83'))))
print('TC derivative on [0.83, 1.0472]: ', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TC'], mp.mpf('0.83'), mp.mpf('1.0472'))))
print('TB derivative on [0.655, 1.0472]:', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TB'], mp.mpf('0.655'), mp.mpf('1.0472'))))
print('TD derivative on [1.0, 1.0472]:  ', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['TD'], mp.mpf('1.0'), mp.mpf('1.0472'))))
print('Qlo derivative on [0.655, 1.0472]:', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['Qlo'], mp.mpf('0.655'), mp.mpf('1.0472'))))
print('F=tmax^2 cg sg^2 on [1.0,1.0472]:', tuple('%.4f'%x for x in dsign(lambda g: comps(g)['F'], mp.mpf('1.0'), mp.mpf('1.0472'))))
print()
print('endpoint values (50 dps):')
for g in ['0.655','0.73','0.83','1.0','1.0014','1.0472']:
    gg = mp.mpf(g)
    c = comps(gg)
    print('g=%s: TA=%.6f TB=%.6f TC=%.6f TD=%.6f Qlo=%.6f F=%.6f' % (g, c['TA'], c['TB'], c['TC'], c['TD'], c['Qlo'], c['F']))
# Qlo zero location
lo, hi = mp.mpf('1.0'), mp.mpf('1.02')
for _ in range(100):
    mid = (lo+hi)/2
    if comps(mid)['Qlo'] > 0: hi = mid
    else: lo = mid
print('Qlo zero = %.10f' % ((lo+hi)/2))
# actual maxima locations
for k in ['TA','TC']:
    best = (-mp.mpf('1e30'), None)
    for i in range(20000):
        g = mp.mpf('0.655') + mp.mpf(i)*(mp.mpf('1.0472')-mp.mpf('0.655'))/20000
        v = comps(g)[k]
        if v > best[0]: best = (v, g)
    print('%s max %.6f @ %.6f' % (k, best[0], best[1]))
