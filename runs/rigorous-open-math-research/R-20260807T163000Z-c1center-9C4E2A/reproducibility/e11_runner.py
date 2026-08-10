# -*- coding: utf-8 -*-
"""runner for e11b: no-space-arg wrapper"""
import sys, subprocess, os
rep = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility"
py = r"C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe"
script = os.path.join(rep, "e11b_transition.py")
jobs = [
    ("950", "1300", "10", "150", os.path.join(rep, "e11_fine1.json")),
    ("1030", "1120", "5", "150", os.path.join(rep, "e11_fine2.json")),
]
for args in jobs:
    print("RUN", args, flush=True)
    out = subprocess.run([py, script] + list(args), capture_output=True, text=True)
    print(out.stdout[-3000:], flush=True)
    if out.returncode != 0:
        print("ERR", out.stderr[-2000:], flush=True)