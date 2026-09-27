---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837"], "created": "2026-08-05", "dependencies": [{"location": "tools/moment-jump-completeness.md", "sha256": "5b1b3639ad05e608faf86866919e49f04065e32cb5a459d53981b60f289e6261"}, {"location": "tools/spectral-domain-checks.md", "sha256": "eb65a8a7e076bd2299695b3e1d3dbaf012d822a311bfd5b890c480c68a50e9c7"}], "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "source": "自研 (会话 11), 方向 2: 边界约束 Hilbert 空间多项式稠密的一般准则", "sources": [{"locator": "Sixth-round range/dependency update only; unchanged earlier branches keep their own scope", "path": "docs/SL_fractional_left_definite.tex", "sha256": "30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186"}], "status": "定理已证 + 精确有理数验证", "tags": ["mathtool", "self-developed", "completeness", "moments", "hilbert-spaces"], "title": "稠密性准则 (denseness criteria)", "tool_id": "denseness-criteria"}
---

# 稠密性准则 (Denseness Criteria)

## 解析

设 $H$ 为 $[-1,1]$ 上函数的 Hilbert 空间, 满足 (H1) 所有多项式 $\Pi \subset H$
且 $\Pi$ 在 $H$ 中稠密; (H2) 矩泛函良定 ($M_k = (w, x^k)_H$ 由 Cauchy-Schwarz
自动成立). 研究对象是稀疏基 $p_0 = 1$, $p_1 = x$,
$p_{2m} = x^{2m} - \frac{m}{m-1}x^{2m-2}$, $p_{2m+1} = x^{2m+1}$
- $\frac{m}{m-1}x^{2m-1}$ ($m \geq 2$, 缺 2, 3 次). 三个通用判据:

1. **矩刻画 (充要, 定理 2)**: $\{p_n\}$ 在 $H$ 中完备 $\iff$ 不存在非零
   $w \in H$ 使矩满足 $M_0 = M_1 = 0$, $M_{2m} = mM_2$,
   $M_{2m+1} = mM_3$. 完备性被归结为矩量问题的可表示性.
2. **一阶矩准则 (定理 3)**: 若 $\|x^k\|_H \leq C k^\beta$ 且 $\beta < 1$,
   则 $\{p_n\}$ 完备. 证明: 正交条件化为一阶递推 $M_{2m} = mM_2$,
   与 $|M_{2m}| \leq \|w\|_H \|x^{2m}\|_H = O(m^\beta)$ 矛盾.
3. **跳变矩准则 (定理 5)**: 若 $\{q_n\} \subset \Pi$ 满足三系数跳变
   $q_{2m} = c_0 x^{2m} - A_m x^{2m-2} + B_m x^{2m-4}$ ($c_0 > 0$,
   $B_m \geq 0$, 且 $A_m - B_m$ 的下界给出超阶乘增长引理, 见
   [[moment-jump-completeness]]), $\|x^k\|_H \leq Ck^\beta$ 为任意多项式阶,
   并且低阶项与奇数支具有相应结构, 钉住 $M_0=M_1=0$, 每支只余一个
   自由初始矩, 则 $\{q_n\}$ 完备. 不能只给偶数支而据此断言整个 H 稠密.

**对角临界指数**: 对角空间 $H_\beta$ (内积 $(x^j, x^k) = \delta_{jk}(k+1)^{2\beta}$)
中 $\{p_n\}$ 完备 $\iff \beta \leq 3/2$. $\beta > 3/2$ 时显式反例
$w = \sum_{m \geq 1} m(2m+1)^{-2\beta} x^{2m}$ 满足矩条件
($M_{2m} = mM_2$, $M_2 = 1$; $\|w\|^2 = \sum m^2/(2m+1)^{2\beta} < \infty$
当且仅当 $\beta > 3/2$). 范数多项式增长本身不充分; 一阶准则的 $\beta<1$ 是充分非必要条件.

**左定应用 (2026-09-20 修订)**: 对真正幂域 $H^s=D(K_c^{s/2})$,
H2/H3 的矩跳跃分别在 $L^2,H^1$ 内使用, 这些空间包含取矩单项式.
由 H3 稠密性, 谱截断及 $\|g\|_{H^s}\le c^{(s-3)/2}\|g\|_{H^3}$,
同一稀疏族在 $0\le s\le3$ 中稠密. 原任意整数阶推广已撤回:
$p_4=x^4-2x^2\notin H^4$, 因 $(K_cp_4)'(\pm1)=\mp24$ 不满足边界条件.
第二轮谱系数进一步给出 $p_4\in H^s$ 当且仅当 $s<7/2$ (非负阶), 故 $s\ge7/2$ 的原陈述为假, 第六轮另由四迹图核和谱截断补齐 $3<s<7/2$, 得到完整非负范围 $0\le s<7/2$. 该补证不假设幂域含全部单项式. 见 [[spectral-domain-checks]].
代数线性包为 $\operatorname{span}\{p_n\}=\Pi\cap D(K_c)$, 在 $\Pi$ 中余维 2.

## 适用范围

- 适用: (H1)(H2) 成立的任意 Hilbert 空间; 缺次数 2, 3 的稀疏三角基;
  判据只依赖矩的增长界与跳变结构, 不依赖具体边界条件.
- 边界情形: $\beta < 1$ (一阶); 任意多项式 $\beta$ (跳变 + 超阶乘);
  对角族临界 $\beta = 3/2$ 精确且可达; $s = 0, 1$ (L^2, H^1) 由一阶准则,
  $s=2,3$ 用跳变矩; $0\le s\le3$ 用谱截断传输.
- 不适用: 需要 Schauder/Riesz 基等强于稠密性的结论; 无跳变结构且
  $\beta \geq 1$ 的范数增长 (一般 $H$ 由定理 2 的矩量问题刻画, 无闭式判据);
  未验证幂域成员关系的高阶取矩. 旧分数窗口 $3/2\le s<2$ 已由低阶推论覆盖.

## 验证与备注

2026-09-20: 下列历史计算中的高阶单项式范数与投影, 只作形式微分数据; 不能证明真正幂域的成员关系或稠密性. 本轮未重跑这些旧脚本.


- 精确有理数: `scripts/d2_criterion_verify.py` - 跳变恒等式对 $s = 0..5$,
  $w \in \{x^2, x^3, 1+x+x^5, x^2+x^4\}$ 逐项精确 (240 项);
  对角临界部分和: $\beta = 1.0, 1.4, 1.5$ 发散, $\beta = 1.51, 1.6, 2.0$ 收敛;
  $\beta = 2$ 截断 $w$ 与 $p_{2m}$ 内积 $\leq 8.9\times10^{-16}$.
- 浮点: `scripts/d2_v4_float.py` - $\|x^k\|_s$ 数值指数 $s = 0..5$:
  $-0.50, 0.49, 1.51, 2.53, 3.58, 4.65$ ($\cong s - 1/2$);
  $\{K_c p_n\}$ 在 $H^s$ ($s = 0..4$) 投影残差 $N \geq 10$ 达机器精度;
  $K_c^{s/2}p_{2m}$ 非零项数 $3, 4, 5$ ($s = 2, 4, 6$), 证实更正.
- 文档: `docs/SL_denseness_criteria.pdf` (7 页, 零警告). 相关工具:
  [[left-definite-moment-recurrence]], [[moment-jump-completeness]],
  [[left-definite-theory]], [[left-definite-orthogonal-systems]].
- 诚实边界: 对角族给出精确临界指数, 但仅对对角 (正交单幂) 空间;
  一般 $H$ 的充要判据即定理 2 的矩量问题, 可表示性无一般闭式.


第六轮投影与有限矩修订见 [[constrained-denseness-runs]]. 本卡假设Pi稠密不意味着span{p_n}=Pi; 稀疏族投影须另检验全族稠密性或补入x²,x³方向. 尾部保留时的有限矩单射检验应作用在有限维尾部障碍, 不能作用在含无限尾部的整个V.
