# -*- coding: utf-8 -*-
import re
s = open("cert_gap1r_constants.py", encoding="ascii").read()
s = s.replace("F2 = cell_max(fconst2_iv, a0f-Da, a0f+Da, 400)", "F2 = cell_max(lambda x: iv.fabs(fconst2_iv(x)), a0f-Da, a0f+Da, 400)")
s = s.replace("F3 = cell_max(fconst3_iv, a0f-Da, a0f+Da, 400)", "F3 = cell_max(lambda x: iv.fabs(fconst3_iv(x)), a0f-Da, a0f+Da, 400)")
s = s.replace("P = cell_max(lambda b: iv.abs(phi_iv(b)), a0f, 1.0, N)", "P = cell_max(lambda b: iv.fabs(phi_iv(b)), a0f, 1.0, N)")
s = s.replace("Phi_max = cell_max(lambda b: iv.abs(dphi_iv(b)), a0f, 1.0-1e-12, N)", "Phi_max = cell_max(lambda b: iv.fabs(dphi_iv(b)), a0f, 1.0-1e-12, N)")
open("cert_gap1r_constants.py", "w", encoding="ascii").write(s)
print("patched")
