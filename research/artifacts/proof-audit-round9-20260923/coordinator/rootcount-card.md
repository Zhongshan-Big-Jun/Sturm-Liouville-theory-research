# 平衡交替配置的归一化世俗函数与 2n 简单根

取整数 n>=1, R>1, s=sqrt(R), t_n=1/((n+1)s+n).
规定配置 `[1,R,1,...,1]` 的轻块宽 s t_n, 重块宽 t_n.
物理状态为 (u,u'), 相位 y=omega s t_n, omega=sqrt(lambda)>0.
物理函数 `F_n=(T_end T_cell^n)_(01)` 与归一化函数
`G_n=Fhat_n=omega F_n` 必须区分.

归一化状态 (u,u'/omega) 的矩阵为

`N_cell=[[C^2-S^2/s,(s+1)SC/s],[-(s+1)SC,C^2-sS^2]]`,
`N_end=[[C,S],[-S,C]]`, C=cos y,S=sin y.

J=diag(1,-1) 给出 `N_cell(pi-y)=J N_cell(y)J`,
`N_end(pi-y)=-J N_end(y)J`. 于是任意 n 有
`Fhat_n(pi-y)=Fhat_n(y)`, 而
`F_n(pi-y)=y F_n(y)/(pi-y)` (0<y<pi).
omega 随 y 改变, 不能冻结. 正比例因子保留内部零点及重数.

行列式为一的 Cayley-Hamilton 递推给出

`Fhat_n(y)=sin y P_n(cos^2 y)`,
`P_0=1`, `P_1=A x-s`, `P_n=(A x-B)P_(n-1)-P_(n-2)`,
`A=(s+1)^2/s`, `B=s+1/s=A-2`.

等价地 `P_n(x)=U_n(z/2)+delta U_(n-1)(z/2)` (n>=1),
`z=A x-B`, delta=1/s. 它是首对角 -delta、其余对角零、次对角一的
实对称 Jacobi 矩阵 J_n 的特征多项式. 末对角 -delta 的历史版本与之倒序相似.
两组平方和给出 `-2I<J_n<2I`; 三对角递推使特征空间一维,
配合对称性得谱简单. 因 B>2,A=B+2, P_n 的 n 个根均在 (0,1),
每个产生两个互补相位, 导数不为零. 所以 Fhat_n 与 F_n 在 (0,pi)
均恰有 2n 个简单根. y=0 的归一化零点不能计入正谱.

完整平方和、边界情形和指标对应见
[本轮证明 B1-B2](../research/artifacts/proof-audit-round9-20260923/analytic-repair.md) 与
[当前固定 n 文稿](../docs/SL_fixed_n_supremum.tex).
历史 `runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md`
Part B 已写 G_n=omega F_n, 其根计数没有被物理函数值错误推翻; 原包不改写.

仅适用规定的平衡交替配置. 不给非平衡根计数或全局最优值.
候选序列的严格单调极限另见 [[bloch-band]], O1/O2 仍开放.
