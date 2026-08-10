# -*- coding: utf-8 -*-
"""Check TA derivatives on both branches separately."""
import mpmath as mp
mp.mp.dps = 40
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B1 = A*cg-2*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    return dict(A=A, sg=sg, cg=cg, B1=B1, M=M, B2=B2)
def TA_branch(g, which):
    f = facts(g); A, sg, cg = f['A'], f['sg'], f['cg']
    d2 = 1+3*sg*sg
    c12 = cg*abs(f['B2']) if which=='B2' else cg*abs(f['M'])
    return 4*c12*A*A*sg*sg*cg**3/d2**2
h = mp.mpf('1e-9')
def der_range(fn, a, b, N=1000):
    lo = mp.mpf('1e30'); hi = -mp.mpf('1e30')
    for i in range(N+1):
        g = a + mp.mpf(i)*(b-a)/N
        if i in (0,N): continue
        v = (fn(g+h)-fn(g-h))/(2*h)
        lo = min(lo, v); hi = max(hi, v)
    return lo, hi
for (a,b) in [(mp.mpf('0.72'), mp.mpf('0.85')), (mp.mpf('0.85'), mp.mpf('0.86')), (mp.mpf('0.86'), mp.mpf('1.0472'))]:
    l1, h1 = der_range(lambda g: TA_branch(g,'B2'), a, b)
    l2, h2 = der_range(lambda g: TA_branch(g,'M'), a, b)
    print('[%.2f, %.2f]: B2-branch TA d [%.4f, %.4f] ; M-branch TA d [%.4f, %.4f]' % (a,b,l1,h1,l2,h2))
# B1 signs
for g in [mp.mpf('0.85'), mp.mpf('0.86'), mp.mpf('0.8527')]:
    print('B1(%.4f) = %.6f' % (g, facts(g)['B1']))
# also B1 derivative range to prove B1 crossing uniqueness
lo, hi = der_range(lambda g: facts(g)['B1'], mp.mpf('0.655'), mp.mpf('1.0472'))
print('B1 derivative range: [%.4f, %.4f]' % (lo, hi))
