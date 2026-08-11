# -*- coding: utf-8 -*-
# 2026-08-12 会话 58 续作: 缺口 (a') 全 R 对称线证明的数值交叉检验 (EVIDENCE only)
# 对应 docs/SL_gap_n1_symline_allR_proof.tex 附录 B 的六项声明.
# 大网格用 scipy 双精度; 角点/端点/最小余量点用 mpmath 50 位复核.
# 所有输出仅供交叉检验, 不构成证明依据.
import math
import numpy as np
from scipy.optimize import brentq as scipy_brentq
from mpmath import mp, mpf, tan, sin, cos, acos, atan, pi, findroot

mp.dps = 50

def alpha1_dbl(qt, c):
    # tan(a)*tan(c*a) = 1/qt, a in (0, pi/2); 用 u = pi/2 - a 稳定形式
    f = lambda u: math.tan(c*(math.pi/2 - u))/math.tan(u) - 1.0/qt
    return math.pi/2 - scipy_brentq(f, 1e-300, math.pi/2 - 1e-13)

def alpha2_dbl(qt, c):
    f = lambda a: qt*math.tan(a) + math.tan(c*a)
    return scipy_brentq(f, math.pi/2 + 1e-13, math.pi - 1e-13)

def Phi_dbl(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2

def Mf_dbl(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi_dbl(qt, x))

def Fe_dbl(qt, c):
    return Mf_dbl(qt, c, alpha1_dbl(qt, c)) - Mf_dbl(qt, c, alpha2_dbl(qt, c))

def rho_dbl(qt, g):
    c = math.atan(qt*math.tan(g))/(math.pi - g)
    a1 = alpha1_dbl(qt, c)
    y = math.pi - g; s1 = math.sin(a1); s2 = math.sin(g)
    Del = y*y*s2*s2 - a1*a1*s1*s1
    return c*(1-qt*qt)*s1*s1*s2*s2*(y*y - a1*a1)/((qt + c)*Del)

def rho0_dbl(g):
    y = math.pi - g; t = math.tan(g); s2 = math.sin(g); p = math.pi*math.pi/4
    return t/(y+t)*s2*s2*(y*y - p)/(y*y*s2*s2 - p)

def W0_dbl(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)

# ---- mpmath 版本 (复核用) ----
def alpha1_mp(qt, c):
    f = lambda u: tan(c*(mpf(1)/2*pi - u))/tan(u) - 1.0/qt
    return pi/2 - _bisect(f, mpf('1e-300'), pi/2 - mpf('1e-45'))

def _bisect(f, lo, hi, tol=mpf('1e-50')):
    flo, fhi = f(lo), f(hi)
    assert flo*fhi < 0, (flo, fhi)
    while hi - lo > tol:
        mid = (lo + hi)/2
        fm = f(mid)
        if flo*fm <= 0:
            hi = mid
        else:
            lo = mid; flo = fm
    return (lo + hi)/2

def rho_mp(qt, g):
    c = atan(qt*tan(g))/(pi - g)
    a1 = alpha1_mp(qt, c)
    y = pi - g; s1 = sin(a1); s2 = sin(g)
    Del = y*y*s2*s2 - a1*a1*s1*s1
    return c*(1-qt*qt)*s1*s1*s2*s2*(y*y - a1*a1)/((qt + c)*Del)

def rho0_mp(g):
    y = pi - g; t = tan(g); s2 = sin(g); p = pi*pi/4
    return t/(y+t)*s2*s2*(y*y - p)/(y*y*s2*s2 - p)

gstar_d = scipy_brentq(W0_dbl, 1e-9, math.pi/2 - 1e-9)
gstar_m = findroot(lambda g: 3 - 2*(pi - g)*cos(g)/sin(g), mpf('0.9669'))

print("=== A1. 张力比链 rho <= rho0 (37500 点: q~ in [1e-13,1), gamma in [g0*, pi/2)) ===")
nq, ng = 150, 250
gs = gstar_d + (math.pi/2 - 1e-8 - gstar_d)*np.arange(ng)/(ng-1)
qs = np.geomspace(1e-13, 1-1e-13, nq)
worst = 1e9; worst_at = None; viol = 0
for g in gs:
    for q in qs:
        r = rho_dbl(q, g); r0 = rho0_dbl(g)
        m = r0 - r
        if r > r0 + 1e-12:
            viol += 1
        if m < worst:
            worst = m; worst_at = (q, g)
print("points=%d violations=%d min(rho0-rho)=%.3e at q=%.3e gamma=%.9f" % (nq*ng, viol, worst, worst_at[0], worst_at[1]))
# mpmath 复核最小余量点邻域 (角点附近)
q0, g0 = worst_at
for (qq, gg) in [(q0, g0), (mpf('1e-6'), pi/2 - mpf('1e-6')), (mpf('1e-9'), pi/2 - mpf('1e-9')), (mpf('1e-12'), pi/2 - mpf('1e-12'))]:
    r = rho_mp(mpf(qq), mpf(gg)); r0 = rho0_mp(mpf(gg))
    print("  mpmath q=%.3e g=pi/2-%.3e: rho=%.10f rho0=%.10f margin=%.3e" % (qq, pi/2 - gg, r, r0, r0 - r))

print("=== A2. rho0 < 1 (200000 点, gamma in [g0*, pi/2)) ===")
N = 200000
gs2 = gstar_d + (math.pi/2 - 1e-12 - gstar_d)*np.arange(N)/(N-1)
vals = np.array([1 - rho0_dbl(g) for g in gs2])
i = int(np.argmin(vals))
print("min(1-rho0)=%.3e at gamma=%.12f (pi/2-gamma=%.3e)" % (vals[i], gs2[i], math.pi/2 - gs2[i]))
r0m = rho0_mp(mpf(gs2[i]))
print("  mpmath 复核: 1-rho0 = %.6e" % (1 - r0m))

print("=== A3. 等价性 F~e<0 <-> rho<1 (20000 点, Claim A 域 gamma in [g0*, gamma0(q)]) ===")
nq, ng = 100, 200
viol = 0; total = 0; minmarg = 1e9
qs3 = np.linspace(1e-8, 0.999999, nq)
for q in qs3:
    g0q = math.acos(q/(1+q))
    gs3 = gstar_d + (g0q - gstar_d)*np.arange(ng)/(ng-1)
    for g in gs3:
        c = math.atan(q*math.tan(g))/(math.pi - g)
        if not (1e-12 < c < 0.5 - 1e-12):
            continue
        total += 1
        fv = Fe_dbl(q, c); r = rho_dbl(q, g)
        if (fv < 0) != (r < 1):
            viol += 1
        minmarg = min(minmarg, abs(fv))
print("points=%d violations=%d min|Fe|=%.3e (mpmath 复核下一点)" % (total, viol, minmarg))

print("=== A4. 端点: F~e(0+)=pi^2/(4q), F~e(1/2)<0, F~e(c0(q))<0 (mpmath 50 位) ===")
def Fe_mp(qt, c):
    a1 = alpha1_mp(qt, c)
    a2 = _bisect(lambda a: qt*tan(a) + tan(c*a), pi/2 + mpf('1e-45'), pi - mpf('1e-45'))
    Ph1 = cos(a1)**2 + qt*qt*sin(a1)**2
    Ph2 = cos(a2)**2 + qt*qt*sin(a2)**2
    M1 = a1*a1*sin(a1)**2/(qt + c*Ph1)
    M2 = a2*a2*sin(a2)**2/(qt + c*Ph2)
    return M1 - M2
for q in [mpf('0.001'), mpf('0.01'), mpf('0.1'), mpf('0.3'), mpf('0.5'), mpf('0.7'), mpf('0.9')]:
    c0 = atan(q*tan(gstar_m))/(pi - gstar_m)
    f_eps = Fe_mp(q, mpf('1e-12'))
    f_half = Fe_mp(q, mpf('0.5') - mpf('1e-30'))
    f_c0 = Fe_mp(q, c0)
    print("q=%.3f c0=%.8f F~e(1e-12)=%.6e (pi^2/(4q)=%.6e)  F~e(1/2-)=%.6e  F~e(c0)=%.6e"
          % (q, c0, f_eps, pi*pi/(4*q), f_half, f_c0))

print("=== A5. 角点渐近: gamma = pi/2 - t*q~, K(t) := (1-rho)/q~ (mpmath 50 位) ===")
for t in [mpf('0.25'), mpf('0.5'), mpf('1'), mpf('2'), mpf('5'), mpf('10'), mpf('20')]:
    q = mpf('1e-10')
    g = pi/2 - t*q
    r = rho_mp(q, g)
    K = (1 - r)/q
    print("t=%.2f  q~=1e-10  K(t)=%.6f" % (t, K))

print("=== A6. 引理 ys2: y^2 sin^2 gamma >= pi^2/4 on [g0*, pi/2) ===")
gs6 = gstar_d + (math.pi/2 - 1e-12 - gstar_d)*np.arange(50000)/49999
v6 = (math.pi - gs6)**2 * np.sin(gs6)**2 - math.pi*math.pi/4
i6 = int(np.argmin(v6))
print("min(y^2 s2^2 - pi^2/4)=%.3e at gamma=%.12f (应仅在 pi/2 处取 0)" % (v6[i6], gs6[i6]))
