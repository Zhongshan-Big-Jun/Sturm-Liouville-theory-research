---
canonical_key: tension-ratio-chain (INF side, gap (a') closure for all R>1)
title: 张力比链: 比值上界化到退化极限 + 一维单峰不等式 (tension-ratio chain)
tags: [mathtool, self-developed, phase-param, gap-extremals, inf-side, rational-certificate]
source: 自研 (会话续作 2026-08-12; 承接 [[symline-n1-monotonicity]] 缺口 (a'))
status: 定理已证 (STRICT, docs/SL_gap_n1_symline_allR_proof.pdf, 9 页零警告; 精确有理证书 ALL PASS; 数值交叉检验为 EVIDENCE)
created: 2026-08-12
---

# 张力比链: 比值上界化到退化极限 + 一维单峰不等式

## 解析
对 Dirichlet 弦 -y'' = lambda*rho*y 的阱族对称线
rho_v = R*1_[0,v)∪(1-v,1] + 1_[v,1-v] (v in (0,1/2), 全部 R>1):
m = sqrt(R), q~ = 1/m in (0,1). 相位参数 c = (1-2v)/(2mv) in (0,1/2),
偶分支 A = alpha_1 in (0,pi/2), 奇分支 alpha_2 = pi - gamma,
gamma in (0, gamma_0(q~)], gamma_0(q~) = arccos(q~/(1+q~)),
c = arctan(q~ tan gamma)/y, y = pi - gamma, s_1 = sin A, s_2 = sin gamma.

**等价性引理 (STRICT)**: 设 Delta = y^2 s_2^2 - A^2 s_1^2 > 0, 则
F~_e(c) < 0 等价于张力比
rho(q~,gamma) = c(1-q~^2) s_1^2 s_2^2 (y^2 - A^2) / ((q~+c) Delta) < 1.
纯代数: 由 M_f 的显式式交叉相乘后消去公因子 c(1-q~^2) s_1^2 s_2^2 (y^2-A^2)
(其中 M_f(x;c) = x^2 sin^2 x/(q~ + c Phi(x)), Phi = cos^2 + q~^2 sin^2).

**张力比链 (定理 3.4, STRICT)**: 对一切 q~ in (0,1), gamma in
[gamma_0^*, pi/2):
rho(q~,gamma) <= rho_0(gamma) := (t/(y+t)) * (s_2^2 (y^2-p) / (y^2 s_2^2 - p)),
p := pi^2/4, t := tan gamma.
- **P1 (引理 3.1)**: c/(q~+c) <= t/(y+t). 证明: u := cy = arctan(q~ t),
  则 c/(q~+c) <= t/(y+t) 等价于 u <= tan u (u < pi/2), 恒真.
- **P2 (引理 3.2)**: s_1^2 (1-q~^2) T/Delta <= s_2^2 (y^2-p)/(y^2 s_2^2 - p),
  T := y^2 - A^2. 交叉相乘后差 E = (y^2-p)Delta - s_1^2(1-q~^2)T(y^2 s_2^2-p),
  用 0 < 1-q~^2 <= 1 放大 W <= W_0, 再展开得到三项非负分解
  E_0/y^2 = cos^2 gamma (p-A^2) + cos^2 A (y^2 s_2^2 - p) + cos^2 A * A^2 * cos^2 gamma >= 0,
  只用 A < pi/2 与 (y sin gamma)^2 >= pi^2/4 (引理 2.2, 端点 gamma_0^* 证书).
- **一维不等式 (定理 4.1, STRICT)**: 对 gamma in [gamma_0^*, pi/2), rho_0 < 1,
  等价于 F(gamma) := y^3 sin^2 gamma - p (y + sin gamma cos gamma) > 0.
  G-论证: w = pi/2 - gamma in [0, w_0], w_0 = y_0 - pi/2,
  G(w) = (pi/2+w)^3 cos^2 w - p(pi/2+w) - (p/2) sin 2w:
  (a) G'(0) = pi^2/4 > 0; (b) G'(w_0) = -sin^2(gamma_0^*) * pi^2/2 < 0 (用
  cot(gamma_0^*) = 3/(2 y_0), 来自 tan(gamma_0^*) = 2 y_0/3);
  (c) G''(0) = pi(3 - pi^2/4) > 0 (pi^2 < 12), G''(w_0) < -13 (证书 C4);
  (d) G''' < 0 于 [0, w_0] (证书 C3: 用精化有理界 y_0max = 15273/7000,
  w_0max = y_0max - 223/142; 粗略界 w_0 < 0.6115 只压到 -0.4303, 不够).
  故 G'' 恰有一个零点, G' 单峰, G' 恰有一个零点 w*, G 先增后减,
  min G = min{G(0), G(w_0)} = 0 (G(w_0) = F(gamma_0^*) > 0 由证书 C5:
  16 y_0^4 - 4 pi^2 y_0^2 - 15 pi^2 > 19).

**Claim A (定理 5.1, STRICT)**: 对 q~ in (0,1), gamma in
[gamma_0^*, gamma_0(q~)] 有 rho(q~,gamma) < 1. 证明: 定理 3.4 (链,
需 gamma in [gamma_0^*, pi/2), 而 gamma_0(q~) <= pi/2 且对 q~ > 0 严格小于
pi/2) + 定理 4.1 (rho_0 < 1).

**KEY LEMMA 全 R (定理 1.2, STRICT)**: F~_e 在 (0,1/2) 恰有一个零点
c*(q~), F~_e > 0 于 (0,c*), < 0 于 (c*,1/2), 且 c* in (0, c_0(q~)),
c_0(q~) = arctan(q~ tan gamma_0^*) / (pi - gamma_0^*) in (0,1/2).
归约引理 (引理 1.4): 假设 Claim A 即得 KEY LEMMA, 需要 (i) 端点
F~_e(0+) = pi^2/(4q~) > 0 与 F~_e(1/2) < 0 (易区 c >= 1/2, 与 q~ 无关),
(ii) P1 全 R 版 G_1 <= -6 q~/(2+q~) < 0, (iii) W_0 引理全 R 版
(W_0(gamma) = 3 - 2 y cot gamma 严格递增, 唯一零点 gamma_0*);
再在 Z = {F~_e >= 0} 上用分解 F~_e' = (M_1-M_2)G_1 + M_2(G_1-G_2),
G_1 < 0 且 G_1 < G_2 (后者来自 [S,(4.13)] G_2 = -Phi W_0/(q~+c Phi) + P,
P >= 0, 于 (0,c_0) 上 W_0 < 0), 得横截唯一零点.

**推论 (INF 闭合, 全部 R>1, STRICT)**: 结合 O1-INF 归约 (独立审计),
阱族刚性全 R ([[well-family-rigidity]], 2026-08-10 会话 56) 与 O3b 两块
边界排除: INF 下确界 I(R) 在对称阱 [R,1,R] 达到,
I(R) = D(rho_{v*(R)}) < 3 pi^2/R, v* = v(c*(q~)). 模缺口 (c) Theorem A
独立复核与 (d) good-root 全局论证残差 (均与本文正交).

## 适用范围
- **适用**: 阱族对称线 1D 分析 (全部 R>1, q~ in (0,1)); 闭合缺口 (a'),
  把 [[symline-n1-monotonicity]] 的 1 < R <= 3/2 限制完全去掉. 与
  [[well-family-rigidity]] (全 R 刚性) + [[gap-n1-reduction]] (O1-INF 归约)
  配合给出 INF 侧全 R 闭合 (模 (c)/(d)).
- **边界情形**: R -> 1+ (q~ -> 1-, 链退化为平凡); R -> inf (q~ -> 0+,
  角点 gamma -> pi/2, rho_0 -> 1 且 1 - rho ~ K(t) q~, K(t) >= 1.97,
  K(1) = 2; 对应中心质量钉扎极限); gamma = gamma_0* 端点 (证书 C1 定位
  gamma_0* in (0.961, 0.97)); gamma -> pi/2 处 F(pi/2) = 0, F' < 0,
  线性速率趋于 0.
- **不适用**: 垒族 (q > 1) 由 [[phase-ratio-rigidity]] 处理 (符号结构不同);
  非对称阱族 (a+b != 1) 已被刚性定理排除; c >= 1/2 易区由 [S, 引理 2.1]
  直接处理, 不经过张力比.
- **关键技巧**: (i) 把二维 (q~, gamma) 不等式链式放大到 q~ = 0 的退化
  极限 rho_0, 一维化; (ii) P2 的三项非负分解 (平方型判别式) 代替精细盒式
  证书; (iii) 单峰 G-论证 + 端点有理证书 (交错级数 + pi 界
  223/71 < pi < 22/7); (iv) 证书要用精化有理界 (粗略界 w_0 < 0.6115 不够).

## 验证与备注
- 严格证明文档: `docs/SL_gap_n1_symline_allR_proof.pdf` (9 页, 零警告
  (除 SimSun 字体字形替换), 2026-08-12), 含 Claim A 定理 5.1, 附录 A
  精确有理证书 C1-C5, 附录 B 数值交叉检验 (EVIDENCE).
- 精确有理证书脚本: `scripts/_symline_allR_certificates.py`
  (fractions.Fraction 精确算术, 全部断言 PASS, 2026-08-12):
  C1 (gamma_0* 定位, 交错级数精确比值链), C2 (f(gamma_0*) > pi/2 经
  1623/912 链), C3 (G''' < -56/129, 精化界), C4 (G''(w_0) < -13,
  93/200 与 63/250 链), C5 (16 y_0^4 - 4 pi^2 y_0^2 - 15 pi^2 > 19).
- EVIDENCE 脚本 (不构成证明): `scripts/_symline_allR_check.py`
  (scipy 双精度 + mpmath 50 位): 张力比链 37500 点零违例 (角点最小余量
  mpmath 复核 +2.9e-18), rho_0 < 1 二十万点 (min 1-rho_0 = 7.9e-13 仅当
  gamma -> pi/2), 等价性 19901 点零违例, 端点 7 个 q~ 值 mpmath 复核,
  角点渐近 K(t) 与引理 2.2 扫描. 全部数值仅为交叉检验.
- 探索脚本: `scripts/_explore_a1_allR*.py` (8 个, 探索过程, EVIDENCE).
- 文档修复记录 (本会话): G''(0) = 3pi - pi^3/4 (原 3pi 错, 附 pi^2 < 12
  证明); C1 证书链重写 (原分数不可复现, 十进制界方向/数值错); C3 精化
  有理界; C5 常数 3817/200 -> 19 (精确值 19.081); Claim A 引理补入并编号
  5.1; 摘要/章节标题 texorpdfstring (PDF 字符串警告); 巨分数拆行与长
  ASCII 词断点 (overfull 清零).
- 相关工具: [[symline-n1-monotonicity]], [[well-family-rigidity]],
  [[gap-n1-reduction]], [[feynman-hellmann]], [[rational-envelope-certificates]],
  [[key-lemma-decomposition]].
