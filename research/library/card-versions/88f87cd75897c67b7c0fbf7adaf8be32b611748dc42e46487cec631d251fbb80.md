---
title: 二维相位参数化证书 (phase-param-2d-certificate)
tags: [mathtool, self-developed]
source: 自研 (O3a I3, 会话 38, 2026-08-09)
status: E1 端点与包含性已证; J1 侧 16 叶盒证书已被定理 5.8 完全解析化取代 (会话 40); J2 侧 67 叶盒证书仍为 E2
created: 2026-08-09
---

# 二维相位参数化证书 (phase-param-2d-certificate)

## 解析
目标: 证明 $\widetilde F_e''(q,c)>0$ 于 $Q=[1,2]\times[0.4,0.5]$ (KEY LEMMA 的 I3 子命题).
1. **二阶导恒等式** (E1): $\widetilde F_e''=\widetilde M_{f1}J_1-\widetilde M_{f2}J_2$,
   其中 $M_k=\widetilde M_f(\alpha_k(c);c)>0$,
   $J(x;c)=G(x;c)^2-\frac{x\Phi_q(x)}{q+c\Phi_q(x)}G_x(x;c)+G_c(x;c)$,
   $G_x=\partial_xG$, $G_c=\partial_cG$, 末项来自 $\alpha_k'(c)=-\alpha_k\Phi_q/(q+c\Phi_q)$.
2. **相位方程显式反解** (E1): 沿真实曲线
   $c=c_1(x,q):=\frac1x\arctan\frac1{q\tan x}$ ($x=\alpha_1$),
   $c=c_2(\gamma,q):=\frac{\arctan(q\tan\gamma)}{\pi-\gamma}$ ($\gamma=\pi-\alpha_2$);
   定义 $J_1^{(2)}(x,q):=J(x;c_1(x,q))$, $J_2^{(2)}(\gamma,q):=J(\pi-\gamma;c_2(\gamma,q))$.
3. **包含引理** (E1): 隐函数单调性 ($\alpha_1$ 关于 $q,c$ 递减; $\gamma$ 关于 $q$ 递减、$c$ 递增) 给出
   $0.841<\alpha_1(q,c)<1.1220$, $0.655<\gamma(q,c)<1.0472$ 于 $Q$.
   端点闭式: $\alpha_1(2,1/2)=\arccos(2/3)$, $\alpha_1(1,2/5)=5\pi/14$,
   $\gamma(1,1/2)=\pi/3$; $\gamma(2,2/5)>0.655$ 由有理三角级数界链
   (cos 交错下界 $>2/3$; tan 上界 $<0.7682$; atan S5 下界 $>0.5767$; $\pi\in(3.14159,3.1416)$).
4. **叶盒证书** (E2): 原 $J_1^{(2)}>0$ 于 $[0.841,1.1220]\times[1,2]$ 的 16 叶盒证书
   (认证下界 $+0.420803280435$) 已被定理 5.8 (会话 40) 的完全解析下界
   $J_1^{(2)}\ge6499/7500$ 取代并从证明移除 (叶盒文件保留为历史产物);
   $J_2^{(2)}<0$ 于 $[0.655,1.0472]\times[1,2]$
   (67 叶盒, 认证上界 $-0.062083223779$). 引擎: mpmath.iv dps=50 向外舍入,
   atan 用交替级数 + 显式余项 ($z>1$ 用 $\arctan z=\pi/2-\arctan(1/z)$ 约化),
   叶面积覆盖审计 + 80 位点交叉检验 (415 点 0 失败).

## 适用范围
- 适用: 相位方程可显式反解出 $c$ 的一维隐式曲线场景; 把 ``隐式相位根 + 三维盒'' 证书
  降维为二维显式函数叶盒证书; 与 [[interval-ad-certificate]] 配合.
- 边界情形: 盒端点必须严格包含真实曲线; 优先用端点闭式, 否则用单调性 + 有理三角
  级数界 (E1) 或同一区间引擎验证 (E2); 盒端点有理化时注意交错级数上下界方向
  (sin/cos/atan 的奇偶部分和方向不同).
- 不适用: 相位方程不可显式反解; 单调性不成立的参数域; 区间依赖性问题使认证余量过小.
- 重要教训 (本会话): 交接摘要声称的盒下界 0.8411 与 0.6557 经严格核验分别大于真实端点
  $\arccos(2/3)=0.8410687$ 与 $\gamma(2,2/5)=0.6556493$, 原盒漏条 (差值约 3e-5 与 5e-5);
  修正为 0.841 与 0.655 后重算证书. 任何数值声称的盒端点必须先做包含性核验.

## 验证与备注
- 来源: 会话 38 (O3a I3 去证书化, 3D 盒到 2D 参数化); 脚本
  scripts/verify_o3a_i3_2d.py (SHA-256 132e998f2a4f4807443c33e669435d6382de646b88be25d42e455251c7447f4a);
  叶盒 misc/i3_2d_leaves_P1_J1_gt0.json (SHA-256 c3375dc2...) 与
  misc/i3_2d_leaves_P2_J2_lt0.json (SHA-256 9317c6f6...).
- 精度: J2 侧认证余量 0.0621 (67 叶盒); J1 侧证书已移除 (解析化); 叶面积总和 = 盒面积; 80 位点交叉 0 失败.
- 会话 40: J1 侧解析化由 scripts/verify_o3a_i3_t1_e1.py (SHA-256
  64e24ace3117772b6cd2ea2ac53986a75cad6c3fd797b61369472ac87ec6ab04) 复核,
  七步链给出 J1_2d >= 6499/7500 于 T1 闭包 (定理 5.8).
- 相关: [[key-lemma-decomposition]], [[interval-ad-certificate]], [[phase-ratio-rigidity]].
