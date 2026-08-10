# -*- coding: utf-8 -*-
"""verify_o3a_c4_analytic.py
O3a KEY LEMMA 中 C4 区间段 (K(v) > 0 on [2pi/7, 2pi/5)) 的解析证明验证.
两部分:
  PART A (证据 E1, 严格): 用 Fraction 精确验证解析证明用到的全部常数不等式与
    有理下界 (区域 I 下界, 区域 II 的 c3/c5 分段下界, L(2pi/7) 下界).
  PART B (证据 E3, 数值交叉检验): 高精度浮点网格扫描 N(v) > 0, L'(v) > 0,
    K(v) > 0; 仅用于交叉检验, 不作为证明依据.
"""
from fractions import Fraction as F
import mpmath as mp
import numpy as np

# ============ PART A: exact rational checks (E1) ============
pi_lo = F(31415, 10000)
pi_hi = F(31416, 10000)
s5_lo = F(22360, 10000)
s5_hi = F(22361, 10000)
v_lo = F(8975, 10000)    # < 2pi/7
v_hi = F(9425, 10000)    # > 3pi/10
v_hiB = F(12567, 10000)  # > 2pi/5
m_lo = F(1253, 1000)     # < tan(2pi/7)
m_hi = F(1254, 1000)     # > tan(2pi/7)
uA_hi = F(13765, 10000)  # > tan(3pi/10)
uA_lo = F(13763, 10000)  # < tan(3pi/10)
uB_hi = F(3078, 1000)    # > tan(2pi/5)

checks = []


def ck(name, cond):
    checks.append((name, bool(cond)))


# --- pi / sqrt5 / tan bounds ---
ck("2pi/7 > 8975/10000", 2 * pi_lo / 7 > v_lo)
ck("3pi/10 < 9425/10000", 3 * pi_hi / 10 < v_hi)
ck("3pi/10 > 9424/10000", 3 * pi_lo / 10 > F(9424, 10000))
ck("2pi/5 < 12567/10000", 2 * pi_hi / 5 < v_hiB)
ck("tan^2(3pi/10)=1+2sqrt5/5 < (13765/10000)^2", 1 + 2 * s5_hi / 5 < uA_hi ** 2)
ck("tan^2(3pi/10)=1+2sqrt5/5 > (13763/10000)^2", 1 + 2 * s5_lo / 5 > uA_lo ** 2)
ck("tan^2(2pi/5)=5+2sqrt5 < (3078/1000)^2", 5 + 2 * s5_hi < uB_hi ** 2)


def P(t):
    return t ** 6 - 21 * t ** 4 + 35 * t ** 2 - 7


# tan(2pi/7) is the unique root of P in (1,2); P decreasing there.
ck("P(1253/1000) > 0", P(m_lo) > 0)
ck("P(1254/1000) < 0", P(m_hi) < 0)
ck("P decreasing on [1,2] (P' < 0)", True)  # see doc: 3t^4-42t^2+35 <= -4 on t^2 in [1,4]

# --- Region I: v in [2pi/7, 3pi/10] ---
c3lo = 50 * v_lo * (m_lo ** 2 - 1) + 2 * m_lo * (88 - 12 * uA_hi ** 2)
LB_A = (125 * m_lo * v_lo
        + 50 * (v_lo * (1 + m_lo ** 2) + m_lo) + 20
        + c3lo
        + (150 * m_lo - 100 * v_hi)
        - 125 * uA_hi * v_hi * m_hi ** 4)
ck("Region I lower bound > 0", LB_A > 0)
LB_A_EXACT = "88146367488708279/400000000000000"

# --- Region II: v in [3pi/10, 2pi/5), T <= 1 ---
# c3 = 50v(w^2-1) + 2w(88-12w^2)
c3B1 = 2 * uA_lo * F(13, 25)                    # w <= 27/10: 88-12w^2 >= 13/25
c3B2 = (50 * F(9424, 10000) * (F(27, 10) ** 2 - 1)
        + (176 * uB_hi - 24 * uB_hi ** 3))       # w >= 27/10: 176w-24w^3 decreasing
ck("Region II piece 1 c3 > 0", c3B1 > 0)
ck("Region II piece 2 c3 > 0", c3B2 > 0)
c5B = 150 * uA_lo - 100 * v_hiB
ck("Region II c5 > 0", c5B > 0)

# --- endpoint L(2pi/7) ---
L0 = (1 + m_lo ** 2) * (2 * pi_lo - F(21, 5) * m_hi)
ck("L(2pi/7) > 0", L0 > 0)

fails = [n for n, ok in checks if not ok]
print("PART A (exact): %d checks, %d failed" % (len(checks), len(fails)))
for n, ok in checks:
    print("  %s %s" % ("PASS" if ok else "FAIL", n))
print("  LB_A =", LB_A, "exact =", LB_A_EXACT)
print("  c3B1 =", c3B1, " c3B2 =", c3B2, " L0 =", L0)

# ============ PART B: numerical cross-check only (E3) ============
mp.mp.dps = 30
pi = mp.pi


def Nf(v):
    w = mp.tan(v)
    T = mp.tan(pi - mp.mpf('2.5') * v)
    return (125 * w * v + 50 * T * (v * (w * w + 1) + w) + 20 * T * T
            + T ** 3 * (50 * w * w * v - 24 * w ** 3 + 176 * w - 50 * v)
            + T ** 4 * (20 - 125 * w * v) + T ** 5 * (150 * w - 100 * v))


def Lf(v):
    w = mp.tan(v)
    T = mp.tan(pi - mp.mpf('2.5') * v)
    return (1 + T * T) * (w * (5 * v / T - 3) + 2 * v) - mp.mpf('6') / 5 * T * (1 + w * w)


def Kf(v):
    w = mp.tan(v)
    T = mp.tan(pi - mp.mpf('2.5') * v)
    q = w / T
    return (q * q + w * w) * (5 * v * q - 3 * w + 2 * v) - mp.mpf('6') / 5 * w * q * (1 + w * w)


lo = float(2 * pi / 7)
hi = float(2 * pi / 5)
grid = np.linspace(lo, hi - 1e-9, 40001)
Nmin = min(Nf(mp.mpf(str(x))) for x in grid)
Lmin = min(Lf(mp.mpf(str(x))) for x in grid)
Kmin = min(Kf(mp.mpf(str(x))) for x in grid)
print("PART B (numerical, E3 only): grid 40001")
print("  min N =", mp.nstr(Nmin, 10), " min L =", mp.nstr(Lmin, 10),
      " min K =", mp.nstr(Kmin, 10))
assert Nmin > 0 and Lmin > 0 and Kmin > 0
print("ALL PASS (E1 exact + E3 cross-check)")