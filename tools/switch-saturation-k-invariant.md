---
title: 开关饱和与块能量不变量
tags: [mathtool, extremal, sl-spectral]
created: 2026-08-10
status: 定理已证 (独立审计 PASS)
---

# 开关饱和与块能量不变量 (switch-saturation-k-invariant)

## 解析
一维加权 Dirichlet 问题 $-u''=\lambda\rho u$, $u(0)=u(1)=0$, 完整可测盒
$1\le\rho\le R$ a.e. 中, 相邻谱隙 $D_n=\lambda_{n+1}-\lambda_n$ ($n\ge2$) 的
极值子结构由三个互锁机制决定:

1. **完全盒饱和 (FH 一侧变分)**: 以归一化特征函数定义切换函数
   $F=\lambda_n u_n^2-\lambda_{n+1}u_{n+1}^2$. 全局最大化子在 $\{F>0\}$ 上
   $\rho=R$、在 $\{F<0\}$ 上 $\rho=1$; 全局最小化子指派相反. 推导只用
   任意有界方向的一阶公式 $D_n'[h]=\int hF\,dx$ (紧自伴算子扰动, 不需特征
   向量预可微) 与盒约束一侧可行方向.
2. **零点-开关双向相等**: Wronskian $W=u'_{n+1}u_n-u_{n+1}u'_n$ 在 $(0,1)$
   严格为负 (由振荡与严格交错推出, 不用极值性), 故商 $Q=u_{n+1}/u_n$ 在每个
   结点区间严格递减; 精确零点公式
   $\#Z(F;(0,1))=2n-2+\mathbf 1_{\{q_0>c\}}+\mathbf 1_{\{q_1<-c\}}$,
   $c=\sqrt{\lambda_n/\lambda_{n+1}}$, 且全部零点简单. 饱和律把每个定号分支
   固定为盒端点, 故 $\{$有效开关$\}=Z(F;(0,1))$.
3. **块能量不变量**: 常密度块上的两模态能量差
   $K=(u_n'^2+\lambda_n r u_n^2)-(u_{n+1}'^2+\lambda_{n+1} r u_{n+1}^2)$ 在
   块内为常数; 接口跳量 $K(s_+)-K(s_-)=(r_+-r_-)F(s)$, 极值子饱和使所有接口
   落在 $F=0$, 故全局拼接为常数. 两次归一化贡献给出严格恒等式 $K=-2D<0$,
   从而端点斜率比 $q_0>1>c$、$q_1<-1<-c$, 两个端点指标都为 $1$, 精确零点数
   收紧为 $2n$. 最大化子首尾块取 $1$, 最小化子首尾块取 $R$.

## 适用范围
- 适用: Dirichlet 边界, 正可测权 $L^\infty$ 盒 (不要求连续/分段/对称/单调),
  有限 $R>1$, 任意整数 $n\ge2$ (n=1 亦成立但非冻结目标).
- 边界情形: $R=1$ 退化单点被排除; $R=\infty$ 不在允许集; $q_0=c$ 或
  $q_1=-c$ 的等号只发生在端点, 不计入零点; 有限个接口点赋值不影响结论.
- 不适用: 非盒类约束 (L^p 球/MDE 测度类由 [[mde-extremal]] 处理); 无饱和的
  任意 bang-bang 权重 (接口可有非零能量跳量, 端点刚性不成立); Robin/混合
  边界与非相邻谱隙未在本工具范围内.

## 验证与备注
- 来源: 用户提供 SL_gap_nge2_finite_reduction_proof_zh.pdf 与
  SL_gap_nge2_exact_2n_switches_proof_zh.pdf (Blueprint v2.2 证明包), 项目
  忠实转录为 docs/SL_gap_nge2_finite_reduction_proof.tex/.pdf (15 页) 与
  docs/SL_gap_nge2_exact_2n_switches_proof.tex/.pdf (16 页), 均零警告.
- 审计 (2026-08-10): 解析逐条复核 PASS (谱事实/交错/Wronskian/精确零点/FH/
  一侧变分/饱和/接口跳量/因子 2/端点奇偶, 均与原文一致, 未发现缺陷).
- 数值: scripts/audit_nge2_pdfs.py Part A 40/40 (随机 bang-bang, R in
  {1.1..100}, n=2..5) + Part B 16/16 (R=4, n=1..8 SUP/INF: 恰 2n 零点,
  q0>1, q1<-1, K+2D~1e-4..1e-8, 接口跳量~1e-6); scripts/_hp_nge2.py
  (mpmath 50 位: n1_SUP/n4_INF/n8_INF 零点计数精确匹配, K=-2D 残差
  8.3e-12..2.5e-7, 后者受近简并对精度限制); scripts/_smooth_nge2.py
  (光滑振荡权 R=1.5/4/10/100, n=2/3/5/4, 4/4: 零点公式与 W<0 成立).
- 文献: 未检索到"所有 n>=2 + 完整可测盒 + 最大与最小两端 + 每个极值子 +
  精确 2n 开关"同时出现的直接等价已发表定理; Willner-Mahar 1979
  (JMAA 72(2):730-739) 为明确既有工作风险, Sun 2022 仅覆盖第一谱隙最小化
  (INF 侧 n=1, 分段连续有界跳). 本工具不声称首创.
- 未解决 (见 docs/SL_spectral_topics_summary.tex 开放问题 1): 开关位置/块长,
  反射对称性, 唯一性与完整分类, 最优值闭式, 渐近, 稳定性, 模型推广.

## 更新 2026-08-13 (会话 58 续作 8): (G2) 闭合应用
块能量不变量与精确零点公式联手闭合全局分类框架 (docs/SL_gap_nge2_
symmetry_local_proof.tex) 的边界排除条件 (G2):
- 新引理 (STRICT, 本会话): 对任意正权与相邻特征对, f 在 (0,1) 内无 f=f'=0
  点 (Cauchy 数据唯一性 + Sturm 交错); 故带自洽解列不能发生内部开关并合
  (Rolle).
- 新定理 (STRICT, 本会话): 若带自洽解列某块宽 -> 0 (紧 R 区间), 子列极限
  字符串上 K==-2D 给出 q0*>1, q1*<-1, 精确零点公式给出 #Z(f*)=2n, 而
  存活开关零点数 <= 2n-1, 与带匹配保持 (f* 在块内定号, 内部零点简单) 矛盾.
  塌缩奇偶性无关, 两端同时塌缩同理. 故 (G2) 成立 STRICT: 紧 R 区间上块宽
  一致有正下界, Sigma 无边界聚点.
- 端点斜率约定修正: 本工具 q0 := u'_{n+1}(0)/u'_n(0) (框架约定); 端点
  塌缩强制 q0 = c (a = lambda_n u_n'(0)^2 (1-q0^2/c^2) 的零), 与 K 恒等式
  q0 > 1 > c 直接矛盾. 早期 sqrt(lambda) 加权比率的证据行已撤回.
- 完整论证: runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13.md (定理 B/C/E). 数值交叉 (EVIDENCE):
  K(0)+2D ~ 1e-11, 完整分支 q0 > 1 (n=2 R=4: SUP 2.376980, INF 1.142677),
  所有发现的约化根 q0 > 1 且 q1 < -1 (band=False).
- 相关: [[endpoint-collapse-reduction]] (归约, 现已被直接闭合超越),
  [[band-selfconsistency-equivariance]] ((G1')/(G2) 框架).

## 更新 2026-08-13 (R-205): 全局 ε 交错推论 (STRICT, 不依赖对称性)
精确零点公式的胞腔分析直接给出一个**全局**推论: 设 $x_1<\cdots<x_{2n}$ 为
$f$ 的 $2n$ 个简单零点 (带自洽点), $\varepsilon_j:=\operatorname{sign}
(u_{n+1}(x_j)/u_n(x_j))\in\{\pm1\}$ (在零点处 $u_{n+1}=\varepsilon_j c u_n$),
则
\begin{equation*}
  \varepsilon_j=(-1)^{j+1}\quad(j=1,\dots,2n).
\end{equation*}
证明: $W<0\Rightarrow Q=u_{n+1}/u_n$ 在每个胞腔严格递减, 且 $Q$ 从
$+\infty$ 经 $0$ 到 $-\infty$; 故每胞腔左零点 $Q=+c$ ($\varepsilon=+1$),
右零点 $Q=-c$ ($\varepsilon=-1$), 逐胞腔从左到右排列即得交错. 该推论
**不需要宽度对称** (回文高度不足以给出特征函数奇偶性; 奇偶性需要
$\rho(1-x)=\rho(x)$, 见 [[green-half-inertia]] 的更正), 是 $K$ 的非对角
闭式 (C1)/(C2) 在**一切**带自洽点成立的正确全局输入. 数值 (随机非对称
宽度, n=2,3, R in {2,4}, 两模式): 全部抽样 $f$ 恰 $2n$ 个零点且
$\varepsilon$ 图案为 $[1,-1,1,-1,\dots]$. 来源:
run_notes_addendum_2026-08-13b.md (R-205).
