import re
p = r"scripts/verify_o3a_M2_analytic.py"
s = open(p, encoding="utf-8").read()
s = s.replace("""worst = 0
for i in range(401):
	q = 1 + 19 * i / 400
	for j in range(401):
		u = s3_hi * j / 400
		worst = max(worst, d2M2dq2(q, u))""", """SQRT3 = mp.sqrt(3)
worst = 0
for i in range(401):
	q = 1 + 19 * i / 400
	for j in range(401):
		u = SQRT3 * j / 400
		worst = max(worst, d2M2dq2(q, u))""")
s = s.replace("""worst = 0
for i in range(2001):
	u = s3_hi * i / 2000
	worst = max(worst, dM2dq(1, u))""", """worst = 0
for i in range(2001):
	u = SQRT3 * i / 2000
	worst = max(worst, dM2dq(1, u))""")
open(p, "w", encoding="utf-8").write(s)
print("patched")
