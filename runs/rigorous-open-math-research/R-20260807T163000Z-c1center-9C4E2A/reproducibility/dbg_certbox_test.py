# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_c1 import cert_roots, I, P
import sym_cert_partials as scp

a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
# test box: a point at a0, b-box width db, eps-box width de
for (db, de) in [(1e-2, 1e-3), (1e-3, 1e-3), (1e-3, 1e-4), (1e-4, 1e-4)]:
    t0 = time.time()
    a_iv = P(a0)
    b_iv = I(0.5 - db/2, 0.5 + db/2)
    R_iv = I(1.0, 1.0 + de)
    r = cert_roots(a_iv, b_iv, R_iv, 3.14159, 6.2832)
    dt = time.time()-t0
    if r is None:
        print("db=%.0e de=%.0e: FAIL (%.1fs)" % (db, de, dt))
    else:
        s1, s2 = r
        print("db=%.0e de=%.0e: OK (%.1fs) s1 width=%.1e s2 width=%.1e" % (db, de, dt, float(s1.b-s1.a), float(s2.b-s2.a)))
