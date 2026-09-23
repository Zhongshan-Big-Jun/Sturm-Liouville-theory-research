---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837"], "created": "2026-09-20", "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "scope": "Fixed c>0; original complete named sparse family in genuine powers of the positive self-adjoint Krein operator; no uniform-c, arbitrary-subspace or stable-basis claim.", "source": "docs/SL_fractional_left_definite.tex, 2026-09-20 round 2", "sources": [{"locator": "Full spectrum, all-member threshold and four-trace graph-core proof", "path": "docs/SL_fractional_left_definite.tex", "sha256": "30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186"}], "status": "第六轮精确非负窗0<=s<7/2; 解析证明与局部Lean范围分开", "tags": ["mathtool", "spectral-theory", "domain", "correction"], "title": "Krein 谱系与幂域成员性检查", "tool_id": "spectral-domain-checks"}
---

# Krein 谱系与幂域成员性检查

设 `c>0`, 在 `L2(-1,1)` 中取 `Kc f=-f''+cf`, 定义域为通常 Sobolev
`H2` 中满足 `f'(1)=f'(-1)=(f(1)-f(-1))/2` 的函数. 对非负实数 s,
这里的 `Hs` 专指 `D(Kc^(s/2))`, 不直接指通常 Sobolev 空间.

完整正交谱系包含两个低模态:

| 未归一化模态 | 特征值 | L2 范数平方 |
| --- | --- | --- |
| 1 | c | 2 |
| x | c | 2/3 |
| cos(n pi x), n>=1 | (n pi)^2+c | 1 |
| sin(mu_n x), n>=1 | mu_n^2+c | mu_n^2/(1+mu_n^2) |

`mu_n` 是 `(n*pi,(n+1/2)*pi)` 中 `tan(mu)=mu` 的唯一根. 偶、奇子空间
分别化为 `[0,1]` 上的 Neumann-Neumann 和 Dirichlet-Robin 问题, 后者
含零频模态 x. 有 `||x||_s^2=2*c^s/3>0`; 漏掉它会让投影产生零方向.

采用归一化模态 e_j 后, 真正的成员条件是
`sum lambda_j^s |<f,e_j>|^2 < infinity`. 使用未归一化模态时要除以表中范数平方.
令 `p4=x^4-2*x^2`. 分部积分给出

```text
<x²,cos(n*pi*x)> = 4*(-1)^n/(n*pi)^2,
<p4,cos(n*pi*x)> = -48*(-1)^n/(n*pi)^4,
||x²||_t² = 2*c^t/9 + 16*sum_{n>=1} (((n*pi)^2+c)^t)/(n*pi)^4,
||p4||_s² = 98*c^s/225 + 2304*sum_{n>=1} (((n*pi)^2+c)^s)/(n*pi)^8.
```

这些等式中的无穷值表示不属于该幂域. 非负阶内的精确条件为
`x² in Ht iff t<3/2`, `p4 in Hs iff s<7/2`; 端点均发散. 依据是正项尾部
分别与 `n^(2t-4)` 和 `n^(2s-8)` 等价, 不是有限截断的数值趋势.
第六轮补证给出精确非负范围: 对每个固定 c>0, 全部命名成员在 `0<=s<7/2` 中属于 Hs 且线性包稠密. 每个非仿射 p_n 的阈值都是 `s<7/2`, 1,x 则属于全部非负幂域. 对 `s>=7/2`, 原族不是 Hs 的子集, 单独筛选可用命名成员只剩1,x, 不稠密. 这不排除若干不可单独使用的成员先作有限线性组合后抵消边界残差, 得到高阶域内的多项式.

对负实数 s, Hs 是 L2 在上述弱范数下的完备化, 不只是在 L2 集合上换范数.
余弦系数 `a_n=n^(-1/2)` 给出弱范数可和而 L2 不可和的例子.
完整尺度上的等距映射 `Hs -> H(s-2)` 是谱系数乘以 lambda_j 的延拓;
只有在原算子定义域内才能直接将其解释为经典微分算子 Kc.

数值应用先检查模态覆盖、归一化和成员性. 两个 op10 程序现在报告有限谱投影、
解析域判据和浮点尾界估计; 它们不提供无限维稠密性或向外舍入证书.
证明及实际复核指针见 [第二轮报告](../reports/proof-audit-round2-20260920/REPORT.md).


## 第六轮补证的可复用结构

对任意固定多项式 g, 两支未归一化谱系数均为 O(k^-2). 对 p in Pi intersect D(Kc), 自伴性再除以特征值, 得到 O(k^-4). 对每个 m>=2, p_(2m)′′′(1)=4m(4m-5), 而 p_(2m+1)′′′(1)-p_(2m+1)′′(1)=4m(4m-3). 首项分别为 -8m(4m-5)(-1)^k/(k*pi)^4 和 -8m(4m-3)*sin(mu_k)/mu_k^4, 余项 O(k^-6). 非零主项和正项级数给出端点7/2发散. 正弦模态的范数平方有正下界, 不能漏掉归一化.

密度用另一条完整证明: span{p_n}=Pi intersect D(Kc). D(Kc²) 的多项式须满足 Bf=0 和 B(f'')=0 四条迹, 其在 x²,x³,x4,x5 上的矩阵行列式为15360. 四阶 Sobolev 多项式逼近后减去固定右逆产生的残差修正, 得到 Pi intersect D(Kc²) 的图范数稠密性. 谱截断和 ||u||_s<=c^((s-4)/2)||u||_4 再传至 s<7/2. 例如 p6-(7/2)p4=x6-5x4+7x² 已满足四条迹.

[当前证明](../docs/SL_fractional_left_definite.tex)及[第六轮报告](../reports/proof-audit-round6-20260921/REPORT.md)给出完整量词与独立验收. H3向低阶传输仍正确, 但不是新增窗口的证明. 固定c和固定多项式的常数不声称关于c或次数一致; 一般受约束V、任意删除、Riesz/Schauder基和完整分数阶边界分类不在结论中. 局部Lean的四迹代数不等于整个解析论证已形式化.
