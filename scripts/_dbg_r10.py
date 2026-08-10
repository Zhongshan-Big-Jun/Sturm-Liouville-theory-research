# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
from audit_o3a_pdf_part2 import y1_at_1, eigvals, eigenmode, residual

q = np.sqrt(10.0)
for a in [0.40, 0.43, 0.45, 0.47, 0.49]:
    b = 1-a
    try:
        R1, R2, v_a, v_b, s1, s2, n1, n2 = residual(a, b, q)
        print(f"a={a:.4f} b={b:.4f} R1={R1:.6e} R2={R2:.6e} v_a={v_a:+.4f} v_b={v_b:+.4f} s1={s1:.6f} s2={s2:.6f}")
    except Exception as e:
        print(f"a={a:.4f} FAILED: {e}")
