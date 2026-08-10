p = r"scripts/verify_o3a_M2_analytic.py"
s = open(p, encoding="utf-8").read()
s = s.replace("worst = 0\n", "worst = -mp.inf\n")
s = s.replace("worstR, worstT = 0, 0\n", "worstR, worstT = -mp.inf, -mp.inf\n")
open(p, "w", encoding="utf-8").write(s)
print("patched worst init")
