# -*- coding: utf-8 -*-
"""Numerical margins for all monotonicity facts at chosen cuts + endpoint values."""
import mpmath as mp
mp.mp.dps = 40
glo = mp.mpf('0.655'); ghi = mp.mpf('1.0472')
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
def TA(g, branch):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d2 = 1+3*sg*sg
    c12 = cg*abs(f['B2']) if branch=='B2' else cg*abs(f['M'])
    return 4*c12*A*A*sg*sg*cg**3/d2**2
def TC(g):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    return mp.mpf('0.3164')*f['G5']*A*sg*cg*cg
def TB(g):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d = mp.sqrt(1+3*sg*sg); tmax = mp.atan(2*mp.tan(g))
    return 2*A**3*sg*sg*tmax*cg**5/d**5
def Qlo(g):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d2 = 1+3*sg*sg; z = cg*cg/d2
    return 4*A*A*z*z - A*f['B7']*z + 6*cg*cg*sg*sg
def Fv(g):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    tmax = mp.atan(2*mp.tan(g))
    return tmax*tmax*cg*sg*sg
def B1v(g): return facts(g)['B1']
h = mp.mpf('1e-9')
def drange(fn, a, b, N=1200):
    lo = mp.mpf('1e30'); hi = -mp.mpf('1e30')
    for i in range(N+1):
        g = a + mp.mpf(i)*(b-a)/N
        if i in (0,N): continue
        v = (fn(g+h)-fn(g-h))/(2*h)
        lo = min(lo, v); hi = max(hi, v)
    return lo, hi
tests = [
 ('TA-B2 inc [0.655,0.72]', lambda g: TA(g,'B2'), mp.mpf('0.655'), mp.mpf('0.72'), '>0'),
 ('TA-B2 dec [0.73,0.85]', lambda g: TA(g,'B2'), mp.mpf('0.73'), mp.mpf('0.85'), '<0'),
 ('TA-B2 dec [0.85,0.86]', lambda g: TA(g,'B2'), mp.mpf('0.85'), mp.mpf('0.86'), '<0'),
 ('TA-M  dec [0.85,0.86]', lambda g: TA(g,'M'), mp.mpf('0.85'), mp.mpf('0.86'), '<0'),
 ('TA-M  dec [0.86,1.0472]', lambda g: TA(g,'M'), mp.mpf('0.86'), mp.mpf('1.0472'), '<0'),
 ('TC inc [0.655,0.82]', TC, mp.mpf('0.655'), mp.mpf('0.82'), '>0'),
 ('TC dec [0.82,1.0472]', TC, mp.mpf('0.82'), mp.mpf('1.0472'), '<0'),
 ('TB dec [0.655,1.0472]', TB, mp.mpf('0.655'), mp.mpf('1.0472'), '<0'),
 ('Qlo inc [0.655,1.0472]', Qlo, mp.mpf('0.655'), mp.mpf('1.0472'), '>0'),
 ('F inc [1.0014,1.0472]', Fv, mp.mpf('1.0014'), mp.mpf('1.0472'), '>0'),
 ('B1 neg [0.86,1.0472]', B1v, mp.mpf('0.86'), mp.mpf('1.0472'), '<0'),
]
for name, fn, a, b, want in tests:
    lo, hi = drange(fn, a, b)
    ok = (lo > 0) if want=='>0' else (hi < 0)
    print('%-28s [%9.4f, %9.4f]  %s' % (name, lo, hi, 'OK' if ok else 'FAIL'))
# Qlo <= 0 on [0.655, 1.0014]
mn = mp.mpf('1e30')
for i in range(5000):
    g = mp.mpf('0.655') + mp.mpf(i)*(mp.mpf('1.0014')-mp.mpf('0.655'))/5000
    mn = min(mn, Qlo(g))
print('Qlo max on [0.655,1.0014]: %.8f %s' % (mn, 'OK' if mn < 0 else 'FAIL'))
# B1 positive on [0.655, 0.85]
mn = mp.mpf('1e30')
for i in range(5000):
    g = mp.mpf('0.655') + mp.mpf(i)*(mp.mpf('0.85')-mp.mpf('0.655'))/5000
    mn = min(mn, B1v(g))
print('B1 min on [0.655,0.85]: %.8f %s' % (mn, 'OK' if mn > 0 else 'FAIL'))
print()
print('endpoint values:')
for g in ['0.655','0.72','0.73','0.82','0.85','0.86','1.0014','1.0472']:
    gg = mp.mpf(g)
    print('g=%s: TA(B2)=%.6f TA(M)=%.6f TC=%.6f TB=%.6f Qlo=%.6f F=%.6f' % (g, TA(gg,'B2'), TA(gg,'M'), TC(gg), TB(gg), Qlo(gg), Fv(gg)))
