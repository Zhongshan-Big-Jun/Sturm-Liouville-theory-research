---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0d97a-d4b5-7e43-8feb-feb059b8d636"], "conditions": ["For every fixed real c>0, use complex L2(-1,1), with inner product linear in its first argument.", "Kc f=-f_second+c f, D(Kc)={f in ordinary H2: f_prime(1)=f_prime(-1)=(f(1)-f(-1))/2}.", "Hc^s=D(Kc^(s/2)), with norm ||Kc^(s/2)f||_2; every real 0<=s<7/2 is included.", "D={0,1} union {4,5,...}; p0=1, p1=x, p_(2m)=x^(2m)-m/(m-1)x^(2m-2), p_(2m+1)=x^(2m+1)-m/(m-1)x^(2m-1), every integer m>=2.", "For every N subset D with D\\N finite. Spans consist of finite complex linear combinations."], "created": "2026-09-26", "dependencies": [], "evidence_status": "ANALYTIC_PROOF; EXACT_INDEPENDENT_REVIEW_RECORDED_SEPARATELY", "scope": "All and only cofinite retained subsets of the specified original family in the stated fixed-c complex power spaces.", "sources": [{"locator": "Theorem1; sections2-9; non-basis Corollary3, with full quantifiers and critical equality cases", "path": "research/artifacts/proof-audit-round11-20260926/cofinite-author/cofinite-all-orders.md", "sha256": "276720b6a28bbdbd06719d88aa003e8e1602b338bfaf75d2f03ce1f8b5312c9a"}], "status": "解析推导; 精确版本独立验收见第十一轮报告; 非完整Lean形式化/非canonical接收", "structured_content": {"corollary": "Deleting only p6 leaves a dense family at every requested order. Hence the original family, under any nonzero termwise complex scaling and any bijective enumeration, is neither a Schauder basis nor a Riesz basis in that window.", "critical_cases": [{"essential_indices": [], "forbidden_extra_condition": "f(0)=0", "s": "1/2"}, {"essential_indices": [0], "forbidden_extra_condition": "f_prime(0)=0", "s": "3/2"}, {"essential_indices": [0, 1], "forbidden_extra_condition": "f_second(0)=0", "s": "5/2"}], "essential_indices": [{"essential_indices": [], "s_condition": "0 <= s <= 1/2", "trace_derivative_orders": []}, {"essential_indices": [0], "s_condition": "1/2 < s <= 3/2", "trace_derivative_orders": [0]}, {"essential_indices": [0, 1], "s_condition": "3/2 < s <= 5/2", "trace_derivative_orders": [0, 1]}, {"essential_indices": [0, 1, 4], "s_condition": "5/2 < s < 7/2", "trace_derivative_orders": [0, 1, 2]}], "exclusions": ["c=0", "uniform constants as c tends to zero", "s>=7/2 original nonaffine members", "arbitrary infinite deletions", "arbitrary constraint-generated or projected families", "approximation rates", "frame bounds", "orthogonalized or otherwise reconstructed replacement systems"]}, "summary": "固定 c>0 的复 Krein 幂域中, 每个余有限保留集的闭包恰由遗漏且连续的中心迹刻画. 必须保留的指标依次为 {}, {0}, {0,1}, {0,1,4}; 三个等号点属于较少迹的一侧.", "tags": ["mathtool", "Krein", "cofinite", "critical-traces", "closure", "original-family"], "title": "原稀疏多项式族在全部 0<=s<7/2 Krein 幂域中的余有限闭包", "tool_id": "krein-cofinite-closure-all-orders", "updated": "2026-09-26"}
---
# 原稀疏多项式族: 全部成员窗口内的余有限闭包

固定实数 $c>0$, 采用复 $L^2(-1,1)$ 中的实际 Krein 算子
$K_cf=-f''+cf$, $D(K_c)=\{f\in H^2:f'(1)=f'(-1)=(f(1)-f(-1))/2\}$.
令 $\mathcal H_c^s=D(K_c^{s/2})$, 范数为 $\|K_c^{s/2}f\|_2$.
原族指标 $\mathcal D=\{0,1\}\cup\{4,5,\ldots\}$, $p_0=1,p_1=x$,
$p_{2m}=x^{2m}-\frac m{m-1}x^{2m-2}$,
$p_{2m+1}=x^{2m+1}-\frac m{m-1}x^{2m-1}$, $m\ge2$.

对每个 $0\le s<7/2$ 和每个余有限 $N\subset\mathcal D$, 有

$$
\overline{\operatorname{span}_{\mathbb C}\{p_n:n\in N\}}^{\mathcal H_c^s}
=\bigcap_{j\in I(s)\setminus N}\ker\tau_j,
\qquad \operatorname{codim}=|I(s)\setminus N|.
$$

空交集指整个空间. 下标来自原族: $\tau_0 f=f(0)$, $\tau_1 f=f'(0)$,
$\tau_4 f=f''(0)$, 4 不是导数阶数. 全部线性包都是有限复线性包.

| 阶数 | 稠密所必须保留的指标 $I(s)$ |
| --- | --- |
| $0\le s\le1/2$ | 无 |
| $1/2<s\le3/2$ | $0$ |
| $3/2<s\le5/2$ | $0,1$ |
| $5/2<s<7/2$ | $0,1,4$ |

三个等号点属于较少迹的一侧. 例如在 $s=5/2$ 保留 $p_0,p_1$ 即可,
删除 $p_4$ 仍稠密; 在 $5/2<s<7/2$ 删除 $p_4$ 恰留下一个连续二阶中心迹障碍.

证明分成三步. 首先把任意高消失阶的四阶相容多项式闭包识别为四个中心零迹空间,
再以全指标尾部消元把连续零化泛函压缩到这四迹. 最后用内部支撑的对数 Fourier
序列排除全部不连续的最高迹及其复线性组合. 临界范数控制通过双向固定光滑乘子
及显式二次 K-泛函估计证明, 没有交换多项式闭包与插值.

整个窗口内删除 $p_6$ 后仍稠密, 所以原族在任何逐项非零复缩放和双射枚举下
都不是 Schauder 基或 Riesz 基. 这不针对积分 Legendre、正交化或其它重组的替代系.

范围只限指定原族的余有限保留集、固定 $c>0$ 和 $0\le s<7/2$.
不处理一般无限删项、任意约束或投影筛选、$c=0$、关于 $c\downarrow0$ 的一致界、
逼近速度或 frame 界. $s\ge7/2$ 时原非仿射命名成员出域, 不能继续写同一个原族闭包公式.

完整作者证明与精确来源见[第十一轮解析稿](../research/artifacts/proof-audit-round11-20260926/cofinite-author/cofinite-all-orders.md),
可阅读版本见[PDF](../docs/SL_cofinite_all_orders.pdf). 精确版本独立验收见[第十一轮报告](../reports/proof-audit-round11-20260926/REPORT.md).
作者稿保留提交时状态, 最新验收状态由相应回执记录. 本结果不是完整 Lean 形式化或 canonical 接收.
