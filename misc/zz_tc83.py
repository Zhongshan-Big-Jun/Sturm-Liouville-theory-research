# -*- coding: utf-8 -*-
"""Check TC' on [0.83, 1.0472] and TA values at 0.83."""
import mpmath as mp
mp.mp.dps = 40
def facts(g):
    A = mp.pi-g; sg, cg = mp.sin(g), mp.cos(g)
    B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
    B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
    G5 = B5 - A*B4
    return A, sg, cg, G5
def TC(g):
    A, sg, cg, G5 = facts(g)
    return mp.mpf('0.3164')*G5*A*sg*cg*cg
h = mp.mpf('1e-9')
lo = mp.mpf('1e30'); hi = -mp.mpf('1e30')
N = 2000
for i in range(N+1):
    g = mp.mpf('0.83') + mp.mpf(i)*(mp.mpf('1.0472')-mp.mpf('0.83'))/N
    if i in (0, N): continue
    v = (TC(g+h)-TC(g-h))/(2*h)
    lo = min(lo, v); hi = max(hi, v)
print('TC derivative on [0.83, 1.0472]: [%.6f, %.6f] %s' % (lo, hi, 'OK' if hi < 0 else 'FAIL'))
print('TC(0.83) = %.6f' % TC(mp.mpf('0.83')))
print('TA(0.83): need B2-branch (B1>0 at 0.83?)')
A, sg, cg, G5 = facts(mp.mpf('0.83'))
B1 = A*cg - 2*sg
print('  B1(0.83) = %.6f' % B1)
def TA(g, branch):
    A, sg, cg, _ = facts(g)
    d2 = 1+3*sg*sg
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
    c12 = cg*abs(B2) if branch=='B2' else cg*abs(M)
    return 4*c12*A*A*sg*sg*cg**3/d2**2
print('TA_B2(0.83) = %.6f' % TA(mp.mpf('0.83'),'B2'))
