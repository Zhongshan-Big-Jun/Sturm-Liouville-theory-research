---
title: 区间自动微分证书 (interval-ad-certificate)
tags: [mathtool, self-developed]
source: 自研 (O3a, run R-20260806T011500Z-o3abranch-E8E56F)
status: 已实现并通过 (CE-1 严格化; mpmath.iv 外舍入)
created: 2026-08-06
---

# 区间自动微分证书 (interval-ad-certificate)

## 解析
把数值反例升级为严格反例的可复现方法, 由四步组成:

1. 区间求根包络: 对隐式量 (如分支点 b1(a), b2(a); secular 根 s1, s2) 用区间
   中值定理 (区间值在端点符号确定且相反) 加二分, 得到宽度 ~1e-27 的包络
   [b-, b+]; 用区间导数在矩形上的符号确定保证括号内根的唯一性.
2. 前向模式区间 AD: 对 elementary 函数 (sin/cos/sqrt/幂) 实现带区间值与区间
   梯度的 AD, 计算隐式偏导 (secular 方程 + 残差函数) 在包络矩形上的包络.
3. 隐函数闭式: 分支斜率 g' 由
   g1' = (-r1a + r1s1*sec_a1/sec_s1 + r1s2*sec_a2/sec_s2)
         / (r1b - r1s1*sec_b1/sec_s1 - r1s2*sec_b2/sec_s2)
   给出 (对 g2' 同理); 只需验证分母与 sec_s 区间符号确定 (隐函数定理适用).
4. 结论: 若目标量的区间包络不含 0 (或上界 < 0), 则符号被严格证明.

本 run 用法: 证伪 Lemma A. 在 (R, a*) = (1500, 0.57364) 与 (1e4, 0.57364),
h' = g1' - g2' 的区间包络为 [-3.43e-4, -3.43e-4] 与 [-3.20e-3, -3.20e-3],
严格 < 0.

## 适用范围
- 适用: 隐函数斜率/残差符号的严格判定; 把浮点反例升级为可复现的区间证书;
  一维/二维隐式量包络 (IVT 二分).
- 边界情形: 要求所有被除数区间远离 0 (需先验证); 要求区间函数的包含单调性;
  信任模型为区间算术库的外舍入 (mpmath.iv 的 libmp mpi_* 用 round_floor /
  round_ceiling, sin/cos 用象限单调性包络) - 标准 verified computation 实践,
  但未经形式化证明器机器核验.
- 不适用: 大区间上的全局符号断言 (区间过宽时包含单调性使结论退化); 依赖问题
  使包络过宽的场景 (应缩小包络或改写表达式).
- 实现注意: mpmath.iv 对 `iv * AD对象` 抛 NotImplementedError 而非
  NotImplemented, 必须保证 AD 对象恒在乘法/除法的左侧; 区间 AD 的公式若混用
  R (密度) 与 m = sqrt(R) (波数) 会产生数值巨大偏差, 每个偏导都要与有限差分
  对拍.

## 验证与备注
- 来源: run R-20260806T011500Z-o3abranch-E8E56F 的 cert_ce1.py +
  cert_ce1_output.txt (输出含全部包络与符号检查); 开发期失败与修复见
  research_ledger R-122 (AD bug 1-3, ir1/ir2 丢 s^2 因子, 括号越界等).
- 精度: 包络宽度 ~5e-28 (根), h' 包络宽度 ~1e-31; 全部偏导与高精度有限差分
  对拍一致 (60 位有效数字).
- 相关: [[fh-hessian-branch-reduction]] (被证伪的目标), [[residual-exactness]].