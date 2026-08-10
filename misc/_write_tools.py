import os
base = r"F:\LaTeX\BVE research\tools"
os.makedirs(base, exist_ok=True)

t1 = """---
title: 两块族归约定理 (gap-n1 reduction)
tags: [mathtool, self-developed, reduction]
source: 自研 (O1, run R-20260805T000000Z-gapn1-a1b2c3)
status: 定理证明草稿 PROVED (独立审计待补) + 数值佐证
created: 2026-08-05
---

# 两块族归约定理 (gap-n1-reduction)

## 解析
对 Dirichlet 弦 $-y''=\\lambda\\rho y$ ($y(0)=y(1)=0$, $1\\le\\rho\\le R$ a.e.),
相邻间距 $D(\\rho)=\\lambda_2-\\lambda_1$ 的上下确界可归约到两块密度族:

$$S(R)=\\sup_{\\rho}D(\\rho)=\\max_{0\\le a\\le b\\le 1}D(\\rho=R\\text{ on }(a,b),\\ 1\\text{ 其余}),$$
$$I(R)=\\inf_{\\rho}D(\\rho)=\\min_{0\\le a\\le b\\le 1}D(\\rho=1\\text{ on }(a,b),\\ R\\text{ 其余}).$$

## 证明机制 (七步)
1. **L1 连续性**: 对 Green 算子 $T_\\rho f=\\int_0^1 G(x,t)\\rho(t)f(t)\\,dt$ ($G=\\min(x,t)(1-\\max(x,t))$),
   $\\lambda_k(\\rho)^{-1}=\\mu_k(T_\\rho)$ 为紧自伴算子特征值; 由 $\\|T_\\rho-T_\\sigma\\|\\le\\|G\\|_\\infty\\|\\rho-\\sigma\\|_2$
   与 $\\|\\rho-\\sigma\\|_2^2\\le 2R\\|\\rho-\\sigma\\|_1$, 及 min-max 原理, $\\lambda_k$ 在 $L^1$ 拓扑连续.
2. **N 跳紧性**: $\\mathcal{K}_N$ 为闭单纯形与 $[1,R]^{N+1}$ 的连续像, 极值存在.
3. **FH 移动跳点**: 把 $x_j$ 处由 $c_-$ 到 $c_+$ 的跳点移动 $\\varepsilon$,
   $dD/d\\varepsilon|_0=(c_+-c_-)f(x_j)$, $f=\\lambda_1u_1^2-\\lambda_2u_2^2$.
4. **f 的结构** (Wronskian): $v=u_2/u_1$ 严格递减 (与 $\\rho$ 无关), 故 $f$ 至多两零点,
   $\\{f>0\\}$ 为单区间.
5. **极值点至多两跳**: 每个有效跳点是 $f$ 的零点, 至多两个.
6. **阶梯稠密**: $M_N\\to\\sup_{\\mathcal{K}}D$.
7. **bang-bang**: 全局极值点在 $\\{f>0\\}$ 取 $\\rho=R$, $\\{f<0\\}$ 取 $\\rho=1$
   (INF 相反), 由单区间性得单垒/单阱两块配置.

## 适用范围
- 适用: 逐点界类 $1\\le\\rho\\le R$ 的 Dirichlet 弦, 前两个特征值间距 (及推广到
  $\\lambda_{k+1}-\\lambda_k$ 时需重证 f 的单区间结构); 与 [[keller-variational]],
  [[bang-bang]], [[single-well-intersection]] 配合.
- 边界情形: 两块族退化成员 ($a=0$, $b=1$, $a=b$) 在闭族内被自动覆盖.
- 不适用: 有质量/范数约束的类 ($L^p$ 球, MDE), 极值可含原子测度; 见 [[mde-extremal]].
- 注意: 归约只给出族上的极值, 不给出块内极值点的对称性/唯一性 (那是 O2/O3a 的义务).

## 验证与备注
- 来源: run R-20260805T000000Z-gapn1-a1b2c3 的 O1_reduction_draft.md (PROVED 草稿,
  各步均为初等论证; O1c Wronskian 一步与 AEH arXiv:2407.02459 Lemma 2.2 独立重导).
- 数值佐证: 对 $R\\in\\{1.05,\\dots,1000\\}$ 全景观测 SUP/INF 唯一临界点均在对称点, 无反例.
- 上游审计: 尚未安排独立 verifier 对 O1 草稿的逐行审计 (记入义务图 O4).
"""

t2 = """---
title: 两块相位间距界 (two-block gap bounds)
tags: [mathtool, self-developed, estimate]
source: 自研 (Agent C, run R-20260805T000000Z-gapn1-a1b2c3)
status: 定理已证 (UPSTREAM_AUDITED 级: 完整证明 + 4000 点零违例)
created: 2026-08-05
---

# 两块相位间距界 (two-block-gap-bounds)

## 解析
对重右两块密度 $\\rho=1$ on $[0,t]$, $R$ on $(t,1]$ (重左由镜像 $x\\mapsto1-x$ 归入),
Dirichlet 弦前两个特征值间距满足

$$\\frac{3\\pi^2}{R}<D(t)<3\\pi^2\\qquad\\forall\\,t\\in(0,1),\\ R>1,$$

且两端仅作为极限达到: $t\\to1^-$ 时 $D\\to3\\pi^2$, $t\\to0^+$ 时 $D\\to3\\pi^2/R$.

## 证明机制 (相位坐标)
令 $\\mu=\\sqrt R$, $c=\\mu(1-t)/t$, $\\theta(x)=\\arctan(\\mu\\tan x)$ (连续分支,
$\\theta(x+\\pi)=\\theta(x)+\\pi$), $x_1<x_2$ 为 $\\theta(x)+cx=k\\pi$ ($k=1,2$) 的前两根, 则
$$\\lambda_k=\\frac{x_k^2(\\mu+c)^2}{\\mu^2},\\qquad
D=\\frac{(\\mu+c)^2}{\\mu^2}(x_2^2-x_1^2).$$
- **下界**: $\\theta'<\\mu$ 严格 $\\Rightarrow$ $x_1>\\pi/(\\mu+c)$, $x_2-x_1>\\pi/(\\mu+c)$
  $\\Rightarrow$ $D>3\\pi^2/R$.
- **上界**, 三区:
  - $c\\ge1$: $x_1\\le\\pi/(1+c)$; $\\theta'\\ge1/\\mu$ 给出 $x_2-x_1\\le\\pi\\mu/(1+\\mu c)$,
    $x_2\\le2\\pi\\mu/(1+\\mu c)$; 归约为 $D\\le3\\pi^2 G(\\mu,c)$ 且 $dG/d\\mu<0$,
    $G(1,c)=1$ (sympy 精确分解, $P\\ge4>0$).
  - $1/3\\le c\\le1$: 弦/凸性 $\\Rightarrow x_2^2-x_1^2\\le3\\pi^2/(1+c)^2$,
    用 $(\\mu+c)^2<\\mu^2(1+c)^2$.
  - $0<c\\le1/3$: $\\varepsilon_k=k\\pi-x_k$, $s_k=\\tan(cx_k)=\\mu\\tan\\varepsilon_k$,
    证明 $W'(\\mu,c)<0$, 故 $W<W(\\mu,0)=3\\pi^2\\mu^2$.

## 适用范围
- 适用: 两块 (或经过拼接的) Dirichlet 弦, $D=\\lambda_2-\\lambda_1$ 的逐点界;
  相位坐标在极端 $R$ ($10^4$ 以上) 下数值稳定, 优于转移矩阵粗网格.
- 边界情形: $c\\to0$ 与 $c\\to\\infty$ 两端均为极限; $\\mu=1$ 退化 ($W'=0$) 需排除.
- 不适用: 不直接给出多块族的全局界 (仅两块); 需与归约定理配合.
- 注意: 上界证明中的 $dG/d\\mu<0$ 对 $c\\ge1$ 成立; 对 $c<1$ 用另外两区的论证.

## 验证与备注
- 来源: agentC_O3b_boundary.md (完整证明); 相位恒等式精度 1e-13;
  4000 点网格 (R 1.05..1e4 x t) 零违例, 下界余量 +1.25e-8, 上界余量 +1.28e-6;
  $W'<0$ 用 mpmath 60 位确认.
- 独立复核 (coordinator, 2026-08-05): 相位求解器扫描 0 违例, 最小相对余量 1.6e-9.
- 失败经验: 比值路线 ($\\lambda_2/\\lambda_1\\le4$ 反例, 两块族可到 ~9) 失败;
  独立框定 $\\varepsilon_k$ 失败 (端点界过粗); 全 $c$ 上 $W'<0$ 为假 (仅 $c\\le1/3$).
"""

t3 = """---
title: KEY LEMMA 分解与逐项 q-单调性否证 (key-lemma-decomposition)
tags: [mathtool, self-developed, obstruction]
source: 自研 (coordinator, run R-20260805T000000Z-gapn1-a1b2c3)
status: 分解推导 + 精确角点极限 (已证) + B-D q-单调性否证 (反例已复现)
created: 2026-08-05
---

# KEY LEMMA 分解与逐项 q-单调性否证 (key-lemma-decomposition)

## 解析
对对称垒 $[1,R,1]$, 记 $q=\\sqrt R$, $\\alpha_k(c)$ 为半问题 secular 曲线与 $\\beta=c\\alpha$
的交点. O2 的 KEY LEMMA 等价于 $G(\\alpha_2(c);c)>G(\\alpha_1(c);c)$, 其中
$$G(\\alpha;c)=-\\frac{\\Phi(\\alpha)W(\\alpha)}{q+c\\Phi(\\alpha)}
+\\frac{2c\\alpha\\Phi(\\alpha)(q^2-1)\\sin\\alpha\\cos\\alpha}{(q+c\\Phi(\\alpha))^2},
\\qquad W(\\alpha)=3+2\\alpha\\cot\\alpha.$$

**分解**: 令 $\\alpha_2=\\pi-\\gamma$, 则
$$G_2-G_1=(A-C)+(B-D),$$
$$A-C=\\frac{\\Phi_1W_1}{q+c\\Phi_1}-\\frac{2c(q^2-1)\\alpha_1\\Phi_1\\sin\\alpha_1\\cos\\alpha_1}{(q+c\\Phi_1)^2},
\\qquad
B-D=-\\frac{\\Phi_2W_2}{q+c\\Phi_2}
+\\frac{2c(q^2-1)\\alpha_2\\Phi_2|\\sin\\alpha_2\\cos\\alpha_2|}{(q+c\\Phi_2)^2}.$$

**q=1 基值闭式**: $\\alpha_1=\\pi/(2(1+c))$, $\\alpha_2=\\pi/(1+c)$, $\\Phi\\equiv1$,
$(q^2-1)=0$ 时
$$(A-C)|_{q=1}=\\frac{W(\\alpha_1)}{1+c},\\qquad (B-D)|_{q=1}=-\\frac{W(\\alpha_2)}{1+c}.$$
由 $W'=2(\\sin\\alpha\\cos\\alpha-\\alpha)/\\sin^2\\alpha<0$ 得
$$(G_2-G_1)|_{q=1}\\ge\\frac{W(\\pi/3)-W(2\\pi/3)}{3/2}=\\frac{4\\pi}{3\\sqrt3}=2.41840\\ldots>0.$$

**精确角点极限** ($q\\to1^+$, $c\\to1/2^-$): $A-C\\to W(\\pi/3)/(3/2)=2.80613\\ldots$,
$B-D\\to-W(2\\pi/3)/(3/2)=-0.38773\\ldots$, 和 $\\to4\\pi/(3\\sqrt3)$.

## 否证 (逐项 q-单调性, 精确反例)
交接稿曾主张 $d(A-C)/dq\\ge0$ 且 $d(B-D)/dq\\ge0$ 在全网格成立, 据此闭环 KEY LEMMA.
独立复核 (细网格): **$A-C$ 对 $q$ 单调递增 (全采样通过), 但 $B-D$ 不单调**:
反例 $c=0.01$, $q\\colon5000\\to20000$ 时 $B-D\\colon199.79\\to193.99$ (递减);
$c\\le0.1$ 均递减, $c\\ge0.3$ 才递增. 因此``分解 + 逐项 q-单调''闭环作废.

## 适用范围
- 适用: 对称三块族相邻间距的驻点/单次穿零分析; KEY LEMMA 型对数导数不等式
  $d\\log(M_1/M_2)/dc<0$ 的等价变换; 分解+基值+单调性的复合证明模板.
- 边界情形: $q\\to1^+$ 角点需按 $c\\to1/2^-$ 展开; 大 $q$ 小 $c$ 区是单调性最容易
  失效的区域 (B-D 大正但递减, 和仍稳健).
- 不适用: 当需要逐项单调性时, 必须逐项独立验证; 任何``数值全网格通过''的声明
  都要交代网格分辨率与极端区采样 (本工具即以反例说明此陷阱).
- 限制: 分解本身是恒等式, 精确角点极限已证; 但 KEY LEMMA 的整体证明仍开放.

## 验证与备注
- 来源: run R-20260805T000000Z-gapn1-a1b2c3 (Agent A 的 O2 报告 + coordinator 分解);
  独立复核脚本 misc/_verify_decomp.py, misc/_verify_bdmono.py, misc/_verify_acmono.py.
- 数值: 全网格 $q\\in[1.00025,10^6]$, $c\\in(0,1/2)$ 上 $G_2-G_1\\ge2.41840$,
  最小值在角点; KEY LEMMA 余量 (对数导数形式) min 2.4481 (R=1.1) 至 19.45 (R=1e4).
- 经验: 交接数值表 (A-C min 2.8086, B-D min -0.3751, 和 2.4258) 为粗网格值,
  精确角点极限为 2.80613/-0.38773/2.41840, 以本文为准.
"""

for name, content in [("gap-n1-reduction.md", t1), ("two-block-gap-bounds.md", t2), ("key-lemma-decomposition.md", t3)]:
    p = os.path.join(base, name)
    open(p, "w", encoding="utf-8", newline="\n").write(content)
    print("wrote", name)