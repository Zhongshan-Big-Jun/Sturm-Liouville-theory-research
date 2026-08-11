# -*- coding: utf-8 -*-
# 2026-08-12: 张力不等式新形式 (qt+c)*Delta > c(1-qt^2)s1^2s2^2[(pi-g)^2-a1^2]
# 全局 2D 扫描: 最大值, 以及分解路径的验证
import math
import numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)

def quant(qt, g):
    c = math.atan(qt*math.tan(g))/(math.pi - g)
    a1 = alpha1(qt, c)
    s1 = math.sin(a1); s2 = math.sin(g)
    Del = (math.pi-g)**2*s2*s2 - a1*a1*s1*s1
    return c, a1, s1, s2, Del

# 2D scan: max of tension ratio R = c(1-qt^2)s1^2s2^2[(pi-g)^2-a1^2] / ((qt+c)*Del)
worst = 0.0; worst_at = None
grid_q = np.linspace(0.0005, 0.999, 120)
for qt in grid_q:
    g0q = math.acos(qt/(1+qt))
    gs = np.linspace(gstar + 1e-6, g0q - 1e-6, 800)
    for g in gs:
        c, a1, s1, s2, Del = quant(qt, g)
        if Del <= 0:
            print("Del<=0!", qt, g, Del); raise SystemExit
        num = c*(1-qt*qt)*s1*s1*s2*s2*((math.pi-g)**2 - a1*a1)
        den = (qt+c)*Del
        r = num/den
        if r > worst:
            worst = r; worst_at = (qt, g)
print(f"global max tension ratio = {worst:.6f} at qt={worst_at[0]:.4f} gamma={worst_at[1]:.5f} (gstar={gstar:.5f})")

# 分解路径 1: (A) c <= qt/(1-qt^2) 且 (B) Del >= s1^2s2^2[(pi-g)^2-a1^2]  => 张力<1
# 检查 (A) 与 (B) 各自成立范围及并集覆盖
covA = covB = covAB = 0; total = 0
for qt in grid_q:
    g0q = math.acos(qt/(1+qt))
    gs = np.linspace(gstar + 1e-6, g0q - 1e-6, 300)
    for g in gs:
        total += 1
        c, a1, s1, s2, Del = quant(qt, g)
        A = c <= qt/(1-qt*qt) + 1e-12
        B = Del >= s1*s1*s2*s2*((math.pi-g)**2 - a1*a1) - 1e-12
        if A: covA += 1
        if B: covB += 1
        if A or B: covAB += 1
print(f"coverage: A={covA/total:.4f} B={covB/total:.4f} AorB={covAB/total:.4f} total={total}")

# 分解路径 2: 直接验证张力 <= 0.72 的端点界: 检查张力在 gamma 上的最大值 = gamma0* 处
print("== 张力端点最大验证 (细化) ==")
for qt in [0.5, 0.3, 0.15, 0.08, 0.04, 0.02, 0.01, 0.005, 0.002, 0.001]:
    g0q = math.acos(qt/(1+qt))
    gs = np.linspace(gstar + 1e-7, g0q - 1e-7, 3000)
    mx = 0.0; mg = None
    for g in gs:
        c, a1, s1, s2, Del = quant(qt, g)
        num = c*(1-qt*qt)*s1*s1*s2*s2*((math.pi-g)**2 - a1*a1)
        r = num/((qt+c)*Del)
        if r > mx: mx = r; mg = g
    print(f"qt={qt:7.4f} max_ratio={mx:+.6f} at gamma={mg:.5f}")