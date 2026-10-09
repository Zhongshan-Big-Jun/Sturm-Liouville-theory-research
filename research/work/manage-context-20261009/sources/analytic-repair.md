# 第九轮修订的数学契约与证明

2026-09-23. 外部审计基线为 `2a81b608d53e3decee04c46716a8d8f8c2d9b1b4`.
本稿吸收并重新推导用户附件中的补证. 作者自检不代表独立验收; 精确版本的验收见本轮报告及纠错回执.
本轮不重新认证 INF 极限、整个 Green/M3/KP 链或固定指标的全局最优性.

## V1. 模型、解析分支与本征函数规范

全节取实函数, 区间为 [0,1], Dirichlet 边界, `0<m<=rho<=M<infinity` 几乎处处.
取固定实 `h in L^infinity`, 沿线性路径 `rho_t=rho+t h`, 只在仍有一致正下界的小邻域内求导.
记按指标排序的简单特征值为 lambda_k, 本征函数按 `int rho u_k^2=1` 归一.

所用可微分支可从射击解直接得到, 不依赖数值根定位. 初值 `y(0)=0,y'(0)=1` 的方程写成

`y(x)=x-lambda int_0^x (x-r)(rho(r)+t h(r))y(r) dr`.

Volterra 迭代在参数紧集上一致收敛, 所以 y 及 y' 对 (lambda,t) 解析.
在一个 Dirichlet 根, 记 `dot y=partial_lambda y`, Wronskian 恒等式给出

`y'(1) dot y(1)=int_0^1 rho y^2>0`.

由于 y'(1) 非零, 隐函数定理给出简单根的解析分支; 再除以正的加权范数得到同号的解析本征函数分支.
以下二阶公式在任意基点成立, 不需要基点为优化驻点.

令 `a=int h u_k^2`, `v=partial_t u_k(t)|0`, `L=A-lambda_k B`, `A=-d^2/dx^2`, `B=rho`.
一阶方程与归一化分别给出

`lambda_k'=-lambda_k a`, `L v=lambda_k(h-a rho)u_k`, `int rho u_k v=-a/2`.

在加权完备正交基下, 对 l 不等于 k 作配对得到

`(lambda_l-lambda_k) int rho v u_l = lambda_k int h u_k u_l`.

因此真正的归一化导数为

`v=-(a/2)u_k + lambda_k sum_(l!=k) [int h u_k u_l/(lambda_l-lambda_k)] u_l`.

这里 `(h/rho)u_k` 属加权 L2, 其系数平方可求和. 固定 k 的非零谱间隔离零有正距离,
所以所列级数在加权 L2 中收敛, 可与 h u_k 配对. 对各 t 的一阶公式再求导:

`lambda_k''=lambda_k a^2-2lambda_k int h u_k v`

`=2lambda_k a^2-2lambda_k^2 sum_(l!=k) (int h u_k u_l)^2/(lambda_l-lambda_k)`.

若 `R_perp` 专指普通 L2(dx) 中 L 的约化逆, 则其像只是一个特解

`v0=lambda_k R_perp[(h-a rho)u_k]`.

真实导数须恢复为

`v=v0-(a/2+int rho u_k v0)u_k`.

因为 `int rho u_k^2=1`, 该式恰好恢复归一化约束, 且加核项不改变 L v.
普通 L2 的正交性不能替换加权正交性. 取 h=rho 的精确负对照:
`lambda_k(t)=lambda_k/(1+t)`, `u_k(t)=u_k/sqrt(1+t)`, 所以 v=-u_k/2, 而 v0=0.
主要 lambda'' 公式仍给出 2lambda_k.

## V2. 分块方向的真实切空间

定义 `D_n=lambda_(n+1)-lambda_n`, `f=lambda_n u_n^2-lambda_(n+1)u_(n+1)^2`.
任意有界 h 的一阶变分是 `D_n'[h]=int f h`.
分割块 I_i 的长度为 L_i>0, h 在第 i 块取 b_i, 记 `A_i=int_(I_i) f`, `g_i=A_i/L_i`.
则切向条件精确为 `sum b_i A_i=0`.

在普通系数欧氏度量下, A 非零时用

`b=b0-(dot(b0,A)/dot(A,A)) A`.

直接代入得 dot(b,A)=0. A=0 时原方向 b0 已切向, 不作除法.
若采用真实 L2 的系数度量 `sum L_i b_i c_i`, 则用

`b=b0-[sum L_i b0_i g_i / sum L_i g_i^2] g`.

这两种都正确, 但不能把未加权的平均值投影当作后一种.
rho=1, n=1, 两块宽度 (1/4,3/4) 给出精确反例:

`A=(-3pi^2/4-pi/2, -9pi^2/4+pi/2)`,

`b=(-(9pi-2)/(3(3pi+2)), 1)`.

此时 dot(b,g)=0, 而 `dot(b,A)=-3pi^2/2+pi/3<0`.
数值实现须使用真实块端点积分, 并以独立积分机制检查 int f h, 不能仅打印构造时置零的内积.
有限个方向同号、有限谱截断或浮点矩阵的特征值, 均不证明无限维切空间定号.
这些方向属于正密度局部摄动空间; 在饱和盒约束点还需另检单侧可行性, 不能自动当作盒内可行方向.

## V3. 约化 Green 有限部与窄脉冲

这里的谱核是 `Gtilde_k(x,y)=sum_(l!=k) u_l(x)u_l(y)/(lambda_l-lambda_k)`,
即 `(A-z B)^(-1)` 的去极点有限部. 它一般不同于普通 L2 中 L 的正交约化逆;
不能把两种规范混用.

左右 Dirichlet 基本解与其一阶导数在闭区间连续, 对 z 解析. 它们组成的 Green 核
是左右基本解乘积除以 Wronskian, 在 x=y 两侧具有相同函数值.
Wronskian 在简单特征值只有一阶零点, 由 V1 的非零射击导数可见.
其 Laurent 极点的空间因子必为 u_k(x)u_k(y) 的倍数; 恒等式
`(A-z B)^(-1)(rho u_k)=u_k/(lambda_k-z)` 与加权归一化确定该倍数为一.
因此减去 `u_k(x)u_k(y)/(lambda_k-z)` 后的常数项在整个闭正方形上连续且有界.
上述 Laurent 展开对空间变量一致: 基本解及导数在紧空间/参数集上一致连续, 分母只依赖 z.
有限密度跳点改变二阶空间导数, 不导致这个核的对角值无穷大.

对固定 eta 的有界方向 h_eta, V1 中谱和的二次型为

`int int h_eta(x)h_eta(y)u_k(x)u_k(y)Gtilde_k(x,y) dx dy`.

若其有符号测度的总变差一致有界, 且支持集中到 a、总质量趋于 q,
连续核的均匀连续性使该二次型趋于 `q^2 u_k(a)^2 Gtilde_k(a,a)`.
有限个集中脉冲同理得到有限的双重有限和. 这不是对无限质量缩放、核导数或高维奇异核的结论.

一个完整可算反例取 rho=1, `u_k=sqrt(2)sin(k pi x)`, `lambda_k=k^2 pi^2`,
`h_eta=(2eta)^(-1) 1_(|x-1/2|<eta)`, `0<eta<1/2`.
对固定 k,l 有 `B_kl=int h_eta u_k u_l -> u_k(1/2)u_l(1/2)` 且 `|B_kl|<=2`.
由于 `sum_(l!=k) 1/|l^2-k^2|<infinity`, 控制收敛适用于完整谱和, 不是只截断若干模态.
中点处

`sum_(l!=1) u_l(1/2)^2/(lambda_l-lambda_1)`

`=(2/pi^2)sum_(m>=1)1/[4m(m+1)]=1/(2pi^2)`.

V1 于是给出 `lambda_1'' -> 6pi^2`, `lambda_2'' -> 0`,
`Q=(1/2)D_1'' -> -3pi^2`.
每次先在固定 eta 下求路径导数, 再取 eta 极限; 没有假设一个对所有 eta 通用的密度摄动半径.

## V4. 移动接口的有限加速度项

取固定不碰撞接口 a_i(t)=a_i+t d_i, 跳量 `s_i=rho_right-rho_left`.
对光滑测试函数 phi, 直接两次求导其分块积分得到

`dot rho=-sum s_i d_i delta_(a_i)`,

`ddot rho=sum s_i d_i^2 delta'_(a_i)`,

`<ddot rho,phi>=-sum s_i d_i^2 phi'(a_i)`.

故在适用二阶路径链式法则的场合, D_n 的接口二阶导数除线性密度 Hessian 项外,
还含 `-sum s_i d_i^2 f'(a_i)`. 本征函数为 C1, 所以 f' 在接口有唯一有限值.
`f(a_i)=0` 不能消去 f'(a_i). 此项是有限主阶项, 不是必然 Green 对角发散.
本稿不凭分布形式的链式法则宣称任意分布路径可微, 也不以旧 P3 的稀网格脉冲实验
证明任一普遍 Hessian 恒等式或符号结论. (G1') 仍开放; 纠正否定理由后, 补齐接口项的路线可重新研究.

## B1. 物理与归一化世俗函数

固定整数 n>=1, R>1, s=sqrt(R), `t_n=1/((n+1)s+n)`.
规定交替密度 `[1,R,1,...,1]` 的轻块宽 s t_n、重块宽 t_n.
令 `y=omega s t_n`, `omega=sqrt(lambda)>0`, 物理状态为 (u,u').
记 `F_n(y)=(T_end T_cell^n)_(01)`, 并定义 `Fhat_n(y)=omega(y) F_n(y)`.

以 `P_omega=diag(1,omega)` 作 `N=P_omega^(-1) T P_omega`, 记 C=cos y,S=sin y:

`N_cell=[[C^2-S^2/s, (s+1)SC/s],[-(s+1)SC,C^2-s S^2]]`,

`N_end=[[C,S],[-S,C]]`.

J=diag(1,-1) 给出 `N_cell(pi-y)=J N_cell(y) J`,
`N_end(pi-y)=-J N_end(y) J`. 因 J^2=I, 任意整数 n 的乘积满足
`N_end(pi-y) N_cell(pi-y)^n = -J [N_end(y)N_cell(y)^n] J`.
01 项不变, 即 `Fhat_n(pi-y)=Fhat_n(y)`.
对 0<y<pi, 两个 omega 均正, 所以

`F_n(pi-y)=[y/(pi-y)] F_n(y)`.

严格反例: n=1,R=4 时, `F_1(pi/3)=-21sqrt(3)/(40pi)`,
`F_1(2pi/3)=-21sqrt(3)/(80pi)`.
正比例因子保留内部根及其单重性; y=0 是归一化引入的端点零点, 不得计入 Dirichlet 正谱.

## B2. 根计数与嵌套 Jacobi 证明

令 `A=(s+1)^2/s`, `B=s+1/s=A-2`, `delta=1/s in (0,1)`.
归一化矩阵行列式为一. Cayley-Hamilton 与首项计算给出

`Fhat_n(y)=sin(y) P_n(cos^2 y)`,

`P_0=1`, `P_1=A x-s`, `P_n=(A x-B)P_(n-1)-P_(n-2)`.

设 `z=A x-B`. 对称 n 阶三对角矩阵 J_n 的第一对角元为 -delta,
其余对角元为零, 两条次对角线为一. 沿最后一行的行列式递推给出
`det(z I-J_n)=P_n((z+B)/A)`, 包括初值 `1,z+delta`.
它和历史末对角为 -delta 的矩阵经坐标倒序相似, 但第一对角的约定使 J_n 自然嵌入 J_(n+1).

对任意实非零 v (n=1 时求和为空, 两个端点项仍分别保留):

`v^T(J_n+2I)v=sum_(j=1)^(n-1)(v_j+v_(j+1))^2+(1-delta)v_1^2+v_n^2>0`,

`v^T(2I-J_n)v=sum_(j=1)^(n-1)(v_j-v_(j+1))^2+(1+delta)v_1^2+v_n^2>0`.

因而所有特征值在 (-2,2). 三对角递推使一个本征向量由第一坐标唯一确定,
第一坐标为零则全向量为零. 对称性保证可对角化, 所以每个特征值简单.
又 B>2,A=B+2, 每个对应 x 在 (0,1), 每个 x 产生两个关于 pi/2 对称的相位根.
在这些根 sin y 非零、cos y 非零, 变量变换导数也非零, 故 Fhat_n 和 F_n
在 (0,pi) 恰有 2n 个简单根. 它们是前 2n 个物理正特征值的相位, 没有遗漏更小的正根.

设 z_n=min spec(J_n). 主子矩阵极小极大原理给出 z_(n+1)<=z_n.
若相等, J_n 的最小本征向量末尾补零便达到 J_(n+1) 的最小 Rayleigh 商,
必为本征向量. 最后一行强迫原末坐标为零, 向前递推使全向量为零, 矛盾.
故 z_(n+1)<z_n. 取 `v_j=(-1)^j/sqrt(n)` 得

`-2<z_n<=-2+(2-delta)/n`, 所以 `z_n downarrow -2`.

最小 x 对应下半相位区间的最大根, 即

`y_n=arccos sqrt((B+z_n)/A) up to phi=arccos((s-1)/(s+1))`.

这里箭头为严格递增收敛. 根配对给出规定配置的实际相邻比值

`c_n(R)=((pi-y_n)/y_n)^2`.

函数 `H(y)=(pi/y-1)^2` 在 (0,pi/2) 的导数
`-2pi(pi/y-1)/y^2<0`, 故

`c_n(R) downarrow c_infinity(R)=((pi-phi)/phi)^2`.

该结论包含每个 n, 不由有限矩阵样本推出. 它只研究规定的平衡候选,
不证明 `c_n(R)=Lambda_n^sup(R)`, 不解决 O1/O2, 也不证明整个全局最优值序列单调.
R=4 的极限约 2.4091685548064623 只是公式的数值展示.

## 验证分层

V1-V4 和 B1-B2 的普遍命题以上述解析论证为依据. 用户附件的 checks.py 包含
精确有限恒等式、反例及有限数值交叉检查. 修正后的实际脚本另外重算受影响方向.
Lean 仅覆盖其精确声明列出的局部接口, 不等同于无限维 Green 极限、所有本征函数的
解析扰动或完整 Jacobi 序列收敛的形式化. 新的无状态隔离审查将检查这些边界及当前卡片.
