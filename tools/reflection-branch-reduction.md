---
canonical_key: reflection branch reduction R1-R6 (O3a C1 -> E1+M)
title: 反射分支归约 (reflection-branch-reduction)
tags: [mathtool, self-developed, reduction]
source: 自研 (run R-20260806T140000Z-o3ac1-42F931, Beauvoir)
status: R1-R6 已证 (审计 PASS); C1 归约到 E1+M (开放)
created: 2026-08-06
---

# 反射分支归约 (reflection-branch-reduction)

## 解析
对垒族 $\rho_{(a,b)}=R\cdot\mathbf1_{(a,b)}+1$, 记 $\sigma(a,b)=(1-b,1-a)$ 为反射.
$f=\lambda_1u_1^2-\lambda_2u_2^2$, $R_1=f(a)$, $R_2=f(b)$,
$g_1,g_2$ 为残差分支 ($R_1=0$/$R_2=0$ 主叶), $h=g_1-g_2$ on $I=[a_0,\beta]$.
- R1 (残差反射): $R_1(\sigma(a,b))=R_2(a,b)$, $R_2(\sigma(a,b))=R_1(a,b)$;
  镜像问题特征对经 $y(x)\mapsto y(1-x)$ 等距.
- R2 (分支反射): $\sigma(\Gamma_1)=\Gamma_2$ (主叶), $g_2(a)=1-g_1^{-1}(1-a)$;
  符号一致性由 $c_v=y_2'(1)/y_1'(1)<0$ 保持; 主叶一步依赖 H2 (单分支结构).
- R3 (h 反射公式): $h(a)=g_1(a)-1+g_1^{-1}(1-a)$,
  $h'(a)=g_1'(a)-1/g_1'(u(a))$, $u(a):=g_1^{-1}(1-a)$.
- R4 (积分恒等式): $h(a)=\int_{u(a)}^a(g_1'(t)-1)\,dt$ (FTC); MVT 推论显示
  符号结构, 但``$g_1'>1$ on I''充分条件被否证 (CE-3: 大 R 时 $g_1'$ 降到 ~0.98).
- R5 (好根 = h 零点): $R_1=R_2=0$ 的解必为符号一致好根 ($a=x_-$, $b=x_+$);
  C1 等价于系统 $\{R_1=0,R_2=0\}$ 在 $\{0<a<b<1\}$ 内唯一解.
- R6 (C1 归约): C1 成立若 (E1) 端点符号 $h(a_0)<0<h(\beta)$ + (Z) $h(a_{fp})=0$
  + (M) $h'$ 至多两零点 (符号模式 $-+-$, $h(x_1)<0<h(x_2)$).

## 适用范围
- 适用: 对称性显著的二参数极值问题; 残差函数分支的反射结构; 把``分支唯一
  相交''归约为一维函数 h 的零点计数; 大 R 多叶分支的规避 (用反射公式从单叶
  $g_1$ 计算 $g_2$, 避免直接追踪 $\Gamma_2$).
- 边界情形: $R\to1+$ 分支退化为垂直/水平线 (IFT 退化); $R\ge\sim1000$ 时
  $g_1'$ 可小于 1 (MVT 充分条件失效, 必须用积分形式 R4); 大 R 右端
  $\Gamma_2$ 多叶 (R=1e4, a=0.57364 处三个 R2 根).
- 不适用: 无对称性的问题 (反射是核心); 需要分支全局单叶性的结论 (H2 未证).

## 验证与备注
- 来源: run R-20260806T140000Z-o3ac1-42F931 (candidate_proof.md + audit_report.md +
  research_ledger.md R-101..R-108); 数值验证 R in {1.02..1e7}, 反射恒等式到 1e-16,
  分支反射残差 1e-9..1e-11.
- 关键陷阱 (ledger R-103): secular 根扫描上限 2pi+1e-3 会漏掉重垒推到 4pi^2 以上的
  特征值 (R=1e4 时 s2 > 6.284), 造成幻影分支缺口; 必须自适应到 6pi.
- 状态: R1-R6 已证 (初等, 审计 PASS); E1 与 M 为精确剩余缺口 (数值全通过, 解析开放).