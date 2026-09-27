---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0bfab-01ac-7dd2-b9e3-15edb3ffd3f3", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837", "coordinator-20260920-round3"], "created": "2026-08-04", "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "source": "Littlejohn-Quintero-Roba 2025 (OPSFA-16, DOI 10.1007/978-3-031-90135-5_7); 姊妹论文 Jones-Littlejohn-Quintero Roba, Axioms 14 (2025) 115", "sources": [{"locator": "Setting and thm:high/unit; ordinary representatives versus quotient classes", "path": "docs/SL_krein_c0_limit.tex", "sha256": "bf56125edd8bcc635893b6f9a1a81a232d82d22f6a9620171a4a4b9014e50b87"}, {"locator": "Sixth-round sharp 0<=s<7/2 range, distinct from the fixed-mode c-to-zero quotient proof", "path": "docs/SL_fractional_left_definite.tex", "sha256": "30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186"}, {"locator": "Operator inverse versus algebraic polynomial inverse", "path": "tools/krein-power-domain-polynomial-obstruction.md", "sha256": "09916637f07ca33bea8c4411842d95e05946bbd3749bc6817474a0f4c9d3aa55"}], "status": "姊妹论文全文还原 (基准论文全文未获取)", "tags": ["mathtool", "left-definite", "orthogonal-polynomials"], "title": "Krein-Sobolev 正交多项式", "tool_id": "krein-sobolev-polynomials"}
---

# Krein-Sobolev 正交多项式

## 解析
移位 Krein Laplacian $K_c$ (边界 $f'(1)=f'(-1)=(f(1)-f(-1))/2$) 的第一左定空间为 $(H^1[-1,1],(\cdot,\cdot)_{1,c})$. 对其作 Gram-Schmidt 正交化得到 Krein-Sobolev 多项式 $\{K_n\}$: 在 $H^1$ 中完备正交, 根全实单且位于 $(-1,1)$; 偶次 $K_{2n}$ 与 Althammer (Sobolev-Legendre) 多项式重合; 显式系数由超几何求和给出; 对偶恒等式 $(f,g)_{1,c}=c\langle f,g\rangle_{1/c}$.

## 适用范围
- 适用: 左定空间中构造完备正交多项式基; 研究代数完备与解析完备的区别.
- 边界情形: $H^2[-1,1]$ (边界约束) 中多项式基 $\{p_n\}$ 缺 2,3 次项, 代数不完备; 其 H2/H3 解析完备性已有项目证明; 第六轮四迹图核证明给出原族在整个0<=s<7/2稠密, 每个非仿射成员在s>=7/2均不属于该幂域. 先作有限组合可以抵消域残差; 不能恢复旧的全阶命名族推广.
- 不适用: 不能直接用于特征值比值问题 (那是主题 2).

## 与完备性证明基 {p_n} 的区别 (重要)

完备性证明 (会话 9-10) 使用的稀疏基 {p_n} (p_{2n} = x^{2n} - n/(n-1)x^{2n-2}, 缺 2,3 次)
**不是** Krein-Sobolev 多项式 {K_n}: 例如 (p_4, p_6)_1 = 128/105 + 181c/693 != 0.
{p_n} 的选择动机是 K_c p_{2m} 为三系数跳变多项式 (矩跳跃机制), 而非正交性.
{K_n} 是 (H^1, (·,·)_1) 中 Gram-Schmidt 化单幂基的完备正交系.
真正算子逆与多项式上的代数逆必须区分. 由算子传输得到的正交函数系不能未经证明称为同阶多项式系; 旧的全阶多项式解释已撤回 (历史: [[left-definite-orthogonal-systems]]). 域检查先读 [[krein-power-domain-polynomial-obstruction]].

## 验证与备注
- 会话 2 依据 Axioms 姊妹论文完整还原; 基准论文全文受版权保护未获取.
- 详细公式: docs/SL_spectral_topics_summary.tex 主题一.


- 2026-09-20 第三轮传播核查仅修正边界导数、H2/H3 状态与全阶传输表述; 上述其它文献摘要未在本轮重新审计. 来源与证据范围见第三轮报告.


## 2026-09-21: c下降到0时的函数代表与商类

令S_n=P_n-P_(n-2), W=span{1,x}. 零参数配对满足(S_n,S_m)_(1,0)=2(2n-1)delta_nm, 因而标准Gram-Schmidt的正首项代表为Q_n=S_n/sqrt(2(2n-1)). 对每个固定n>=2, 单位归一化Krein-Sobolev多项式的商类收敛到[Q_n]. 普通Sobolev H1中的函数极限则是P2/sqrt(6)、P3/sqrt(10) (n=2,3), 以及Q_n (n>=4). 低阶仿射差在商空间中消失, 在普通H1中并不消失. 不声称关于n一致的收敛.

高阶系数按奇偶归纳使用主项(4n^2-1)a_n/c与O(a_n)余项. a6-(63/c)a4=1+42/c, 不能把余项写成O(1). 这修正证明而不撤回固定高模态的发散结论. 完整解析证明见`docs/SL_krein_c0_limit.tex`的thm:high及thm:unit; 本轮未重新审计本卡其它既有文献摘要.
