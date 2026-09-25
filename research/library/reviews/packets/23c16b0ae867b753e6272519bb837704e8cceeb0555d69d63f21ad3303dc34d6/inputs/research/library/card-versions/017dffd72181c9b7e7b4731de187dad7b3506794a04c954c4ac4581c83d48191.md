---
title: Feynman-Hellmann 公式
tags: [mathtool, spectral]
source: 量子力学标准公式
status: 文献引用
created: 2026-08-04
---

# Feynman-Hellmann 公式

## 解析
对单参数算子族 $H(\tau)$ 与简单特征值 $\lambda_k(\tau)$, 归一化特征函数 $y_k$ (满足 $\int \rho y_k^2=1$) 满足
$$\partial_\tau\lambda_k(\tau) = \langle (\partial_\tau H)\,y_k,\,y_k\rangle.$$
对 $H(\tau)=-d^2/dx^2+\tau\rho(x)$, 有 $\partial_\tau\lambda_k=\int \rho\, y_k^2\,dx$ (已归一化).

## 适用范围
- 适用: 特征值对参数的单调性; 极值问题的一阶必要条件; 数值梯度.
- 边界情形: 退化 (重) 特征值处公式需用子空间形式; 归一化必须是权重归一化 $\int\rho y^2=1$.
- 不适用: 二阶变分需要额外计算 (本工具只给一阶).

## 验证与备注
- 在 Keller 变分条件 ([[keller-variational]]) 的推导背景中出现; 忽略权重归一化会得到错误条件 (会话 5 失败登记).
