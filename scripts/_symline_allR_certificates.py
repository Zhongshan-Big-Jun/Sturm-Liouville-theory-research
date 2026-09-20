# -*- coding: utf-8 -*-
# 2026-08-12 会话 58 续作: 缺口 (a') 全 R 对称线证明的精确有理证书 (STRICT 部分)
# 对应 docs/SL_gap_n1_symline_allR_proof.tex 附录 A 的 C1-C5 与 G''(0) 正性.
# 全部用 fractions.Fraction 精确算术; 每个断言输出 PASS/FAIL 与余量.
from fractions import Fraction as F
from math import factorial

ok = True
def check(name, cond, margin):
    global ok
    print("%-58s %s   (余量 %s)" % (name, "PASS" if cond else "FAIL", margin))
    ok = ok and cond

PI_LO, PI_HI = F(223, 71), F(22, 7)          # 223/71 < pi < 22/7

# ---------- 预备: 交错级数精确夹逼 sin/cos ----------
def taylor_bound(X, N, Parity, Sine):
	# On [0, 1], term magnitudes decrease. An odd term count ends positive
	# (upper bound); an even count ends negative (lower bound).
	if not isinstance(N, int) or N < 1 or N % 2 != Parity:
		raise ValueError("term-count parity does not certify the requested bound")
	if not F(0) <= X <= F(1):
		raise ValueError("Taylor bound is certified only on [0, 1]")
	Total = F(0)
	for K in range(N):
		Degree = 2*K + int(Sine)
		Total += (-1)**K * X**Degree / factorial(Degree)
	return Total

def sin_up(X, N=7):
	return taylor_bound(X, N, 1, True)

def sin_lo(X, N=6):
	return taylor_bound(X, N, 0, True)

def cos_lo(X, N=6):
	# C10 ends with -X**10/10!, hence is a lower bound.
	return taylor_bound(X, N, 0, False)

def cos_up(X, N=5):
	return taylor_bound(X, N, 1, False)

x1 = F(961, 1000); x2 = F(97, 100)
sin1_up = sin_up(x1); cos1_lo = cos_lo(x1)
assert cos1_lo > 0  # Positive denominator is part of the quotient certificate.
tan1_up = sin1_up / cos1_lo
sin2_lo = sin_lo(x2); cos2_up = cos_up(x2)
tan2_lo = sin2_lo / cos2_up

print("tan(0.961) <= %s = %.12f" % (tan1_up, float(tan1_up)))
print("tan(0.97)  >= %s = %.12f" % (tan2_lo, float(tan2_lo)))

# ---------- C1: gamma0* in (0.961, 0.97) ----------
# 修正后的链 (2026-08-12 复核): 分数取交错级数精确比值; 十进制常数与 pi 界方向改正.
#   phi(0.961) < 0: tan <= R1 < 14315/10000 < 14472/10000 < 2(223/71-0.961)/3  (用 pi > 223/71)
#   phi(0.97)  > 0: tan >= R2 > 14591/10000 > 14546/10000 > 2(22/7-0.97)/3     (用 pi < 22/7)
R1 = F(5104691704723563842653351044859938032346287993281, 3566217966719202085941974656584935652684000000000)  # S13/C10, corrected 2026-09-20
R2 = F(329267980378932303644934573247, 225649563795645795591390000000)
check("C1a: R1 equals S13/C10 (envelope follows from alternating remainder)", tan1_up == R1, R1 - tan1_up)
check("C1b: R1 < 14315/10000 < 14472/10000", R1 < F(14315, 10000) < F(14472, 10000), F(14472, 10000) - R1)
check("C1c: 14472/10000 < 2(223/71-0.961)/3 (pi > 223/71)",
      F(14472, 10000) < 2*(PI_LO - x1)/3, 2*(PI_LO - x1)/3 - F(14472, 10000))
check("C1d: tan(0.97) >= R2 (= sin_lo/cos_up 精确比值)", tan2_lo >= R2, tan2_lo - R2)
check("C1e: R2 > 14591/10000 > 14546/10000", R2 > F(14591, 10000) > F(14546, 10000), R2 - F(14546, 10000))
check("C1f: 14546/10000 > 2(22/7-0.97)/3 (pi < 22/7)",
      F(14546, 10000) > 2*(PI_HI - x2)/3, F(14546, 10000) - 2*(PI_HI - x2)/3)

# 结论: gamma0* in (0.961, 0.97), y0 = pi - gamma0* in (pi-0.97, pi-0.961) = (y0min, y0max)
y0min = PI_LO - x2          # 15413/7100
y0max = PI_HI - x1          # 15273/7000
check("C1g: 区间非退化 y0min < y0max", y0min < y0max, y0max - y0min)
print("y0 in (%s, %s) = (%.10f, %.10f)" % (y0min, y0max, float(y0min), float(y0max)))

# ---------- C2: f(gamma0*) = 2 y0^2/sqrt(9+4y0^2) > pi/2 ----------
# f 在 y>0 严格递增; y0>y0min, y0<y0max:
# f >= 2 y0min^2 / sqrt(9+4 y0max^2); 平方比较: 4 y0min^4/(9+4 y0max^2) > (1623/912)^2
lhs2 = 4*y0min**4 / (9 + 4*y0max**2)
rhs2 = F(1623, 912)**2
check("C2a: 4 y0min^4/(9+4 y0max^2) > (1623/912)^2", lhs2 > rhs2, lhs2 - rhs2)
check("C2b: 1623/912 > pi/2 (经 pi < 22/7: 1623/912 > 11/7)",
      F(1623, 912) > F(11, 7), F(1623, 912) - F(11, 7))
check("C2c: pi/2 < 11/7 (223/71 < pi => 223/142 < pi/2)", F(223, 142) < F(11, 7), F(11, 7) - F(223, 142))

# ---------- G''(0) 正性 (修正显示值 3pi -> 3pi - pi^3/4) ----------
# G''(0) = 6y - 2y^3 at y = pi/2  = 3pi - pi^3/4 = pi(3 - pi^2/4) > 0 iff pi^2 < 12
check("G''(0): pi^2 < 12 (经 (22/7)^2 = 484/49 < 12)",
      F(484, 49) < F(12), F(12) - F(484, 49))

# ---------- C3: G''' < -56/129 (用精化界 w0 < w0max, y0 < y0max) ----------
# w0 = y0 - pi/2 < y0max - pi/2; pi/2 > 223/142:
w0max = y0max - F(223, 142)      # 303883/497000
cos2w0_lo = 1 - 2*w0max**2       # cos 2w0 >= 1 - (2w0)^2/2 >= 1 - 2 w0max^2
check("C3a: cos2w0 下界为正", cos2w0_lo > 0, cos2w0_lo)
gppp_ub = F(6) - F(7,2)*F(223,71)**2 * cos2w0_lo + 2*y0max*(2*y0max**2 - 9)
check("C3b: G''' <= 6 - (7/2)(223/71)^2 cos2w0_lo + 2 y0max (2 y0max^2-9) < -56/129",
      gppp_ub < -F(56, 129), -F(56, 129) - gppp_ub)
check("C3c: -56/129 < 0 且 G''' < -0.43 (经 -56/129 < -43/100)", -F(56,129) < -F(43,100), F(56,129) - F(43,100))

# ---------- C4: G''(w0) < -13 ----------
# sin w0 cos w0 = (1/2) sin 2w0 >= (1/2) sin(2 w0min), w0min = y0min - pi/2 > y0min - 22/7/... 
# pi/2 < 22/14 = 11/7 => w0min > y0min - 11/7
w0min = y0min - F(11, 7)
s2w0_lo = 2*w0min - (2*w0min)**3/6 + (2*w0min)**5/120 - (2*w0min)**7/5040   # sin 下界 (交错, 项递减)
check("C4a: (1/2) sin(2 w0min) >= 93/200", s2w0_lo/2 >= F(93, 200), s2w0_lo/2 - F(93, 200))
cos2w0_lo4 = 1 - 2*w0max**2
check("C4b: cos 2w0 >= 1 - 2 w0max^2 >= 63/250", cos2w0_lo4 >= F(63, 250), cos2w0_lo4 - F(63, 250))
gpp_ub = 6*y0max - 12*y0min**2*F(93, 200) - 2*y0min**3*F(63, 250) + 2*F(22, 7)**2/4
check("C4c: G''(w0) <= 6 y0max - 12 y0min^2(93/200) - 2 y0min^3(63/250) + 2(22/7)^2/4 < -13",
      gpp_ub < -F(13), -F(13) - gpp_ub)

# ---------- C5: F(gamma0*) > 0 等价 16 y0^4 - 4 pi^2 y0^2 - 15 pi^2 > 0 ----------
# h(y0) 在本证书区间 y0>=y0min>2 递增 (y0^2 > pi^2/8), 在 pi 递减
c5 = 16*y0min**4 - 4*F(22, 7)**2*y0max**2 - 15*F(22, 7)**2
# 修正: 该下界实际约 19.081, 不能取 3817/200 = 19.085
check("C5a: 16 y0min^4 - 4(22/7)^2 y0max^2 - 15(22/7)^2 > 19", c5 > F(19), c5 - F(19))
check("C5b: 19 > 0", F(19) > F(0), F(19))

print()
print("ALL PASS" if ok else "SOME FAILURES")
raise SystemExit(0 if ok else 1)
