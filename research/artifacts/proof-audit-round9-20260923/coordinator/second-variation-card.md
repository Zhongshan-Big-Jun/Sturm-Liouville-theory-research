# 加权特征值二阶变分与路径规范

设 `-u''=lambda rho u`, Dirichlet 区间 [0,1], 实 `0<m<=rho<=M<infinity`,
`int rho u_k^2=1`, 实有界方向 h, 线性密度路径 rho+t h 在零点附近保持正下界.
记 `a_k=int h u_k^2`, `B_kl=int h u_k u_l`. 在任意基点,

`lambda_k'=-lambda_k a_k`,

`lambda_k''=2lambda_k a_k^2-2lambda_k^2 sum_(l!=k) B_kl^2/(lambda_l-lambda_k)`.

所有 B_kl 配对均按 dx 积分. 分母有符号, 不能换为绝对值. 完整解析论证见
[本轮证明 V1-V4](../research/artifacts/proof-audit-round9-20260923/analytic-repair.md).
它从 Volterra 射击解构造解析分支, 再由加权正交展开与可求和性得到公式.

归一化导数必须包含核分量:

`v=-(a_k/2)u_k+lambda_k sum_(l!=k) B_kl/(lambda_l-lambda_k) u_l`.

若普通 L2(dx) 的正交约化逆给出
`v0=lambda_k R_perp[(h-a_k rho)u_k]`, 则
`v=v0-(a_k/2+int rho u_k v0)u_k`.
取 h=rho 有 v0=0, v=-u_k/2; 旧稿将两者直接相等的式子撤回.
谱 Green 有限部和普通 L2 正交约化逆也不是同一规范.

对 `D_n=lambda_(n+1)-lambda_n`, 定义
`f=lambda_n u_n^2-lambda_(n+1)u_(n+1)^2`, 则 `D_n'[h]=int f h`,
`Q(h)=(lambda_(n+1)''-lambda_n'')/2`. Q 在非驻点也有意义.
分块常值方向 b 的切向条件是 `dot(b,A)=0`, `A_i=int_(I_i) f`.
普通欧氏投影为 `b=b0-dot(b0,A)A/dot(A,A)`; A=0 时保留 b0.
若用真实 L2 系数度量 `sum L_i b_i c_i`, 则用
`b=b0-[sum L_i b0_i g_i/sum L_i g_i^2]g`, `g_i=A_i/L_i`.
旧脚本对未加权块平均值的投影不保证真实切向性; 常密度不等宽反例见 V2.
这些是局部正密度方向, 还不能自动作为饱和盒约束的可行方向.

一维正则问题的去简单极点 Green 核在闭正方形连续有界.
固定总变差的集中脉冲二次型因此有有限点值极限. 特别在 rho=1,
单位质量脉冲集中到 1/2 时 `lambda_1''->6pi^2`, `lambda_2''->0`,
`Q->-3pi^2`. V3 给出完整谱和的控制收敛, 不依赖有限截断.
旧“bump 越窄必然 Green 对角发散”的理由撤回; 不推广到无界总质量、核导数或高维.

移动接口 a_i(t)=a_i+t d_i, 跳量 s_i=rho_right-rho_left 时,
`dot rho=-sum s_i d_i delta_(a_i)`, `ddot rho=sum s_i d_i^2 delta'_(a_i)`.
二阶路径链式法则中还应计入有限项 `-sum s_i d_i^2 f'(a_i)`
(这是完整二阶导数的项, 对 Q 需除以二). 驻点 f(a_i)=0 不使 f'(a_i) 消失.
本卡没有把任意分布路径的可微性当成已证前提, 没有据此证明 G1' 的定号.

历史 R-206 addendum 及旧 P1/P2/P3 输出按原字节保留.
F01 撤回其分块 P2 的“切向”解释, 不凭该错误否定任意方向 P1 二阶公式或实际积分的 P2b 分支.
随机同号样本不能证明切空间负定. 新脚本的方向残差、截断和有限差分结果按
[第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md) 中真实重算范围阅读.
旧 P3 的稀网格窄脉冲和符号差异不能封死整条路线.

可继续研究: 在固定接口族中严格建立线性密度极限与有限加速度项的组合,
再研究完整宽度 Hessian 的符号. 此为重开的待证路线, 不是已解决的 G1'/O1/O2.
