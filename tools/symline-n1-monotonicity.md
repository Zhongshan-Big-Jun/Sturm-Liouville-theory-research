---
canonical_key: symmetric-line 1D monotonicity (INF side, gap (a) closure)
title: 对称线 1D 单调性: KEY LEMMA 与精确降维恒等式 (symmetric-line n=1 monotonicity)
tags: [mathtool, self-developed, phase-param, gap-extremals, inf-side]
source: 自研 (会话续作 2026-08-10; 承接 [[well-family-rigidity]] 缺口 (a))
status: 定理已证 (STRICT, docs/SL_gap_n1_symline_proof.pdf, 10 页零警告); W0 证书精确有理不等式 sympy 全过; 数值交叉检验为 EVIDENCE; 2026-08-12 更新: 全 R>1 版本已闭合 (见 [[tension-ratio-chain]])
created: 2026-08-10
---

# 对称线 1D 单调性: KEY LEMMA 与精确降维恒等式

## 解析
对 Dirichlet 弦 -y'' = lambda*rho*y 的阱族对称线
rho_v = R*1_[0,v)∪(1-v,1] + 1_[v,1-v] (v in (0,1/2), 1 < R <= 3/2):
m = sqrt(R), q~ = 1/m in [q0,1), q0 = sqrt(2/3). 相位参数
c = (1-2v)/(2mv) in (0,inf). 偶/奇相位分支 alpha_1 in (0,pi/2),
alpha_2 in (0,pi) 满足 E(alpha_1) = c*alpha_1, O(alpha_2) = c*alpha_2
(E(x) = arctan(1/(q~ tan x)), O 为连续奇支); alpha_k'(c) =
-alpha_k*Phi(alpha_k)/(q~ + c*Phi(alpha_k)), Phi = cos^2 + q~^2 sin^2,
s_k = 2(c+q~)*alpha_k.

**KEY LEMMA (定理 5.2, STRICT)**: F~_e(c) = M_f(alpha_1;c) - M_f(alpha_2;c),
M_f(x;c) = x^2 sin^2x/(q~ + c*Phi(x)), 在 (0,inf) 恰有一个零点
c* in (0,1/2). 三个成分:
1. **分解**: F~_e' = (M_1-M_2)G_1 + M_2(G_1-G_2),
   G(x;c) = -Phi(3+2x cot x)/(q~+c*Phi) + 2cx*Phi(q~^2-1)sin x cos x/(q~+c*Phi)^2.
   若 G_1 < 0 且 G_1 < G_2, 则 F~_e >= 0 推出 F~_e' < 0
   (``非负集上严格递减''), 加端点符号得唯一零点.
2. **P1 (引理 4.1)**: G_1 <= -(6*sqrt6 - 6)/5 < -4/3. 只用 alpha_1 in (0,pi/2),
   Phi_1 >= q~^2, W_1 = 3+2*alpha_1*cot(alpha_1) >= 3, c < 1/2.
3. **P2 (引理 4.1+4.2)**: G_2 > -4/3. gamma := pi - alpha_2 in (0,Gamma],
   Gamma = arccos(q0/(1+q0)) ~ 1.1046 < pi/2; W0 引理: W0(gamma) =
   3 - 2(pi-gamma)cot(gamma) 在 (0,Gamma] 严格递增且 W0(Gamma) < (4/3)q0
   (附录 A 精确有理证书). 分情形: W0 <= 0 则 G_2 >= 0; 0 < W0 则
   G_2 >= -W0/q~ >= -W0/q0 > -4/3.

**精确降维恒等式 (引理 3.3, STRICT)**: 对 xi 对称参数化
S_R(xi) = R_1(xi,1-xi) = R_2(xi,1-xi) = -8q~^2(c+q~)^3 F~_e(c);
D_c = -8(c+q~)q~(1-q~^2) F~_e(c). 推导: D_c 用 alpha_k' 直接代入; S_R 用
Feynman-Hellmann (dD/da = -(R-1)f(a), dD/db = +(R-1)f(b)) + 链式法则
D_xi = -2(R-1)S_R, xi'(c) = -q~/(2(c+q~)^2), R-1 = (1-q~^2)/q~^2.
结论: f(v) 的零点与 D(v) 的临界点归结为标量函数 F~_e 的唯一零点.

**端点与易区**: F~_e(0+) = pi^2/(4q~) > 0; F~_e(1/2) < 0, 用结构恒等式
alpha_1(1/2)+alpha_2(1/2) = pi (t = tan(alpha_1/2) 满足 t^2 = 1/(2q~+1)
同时解偶/奇方程) 得 F~_e(1/2) = pi*sin^2(alpha_1)(2alpha_1-pi)/(q~+Phi/2) < 0.
c >= 1/2 易区: phi_c(x) = x^2 sin^2x/(q~+c*Phi) 在 (0,pi/2) 严格递增
(q~ < 1 第三项为正), 分 c in [1/2,1] (gamma >= alpha_1 + ((pi-gamma)/gamma)^2 >= 1)
与 c >= 1 (alpha_1 < alpha_2) 两段得 F~_e < 0.

**D 单峰 (定理 5.1)**: sign(dD/dv) = sign F~_e(c(v)) (sign D_c = -sign F~_e,
v' < 0), 故 D 在 (0,v*) 严格递减、(v*,1/2) 严格递增; v* = v(c*) in
(1/(m+2),1/2); D(v*) < 3pi^2/R; 端点 D(0+) = 3pi^2, D(1/2-) = 3pi^2/R.

**推论 (INF 闭合, 1 < R <= 3/2)**: 极小点为 good root (O1 第 5-7 步) +
小 R 阱族刚性 (a+b=1) + 对称线上唯一临界点即整体极小 + 边界情形排除
(O3b: D > 3pi^2/R 于两块边界; D(v*) < 3pi^2/R) => INF 下确界 I(R) 在
对称阱 [R,1,R] 达到, I(R) = D(v*(R)) < 3pi^2/R.

## 适用范围
- **适用**: 阱族对称线 1D 分析 (1 < R <= 3/2, 本文件的小 R 版本), 即
  [[well-family-rigidity]] 缺口 (a) 的闭合; 与 [[gap-n1-reduction]] (O1-INF 归约)
  + 小 R 刚性定理配合得到 INF 侧 1 < R <= 3/2 的完整闭合.
  全部 R>1 的闭合见 [[tension-ratio-chain]] (2026-08-12, 会话续作): 张力比链
  rho <= rho0 + 一维单峰不等式, STRICT, 9 页零警告.
- **边界情形**: R = 3/2 (q~ = q0, 含于定理, P2 证书严格); R -> 1+ (q~ -> 1-,
  c* -> 0.1917 极限); c -> 0+ / c -> inf 对应 v -> 1/2- / v -> 0+ 端点极限.
- **不适用**: R > 3/2 (q~ < q0) 时本文件 P1/P2 常数失效 (q0 = sqrt(2/3)
  为阈值, 数值显示 R > 1.5 出现离轴 E=0 分支, 机制不同); 该限制已由
  [[tension-ratio-chain]] 的全 R 链消除 (2026-08-12). 垒族 (q > 1) 由
  [[phase-ratio-rigidity]] 处理, 符号结构不同.
- **关键技巧**: (i) ``非负集上严格递减'' 比逐点 F' < 0 弱但足够, 避免证明
  G_2 全域正下界; (ii) 端点闭式优先找结构恒等式 (c = 1/2 处 alpha_1+alpha_2 =
  pi), 显式闭式仅备查; (iii) 大余量初等界 (Phi <= 1, D >= q~, Phi_1 >= q~^2,
  W_1 >= 3) 优于精细盒式证书.

## 验证与备注
- 严格证明文档: `docs/SL_gap_n1_symline_proof.pdf` (10 页, 零警告, 2026-08-10),
  含 W0 引理与附录 A 精确有理证书 (q0 > 2247/2753, Gamma < 10/9,
  cot(10/9) > 2121769/4288410, 组合不等式 271586432/135084915 >
  15789/8259), 全部 sympy True (`scripts/_symline/key_lemma_certificate.py`).
- EVIDENCE 脚本 (不构成证明): `master_verify.py` (相位分支 vs 直接 secular
  1e-51; mode-2 范数闭式缺陷已登记); `key_lemma_verify.py` (P1 max ~ -2.4621
  < -1.7394; P2 min ~ -0.4000 > -1.2247; c*: 0.1821@q0, 0.1917@q=1;
  max F~_e' 于 {F~_e >= 0} <= -7.58; 易区 [0.5,50] max <= -2.6e-7;
  D_c 符号同 -F~_e 0 违规; S_R 恒等式 <= 1.3e-11); `key_lemma_verify2.py`
  (gamma <= Gamma 全过; W0 分情形 878+151 例; alpha_1+alpha_2 = pi 至 1e-31;
  F~_e(1/2) 公式比值 = 1); `sym_endpoint_fixed.py` (导数闭式
  F~_e'(q,1/2) = -2pi(1-cos x)^3 T(x)/sin^3 x, x = arccos(q/(1+q)),
  T > 0 于 [pi/3,pi/2], 验证至 1e-29; 值由结构恒等式给出, 两者均负).
- 缺陷登记: `master_verify.py` mode-2 范数闭式与直接积分相对误差 ~0.5
  (KEY LEMMA 不依赖, 不影响结论); `sym_endpoint.py` (未修正版) G2 第二项多乘
  因子 t; `key_lemma_verify.py` v1 将 3pi^2/R 对照误打印为 3pi^2*m^2.
- 失败路线: F~_e'' 整符号路线 (F~_e'' 实际在 [0.42,0.5] 为正, 放弃);
  G2 >= 0 于 c <= 0.40 只对相位曲线成立 (自由区域 G2(2.174,gamma->0) = -9);
  W0 全域正性误判 (W0(0.1) ~ -57.6, W0(0+) = 3-2pi < 0, 必须分情形);
  详见 `docs/SL_gap_n1_symline_summary.pdf` (4 页).
- 相关工具: [[well-family-rigidity]], [[phase-ratio-rigidity]], [[gap-n1-reduction]],
  [[feynman-hellmann]], [[gap-band-extremals]], [[key-lemma-decomposition]].
