---
slug: largeR-level-cascade
title: 大 R 层级级联平衡 (band 系统整数幂级数)
tags: [谱优化, 级联, 渐近, bang-bang, 硬常数, 负结果]
status: STRICT 结构已证 (独立审计通过); 分支根开放
source: 会话 105 (R-210/R-211/R-212, run R-20260812T090000Z-g1prime-g2)
related: ["[[balanced-phase]]", "[[gap-band-extremals]]", "[[band-selfconsistency-equivariance]]", "[[transfer-matrix-secular]]"]
---

# 大 R 层级级联平衡

## 解析

对 n=2 对称 INF 分支的闭合 4 方程带自洽系统 (E1=E2=E5=E6=0,
`scripts/_gapn2_largeR_closed.py`), 记 u=R^(-1/6), eps=u^3=R^(-1/2),
ansatz k2=K(u)u, k3=K(u)u+C(u)u^5, p1=pi/2+A(u)u^2, p3=pi/4+B(u)u^2,
K/A/B/C 为 u 的整数幂级数 (系数 K_j, A_j, B_j, C_j). 结论 (STRICT, 独立审计通过):

1. K-清分母 (E2*K^2, E5*K^5, E6*K) 保持零点集 (K>0).
2. Level 0: E1_0=E2_0=E6_3=0 <=> a0*K0=2; E5_2=(a0K0-2)*F 无独立约束.
3. Level 1: a1 = -2 K1/K0^2; K1 在此时自由.
4. 归约种子: E1_2/E2_2/E6_5 关于 (a2,K2,c0) 仿射线性 (K1 只经 K1^2 进入);
   E5_4 二次; b0,b1 推迟到 E5_6/E5_7; C1 首次出现于 E5_5.
5. 硬常数机制: E5_5 = K0^3/2 + 线性(K1,C1) + O(K1^3) (K-清分母后), 故
   偶次 ansatz (K1=A1=B1=C1=0) 结构上不可能; 强制奇分量落在 (K1,C1) 对.
6. 层依赖结构 (更正版): K_j/A_j 同阶推进, B_j 平移约 2+j 阶, C_j 平移约
   5+j 阶; level j>=3 的 4x4 系数矩阵奇异 (B3/C3 列恒零, 审计 F-NL3),
   故"每层解 (K_j,a_j,b_j,c_j)"的机制错误, 正确机制是分族平移层.

## 适用范围

- 适用: 闭合 band 系统的形式整数幂级数平衡分析; 层级依赖结构与硬常数
  障碍的符号判定.
- 边界/不适用: 纯整数幂 ansatz 在本问题失败 (决定性 EVIDENCE: 20 组多
  起点全部收敛到退化极限 K0->0, 拟合极限 K0~3.4553 不是截断系统至 u^7 的
  零点). 真实分支可能需 (i) 非零奇分量 K1 联合求解 {K0,K1,C0,C1}, 或
  (ii) 非整数幂 (对数型) 修正. 未解决.
- 精度注意: 截断幂字典 eq_coeff (smul/spow) 在 2 阶丢项 (a2*K0^3,
  12*K0*K2, -12*K1^2), 已撤回 (R-211); 必须用全代入
  sp.expand(coef.subs(series)*u^m).coeff(u,n).

## 验证与备注

- 状态: STRICT 结构 (levels 0-2 + 硬常数 + 依赖结构) 经独立对抗审计
  (audit_report.md, A1-A8) 判定 INDEPENDENTLY_AUDITED_PROOF; F-NL3 更正
  S4 机制; M3 总体 RIGOROUS_PARTIAL_RESULT.
- 脚本: scripts/_gapn2_largeR_cascade.py, _gapn2_cascade_seed.py,
  _gapn2_cascade_reduce.py, _gapn2_seed_correct.py, _gapn2_seed_multistart.py,
  _gapn2_reduced_dof.py, _gapn2_pddiff_debug.py; 审计 scripts/_audit_m3_*.py.
- 数据锚点: big.json 末行 u=R^(-1/6) 至 4e-17; D*R=2Kc+c^2 u^4 至 3.5e-13
  (50 位 mpmath).
- 来源: 会话 105 (2026-08-14, P0, math-research-workflow 管道); 上游运行
  R-20260812T090000Z-g1prime-g2 (R-210/R-211 求解, R-212 审计).
