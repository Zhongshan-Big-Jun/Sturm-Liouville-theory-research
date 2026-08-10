# -*- coding: utf-8 -*-
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
a0 = float(np.arccos(0.25)/np.pi)
eps = 0.02
for b in np.linspace(a0, a0+0.01, 6):
    a = a0 + eps*0.02
    fa = R1R2(a, b, 1+eps)[0]
    h = 1e-6
    d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
    print("b=%.6f  a=%.6f  fa=%.6e  d=%.3f" % (b, a, fa, d))
    for _ in range(5):
        fa = R1R2(a, b, 1+eps)[0]
        an = a - fa/d
        if not (0 < an < b): print("   an out of range"); break
        a = an
        print("   iter a=%.8f fa=%.3e" % (a, R1R2(a, b, 1+eps)[0]))
