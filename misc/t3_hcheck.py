# -*- coding: utf-8 -*-
"""t3_hcheck: H(u) sign and margin on u in [pi/3, (pi-0.655)/2]."""
import numpy as np, math
u0, u1 = math.pi/3, (math.pi-0.655)/2
print('u range:', u0, u1)
lo = (1e18, None)
for u in np.linspace(u0, u1, 200001):
    cu = math.cos(u); s = math.sin(u)
    H = -6*cu**5 + 2*cu**3*u**2 + 9*cu**3 - 8*cu**2*u*s - 3*cu + 3*u*s
    if H < lo[0]: lo = (H, u)
print('min H =', lo)
# also check the first group and second group separately
u = lo[1]; cu = math.cos(u); s = math.sin(u)
print('at min: first group cu*(-6cu^4+2cu^2 u^2+9cu^2-3) =', cu*(-6*cu**4+2*cu**2*u**2+9*cu**2-3))
print('at min: second group s*u*(3-8cu^2) =', s*u*(3-8*cu**2))
# derivative check
def H(u):
    cu = math.cos(u); s = math.sin(u)
    return -6*cu**5 + 2*cu**3*u**2 + 9*cu**3 - 8*cu**2*u*s - 3*cu + 3*u*s
hs = [H(u) for u in np.linspace(u0, u1, 200001)]
dH = np.diff(hs)/( (u1-u0)/200000 )
print('dH range:', min(dH), max(dH))
