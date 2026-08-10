# -*- coding: utf-8 -*-
import sympy as sp
q, w = sp.symbols('q w', positive=True)
A = sp.pi - sp.atan(w/q)
IN = (q**2+w**2)*A*(2*A*q-3*w+2*sp.atan(w)) - 3*w*q*(1+w**2)*sp.atan(w)
dIN_dw = sp.diff(IN, w)
M2 = 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + sp.atan(w)*(4*A*w-5*q-9*q*w**2)
diff = sp.simplify(dIN_dw - M2)
print("M2 - d_w IN simplified:", sp.simplify(sp.expand_trig(sp.factor(diff))))
# numeric spot check of the simplified difference
import mpmath as mp
mp.mp.dps = 30
f = sp.lambdify((q,w), diff, 'mpmath')
for qq in [1.1, 2.0, 5.0, 20.0]:
    for ww in [0.5, 1.0, 3.0, 6.0]:
        v = f(mp.mpf(qq), mp.mpf(ww))
        if abs(v) > mp.mpf('1e-25'):
            print("NONZERO", qq, ww, v)
print("done M2 check")
