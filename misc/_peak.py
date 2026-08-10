# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 40
# locate zero of d/dg TA_B2 on [0.72, 0.73]
def facts(g):
    A = mp.pi-g; sg = mp.sin(g); cg = mp.cos(g)
    B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
    return A, sg, cg, B2
def TA_B2(g):
    A, sg, cg, B2 = facts(g)
    D2 = 1+3*sg*sg
    return 4*(-B2)*A*A*sg*sg*cg**4/(D2*D2)
h = mp.mpf('1e-8')
g = mp.mpf('0.72')
while g < mp.mpf('0.73'):
    d = (TA_B2(g+h)-TA_B2(g-h))/(2*h)
    if d < 0:
        break
    g += mp.mpf('0.0001')
print('derivative first negative at g ~', g)
# bisect
lo, hi = mp.mpf('0.72'), mp.mpf('0.73')
for _ in range(60):
    mid = (lo+hi)/2
    d = (TA_B2(mid+h)-TA_B2(mid-h))/(2*h)
    if d > 0: lo = mid
    else: hi = mid
print('zero at g =', (lo+hi)/2)
print('TA_B2 at peak:', TA_B2((lo+hi)/2))
print('TA_B2(0.72):', TA_B2(mp.mpf('0.72')))
print('TA_B2(0.724):', TA_B2(mp.mpf('0.724')))
print('TA_B2(0.73):', TA_B2(mp.mpf('0.73')))
