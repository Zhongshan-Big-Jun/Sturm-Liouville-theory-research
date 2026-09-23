# 规定平衡候选序列的严格单调与带边极限

固定 R>1, s=sqrt(R), n>=1. 只研究 `[1,R,1,...,1]` 的 2n+1 块规定配置,
轻块宽 s/((n+1)s+n), 重块宽 1/((n+1)s+n).
令 c_n(R) 为该配置的实际相邻比值 lambda_(n+1)/lambda_n.
由 [[secular-chebyshev-jacobi-rootcount]] 的归一化根计数,
`c_n=((pi-y_n)/y_n)^2`, 其中 y_n 是 (0,pi/2) 中最大的相位根.

令 `A=(s+1)^2/s`, `B=s+1/s`, `delta=1/s in (0,1)`,
J_n 的首对角为 -delta、其余对角为零、两条次对角为一, z_n=min spec(J_n).
则 `y_n=arccos sqrt((B+z_n)/A)`.
J_n 是 J_(n+1) 的主子矩阵, 因而 z_(n+1)<=z_n.
若相等, 最小向量补末尾零将是更大矩阵的本征向量; 最后一行和递推迫使其全零,
故实际严格小于. 两端平方和给 z_n>-2, 交替单位向量给

`z_n<=-2+(2-delta)/n`.

因此 z_n 严格下降到 -2, y_n 严格上升到
`phi(R)=arccos((sqrt(R)-1)/(sqrt(R)+1))`.
函数 H(y)=(pi/y-1)^2 在 (0,pi/2) 严格递减, 所以

`c_n(R) downarrow c_infinity(R)=((pi-phi(R))/phi(R))^2`.

这是全部 n 的解析结论. 完整证明见
[第九轮 B2](../research/artifacts/proof-audit-round9-20260923/analytic-repair.md),
[固定 n 文稿](../docs/SL_fixed_n_supremum.tex).
R=4 时约为 2.4091685548064623, R=2 时约为 1.55403629; 小数仅是公式展示.

范围: 规定平衡候选序列, 不把 c_n 与所有容许密度上的 Lambda_n^sup 等同.
全局最优性 O1/O2、完整 Lambda_n^sup 序列的单调极限仍开放.
本文不主张一般周期介质的谱或任意配置均满足此公式, 不依赖旧有限样本来证明无限 n.
旧版的“仅数值观察”升级仅限上述明确对象, 当前复用状态由精确版本的独立纠错回执控制.
