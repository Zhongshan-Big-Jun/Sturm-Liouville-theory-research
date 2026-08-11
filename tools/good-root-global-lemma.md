---
canonical_key: good-root-global-lemma (INF side, gap (d) closure for all R>1)
title: 内部临界点 => sign-consistent good root: Wronskian 比值单调 + f 零点唯一性 + FH 跳点公式
tags: [mathtool, self-developed, wronskian, gap-extremals, inf-side]
source: 自研 (会话 58 续作 2, 2026-08-12; 承接 [[gap-n1-reduction]] O1 第 5 步与 [[well-family-rigidity]] 第 9 节剩余缺口 (d))
status: 定理已证 (STRICT, docs/SL_gap_n1_global_goodroot_proof.pdf, 6 页零警告; 数值交叉检验为 EVIDENCE, 不构成证明)
created: 2026-08-12
updated: 2026-08-12
---

# 内部临界点 => sign-consistent good root (good-root 全局引理)

## 解析
对 Dirichlet 弦 $-y''=\lambda\rho y$, 阱族 $\rho_{a,b}=R\cdot\mathbf1_{[0,a]\cup(b,1]}+\mathbf1_{(a,b)}$,
参数集 $\Omega=\{(a,b):0\le a\le b\le1\}$, $D(a,b)=\lambda_2-\lambda_1$,
归一化特征函数 $\hat y_k=y_k/\sqrt{\int_0^1\rho\,\hat y_k^2}$, 残差
$R_1(a,b)=f_{a,b}(a)$, $R_2(a,b)=f_{a,b}(b)$,
$f_{a,b}:=\lambda_2\hat y_2^2-\lambda_1\hat y_1^2$, $z_0$ 为 $y_2$ 在 $(0,1)$ 的唯一零点
(Sturm 振荡).

**结构引理 A (比值单调, STRICT)**: 对任意 $0<a<b<1$,
$W:=y_1y_2'-y_1'y_2<0$ 于 $(0,1)$ (于 $(0,z_0)$: $W'=(\lambda_1-\lambda_2)\rho\,y_1y_2<0$,
$W(0)=0$; 于 $(z_0,1)$: $W'>0$, $W(1)=0$), 故 $v:=y_2/y_1$ 严格递减.

**结构引理 B (f 零点结构, STRICT)**: $f/\hat y_1^2=\lambda_1-\lambda_2v^2$ 于
$(0,z_0)$ 严格递增、于 $(z_0,1)$ 严格递减; 故 $f$ 在 $(0,z_0)$ 恰有一个零点
$\alpha$ (端值 $\lambda_1-\lambda_2<0$ 到 $\lambda_1>0$), 在 $(z_0,1)$ 至多一个零点
$\beta$; $\{f>0\}$ 是包含 $z_0$ 的单区间 $(\alpha,\beta)$ (或 $(\alpha,1)$).
若 $0<a<b<1$ 且 $f(a)=f(b)=0$, 则 $a=\alpha$, $b=\beta$, 从而 $a<z_0<b$.

**核心推论 (内部临界点 => good root, STRICT)**: 设 $(a,b)$ 为 $\Omega$ 内点
($0<a<b<1$) 且 $\partial_aD=\partial_bD=0$. 由 Feynman--Hellmann 移动跳点公式
$\partial_aD=-(R-1)R_1$, $\partial_bD=+(R-1)R_2$ 得 $f(a)=f(b)=0$; 由结构引理 B
得 $a<z_0<b$, 于是 $y_2(a)/y_1(a)>0$, $y_2(b)/y_1(b)<0$ (符号一致性自动成立).
即内点临界点必为 sign-consistent good root.

**主定理 (缺口 (d) 闭环, STRICT, 一切 $R>1$)**:
$I(R)=\min_\Omega D=D(v^*(R),1-v^*(R))<3\pi^2/R$, 极小元唯一. 六步证明:
① O1-INF 达到性; ② 边界排除 $\partial\Omega$ 上 $D\ge3\pi^2/R$ (O3b 两块严格界
$+$ $\rho\equiv R$ 精确值), 而 $D(v^*)<3\pi^2/R$ ([[symline-n1-monotonicity]] KEY
LEMMA 全 $R$), 故极小元在内部; ③ 核心推论给出 sign-consistent good root;
④ [[well-family-rigidity]] 全 $R$ 刚性给出 $a+b=1$; ⑤ 对称线唯一临界点 $v^*$;
⑥ 结论与唯一性.

## 适用范围
- **适用**: 任意两参数密度族极值问题的内部临界点与 good root 的衔接; 把
  "极值元落在刚性定理适用的 good-root 集合内" 从条件式推论升级为无条件定理.
  本项目中闭合了 INF 侧 $n=1$ 相邻间距问题的全局极值论证 (缺口 (d)), 与
  (O1-INF 归约) + (阱族刚性) + (对称线 KEY LEMMA) 拼成 INF 侧对一切 $R>1$ 的完全闭合.
- **边界情形**: $a=0$, $b=1$, $a=b$ 上的极值由边界排除单独处理 (两块族 O3b /
  常数密度精确解); $R\to1^+$ 与 $R\to\infty$ 退化极限不破坏本引理 (引理对固定
  $R>1$ 成立, 极限过程由定理 A 等单独处理).
- **不适用 / 注意**: 引理要求临界点在 $\Omega$ 内部 (严格 $0<a<b<1$);
  符号一致性结论依赖 $y_2$ 唯一零点与 $y_1>0$ (第一特征函数无内部零点, 第二
  特征函数恰一个零点), 对 $\lambda_3,\lambda_4$ 等更高指标需重新计数; 参数
  光滑性 (简单特征值解析摄动) 是 FH 公式的前提. 本引理是 $n=1$ (两跳) 专用,
  不直接推广到 $n\ge2$ 多跳配置.

## 验证与备注
- 来源: 自研 (会话 58 续作 2, 2026-08-12); 文档 docs/SL_gap_n1_global_goodroot_proof.pdf
  (6 页, 零警告, 仅 SimSun 字体字形替换; xelatex 两遍). 结构引理与 O1 第 5 步
  双保险 (本文完全自足重述).
- 数值交叉检验 (EVIDENCE, 不构成证明): scripts/_gapd_global_check.py 复跑
  ALL OK, $R\in\{1.2,2,4,10,100\}$: 每 $R$ 恰一个内部临界点且对称 ($a+b=1$
  至 6 位; $R=4$: $(0.382598,0.617402)$, $D=6.78448234$, $3\pi^2/R=7.402203$),
  $z_0=1/2\in(a,b)$, $D$ 与对称线最小值一致 (1e-9); 边界 $D(0,t),D(t,1)>3\pi^2/R$,
  $D(t,t)=3\pi^2/R$ 精确; 31x31 粗网格最小值 $\ge$ 对称线最小值 (1e-6);
  $f_{a,b}<0$ 于 $(a,b)$ 内部 (25 采样点); $R=100$ 退化对角线点
  $t=\arccos(\pm1/4)/\pi$ 在 $\partial\Omega$ 上, 被边界引理覆盖.
- 调试经验: 梯形积分对不连续 $\rho$ 仅 $O(1/n)$ 精度, 用逐块解析范数
  (gap_lib.norm2); least_squares 阈值 1e-18; 内部点判据 $b-a>1e-4$; 对称线
  $v^*$ 用 brentq 求 $f(v,1-v;v)=0$ (勿用 minimize_scalar, 平坦底部不精确).
- 相关工具: [[gap-n1-reduction]] (O1-INF 归约), [[well-family-rigidity]] (全 $R$
  刚性), [[symline-n1-monotonicity]] (对称线 KEY LEMMA), [[two-block-gap-bounds]]
  (O3b 两块界), [[feynman-hellmann]] (跳点公式来源).
- 诚实备注: 与缺口 (c) (定理 A: $R\to\infty$ 极限) 正交, 闭合不依赖 (c);
  上一模型 8 小时墙钟思考无法独立核验, 本会话逐条复核文档、编译日志与脚本.
