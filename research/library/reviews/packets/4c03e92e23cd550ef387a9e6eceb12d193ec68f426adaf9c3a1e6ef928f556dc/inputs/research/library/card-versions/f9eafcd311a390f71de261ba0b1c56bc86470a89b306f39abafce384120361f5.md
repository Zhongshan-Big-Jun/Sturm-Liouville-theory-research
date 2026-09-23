---
title: Bloch 能带与带边比值
tags: [mathtool, spectral]
source: 周期介质理论 + 本项目能带极限推导
status: 数值验证 (能带极限)
created: 2026-08-04
---

# Bloch 能带与带边比值

## 解析
周期介质 (周期胞元重复) 的谱为能带结构: 带内 $\lambda_{n+1}/\lambda_n\to 1$, 带隙处比值较大. 对交替胞元 $[1,R]$ (权重 $1,R$), 带边相位 $\varphi_1=\arccos((\sqrt{R}-1)/(\sqrt{R}+1))$ 决定比值极限
$$c_\infty(R)=\left(\frac{\pi-\varphi_1}{\varphi_1}\right)^2.$$
本项目数值 (R=4): $c_\infty(4)=2.40916855=\mu(4)$; R=2: $c_\infty(2)=1.55403629\neq\mu(2)=3.05139810$.

## 适用范围
- 适用: 固定 $n$ 上确界猜想 ([[balanced-phase]]) 的 $n\to\infty$ 极限; 解释 $\Lambda_n^{\sup}(R)$ 的递减趋势.
- 边界情形: $c_\infty(R)=\mu(R)$ 仅当 $(\sqrt{R}-1)/(\sqrt{R}+1)=1/(\sqrt{R}+1)$, 即 $R=4$ (巧合).
- 不适用: 不能直接给出有限 $n$ 的极值; 能带极限是猜想的一部分, 不是已证定理.

## 验证与备注
- 会话 5: 固定 $n$ 候选配置的 $c_n$ 单调递减趋近 $c_\infty(R)$ (数值), Keller 变分条件对 $n=1..8$ 符号级验证 (1e-11).
- 状态: 作为猜想工具使用, 非定理.
