---
slug: banded-shift-toeplitz-density
title: 稳定移位带 Toeplitz 空间的稀疏族稠密性有限秩判据
tags: [稠密性, 非对角, Toeplitz, 有限线性代数, O1']
status: STRICT (RIGOROUS_PARTIAL_RESULT, 一般 O1' 仍开放)
source: R-20260823T000000Z-o1p-baseline (plugin perf eval round 3)
related: ["[[constrained-denseness-runs]]", "[[denseness-criteria]]", "[[moment-jump-completeness]]"]
---

# 稳定移位带 Toeplitz 空间的稀疏族稠密性有限秩判据

## 解析

设 m >= 1, lambda = (lambda_1,...,lambda_m) in R^m. 在实 l^2(N_0) 中令

    x^k = e_k + sum_{s=1}^m lambda_s e_{k+s}.

若 L(z) = 1 + sum_s lambda_s z^s 在闭单位圆盘无零点 (稳定假设), 则:

- 矩映射 J: w -> (<w,x^k>)_k = I + sum_s lambda_s B^s 是有界可逆
  Toeplitz 算子, 其中 B 为后移. 因此矩序列 M 可由某个 w in H 实现 iff
  M in l^2.
- 对有限多项式 representer v_j = sum_i c_i x^i, 保留集 N 余有限:
  所有 n > max_j d_j + m + 2 均保留.
- 抽象版 (STRICT): 若 H 的单项式由有界可逆算子 A 生成且 Gram 带形, 则同一
  判据成立 (Theorem 2.3): closure(span Q_sp)=V <=> ker(T|B_fin)={0}.
- 精确判据 (STRICT):

      closure(span Q_sp) = V  <=>  ker(T|_{B_fin}) = {0},

  其中 B_fin 是有限游程的自由基, T 的列是有限游程矩向量在成员方程中
  的像. 这推广了 H_lambda (m=1) 的判据到带宽 m >= 1.
- 具体例子 (STRICT): 取 m=2, v_1 = x^4, 则所有稳定 lambda 下
  Q_sp 在 V = ker M_4 中不稠密; 阻挠矩序列为 delta_2.

## 适用范围

- 适用: 实 l^2 上的有限移位扰动, 稳定多项式 L; 有限多项式约束.
- 边界情形: m=1 回归 H_lambda; lambda=0 回归 H_0; r=0 判定稠密.
- 不适用: 一般带形 Gram (无稳定 Toeplitz 可逆矩映射), 加权 L^2,
  非有限多项式 representer, 一般非对角 H.

## 验证状态

- STRICT 证明: candidate_proof.md (run R-20260823T000000Z-o1p-baseline).
- EVIDENCE: scripts banded_shift_verify.py / audit_banded_shift.py 验证
  保留集/游程/阻挠序列; 数值与符号只作一致性检查, 不作为证明.
- Lean scaffold: SL/DensBCO1p3BandShift.lean (sorry, 未验证).
