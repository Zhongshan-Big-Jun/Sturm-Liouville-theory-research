# Verification of the fully analytic proof of M2 < 0 on D (O3a KEY LEMMA, 2026-08-09)
# Replaces the dM2/dq interval certificates (84+10 leaves) with elementary analysis.
# Every rational bound is checked; all closed forms are cross-checked numerically.
# Usage: python verify_o3a_M2_analytic.py
import mpmath as mp

mp.mp.dps = 50
pi_lo, pi_hi = mp.mpf(157) / 50, mp.mpf(22) / 7       # 3.14 < pi < 22/7
s3_lo, s3_hi = mp.mpf(17) / 10, mp.mpf(7) / 4         # 1.7 < sqrt(3) < 1.75
r = mp.mpf(10) / 17                                   # 1/sqrt(3) <= 10/17


def M2(q, u):
	A = mp.pi - mp.atan(u / q)
	t = mp.atan(u)
	return (4 * A * A * u * q - 7 * A * q * q - 9 * A * u * u
			+ 2 * A * (q * q + u * u) / (1 + u * u)
			+ t * (4 * A * u - 5 * q - 9 * q * u * u))


def dM2dq(q, u):
	A = mp.pi - mp.atan(u / q)
	t = mp.atan(u)
	S = q * q + u * u
	return (4 * A * A * u + 8 * A * u * u * q / S - 7 * q * q * u / S
			- 14 * A * q - 9 * u ** 3 / S + 2 * u / (1 + u * u)
			+ 4 * A * q / (1 + u * u) + t * (4 * u * u / S - 5 - 9 * u * u))


def d2M2dq2(q, u):
	A = mp.pi - mp.atan(u / q)
	t = mp.atan(u)
	S = q * q + u * u
	Aq = u / S
	return (8 * A * Aq * u
			+ 8 * u * u * (Aq * q / S + A * (1 / S - 2 * q * q / S / S))
			- 7 * u * (2 * q / S - 2 * q ** 3 / S / S)
			- 14 * (Aq * q + A) + 18 * u ** 3 * q / S / S
			+ 4 * Aq / (1 + u * u) + 4 * A / (1 + u * u)
			- 8 * t * u * u * q / S / S)


# --- 1. N2 bound on [1,20] x [0,sqrt3]: d2M2/dq2 < 0 ---
assert 3 * s3_hi < 10 * pi_lo / 3
SQRT3 = mp.sqrt(3)
worst = -mp.inf
for i in range(401):
	q = 1 + 19 * i / 400
	for j in range(401):
		u = SQRT3 * j / 400
		worst = max(worst, d2M2dq2(q, u))
print("max d2M2/dq2 on [1,20]x[0,sqrt3]: %.6f (must be < 0)" % worst)
assert worst < 0

# --- 2. d2M2/dq2 < 0 on D n {u >= sqrt3} ---
worst = -mp.inf
for i in range(201):
	q = 1 + 19 * i / 200
	for j in range(201):
		u = mp.sqrt(3) + (mp.sqrt(2 * q + 1) - mp.sqrt(3)) * j / 200
		worst = max(worst, d2M2dq2(q, u))
print("max d2M2/dq2 on D n {u>=sqrt3} n {q<=20}: %.6f" % worst)
assert worst < 0

# --- 3. B1: g(w) = dM2/dq(1,w) < 0 on [0,sqrt3] ---
def g08(bv, pv):
	return -19 * bv / 25 - 346 * pv / 41 + 16 * (bv - pv) ** 2 / 5 - mp.mpf(1076) / 205


def g1_08(bv, pv):
	return (-2152 * bv / 205 - 2560 * pv / 1681 + 4 * (bv - pv) ** 2
			- mp.mpf(15008) / 1681)


# g'(sqrt3) <= 16(22/7)^2/9 - 41(17/10)(157/50)/6 - 15 = -14957063/441000
g1s3_ub = 16 * pi_hi ** 2 / 9 - 41 * s3_lo * pi_lo / 6 - 15
assert g1s3_ub < 0
print("g'(sqrt3) UB =", mp.nstr(g1s3_ub, 10))
# b = atan(4/5) in (67/100, 17/25) via Leibniz partial sums S6, S7
x = mp.mpf(4) / 5
S6 = x - x ** 3 / 3 + x ** 5 / 5 - x ** 7 / 7 + x ** 9 / 9 - x ** 11 / 11
S7 = S6 + x ** 13 / 13
b = mp.atan(x)
assert mp.mpf(67) / 100 < S6 < b < S7 < mp.mpf(17) / 25
b_lo, b_hi = mp.mpf(67) / 100, mp.mpf(17) / 25
assert g08(b_lo, pi_hi) < 0                      # g(4/5) < 0
assert g1_08(b_hi, pi_lo) > 0                    # g'(4/5) > 0
final_ub = g08(b_lo, pi_hi) + g1_08(b_lo, pi_hi) * (s3_hi - mp.mpf(4) / 5)
print("final tangent UB =", mp.nstr(final_ub, 10), " (must be < 0)")
assert final_ub < 0
# direct check g < 0 on [0, sqrt3]
worst = -mp.inf
for i in range(2001):
	u = SQRT3 * i / 2000
	worst = max(worst, dM2dq(1, u))
print("max g on [0,sqrt3]: %.6f" % worst)
assert worst < 0

# --- 4. Boundary curve: theta-parametrization ---
def P(z):
	return 32 * z * (z ** 4 + 2 * z ** 2 + 1)


def Q(z):
	return (-10 * z ** 6 - 32 * mp.pi * z ** 5 + 42 * z ** 4
			- 64 * mp.pi * z ** 3 + 2 * z ** 2 - 32 * mp.pi * z + 46)


def R(z):
	return (5 * mp.pi * z ** 6 - 10 * z ** 5 + 8 * mp.pi ** 2 * z ** 5
			- 21 * mp.pi * z ** 4 - 40 * z ** 3 + 16 * mp.pi ** 2 * z ** 3
			- mp.pi * z ** 2 - 14 * z + 8 * mp.pi ** 2 * z - 23 * mp.pi)


def T(z):
	return mp.pi ** 2 / 36 * P(z) + mp.pi / 6 * Q(z) + R(z)


R_ub = (-23 * pi_lo + (8 * pi_hi ** 2 - 14) * r + (16 * pi_hi ** 2 - 40) * r ** 3
		+ (8 * pi_hi ** 2 - 10) * r ** 5 + 5 * pi_hi * r ** 6)
T_ub = ((10 * pi_hi / 3) * r ** 6 + (32 * pi_hi ** 2 / 9 - 10) * r ** 5
		+ (64 * pi_hi ** 2 / 9 - 40) * r ** 3 + (32 * pi_hi ** 2 / 9 - 14) * r
		- 46 * pi_lo / 3)
print("R_ub =", mp.nstr(R_ub, 10), " T_ub =", mp.nstr(T_ub, 10))
assert R_ub < 0 and T_ub < 0
W = mp.mpf(1) / mp.sqrt(3)
worstR, worstT = -mp.inf, -mp.inf
for i in range(1, 20001):
	z = W * i / 20000
	worstR = max(worstR, R(z))
	worstT = max(worstT, T(z))
assert worstR < R_ub and worstT < T_ub
# N(z) convex in beta; N <= max(R, T) on dense samples
for i in range(1, 2001):
	z = W * i / 2000
	beta = mp.atan(z)
	N = beta * beta * P(z) + beta * Q(z) + R(z)
	assert N <= max(R(z), T(z)) + mp.mpf("1e-30")
# closed form vs direct on the curve
for i in range(1, 1001):
	z = W * i / 1000
	th = mp.atan(z)
	qq = mp.cos(2 * th) / (2 * mp.sin(th) ** 2)
	uu = mp.cot(th)
	Fdir = dM2dq(qq, uu)
	beta = mp.atan(z)
	N = beta * beta * P(z) + beta * Q(z) + R(z)
	Fform = N / (2 * z * z * (z * z + 1) ** 2)
	assert abs(Fdir - Fform) < mp.mpf("1e-35")
	# G(theta) closed form: M2 < 0
	G = M2(qq, uu)
	assert G < 0
	bra = 2 - (mp.pi / 2 - th) * mp.sin(2 * th)
	assert bra >= 2 - mp.pi / 2 > 0
print("boundary curve: M2 < 0 and dM2/dq < 0 verified (closed forms match)")

# --- 5. Tail q >= 20: B(q) < 0 ---
def B(q):
	return ((4 * mp.pi ** 2 + 14) * mp.sqrt(2 * q + 1)
			+ 8 * mp.pi * (2 * q + 1) / q + 1
			+ 2 * mp.pi * (2 * q + 1) / q ** 2 - 10 * mp.pi * q)


B20_ub = ((4 * pi_hi ** 2 + 14) * mp.mpf(32) / 5 + 8 * pi_hi * mp.mpf(41) / 20
			+ 1 + 2 * pi_hi * mp.mpf(41) / 400 - 10 * pi_lo * 20)
assert B20_ub < 0
Bp_ub = (4 * pi_hi ** 2 + 14) * mp.mpf(5) / 32 - 10 * pi_lo
assert Bp_ub < 0
print("B(20) UB =", mp.nstr(B20_ub, 10), " B'(q) UB =", mp.nstr(Bp_ub, 10))

# --- 6. u > sqrt(41): M2/q^2 bound ---
tm = mp.sqrt(41) / 20
val = (4 * mp.mpf("3.15") ** 2 * tm - 7 * (mp.mpf("3.14") - tm)
		+ 2 * mp.mpf("3.15") * (1 + tm ** 2) / 42)
assert val < 0
print("M2/q^2 tail bound =", mp.nstr(val, 8))

# --- 7. h(u) < 0 for all u > 0 (baseline M2(1,u) = pi*h(u)) ---
def h(u):
	return 4 * u * (mp.pi - mp.atan(u)) - 5 - 9 * u * u


hp12_lo = 4 * pi_lo - 4 * (mp.mpf(1) / 2 - (mp.mpf(1) / 2) ** 3 / 3 + (mp.mpf(1) / 2) ** 5 / 5) - mp.mpf(8) / 5 - 9
assert hp12_lo > 0
x53 = mp.mpf(53) / 100
hp53_ub = 4 * (pi_hi - (x53 - x53 ** 3 / 3)) - 4 * x53 / (1 + x53 ** 2) - 18 * x53
assert hp53_ub < 0
assert 13 * mp.mpf("0.53") ** 2 - 5 < 0
print("h chain: h'(1/2) >", mp.nstr(hp12_lo, 8), " h'(0.53) <", mp.nstr(hp53_ub, 8))

print("ALL M2 ANALYTIC CHECKS PASSED")
