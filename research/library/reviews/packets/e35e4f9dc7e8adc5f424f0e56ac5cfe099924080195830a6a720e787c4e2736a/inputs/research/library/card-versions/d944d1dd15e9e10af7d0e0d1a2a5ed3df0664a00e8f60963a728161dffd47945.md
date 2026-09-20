---
dependencies: [{"location": "tools/spectral-domain-checks.md", "sha256": "8deeec4e940472b96a502a78ea8a600bb9570547c9819b378199d006233625d4"}]
title: 左定理论与 Hilbert 空间尺度
tags: [mathtool, left-definite]
source: Littlejohn-Wellman 2002; Fischbacher-Gesztesy-Hagelstein-Littlejohn 综述
status: 文献引用
created: 2026-08-04
---

# 左定理论与 Hilbert 空间尺度

## 解析
设 $A$ 为自伴算子, $A\ge kI$ ($k>0$). 对 $s>0$ 定义第 $s$ 个左定空间
$$H_s=(V_s,(\cdot,\cdot)_s),\qquad V_s=D(A^{s/2}),\quad (f,g)_s=(A^{s/2}f,A^{s/2}g).$$
性质: (1) $A$ 无界时 $V_t\subsetneq V_s$ ($0<s<t$), 内积两两不等价; (2) $H_s=A^{-s/2}H$; (3) $A^{(s-t)/2}:H_s\to H_t$ 为等距同构. 左定算子 $A_s$ 与 $A$ 酉等价, 谱相同, 完备特征函数系保持.

负阶需要另作完备化: 对 s<0, 使用 H 在 ||A^(s/2)f|| 下的完备化 (或相应对偶尺度), 不能因为 A^(s/2) 有界就认为 H 集合上的弱范数已经完备. 幂运算在完整尺度上按谱乘子延拓. Krein 例子的完整谱系与精确成员阈值见 [[spectral-domain-checks]].

## 适用范围
- 适用: 回答"解在多大空间中仍构成完备正交系" (问题 1 的框架); 构造尺度空间中的正交多项式基 (见 [[krein-sobolev-polynomials]]).
- 边界情形: $A$ 有界时所有 $V_s=V$; 需 $A\ge kI$ (正定性) 否则左定内积不正.
- 不适用: 不定内积问题 (需要 Krein 空间理论, 超出本工具).

## 验证与备注
- 会话 2 详细整理; 见 docs/SL_spectral_topics_summary.tex 主题一.
- 第一左定空间 $H^1[-1,1]$ 与移位 Krein Laplacian 的关系是基准论文的核心.
