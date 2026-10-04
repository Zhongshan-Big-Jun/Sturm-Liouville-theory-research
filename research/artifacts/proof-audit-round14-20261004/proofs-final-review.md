# 第十四轮最终独立解析复审

日期: 2026-10-04.
原生审查身份: task_name=/root/r14_final_proof_review; 创建方式 fork_turns=none.
作者 /root 与本审查者不同. 本报告没有构造或冒用旧 UUID, multi_agent_v1 回执或旧审查身份.

最终结论: APPROVE, 仅对下面列明的 v4 精确材料、数学合同和活动数学声明成立.
完整 G2, 条件化的 G2+全部零点 ND 推论, A11 的充要稠密判据、发散侧精确闭包和收敛侧无限余维均通过独立解析复审.
ND 本身、全局 G1、无条件全局唯一性、其它 M3/KP 理论、收敛侧全部元素描述及完整 Lean 形式化均没有因此获证.
自动纠错接收、软件执行、TeX 编译和 PDF 验收不是本报告的批准对象.

## 1. 输入隔离、哈希和修订经过

只读取了协调器授权的冻结 proofs、proofs-v2、proofs-v4 包中 hashes.json 及其列明的同一 11 个相对路径. 未读取 proofs-v3, 项目工作区、项目记忆、技能、作者会话、其它审查结果或本轮项目报告.
另外只通过 web 定点读取了下文列明的经典引理 primary author sources. 没有修改作者源或冻结材料.

原 proofs 11 项实际 SHA256 与清单全部一致.
proofs-v2 11 项实际 SHA256 与清单全部一致.
最终 proofs-v4 11 项实际 SHA256 与清单全部一致.
最终清单自身 SHA256:

    08160df3cf09d1eaadd64160e2adcc14bb93d99839c634efcd74710eb4f0bf3d

最终输入根目录:

    F:/tools/math-audit-round14-20261004/final-review/proofs-v4/

| 最终相对路径 | 实际 SHA256 |
| --- | --- |
| docs/SL_G2_compactness_proof.md | 3e81f40a67467269e2f75eca653d90cf3d69791c8701da800071ddd3d21186e9 |
| docs/SL_H2_arbitrary_deletion_proof.md | 507f220a264e03b52f61025853db93612ea79365f09eef3c787346811628b686 |
| docs/SL_gap_nge2_symmetry_local_proof.tex | 7ac96d66493039476f67be315d484cb221cde8364484dd80ae3cb7b2fafdb182 |
| docs/SL_spectral_topics_summary.tex | 5e4b93d2343a0e910529d9177abe762e4bf239143e94152ebb8833457d8c3674 |
| docs/SL_cofinite_all_orders.tex | 11dd413cfa17a2ceaa9b2d1544cf1a2d4950f4fcf4a0533a1057cd1b7ca868b9 |
| research_map.md | 4caaa78b67513ce5237311b91e4c541bb44f51ddcd558faf50fe02c3b5991713 |
| tools/band-selfconsistency-equivariance.md | a5692e263359db5cc4f8e8c5b3102fe9169956c63bbef25d046b2324a369695c |
| tools/switch-saturation-k-invariant.md | 9cce46fa6d463b63bce9f2cfed759c69d630ab0a4c2d7aa5c0de9ed8bb134f78 |
| tools/krein-infinite-deletion-subclasses.md | b8c92949857e461fa3b50efc54b5ee9a9418530602353587fb6438e04a890011 |
| literature/absorption-20260923/approximation/notes/04_infinite_deletions.md | 8dd35ebe86e67eb301716869b7d312b87667ba927bd287b1ffc153e872d60fe0 |
| tools/krein-cofinite-closure-all-orders.md | e6a75ede0fa2233a9f016238df701ceb7bcccaf294a26f39cd75d1e8f6a91214 |

本次实际发现并通知协调器的整合问题如下, 不能省略首次问题记录:

1. 原包与 v2 的 band 卡活动 scope 仍称 Current round12; A11 卡活动 scope 仍明确限于两类删项, 与新增任意保留集定理冲突. 这些不是两个数学证明的缺陷.
2. 原包综述第 923-938 行已经有完整 A11 节; v2 又在文末新增同题节. 逐文件 diff 确认重复插入, 两处数学陈述本身相符.
3. 协调器随后提供 v4. 本审查者核查 v4 的精确字节, 未对未读取的 v3 或修复中的暂态操作出具验收.

原综述 SHA256 为 b671bd745fa9e3aa4fcbdc041060b2b00007ded7a877ea67fb8d07927b4602f9; v2 为 e14bbba61bac1c40d893ea8738930e3a031fdac237cf6330c481ca8646620620.
原包 band、switch、A11 卡哈希分别为 ecf67a46d8a1377d312be3f29cf68ad24a9a9061360c7d36c207bd4866974685, bd92cef088f2bee65edcdd4ca5132580ba8c8a7e10db3ffadf8267a7203df862, f9734e8c3a8854b8d52f01cf66398692f903595a90f20f0e38e4334261d66c45.
这些旧输入记录不因 v4 批准而被改写为从未发生问题.

## 2. 逐项判定

| 项目 | 判定 | 精确范围 |
| --- | --- | --- |
| G2 原合同 | APPROVE | 每个固定 n>=2, 有限 Rmax>1, 两种图案, 全部 1<=R<=Rmax, 全部内部精确 F=f/b 零点的一致正块宽 |
| F=0 到 K=-2D 及符号相容 | APPROVE | 只使用全部接口精确零点, 不预选带匹配、对称或极值分支 |
| 谱、共同质量归一化模态与端点余项 | APPROVE | 允许零宽极限块与任意多个移动跳点; L1 权收敛, 固定谱阶和 C1 模态收敛 |
| Rolle 排除与全部退化情形 | APPROVE | 左/右端点、内部相撞、同时多块塌缩、R下降到1 |
| G2+全部零点 ND 推论 | APPROVE, CONDITIONAL | 条件成立时根数局部常数, 每图案唯一全局解析反射对称分支; 不批准 ND 本身 |
| A11 充要稠密判据 | APPROVE | 固定 c>0, 真实复 Hc2, 原命名族, 任意 J,Se,So, 含有限/空集 |
| 两侧发散的精确闭包 | APPROVE | 恰为缺失仿射列所对应的中心零迹空间 |
| 任一侧收敛的无限余维 | APPROVE | 构造真实无限维 L2 障碍并通过 Kc inverse 返回 Hc2 |
| 活动 G2 TeX 新增正文 | APPROVE | 第 1018-1098 行的完整 G2 和 ND 条件推论; 历史全局矩阵/扫描不在批准内 |
| v4 综述新增/同步数学正文 | APPROVE | G2 全量词与 ND 条件化; A11 唯一节第 923-938 行 |
| research_map 的 A11/B4/相关关系 | APPROVE | A11 分项 CLOSED/PARTIAL, B4 仍 PARTIAL, ND/无条件唯一仍开放 |
| 三张活动卡当前数学 scope/summary/正文 | APPROVE | v4 的当前数学量词与历史范围分离; 不能把这项批准当作自动纠错接收 |
| 冻结 T 输入 | APPROVE AS SUPPLIED INPUT | 仅 s=2, 删除 p0,p1 的 full-tail 两迹命题; 已核对实际 domain、等距和命名族 |
| 软件、数值守卫实际行为 | INCOMPLETE / OUTSIDE THIS REVIEW | 未读取或运行程序, 不能为卡片中的软件执行断言出具验收 |
| Lean、TeX 编译、PDF 渲染 | INCOMPLETE / NOT PERFORMED | 均未执行; 解析批准不等于形式化或编译验收 |
| 历史全范围结论与历史回执 | INCOMPLETE / OUTSIDE THIS REVIEW | 未重新认证其它阶 A12、历史 Hessian/扫描、外部全盒约化、M3/KP 或旧回执身份 |

## 3. G2 的独立推导

### 3.1. 任意极限正权的简单内部零点

令 a=lambda_n, b=lambda_(n+1), D=b-a>0, u=u_n, v=u_(n+1), 均按 int rho u_k^2=1 和 u_k'(0)>0 定向.
相邻 Dirichlet 模态的零点严格交错:

\[
0<\beta_1<\alpha_1<\cdots<\alpha_{n-1}<\beta_n<1.
\]

这可由 Sturm 严格比较与两个模态的确切结点数得到: u 的每个结点区间至少含一个 v 零点, 一共 n 个区间和 n 个 v 内零点, 因而恰好各一个. 结点均简单, 两模态无公共内部零点.

对 W=v'u-vu', 有 W'=-D rho uv. 在 beta_j, v' 与 u 异号, 所以 W<0; 在 alpha_j, v 与 u' 同号, 所以 W=-vu'<0. 相邻交错结点之间 uv 定号, W 单调且端值均负. 首段从 W(0)=0 下降; 末段上升至 W(1)=0. 因而 W<0 于整个内部.
这里只需正有界权, 允许极限阶梯权删除零宽块, 不需驻点或符号相容.

若 f(t)=au(t)^2-bv(t)^2=0, 则 u(t)不能为0. 对 Q=v/u, Q'=W/u^2<0 且 Q(t)=+/-sqrt(a/b), 所以

\[
f'(t)=-2bu(t)^2Q(t)Q'(t)\ne0.
\]

因此极限切换函数也没有内部双零点. 没有在密度跳点错误要求 C2: u,v 和 f 都是 C1, 足以使用此式及 Rolle.

### 3.2. 精确 F=0 alone 给 K 和完整符号

每个常密度开块内,

\[
K=(u'^2+a\rho u^2)-(v'^2+b\rho v^2)
\]

导数为0. 接口处 u,u',v,v' 连续, 所以跳量为 [K]=[rho]f(x_i)=0. b>0, F_i=f(x_i)/b=0 与 f(x_i)=0 等价. 因而 K 全局为常数.
分部积分和共同质量归一化给 int u'^2=a, int v'^2=b, 且区间长度为1. 故

\[
K=\int_0^1K=2a-2b=-2D.
\]

这个等式没有使用块内符号, 不存在先假定 band-consistency 再证明全 F 零点的循环.

令 A=u'(0)>0, B=v'(0)>0. 得 B^2=A^2+2D, 于是

\[
aA^2-bB^2=-D(A^2+2b)<0,\qquad B/A>1>\sqrt{a/b}.
\]

右端的平方恒等式相同, 端点导数因结点数差一而异号, 故 v'(1)/u'(1)<-1.
在 u 的每个结点区间 Q 严格递减. 中间区间的端值为 +infinity 和 -infinity; 首区间由 B/A 开始, 末区间以右端负比值结束. 每区间恰穿过两个水平 +/-sqrt(a/b). 因此 f 恰有2n个简单内部零点.
全部2n个升序接口占满这些零点, 符号依次为 -, +, -, ..., +, -. 对 SUP/INF 恰得到各自定义的饱和符号. R=1 时图案高度相同, 仍保留形式接口和 F; 无需宣称此时有实际材料开关.

### 3.3. 退化块的正确谱拓扑

任取精确零点序列, 用有限图案和闭参数/闭升序区域的紧性取子列, 使 R_j趋于R_*和 x^(j)趋于x^*. 区间指示函数的对称差测度由移动端点差控制, 因而 rho_j趋于rho_*于L1. 保持 1<=rho_*<=Rmax.

在 H0^1 的能量内积上定义 T_rho. 单位能量球在 C[0,1] 紧, 且

\[
\|T_{\rho_j}-T_{\rho_*}\|
\le \|\rho_j-\rho_*\|_1.
\]

T_rho 是紧正自伴算子, 第k个正特征值为1/lambda_k. 算子范数收敛的 minmax 控制给固定 k 的谱连续性. 不能在这里改用未绑定谱阶的近邻数值根.
a_j,b_j分别趋于a_*,b_*; 极限正权的 Dirichlet 单性给 D_*=b_*-a_*>0. 比较界 lambda_k<=(k pi)^2 保证固定模态参数一致有界.

取各固定谱阶的左射击解初值(0,1). 系数 lambda_(k,j)rho_j 在L1收敛且一致有界. 一阶系统积分方程与 Gronwall 给射击解及其导数的一致收敛.
质量 N_j^2=int rho_j y_j^2 趋于 N_*^2>0, 因而按同一质量约定归一化后的 u_j,v_j 于C1收敛. 故 f_j于C1收敛到f_*.

### 3.4. 端点必须用统一二次首项, 不能只用 C1

由一致有界 ODE 系数, |y_j'|<=C 和 |y_j(t)|<=Ct. 直接使用全区间 Volterra 方程,

\[
y_j(t)=t-\lambda_{k,j}\int_0^t(t-s)\rho_j(s)y_j(s)\,ds
=t+O(t^3),
\]

余项可估为常数乘 t^3, 与 [0,t] 内的任意移动跳点数和位置无关.
沿紧性子列 N_j 一致远离0, 从而 u_j(t)=A_jt+O(t^3), v_j(t)=B_jt+O(t^3).
若某接口 t_j趋于0, 精确 f_j(t_j)=0 给

\[
0=\frac{f_j(t_j)}{t_j^2}
=-D_j(A_j^2+2b_j)+O(t_j^2)
\longrightarrow-D_*(A_*^2+2b_*)<0,
\]

矛盾. 这避免了把 f_*'(0)=0 这个 Dirichlet 自动条件误当成排除证据.
反射任意密度得到右端完全相同的平方和质量论证; 不要求原配置对称.

### 3.5. 内部相撞和所有塌缩模式

若相邻接口趋于同一个 t在(0,1), 两处 f_j=0, Rolle 给其中间一点 xi_j满足f_j'=0. C1收敛给 f_*(t)=f_*'(t)=0, 与3.1矛盾.
最小块宽若趋于0, 可以先固定发生塌缩的块指标再取子列. 外端块由3.4排除; 内块的共同极限若为端点也由3.4排除, 否则由 Rolle 排除. 即使多个块同时塌缩, 至少一个固定块仍给同一矛盾. R_*=1 没有例外.
对两种图案取各自下界的较小者, 得完整 G2.

该结果只说内部精确零点族没有边界聚点. 全部形式接口设为0时, F_i可由 Dirichlet端值成为0, 这是闭单纯形的形式边界零点. 本证明不排除也不否认它.

### 3.6. ND 条件推论

在每个[1,Rmax], G2把全部根置于固定 K_eta紧包含于U. F在内部由有限转移矩阵、简单射击谱根和正质量积分给实解析性.
若全部R>1的精确根 D_xF非退化, 加上常密度 R=1 的对角非退化 Jacobian, 每个纤维的根孤立且闭紧, 因而有限.
隐函数定理逐根延拓; 若附近还存在这些延拓以外的根, 紧性子列必趋于原纤维的某个根, 与其局部唯一性矛盾. 空纤维也由同一紧性论证在邻域保持为空.
故根数在[1,Rmax]相对拓扑中局部常数. R=1 的2n个升序接口必须取遍常密度f的2n个简单内零点, 根数为1. 连通性推出根数恒1.
不同 Rmax 上的唯一解析支相容, 形成全局支; 反射等变与唯一性给对称. 行列式连续不为0, 所以继承 R=1 的(-1)^n符号.
这是以全部精确零点的 ND 为前提的推论, 不证明 ND, 也不由一条对称样本支推出它.

## 4. A11 的独立推导

### 4.1. 实际 Kc、命名族和 T 输入核对

采用复 L2(-1,1), 内积第一变量线性,

\[
K_cf=-f''+cf,\quad
D(K_c)=\{f\in H_{\rm Sob}^2:f'(1)=f'(-1)=(f(1)-f(-1))/2\},\quad c>0.
\]

冻结 cofinite TeX 第32-102行与第108-169行的实际定义和论证均与A11一致.
分部积分为

\[
\langle K_cf,f\rangle
=\|f'\|_2^2-\tfrac12|f(1)-f(-1)|^2+c\|f\|_2^2
\ge c\|f\|_2^2.
\]

边界形式为0. 齐次修正的2乘2边界矩阵行列式为
2 sqrt(c) sinh(sqrt(c)) [sqrt(c) cosh(sqrt(c))-sinh(sqrt(c))]>0.
因此可对每个L2右端解边值方程; 正性、满射和对称性给正自伴性.
Hc2采用范数||K_cf||2, 所以 Kc:Hc2到L2 是等距满射, 不是未经核对的代数多项式逆.
||f||_(Hsob2)<=C_c||K_cf||2 也给中心两迹连续.

p0=1、p1=x 都满足边界条件. 偶高列导数在两端均为0; 奇高列的两端导数及半端值差均为 -1/(m-1). 因此所有m>=2的命名列实际在domain中.
冻结 cofinite TeX 的定理1取 s=2, N={4,5,...}, I(2)={0,1}, 恰给

\[
T:\quad \overline{\operatorname{span}\{p_{2m},p_{2m+1}:m\ge2\}}^{H_c^2}
=V_*=\ker f(0)\cap\ker f'(0).
\]

本审查按授权将这个已证T作为精确输入; 不因其状态标签而认证其它阶数.
反射保持实际domain, 与Kc交换, 所以奇偶投影在Hc2连续且正交. 对T投影分别得到完整偶尾和奇尾的精确闭包.

### 4.2. 真实向量的 Mellin 函数和系数

对实际 Hc2 正交向量 g 的所需奇偶部, 令 w=Kcg, h=w restricted to(0,1).
h属于L2也属于L1. 定义 M(z)=int_0^1 h(t)t^z dt.
Cauchy-Schwarz对 t^z(log t)^k 的控制给 Re z>-1/2 的解析性; 在 Re z>=0, |M(z)|<=||h||1, 且沿实轴 z下降到0连续.
因为Kcp是实系数多项式, 第一变量线性的正交式为 int w Kcp=0; 半区间仅少一个非零因子2, 没有丢失共轭约定或奇部换元 Jacobian.

直接微分得到

\[
K_cp_{2m}=ct^{2m}
-\left[2m(2m-1)+\frac{cm}{m-1}\right]t^{2m-2}
+2m(2m-3)t^{2m-4},
\]
\[
K_cp_{2m+1}=ct^{2m+1}
-\left[2m(2m+1)+\frac{cm}{m-1}\right]t^{2m-1}
+2m(2m-1)t^{2m-3}.
\]

令z=2m-4. 原稿E式分别给三系数
c(2m-2), -2m[(2m-2)(2m-1)+c], (2m-2)2m(2m-3).
原稿O式分别给
c(2m-2), -2m[(2m-2)(2m+1)+c], (2m-2)2m(2m-1).
故E1及奇式恰为(2m-2) int h Kcp. 这些是在所有z上由真实函数定义的解析恒等式, 正交性最初只在所选m成立.

### 4.3. 三次归一化、Blaschke与m=2

E、O的多项式系数次数最多3. 在Re z>0, 每个固定a>=0的|z+a|/|z+1|有统一上界, |z+1|>=1. 因而

\[
\Phi_e=H_e/(z+1)^3,\qquad \Phi_o=H_o/(z+1)^3
\]

是有界解析函数, 不是仅在正实轴有界的形式表达式.

对发散的一侧, 舍去m=2后, 其互异零点t=2m-4趋于无穷, sum 1/t发散.
半平面映射z到(z-1)/(z+1)给1-|zeta|=2/(t+1), 违反任何非零有界圆盘解析函数的Blaschke条件.
该条件由Jensen公式先除去原点有限阶零点, 再令r趋于1得到; 原稿所给证明完整.
因此对应H恒零, E1/O给所有m>=3的完整尾正交性.
m=2没有被漏掉: M在0及非负平移连续, 所以 z下降到0给该列的正交式.
特别地, 偶m=2式为2cM4-(24+4c)M2+8M0=0, 奇m=2式为2cM5-(40+4c)M3+24M1=0, 均为正确实际列的两倍正交式.

没有假定被删除指标也满足离散递推. 新等式由实际L2向量的有界解析唯一性产生.
因此所选发散偶尾/奇尾与完整偶尾/奇尾具有相同正交补. 结合T, 两侧均发散时高尾闭包恰为V_*.

### 4.4. 仿射列与发散侧精确闭包

所有高列的中心值和一阶导数为0. p0,p1的中心迹为(1,0),(0,1).
V_*闭, 添加有限维保留仿射空间后仍闭, 且任意目标可减去其中心值倍p0、中心导数倍p1落入V_*.
故两侧发散时的完整闭包恰为

\[
\{f\in H_c^2:
0\notin J\Rightarrow f(0)=0,\ 
1\notin J\Rightarrow f'(0)=0\}.
\]

这没有把扩大单项式空间的稠密性倒推为差分族稠密.
缺失的仿射迹方向不能由高尾恢复, 因而发散情况下全空间稠密当且仅当J={0,1}.

### 4.5. 收敛侧的 Cauchy Gram 距离和真实障碍

收敛的一侧构造去重整数指数集E: 偶侧为{0}及各{2m,2m-2,2m-4}, 奇侧为{1}及各{2m+1,2m-1,2m-3}.
只加入仿射指数而不管是否保留, 是合法的空间扩大.
大m时每个1/(alpha+1)由常数乘1/m控制, 所以 sum_(alpha in E)1/(alpha+1)<infinity.

有限指数Gram矩阵为G_ij=1/(alpha_i+alpha_j+1).
Cauchy行列式为差的平方乘积除以所有(alpha_i+alpha_j+1)乘积.
追加t^q后取Schur行列式之比, 原指数间因子消去, 正好得到

\[
\operatorname{dist}^2(t^q,\operatorname{span}\{t^{\alpha_j}\})
=\frac1{2q+1}\prod_j\left(\frac{q-\alpha_j}{q+\alpha_j+1}\right)^2.
\]

q=1/2不在整数E. 对大alpha, 因子绝对值为1-2/(alpha+3/2); 缺量之和有限, 无限乘积严格正, 有限前缀没有零因子.
穷尽E的有限集合后距离极限是到闭包W_E的距离, 因而W_E proper.
取非零h在W_E正交补, 按偶/奇延拓 w=h(|x|)/sqrt2 或 sgn(x)h(|x|)/sqrt2. 所选Kcp都是E单项式的有限组合; 另一奇偶支自动正交.
Kc inverse给非零g属于真实Hc2, 与全部保留列正交. 这是实际函数空间障碍, 不是未经实现的形式矩序列.

### 4.6. 无限余维, 包括有限/空保留集

若W_E的余维有限, 所有整数单项式稠密性的商像在有限维商中张满; 可选有限个整数单项式补满商.
这使W_E加这些有限列等于整个L2. 但给E加有限整数仍保持上述倒数和收敛, 相同Gram距离式仍说明扩大的闭包proper, 矛盾.
故W_E正交补无限维. 延拓与Kc inverse均单射, 将其送入Y_N正交补. 因而只要任一侧收敛, codim Y_N=infinity, 与J是否保留无关.
有限和空S也被同一证明覆盖.

由4.3-4.6, A11定理的全部量词和更细结论成立. 未给收敛侧闭包的全部空间元素描述, 没有扩展到其它阶、非对角约束空间、稳定基或误差率.

## 5. v4 活动整合的实际核查

1. G2 TeX 第1024-1029行保留固定每个n、有限每个Rmax、两图案、全部R>=1及全部内部精确F零点的原量词. 第1039-1051行只由F=0推K及符号; 第1053-1080行覆盖谱紧性、移动跳点端点余项和Rolle. 第1083-1098行仍明确以全部根ND为条件, 并排除外部全盒/M3/KP重新认证. APPROVE.
2. 综述第66-71及第802-820行把旧G2登记与当前完整证明分开. 第923-938行陈述A11的全部J,Se,So判据、发散侧闭包、任一收敛侧无限余维和开放范围. APPROVE.
3. 实际文本检查: v4中A11同题section仅1个, sec:a11round14 label仅1个. v4与原包综述的thebibliography块文本及换行完全相同; git diff --no-index仅显示新增label和将收敛侧一句改为无限维障碍/有限维商. 该命令退出1表示确有差异, 不是编译失败. 误加重复节已移除.
4. 地图A11分别标注判据/发散闭包CLOSED与收敛全部描述PARTIAL; B4仍PARTIAL并明确ND/无条件全局唯一开放. 关系条目只扩展真实Hc2的A11, 未将一般A4或其它阶接连标SOLVED. APPROVE. 地图顶端Last updated仍为2026-09-27, 是可后续同步的导航日期, 不影响本次数学判定.
5. band与switch卡的v4活动scope、summary和第4-27行同数学全文一致. 卡片 explicitly 保留旧范围, 不用新G2认证旧Hessian/扫描, 不宣称数值守卫是区间证明. APPROVE数学声明. 其软件实际行为仍为本审查未执行项.
6. A11卡scope、summary、title/updated已与任意保留集合同一致. 旧review_status明确移为historical_review_status且限定旧两子类; 当前review_status不继承旧APPROVED, 说明当前精确字节须本轮原生独立证据. APPROVE这种范围分离, 不对未读取的旧回执/旧卡哈希真实性再认证.
7. 从原包到v4, band卡第十二轮标题开始的历史尾、switch卡旧正文标题开始的历史尾、A11卡For arithmetic progressions开始的历史尾均实际逐文本/换行比较一致. 原note04与cofinite输入的完整哈希不变. 历史数学输入没有被新定理标签覆盖.

## 6. 经典来源定点核查和限制

实际读取 [Liehr作者预印本v1的第2节Lemma2.1及半平面映射](https://arxiv.org/html/2409.17563v1). 该处确实陈述非零有界圆盘解析函数的Blaschke条件, 与本证明用法一致.
实际读取 [arXiv作者元数据](https://arxiv.org/abs/2409.17563), journal reference及相关DOI与文稿所列相符. DOI跳转的出版社页面读取失败, 没有声称读取期刊全文.

实际读取 [Erdelyi-Johnson作者稿](https://people.tamu.edu/~terdelyi/papers-online/bill.pdf) Theorem1.3, PDF第3页: distinct real exponents greater than -1/p, 对[0,1]等具有正下密度的紧集给相应Lp稠密性判据. 它只用作单项式必要性对照; A11的收敛侧由本文独立的Cauchy距离式证明, 发散侧由实际Mellin唯一性加T证明.
没有使用Gaussian平移定理, 没有从文献摘要猜测原Krein差分族定理, 没有进行首创性判定.

实际执行仅为冻结文件读取、SHA256核对、受限文件diff和文本完整性比较. 未运行任何项目Python、数值实验、SymPy、Lean、TeX编译或PDF渲染.
历史程序资源和自动纠错接收器未读取/执行. 本报告的解析APPROVE不能代替这些门禁或验收.

最终无剩余需要修改的数学项. 两个首次活动整合问题在v4精确材料中已经关闭. 本批准只绑定第1节所列最终SHA256, 并受第2节与本节明确范围限制.

