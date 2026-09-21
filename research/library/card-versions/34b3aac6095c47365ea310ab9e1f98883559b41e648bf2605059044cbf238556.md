---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837", "coordinator-20260920-round3"], "created": "2026-08-05", "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "scope": "Both parity recurrences; product equality only for B=Bprime=0; formal polynomial images distinguished from Krein domain.", "source": "自研 (会话 11, 方向 3)", "sources": [{"locator": "Unchanged third-round general recurrence, exact model and perturbation proof", "path": "docs/SL_stability_moment_jump.tex", "sha256": "f77079f053c7d22a03ae5dffc38f092fb9b532c92345256582a96d2d41f03c45"}, {"locator": "Sixth-round range/dependency update only; unchanged earlier branches keep their own scope", "path": "docs/SL_fractional_left_definite.tex", "sha256": "30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186"}], "status": "第三轮解析修订; 可复用状态见纠错记录", "tags": ["mathtool", "self-developed", "completeness", "moments", "stability"], "title": "矩跳跃的条件稳定性: 实际递推与 B=0 模型", "tool_id": "jump-stability"}
---
# 矩跳跃的条件稳定性

本卡区分一般二阶递推、实际解的完备性判据和 B=0 的精确模型. 第三轮修订撤回旧的一般增长分类及无条件有界基扰动稳健性. 独立复核与是否可复用以纠错记录及当前指针表为准; 本卡不承担全项目认证.

## 一般递推只给出下界

令 c0>0, u0=0, u1=1, c0*u_m=A_m*u_(m-1)-B_m*u_(m-2). 对每个 m>=2 要求 B_m>=0, A_m-B_m>=c0. 记 eps_m=(A_m-B_m-c0)/c0. 恒等式

```
u_m=(1+eps_m)*u_(m-1)+(B_m/c0)*(u_(m-1)-u_(m-2))
```

给出单调性及 u_m>=prod_(k=2..m)(1+eps_k). 一般 B>0 不能把下界当等式, 也不能由 S(m)=sum log(1+eps_k)=O(log m) 推出实际解多项式有界. 反例 c0=1,A=3,B=2 给出 S=0 而 u_m=2^m-1.

对于包含 q0=c0,q1=c0*x、缺少指标2和3、偶奇侧均为上述三项跳变结构的族, 若实 Hilbert 空间中全部多项式稠密、矩取同一个内积、||x^k||<=C_H*(k+1)^beta, 则两侧的全指标系数条件和 S(m)/log m -> infinity 足以推出完备性. 两侧都须检验. 截断增量 sum min(eps_k,1)/log m -> infinity 是较强的充分条件.

## 精确分类使用实际解或限定的模型

在系数对角空间 (x^j,x^k)=delta_jk*(k+1)^(2*beta) 中, 令 u,u' 为实际偶、奇基本解. 完备当且仅当两个级数都发散:

```
sum_(m>=1) |u_m|^2/(2m+1)^(2*beta)
sum_(m>=1) |u'_m|^2/(2m+2)^(2*beta).
```

一个级数收敛即给出相应奇偶非零正交元. 这项充要判据不要求单调性. 它不能直接代替一般非对角空间的矩可表示性分析.

- 明确 B=B'=0, A=A'=c0*(1+C/k), C>0 时, u_m=Gamma(m+1+C)/(Gamma(2+C)*Gamma(m+1)); 完备 iff beta<=C+1/2. C=2 的精确值是 (m+1)(m+2)/6.
- 明确 B=B'=0, A=A'=c0*(1+C/(k*log k)), C>0 时, u_m 与 (log m)^C 双边可比; 完备 iff beta<=1/2.
- 一般 B=2,A=3+2/m 时仍有 u_m>=2^m-1. 同样的 eps 不决定同样的增长. S=O(log m) 与 S/log m->infinity 也不穷尽所有序列.
- 稀疏例的跳点是真正的 k_j=2^(2^j), j>=1. 在这些点取 eps=exp(k_j), 其余取0, 则 S/log m->infinity, 但截断增量仅 O(log log m).

## 基扰动须检查两个系数、有限前缀与域

原 Krein 两侧系数差是 4m+c*m/(m-1). 固定 c>0 换成任意一致的新 c'>0 后仍有增长充分性, 但套用目标 Hilbert 空间之前必须核对空间假设.

偶侧 p_tilde=x^(2m)-(m/(m-1)+delta_m)*x^(2m-2) 的形式微分像 (c-D^2)p_tilde 有

```
A_delta=2m(2m-1)+c*(m/(m-1)+delta_m)
B_delta=(m/(m-1)+delta_m)*(2m-2)*(2m-3)
A_delta-B_delta=4m+c*m/(m-1)+delta_m*(c-(2m-2)*(2m-3)).
```

c=3,m=4,delta=1 给出 A=63,B=70, 差=-7. 奇侧的导数因子须相应改成 (2m-1)*(2m-2). 若每个 m>=2、两侧均有 |delta_m|<=1/(8m), 则 B>=0、A-B>=(7/2)*m+c, 因而在上述抽象空间假设下得到形式像族完备. 这只是一项足够条件.

不能改为“有界”或“最终足够小”: 在 c=3,L2(-1,1) 中, 取偶侧

```
delta_m=6m(2m+5)/((m-1)(2m+3)(4m^2-6m-7)), m>=2,
```

保留原奇侧, 则 delta2=-36/7, delta3=1, delta_m~3/(2m^2), 全族却与非零 P2=(3x^2-1)/2 正交. 该例前缀的 B2<0, 没有反驳全指标充分条件.

真正 K_c 的边界是 f'(1)=f'(-1)=(f(1)-f(-1))/2. 偶侧扰动的端点导数为 -(2m-2)*delta_m; 非零扰动通常不在 D(K_c). 必须区分形式微分像与算子作用. H_beta 也不是 Krein 幂域 H^s.

## 来源、程序与边界

完整解析证明与反例: `docs/SL_stability_moment_jump.tex`, 第三轮修訂版. 原始错误字节及外部报告保存在 `research/artifacts/proof-audit-round3-20260920/before/` 和 `submitted-audit.md`.

活动程序: `scripts/d3_stability_verify.py`, `scripts/d3_stability_verify2.py`, `scripts/op12_dichotomy_verify.py`, `scripts/op12_threshold_verify.py`, `scripts/op12_sparse_check.py`. 有限部分和和浮点趋势不证明无穷级数敛散. 局部 Lean 不能替代全部 Hilbert 空间与谱域分析.

原 Krein 稀疏族在0<=s<7/2的精确结果由第六轮四迹图核证明另行建立, 不由本卡的一般空间假设直接推出. 本卡保留一般非对角可表示性及变系数算子的研究边界.

2026-09-21 review-binding renewal: the stability mathematics and its proof source are unchanged. The previous shared verification packet also bound the quotient paper, whose separate unit-limit section is now repaired. This card is rechecked in its own precise scope; the fourth-round quotient correction is not a new counterexample to this card.
