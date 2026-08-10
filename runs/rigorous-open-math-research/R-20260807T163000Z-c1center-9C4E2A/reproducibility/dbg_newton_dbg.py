# -*- coding: utf-8 -*-
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import R1R2
a0 = float(np.arccos(0.25)/np.pi)
eps = 0.001
for b in (a0+0.001, 0.43, 0.5, 0.7, 0.9, 0.99, 1.0):
    a = a0 + eps*0.1324
    fa = R1R2(a, b, 1+eps)[0]
    h = 1e-6
    d = (R1R2(a+h, b, 1+eps)[0]-R1R2(a-h, b, 1+eps)[0])/(2*h)
    print("b=%.4f: guess a=%.6f  fa=%.6e  dR1da=%.3f" % (b, a, fa, d))
    # scan a
    vals = [R1R2(aa, b, 1+eps)[0] for aa in np.linspace(0.41, 0.45, 21)]
    print("   scan R1 over a in [0.41,0.45]:", " ".join("%+.3f" % v for v in vals))
