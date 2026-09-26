# 第十二轮解析修订稿: 镜像扇区、归一化 Green 公式与半问题谱指标

日期: 2026-09-26. 身份: 解析作者. 本文提供重新推导的证明及条件, 供之后的新无状态检验使用. 本文自身不构成独立检验记录.

## 0. 任务契约与阅读约定

仓库 /mnt/f/LaTeX/BVE research 及安装插件只读. 本次产物全部位于 /mnt/f/tools/math-audit-round12-20260926/analytic-author/. 两份输入附件是待核实线索, 其数值、历史评价及状态标签不作为证明前提. 读集的完整文件 SHA256、实际阅读范围和路径差异见 assumptions.json; 修改清单和方法边界见 author-note.md.

本文证明的三个命题是:

1. 任意实或复 $2n\times2n$ 矩阵的镜像压缩在交错共轭下交换. 代数恒等式不要求反射对称; 不变子空间分块需要另加对易条件.
2. 对每个固定有限 $R>1$, 每个满足下文条件的 $n=2$ 对称五层带自洽配置, 从形状导数与加权归一化独立推出原 $K$、$K_p=SKS$、交叉 Green 式和原 $K_o$ 的约化 Green 加秩一式. 这是条件化的全参数恒等式, 不包含各 $R$ 上配置存在、唯一、连续延拓或矩阵定号的结论.
3. 对任意有限正分块密度, DD/DN 的第 $j$ 个频率分别由提升相位 $j\pi$、$(j-\tfrac12)\pi$ 唯一确定, 并有逐指标比较括号. 精确实数算法的身份结论与浮点执行的可靠性分开陈述.

所有谱指标从 1 开始. 全问题在 $(0,1)$, 左半问题在 $(0,L)$, $L=1/2$. 半问题记号 D 表示 DD, N 表示 DN, 即左端始终为 Dirichlet. 核的分母统一为“特征值减谱参数”. 本文不讨论 cofinite、其它第十一轮结果、M3/KP 历史结论或全局 G1'.

## 1. 不依赖谱问题的扇区交换

设 $n\ge1$, $Pe_j=e_{2n+1-j}$, 并定义

$$
S=\operatorname{diag}(s^0_1,\ldots,s^0_{2n}),\qquad
s^0_j=(-1)^{j+1},\qquad
E=\operatorname{diag}(s^0_1,\ldots,s^0_n).
$$

这里 $s^0_j$ 是纯符号, 与后文的密度跳量 $s_j$ 不同. 取列正交基

$$
B_e^{(j)}=\frac{e_j+e_{2n+1-j}}{\sqrt2},\qquad
B_o^{(j)}=\frac{e_j-e_{2n+1-j}}{\sqrt2},\quad 1\le j\le n.
$$

于是 $PB_e=B_e$, $PB_o=-B_o$, 且 $T=(B_e\ B_o)$ 为正交矩阵. 由于 $s^0_{2n+1-j}=-s^0_j$, 逐列直接得到

$$
SB_o=B_eE,\qquad SB_e=B_oE,\qquad PS=-SP. \tag{1.1}
$$

对任意 $K\in\mathbb R^{2n\times2n}$, 定义压缩
$K_e=B_e^TKB_e$、$K_o=B_o^TKB_o$ 及 $K_p=SKS$. 只把 (1.1) 代入乘积, 即得

$$
\boxed{B_o^TK_pB_o=E K_eE,\qquad B_e^TK_pB_e=E K_oE.} \tag{1.2}
$$

这既不要求 $K^T=K$, 也不要求 $KP=PK$. 同一乘法证明也适用于复矩阵 $K$; 后面的谱问题取实特征函数. 混合块同时满足

$$
B_e^TK_pB_o=E(B_o^TKB_e)E,\quad
B_o^TK_pB_e=E(B_e^TKB_o)E. \tag{1.3}
$$

必须另外区分以下两个层次:

- 对任意 $K$, (1.2) 是两个压缩矩阵的恒等式. 此时不能默认偶、奇空间均为 $K$ 的不变子空间.
- $KP=PK$ 当且仅当 $T^TKT$ 的两个混合块都为零. 证明是将 $P$ 写为 $T\operatorname{diag}(I,-I)T^T$, 直接比较乘积. 这时才有真正的块对角分解, 且 $\det K=\det K_e\det K_o$.

若再有 $K^T=K$, 正交合同 $K_p=S^TKS$ 保持全矩阵惯性. (1.2) 说明保持的是交换后的扇区惯性, 不是同名扇区逐一不变. 例如纯代数取 $K=P$, 则 $K_e=I$、$K_o=-I$、$K_p=-P$, 因而 $B_o^TK_pB_o=I\ne K_o$. 这个例子只否定错误的矩阵推理, 不声称它由实际 Sturm--Liouville 配置产生.

## 2. DD/DN 的提升相位与每阶身份

### 2.1 谱问题和正坐标缩放

先允许一般 $L>0$. 设 $(0,L)$ 被有限个正长度区间分割, 各块密度 $r_\nu>0$. 记 $0<m=\min r_\nu\le\rho\le M=\max r_\nu<\infty$. 求解

$$
-y''=\omega^2\rho y,\qquad y(0,\omega)=0,\quad y'(0,\omega)=1. \tag{2.1}
$$

在接口匹配 $y,y'$. 对 $\omega>0$, 两者不同时为零. 特征频率满足 D: $y(L)=0$, 或 N: $y'(L)=0$. 两类均无零或负特征值: 乘方程以 $y$ 并积分得 $\int|y'|^2=\mu\int\rho y^2$, 边界项为零; $\mu=0$ 只允许零特征函数.

对 $c>0$, 定义 $F_c:\mathbb R\to\mathbb R$ 为

$$
F_c(0)=0,\quad F_c(t+\pi)=F_c(t)+\pi,\quad
F_c(t)=\operatorname{Arg}_{[0,\pi]}(\cos t+i c\sin t),\quad 0\le t\le\pi.
$$

这是将角坐标对中的正弦坐标乘正数 $c$ 后的连续提升, 不把各次角度折回主值. 直接求导得

$$
F_c'(t)=\frac{c}{\cos^2t+c^2\sin^2t}>0. \tag{2.2}
$$

因此 $F_c$ 严格递增, 并且对于一切整数 $k$,

$$
\boxed{F_c(k\pi)=k\pi,\qquad
F_c((k+\tfrac12)\pi)=(k+\tfrac12)\pi.} \tag{2.3}
$$

正缩放保持坐标轴方向及累计转数. 不能只证明整数点而遗漏 DN 所需的半整数点. 此外 $F_c\circ F_d=F_{cd}$, 由正坐标缩放的复合以及零点处相同的提升规范可得.

### 2.2 块内旋转、接口转换与严格单调性

用角坐标 $\arg(y'+i\omega\sqrt{r_\nu}y)$. 一块内若 $k=\omega\sqrt{r_\nu}$, 则状态 $(ky,y')$ 满足 $(ky)'=k y'$、$(y')'=-k(ky)$. 故其提升角在长度 $\ell_\nu$ 上恰增加 $\omega\sqrt{r_\nu}\ell_\nu$. 进入下一块时物理状态连续, 第一坐标乘 $\sqrt{r_{\nu+1}/r_\nu}$, 故角先作 $F_{\sqrt{r_{\nu+1}/r_\nu}}$ 转换, 再加下一块的旋转量.

从角 0 开始的这个递推定义终端提升相位 $\Psi(L,\omega)$. 它与末块坐标中的实际解的连续角相同. 接口比值独立于 $\omega$; 每个 $F_c$ 的导数正, 每段增加量对 $\omega$ 的导数也正. 递推求导立即证明

$$
\partial_\omega\Psi(L,\omega)>0\quad(\omega>0). \tag{2.4}
$$

为给出比较界, 另用不随密度改变的参考角

$$
\theta(x,\omega)=\arg(y'(x,\omega)+i\omega y(x,\omega)),\quad\theta(0,\omega)=0.
$$

直接代入 (2.1) 得

$$
\theta_x=\omega(\cos^2\theta+\rho(x)\sin^2\theta)>0. \tag{2.5}
$$

这个角在接口连续, 且终点有

$$
\Psi(L,\omega)=F_{\sqrt{r_{\rm last}}}(\theta(L,\omega)). \tag{2.6}
$$

作为另一个单调性证明, $q=\partial_\omega\theta$ 满足

$$
q_x=2\omega(\rho-1)\sin\theta\cos\theta\,q
      +(\cos^2\theta+\rho\sin^2\theta),\qquad q(0)=0.
$$

积分因子公式使 $q(x)>0$ 对 $x>0$ 成立. 有限分块允许逐块求导和连续匹配. 又由 (2.5), $\theta(L,\omega)\ge\omega L\min(1,m)$, 而 $F_c(t)-t$ 有界, 所以 $\Psi(L,\omega)\to\infty$. 当 $\omega\downarrow0$ 时 $\Psi\to0$. 这里把 $\omega=0$ 的相位定义为连续极限 0; 它不是 D 的“第零个特征值”.

### 2.3 每阶唯一性及交错

令

$$
\kappa_j^D=j\pi,\qquad \kappa_j^N=(j-\tfrac12)\pi,\qquad j=1,2,\ldots.
$$

由连续性、(2.4) 和相位取值范围, 每个正目标 $\kappa_j^{\rm bc}$ 恰有一个正频率原像. 根据坐标定义和 (2.3), D 边界条件恰等于相位为正整数倍 $\pi$, N 边界条件恰等于相位为正半整数倍 $\pi$. 所有特征函数均为 (2.1) 的非零倍数, 因为左端 D 条件只留下初始斜率这一维自由度. 因而没有额外的未被相位列出的正特征值.

由于相位严格递增, 第 $j$ 个目标的频率正好是按大小排序的第 $j$ 个频率:

$$
\boxed{\Psi(L,\omega_j^D)=j\pi,\qquad
\Psi(L,\omega_j^N)=(j-\tfrac12)\pi.} \tag{2.7}
$$

特别地,

$$
0<\mu_1^N<\mu_1^D<\mu_2^N<\mu_2^D<\cdots,\qquad
\mu_j^{\rm bc}=(\omega_j^{\rm bc})^2. \tag{2.8}
$$

这是每一个 $j\ge1$ 的身份定理, 不依赖先扫描到前 $j-1$ 个根. 空间上的 (2.5) 也说明 D 第 $j$ 个模态在 $(0,L)$ 有 $j-1$ 个零点, N 第 $j$ 个模态同样有 $j-1$ 个零点; 在整数轴处的穿越方向为正.

### 2.4 比较括号

在相同 $\omega$ 下, (2.5) 的右端随密度单调增加. 标量初值问题的比较给出

$$
\theta_m(L,\omega)\le\theta_\rho(L,\omega)\le\theta_M(L,\omega). \tag{2.9}
$$

具体可将两解的差写成 $\dot d=A(x)d+B(x)$, 其中对较大密度的比较 $B\ge0$, 再用积分因子; 系数在有限分块上有界. 无需假定右端关于角本身单调.

常密度 $r$ 的块坐标相位是 $\omega L\sqrt r$. 在 $\omega=\kappa_j^{\rm bc}/(L\sqrt r)$ 处, (2.3) 表明参考角也恰为 $\kappa_j^{\rm bc}$. 把 $r=M,m$ 分别代入 (2.9), 再用 (2.6) 的严格递增和固定目标性质, 得

$$
\boxed{\frac{\kappa_j^{\rm bc}}{L\sqrt M}
\le\omega_j^{\rm bc}\le
\frac{\kappa_j^{\rm bc}}{L\sqrt m}.} \tag{2.10}
$$

端点可取等号; 常密度时括号退化为一个精确值. 特征值括号是 (2.10) 两端的平方.

精确实数算法据此对每个指定目标独立二分: 若中点相位小于目标则更新左端, 大于目标则更新右端, 等于目标则已找到该频率. 端点相位不等式始终保留, 区间长度每步减半. 唯一性证明保证极限的边界类型及谱指标. 增大输出数量不会改变已定义的前缀.

### 2.5 全区间对称谱与半区间谱

若 $\rho(1-x)=\rho(x)$, 每个全区间 D 特征值简单: 两个左端为零的解初始斜率成比例. 反射把特征函数映为同一一维特征空间, 反射两次为恒等, 故反射因子是 $+1$ 或 $-1$.

偶函数在 $L=1/2$ 处导数为零, 奇函数在该处值为零. 反之, 任意半区间 N/D 特征函数可偶/奇延拓, 在中点均保持函数和一阶导数连续, 因而给出全问题特征函数. 所有全问题谱因此恰为两类半问题谱的并集. 两类不可能有共同特征值, 否则同一个左端射击解在右端值和导数同时为零. 结合 (2.8), 对一切 $j\ge1$,

$$
\boxed{\lambda_{2j-1}=\mu_j^N,\qquad\lambda_{2j}=\mu_j^D.} \tag{2.11}
$$

故 $u_k(1-x)=(-1)^{k-1}u_k(x)$. 特别地 $a=\lambda_2=\mu_1^D$, $b=\lambda_3=\mu_2^N$; $a$ 不在 N 谱中, $b$ 不在 D 谱中. 后文交叉 Green 核由此没有极点.

## 3. 五层模型、完整归一化与接口符号

### 3.1 开参数域和归一化

固定有限 $R>1$, 令 $\eta=R-1>0$. 全接口坐标为

$$
X=(x_1,x_2,x_3,x_4),\qquad 0<x_1<x_2<x_3<x_4<1.
$$

密度的五个固定高度取下表之一. 这里 SUP/INF 是候选图案名称, 不是最优性结论.

| 图案 | 五块高度 | $\sigma$ | 跳量 $s_i=\rho(x_i+)-\rho(x_i-)$ |
|---|---|---|---|
| SUP | $1,R,1,R,1$ | $+1$ | $\sigma\eta(-1)^{i+1}$ |
| INF | $R,1,R,1,R$ | $-1$ | $\sigma\eta(-1)^{i+1}$ |

积分不依赖有限个接口上的密度取值. 特征函数及其一阶导数在接口连续. 全特征函数取实值并固定

$$
-u_k''=\lambda_k\rho_Xu_k,\quad u_k(0)=u_k(1)=0,\quad
\int_0^1\rho_Xu_ku_l=\delta_{kl},\quad u_k'(0)>0. \tag{3.1}
$$

这里的单位归一化针对特征函数, 没有另加密度总质量约束. 若增加这种约束, 驻点方程及受限 Hessian 须另外推导.

令 $u=u_2$, $v=u_3$, $a=\lambda_2$, $b=\lambda_3$, $\Delta=b-a>0$, $c=\sqrt{a/b}>0$, 并定义

$$
f(t;X)=a u(t)^2-b v(t)^2,\quad F_i(X)=f(x_i;X)/b,\quad
J_{ij}=\partial_{x_j}F_i. \tag{3.2}
$$

本文的带自洽条件是 $F_i=0$ 对全部四个接口成立. 本文只在另有

$$
x_4=1-x_1,\quad x_3=1-x_2,\quad 0<x_1<x_2<1/2 \tag{3.3}
$$

时使用半区间及镜像 Green 公式. 即使在 (3.3) 处求导, $J$ 仍是四个独立接口坐标的 Jacobian, 不是先限制到两个镜像参数再求导.

由分块传递可精确规定 (3.1) 的归一化: 在密度 $r$、长度 $\ell$ 的块上, 若起点状态为 $(A,B)=(y,y')$, $k=\sqrt{\lambda r}>0$, 则 $y(t)=A\cos(kt)+(B/k)\sin(kt)$, 并且

$$
\int_0^\ell r y(t)^2dt
=r\left[A^2\left(\frac\ell2+\frac{\sin2k\ell}{4k}\right)
+\frac{AB}{k^2}\sin^2(k\ell)
+\frac{B^2}{k^2}\left(\frac\ell2-\frac{\sin2k\ell}{4k}\right)\right]. \tag{3.4}
$$

从 $y(0)=0,y'(0)=1$ 逐块传播, 将五个积分求和为 $N$, 取 $u_k=y/\sqrt N$. 半问题则只对三个半块积分. 在对称点, 相应半问题单位归一化特征函数为全函数限制的 $\sqrt2$ 倍:

$$
\phi_j=\sqrt2\,u_{2j}|_{[0,L]},\qquad
\psi_j=\sqrt2\,u_{2j-1}|_{[0,L]}. \tag{3.5}
$$

这里 $\int_0^L\rho\phi_i\phi_j=\int_0^L\rho\psi_i\psi_j=\delta_{ij}$. 交叉两类不要求相互正交.

### 3.2 在本模型内证明交错符号和 $W<0$

由 (2.11) 及空间相位, $u>0$ 于 $(0,L)$, $u(L)=0$, $u'(L)<0$. $v$ 在左半区间只有一个零点 $z$: 在 $(0,z)$ 正, 在 $(z,L]$ 负, 且 $v'(L)=0$. 这些符号使用了 $u'(0),v'(0)>0$.

定义连续 Wronskian

$$
W=v'u-vu',\qquad W'=(a-b)\rho uv=-\Delta\rho uv. \tag{3.6}
$$

在 $(0,z)$, $W$ 从 $W(0)=0$ 严格下降, 故为负. 在 $(z,L)$ 它严格上升, 但 $W(L)=-v(L)u'(L)<0$, 所以仍为负. 接口不改变 $W$ 的连续性. 反射奇偶性还给出 $W(1-t)=W(t)$, 因而整个 $(0,1)$ 上 $W<0$.

在 $(0,L)$, 比值 $h=v/u$ 满足 $h'=W/u^2<0$. 两个不同左接口均满足 $|h|=c$. 严格递减排除它们同取 $+c$ 或同取 $-c$, 也排除先 $-c$ 后 $+c$. 因而必为 $v(x_1)=c u(x_1)$、$v(x_2)=-c u(x_2)$. 再反射到右半, 得到完整四接口恒等式

$$
\boxed{v(x_i)=\varepsilon_i c u(x_i),\qquad
\varepsilon_i=(-1)^{i+1},\quad i=1,2,3,4.} \tag{3.7}
$$

所有 $u(x_i)\ne0$. 这在本次 $n=2$ 假设下已直接证明, 不使用历史“全指标符号交错”作为输入. 若改变归一化方向使 $v\mapsto-v$, 则 $W,\varepsilon$ 同时变号; 本文固定 (3.1) 来消除歧义.

接口处的空间导数为

$$
f'(x_i)=2a u_i u_i'-2b v_i v_i'
=-2b\varepsilon_i c W(x_i). \tag{3.8}
$$

从而四个接口零点均为简单零点. 定义

$$
d_i=\frac{f'(x_i)}{b s_i}
=-\frac{2\sigma cW(x_i)}\eta
=\sigma\frac{2c|W(x_i)|}\eta. \tag{3.9}
$$

所以 SUP 的每个 $d_i>0$, INF 的每个 $d_i<0$. 这是对角项的符号, 不是整个矩阵定号. 又 $d_{5-i}=d_i$.

## 4. 从移动接口推导归一化一阶与二阶变分

### 4.1 可微性的来源和简单根

移动跳点不构成 $L^\infty$ 中的可微密度曲线. 这里使用有限块匹配, 而非未经说明地套用有界权扰动定理.

一块的传递矩阵为

$$
T_r(\ell,\lambda)=
\begin{pmatrix}\cos k\ell&\sin k\ell/k\\-k\sin k\ell&\cos k\ell\end{pmatrix},
\qquad k=\sqrt{\lambda r}.
$$

对正块宽及正谱参数解析. 全射击端值、其接口值和 (3.4) 中的范数均由有限次解析运算得到. 特征根为简单根也可不依赖数值: 令 $z=\partial_\lambda y$, 则 $(yz'-y'z)'=-\rho y^2$. 在 D 根处 $y'(L)\partial_\lambda y(L)=\int_0^L\rho y^2>0$; 在 N 根处 $y(L)\partial_\lambda y'(L)=-\int_0^L\rho y^2<0$. 端点剩余的 $y$ 或 $y'$ 非零, 所以相应特征行列式的导数非零. 隐函数定理因此给出每个指定简单特征值在开接口域附近的光滑局部分支. 加权正范数归一化保留这种正则性.

固定空间点处的参数导数在旧接口两侧可按匹配求出. 因原 $y,y'$ 连续, 导数本身连续、属于 $H^1$; 其一阶空间导数可以有跳跃. 这正是下面弱方程允许的情形. 界面处取移动取值的导数时, 两边的链式法则均使用同一个连续 $u_k'(x_i)$.

### 4.2 符号、FH 与不能遗漏的 $1/2$

用 $\partial_i=\partial_{x_i}$ 表示第 $i$ 个接口向右移动. 对连续测试函数 $g$, 直接对分块积分求导:

$$
\partial_i\int_0^1\rho_X(t)g(t)dt=-s_i g(x_i). \tag{4.1}
$$

即分布记号为 $\partial_i\rho=-s_i\delta_{x_i}$. 此符号来自右移后小区间由右高度换成左高度.

取某个全问题单位归一化简单特征对 $(\lambda,w)$, 记 $w_i=w(x_i)$, $z_i=\partial_iw$, $L_\lambda=-\partial_t^2-\lambda\rho$. 由分块方程及匹配微分,

$$
L_\lambda z_i=(\partial_i\lambda)\rho w-\lambda s_iw_i\delta_{x_i}. \tag{4.2}
$$

例如在移动接口处 $[z_i]=0$, $[z_i']=\lambda s_iw_i$; 因此 $-z_i''$ 的 delta 系数正是 $-\lambda s_iw_i$. 这也独立核对了 (4.2) 的符号.

将 (4.2) 与 $w$ 配对并分部积分, 利用同一端点边界条件及归一化, 得

$$
\boxed{\partial_i\lambda=\lambda s_iw_i^2.} \tag{4.3}
$$

归一化的导数则为

$$
0=-s_iw_i^2+2\int_0^1\rho w z_i,\qquad
\int_0^1\rho w z_i=\tfrac12s_iw_i^2. \tag{4.4}
$$

所以不能将 $z_i$ 直接设成与 $w$ 加权正交. 正交的是减去 $(s_iw_i^2/2)w$ 后的分量.

定义全问题约化 Green 核

$$
\widetilde G_k(t,z)=\sum_{l\ne k}
\frac{u_l(t)u_l(z)}{\lambda_l-\lambda_k}. \tag{4.5}
$$

它满足 $L_{\lambda_k}\widetilde G_k(\cdot,z)=\delta_z-\rho u_k u_k(z)$, 同端点条件及加权正交. 其定义和唯一性在第 5 节进一步说明. (4.2)--(4.4) 因此唯一给出

$$
\boxed{\partial_i u_k(t)=
\frac{s_i u_k(x_i)^2}{2}u_k(t)
-\lambda_k s_i u_k(x_i)\widetilde G_k(t,x_i).} \tag{4.6}
$$

这里没有额外的 $\rho(x_i)$ 因子. 在跳点上这样的点值因子还会引入无意义的左右取值歧义.

### 4.3 归一化二阶变分

对 (4.3) 再沿第 $j$ 个接口求导, 同时计入取值点 $x_i$ 的移动, 得

$$
\boxed{\partial_j\partial_i\lambda_k
=2\delta_{ij}\lambda_k s_i u_{k,i}u'_{k,i}
+2\lambda_k s_i s_j u_{k,i}^2u_{k,j}^2
-2\lambda_k^2 s_i s_j u_{k,i}u_{k,j}\widetilde G_k(x_i,x_j).} \tag{4.7}
$$

中间项的两个相同贡献分别来自 $\partial_j\lambda_k$ 和 (4.6) 的归一化分量. 正是 $2u_{k,i}\times(1/2)$ 使第二个贡献留下一个完整系数. 此式在一般开接口域成立, 不要求带自洽或对称.

下面在带自洽点定义 $w_i=a u_i^2=b v_i^2$. 对 $f(x_i;X)$ 求导并用 (4.6) 得

$$
\partial_j f(x_i;X)=\delta_{ij}f'(x_i)+s_j\mathcal M_{ij}, \tag{4.8}
$$

$$
\boxed{\mathcal M_{ij}=
\frac{2w_iw_j\Delta}{ab}
-2a^2u_iu_j\widetilde G_2(x_i,x_j)
+2b^2v_iv_j\widetilde G_3(x_i,x_j).} \tag{4.9}
$$

归一化项的标量化简是

$$
2a u_i^2u_j^2-2b v_i^2v_j^2
=2w_iw_j(1/a-1/b)=\frac{2w_iw_j\Delta}{ab}.
$$

令 $\Sigma=\operatorname{diag}(s_i)=\sigma\eta S$. 因 $F_i=0$, 求导 $f/b$ 中的分母导数项消失, 从而

$$
J=\frac1b\left[\operatorname{diag}(f')+\mathcal M\Sigma\right],\qquad
K:=\Sigma^{-1}J
=\operatorname{diag}(d)+\frac1bS\mathcal M S. \tag{4.10}
$$

最后一步用的是所有跳量绝对值相等. 如果密度高度不再按固定的两值交替, 一般不能将 $\Sigma^{-1}\mathcal M\Sigma$ 换成 $S\mathcal M S$, 也不能沿用这里的 $K$ 对称性断言.

### 4.4 原 $K$、$K_p$ 与谱隙 Hessian

为避免四维和二维记号混淆, 暂定义

$$
\mathbf u=(u(x_i))_{i=1}^4,\quad Q=(u(x_i)^2)_{i=1}^4,\quad
U_4=\operatorname{diag}(\mathbf u),\quad
\Gamma_k=(\widetilde G_k(x_i,x_j))_{i,j=1}^4,\quad
\tau=\frac{2a\Delta}{b^2}.
$$

用 (3.7) 将 (4.9) 代入 (4.10), 每一项独立化简为

$$
\boxed{K=\operatorname{diag}(d)
+\tau(SQ)(SQ)^T
+2a U_4\left(\Gamma_3-\frac ab S\Gamma_2S\right)U_4.} \tag{4.11}
$$

再作交错共轭:

$$
\boxed{K_p=SKS=\operatorname{diag}(d)
+\tau QQ^T
+2a U_4\left(S\Gamma_3S-\frac ab\Gamma_2\right)U_4.} \tag{4.12}
$$

这些矩阵对称, Green 项中的符号由约定 $(\lambda_l-\lambda_k)^{-1}$ 固定.

设谱隙函数 $D(X)=b(X)-a(X)$. 从 (4.3), $\partial_iD=-s_i f(x_i;X)$. 故带自洽点恰为这个开五层家族的驻点, 且由 (4.8) 或相减 (4.7),

$$
\boxed{H:=D_X^2D=-b\Sigma J=-b\eta^2K.} \tag{4.13}
$$

等式 $H=-b\Sigma J$ 在这里使用 $F=0$; 离开驻点还要保留对 $bF$ 求导的项. $K_p$ 的同一关系是在交错变换后的位移坐标下写 Hessian.

对称点处, 反射密度对应接口映射 $X\mapsto\mathbf1-PX$. 谱隙在此变换下不变, 其固定点上的 Hessian 满足 $PHP=H$, 由 (4.13) 得 $KP=PK$. 因而第 1 节的压缩此时才成为两个不变扇区. 也可从 (4.11) 的反射奇偶性直接检查对易. 这里不把残差 Jacobian $J$ 当作对易矩阵.

若仅用左半接口 $Y=(x_1,x_2)$ 参数化对称家族, 则 $X(Y)=(x_1,x_2,1-x_2,1-x_1)$, $D_YX=\sqrt2 B_o$. 所以

$$
H_{\rm sym}=2B_o^THB_o=-2b\eta^2K_o. \tag{4.14}
$$

这个额外的 2 来自未单位化的镜像位移, 不是对完整 Hessian 的统一倍乘. 原 $K_o$ 对应保持物理反射的位移; 原 $K_e$ 对应破坏物理反射的位移.


## 5. 两类半问题 Green 核及原 $K_o$ 的闭式

### 5.1 核的规范、收敛与唯一性

半问题采用 (3.5) 的单位归一化. 在非极点参数处定义

$$
G_D(t,z;\mu)=\sum_{j\ge1}\frac{\phi_j(t)\phi_j(z)}{\mu_j^D-\mu},\qquad
G_N(t,z;\mu)=\sum_{j\ge1}\frac{\psi_j(t)\psi_j(z)}{\mu_j^N-\mu}. \tag{5.1}
$$

在本次自身极点处定义

$$
\widetilde G_D(t,z;a)=\sum_{j\ne1}\frac{\phi_j(t)\phi_j(z)}{\mu_j^D-a},\qquad
\widetilde G_N(t,z;b)=\sum_{j\ne2}\frac{\psi_j(t)\psi_j(z)}{\mu_j^N-b}. \tag{5.2}
$$

这里 D 的极点指标是 1, N 的极点指标是 2. (5.2) 等于从 (5.1) 减去固定归一化本征函数的极点项后取极限, 不是把特征函数也随着取极限的谱参数随意改变.

这些有限点级数的合法性可直接从能量空间说明. 对 D 使用 $H_0^1(0,L)$, 对 N 使用 $\{g\in H^1(0,L):g(0)=0\}$, 能量内积为 $\int g'h'$. 点评价由一维 Cauchy--Schwarz 不等式控制. 嵌入加权 $L^2$ 紧, 权有正上下界, 由正紧自伴逆算子的谱分解, 单位加权特征函数除以特征值平方根构成能量空间正交完备系. 零谱参数的评价表示核分别为

$$
g_0^D(t,z)=\min(t,z)-tz/L,\qquad g_0^N(t,z)=\min(t,z).
$$

故

$$
\sum_j\frac{\phi_j(t)^2}{\mu_j^D}=t-t^2/L,\qquad
\sum_j\frac{\psi_j(t)^2}{\mu_j^N}=t. \tag{5.3}
$$

这个恒等式由评价表示元的能量 Parseval 等式得到, 无需预先假定点值级数收敛. 由 (2.10), 特征值趋于无穷; 对固定谱参数, 除有限项外 $|\mu_j-\mu|\ge\mu_j/2$. 再用 (5.3) 和 Cauchy--Schwarz, 得 (5.1)、(5.2) 的有限点绝对收敛. 全问题 (4.5) 同理. 对固定源点, 级数还在相应能量空间收敛, 因为其能量系数平方和在尾部由常数倍的 (5.3) 控制. 故其连续代表、边界值和弱方程均有意义.

若 $A=-\rho^{-1}\partial_t^2$, 则它的加权空间预解以核表示为

$$
((A-\mu)^{-1}h)(t)=\int_0^L G(t,z;\mu)h(z)\rho(z)dz.
$$

相应微分算子 $L_\mu=-\partial_t^2-\mu\rho(t)$ 满足

$$
L_\mu G(\cdot,z;\mu)=\delta_z. \tag{5.4}
$$

在单位归一化本征函数 $w$ 的极点 $\nu$ 处,

$$
L_\nu\widetilde G(\cdot,z)=\delta_z-\rho(\cdot)w(\cdot)w(z),\qquad
\int_0^L\rho w\widetilde G(\cdot,z)=0. \tag{5.5}
$$

这是分布恒等式, 右侧第一项不带 $\rho(z)$. 任意两满足 (5.5) 及同端点条件的解之差为 $w$ 的倍数, 正交条件使倍数为零, 因而唯一.

为独立核对闭式的符号, 可取 $w$ 之外的第二解 $z_0$, 使 $wz_0'-w'z_0=1$, $z_0(0)=-1/w'(0)$. 设 $I_1(t)=\int_0^t\rho w z_0$, $I_2(t)=\int_0^t\rho w^2$, 并令

$$
B_0(t,z)=\{w(t)z_0(z)-z_0(t)w(z)\}\mathbf1_{t>z}
       -w(t)w(z)I_1(t)+z_0(t)w(z)I_2(t). \tag{5.6}
$$

其一阶导数在 $t=z$ 的跳量为 $-1$. 对其余项直接求导, $I_1',I_2'$ 在一阶导数中的两项抵消, 二阶导数给出 $-\rho w(t)w(z)$ 的源, 因而 $L_\nu B_0=\delta_z-\rho w(t)w(z)$. 左端值为零; 右端 D 的值或 N 的导数因 $I_2(L)=1$ 而为零. 在密度接口处无需额外 $\rho(z)$ 因子, 原解及积分连续.

最后令

$$
P_0(z)=\int_0^L\rho(t)w(t)B_0(t,z)dt,\qquad
\widetilde G(t,z)=B_0(t,z)-w(t)P_0(z). \tag{5.7}
$$

这满足 (5.5), 因而就是谱定义的约化核. 如记 $A_1=\int_0^L\rho w^2I_1$、$A_2=\int_0^L\rho wz_0I_2$, 直接拆开积分可得

$$
P_0(z)=z_0(z)(1-I_2(z))
-w(z)[A_1-A_2+I_1(L)-I_1(z)]. \tag{5.8}
$$

本文重新证明了这个结构, 但未逐式复查 _prims_9 的九个原函数或其全部浮点实现.

同样, 若 $\varphi$ 满足左 D 条件, $\chi$ 满足所选右端条件, $W_0=\varphi\chi'-\varphi'\chi\ne0$, 则非极点核为

$$
G(t,z;\mu)=-\frac{\varphi(t_<)\chi(t_>)}{W_0}. \tag{5.9}
$$

其导数跳量同样是 $-1$. 如果把分母定义成 $\varphi'\chi-\varphi\chi'$, 前面的负号相应消失; 不能只比较源码变量名称而忽略 Wronskian 的方向.

### 5.2 从全区间核压缩到半区间核

下文 $G_D(b),G_N(a),\widetilde G_D(a),\widetilde G_N(b)$ 均表示在左半接口 $(x_1,x_2)$ 上取值形成的 $2\times2$ 矩阵, 使用 (5.1)--(5.2) 的半区间归一化. 设

$$
U=\operatorname{diag}(u(x_1),u(x_2)),\qquad
q=(u(x_1)^2,u(x_2)^2)^T,\qquad E=\operatorname{diag}(1,-1).
$$

这里 $U,q$ 仍由全区间归一化的 $u_2$ 取值, 没有再乘 $\sqrt2$.

若全模态反射为偶, 它的四接口值向量 $g$ 满足 $B_e^Tg=\sqrt2(g(x_1),g(x_2))^T$、$B_o^Tg=0$. 若为奇, 两者交换. 由 (3.5), 非零的这个压缩向量恰为半区间单位模态的接口值. 因而逐项压缩, 并用第 5.1 节收敛性, 得到完整对照:

| 全约化核矩阵 | 偶压缩 $B_e^T(\cdot)B_e$ | 奇压缩 $B_o^T(\cdot)B_o$ |
|---|---|---|
| $\Gamma_2$, 在 $a=\lambda_2$ 去掉全模态 2 | $G_N(a)$ | $\widetilde G_D(a)$ |
| $\Gamma_3$, 在 $b=\lambda_3$ 去掉全模态 3 | $\widetilde G_N(b)$ | $G_D(b)$ |

若仅取核的左上块, 并只求与被去模态相反的奇偶类, 则仍保留全归一化函数值, 故

$$
R_2^\perp=\tfrac12G_N(a),\qquad R_3^\perp=\tfrac12G_D(b). \tag{5.10}
$$

这与上表没有矛盾: 上表的正交镜像投影同时给出两个 $\sqrt2$ 因子, 将 (5.10) 的 $1/2$ 抵消.

另由 $u$ 反射为奇, 有

$$
U_4B_o=B_eU,\qquad U_4B_e=B_oU,\qquad
B_o^TQ=0,\quad B_o^TSQ=\sqrt2 Eq. \tag{5.11}
$$

这里“乘以奇函数值的对角矩阵”本身也交换两个镜像空间, 是判断最终选中哪个 Green 核不可跳过的一步.

### 5.3 交叉 Green 式对应 $K_p$ 的奇块

将 (5.11) 代入 (4.12), 归一化秩一项在奇压缩中消失, 且

$$
B_e^TS\Gamma_3SB_e=E(B_o^T\Gamma_3B_o)E=EG_D(b)E,\qquad
B_e^T\Gamma_2B_e=G_N(a).
$$

因此

$$
\boxed{Z:=B_o^TK_pB_o
=\operatorname{diag}(d_1,d_2)
+2aU\left[EG_D(b)E-\frac abG_N(a)\right]U
=E K_eE.} \tag{5.12}
$$

两个 Green 参数都在另一种边界问题的谱上, 在本边界问题中不是极点. 若用全归一化异奇偶类左限制, 定义 $M_\perp=bE R_3^\perp E-aR_2^\perp$, 则同一式为 $Z=\operatorname{diag}(d)+\frac{4a}{b}U M_\perp U$. 代入 (5.10) 恰还原 $2a$, 没有额外的 2 或 $1/2$.

故在保留本文原 $K=\Sigma^{-1}J$ 的定义时, 不能将 (5.12) 左端标作原 $K_o$. 原 $K_e$ 的直接表达为

$$
K_e=\operatorname{diag}(d)+2aU\left[G_D(b)-\frac abEG_N(a)E\right]U. \tag{5.13}
$$

### 5.4 原 $K_o$ 必须保留约化核及秩一项

这次直接投影 (4.11), 不作 $S$ 共轭. (5.11) 给出 $B_o^T(SQ)(SQ)^TB_o=2(Eq)(Eq)^T$, 而 Green 项选择上表的另一列组合. 因此

$$
\boxed{K_o=B_o^TKB_o
=\operatorname{diag}(d_1,d_2)
+\frac{4a\Delta}{b^2}(Eq)(Eq)^T
+2aU\left[\widetilde G_N(b)-\frac ab E\widetilde G_D(a)E\right]U.} \tag{5.14}
$$

这里两个核都位于自己的本征极点, 必须分别去掉 N 的第 2 模态和 D 的第 1 模态. 秩一项系数是 $2\tau=4a\Delta/b^2$, 它来自 (4.4) 的归一化及这一次镜像投影. (5.12) 中它消失, 不能据此在 (5.14) 中删除.

如果改用半区间归一化接口值 $U_h=\sqrt2U$、$q_h=2q$, 同一两个表达式成为

$$
Z=\operatorname{diag}(d)+aU_h[EG_D(b)E-(a/b)G_N(a)]U_h,
$$

$$
K_o=\operatorname{diag}(d)
+\frac{a\Delta}{b^2}(Eq_h)(Eq_h)^T
+aU_h[\widetilde G_N(b)-(a/b)E\widetilde G_D(a)E]U_h. \tag{5.15}
$$

同时半归一化 Wronskian 为全归一化 $W$ 的 2 倍, 故用它写 (3.9) 时系数变成 $\sigma c|W_h|/\eta$. 这说明归一化变换必须对所有向量、Wronskian 和核一并进行.

## 6. sector_data 的 H/E 合成对象及直接传播

### 6.1 源码版本和本节边界

协调器在真实 CLI 重算中发现并跟进告知: scripts/_gapn2_sector_decomposition.py 的旧 He/Ho/Ee/Eo 合成的是 $K_p$ 的块. 本作者随后首次只读该文件时, 当前源码已含显式 KpHe/KpHo/KpEe/KpEo 及 $Ke=E\,KpOdd\,E$, $Ko=E\,KpEven\,E$ 的返回映射. 因而下文“旧合成”指仍可在源码中定位的原 H/E 数学组装公式, 不声称读取时文件仍缺这项修复. 精确读取版本 SHA256 在 assumptions.json 中单列.

本节只从这些源码表达式及 (4.12) 验证解析对象. 不执行该 CLI、不改变代码、不复现其历史扫描. 解析证明限于第 3 节的精确 $n=2$ 条件. 文件支持其它 $n$ 并不表示本文证明了其它 $n$ 所需的全局接口符号输入.

### 6.2 拆出相邻两模态

仍用全区间单位归一化模态. 对 $\ell\ne2,3$, 写 $t_\ell=\lambda_\ell$, 并定义核

$$
A(t,z)=\sum_{\ell\ne2,3}
\frac{t_\ell\Delta}{(t_\ell-b)(t_\ell-a)}u_\ell(t)u_\ell(z),
$$

$$
B(t,z)=\sum_{\ell\ne2,3}
\left[\frac a{t_\ell-a}+\frac b{t_\ell-b}\right]u_\ell(t)u_\ell(z). \tag{6.1}
$$

它们分别对应源码 S1、S2; 第二个取值点反射到 $1-x_j$ 对应 S1b、S2b. 标量恒等式

$$
\frac b{t-b}-\frac a{t-a}=\frac{t\Delta}{(t-b)(t-a)} \tag{6.2}
$$

说明 (4.12) 去掉模态 2、3 后的 Green 部分 $H_p$ 满足

$$
(H_p)_{ij}=\frac{2a}{b}u_i u_j
\begin{cases}A(x_i,x_j),&\varepsilon_i\varepsilon_j=1,\\
-B(x_i,x_j),&\varepsilon_i\varepsilon_j=-1.
\end{cases} \tag{6.3}
$$

由于相邻两模态被排除, 任一保留项的分母非零. 系数在高谱端是 $O(1/\lambda_\ell)$, 第 5.1 节给出有限点绝对收敛. 对所有核一致使用同一有限指标集合时, 以下有限和代数同样成立, 但它们仅构成相应截断矩阵.

从 $\Gamma_3$ 中抽出的模态 2 项为 $-\mathbf u\mathbf u^T/\Delta$; 从 $\Gamma_2$ 中抽出的模态 3 项为 $\mathbf v\mathbf v^T/\Delta$, 其中 $\mathbf v=cS\mathbf u$. 放回 (4.12), 两项合计为

$$
\nu(SQ)(SQ)^T,\qquad
\nu=-\frac{2a(a^2+b^2)}{b^2\Delta}. \tag{6.4}
$$

所以有另一种严格分解

$$
K_p=\operatorname{diag}(d)+\tau QQ^T+\nu(SQ)(SQ)^T+H_p. \tag{6.5}
$$

这里 $Q$ 镜像为偶、$SQ$ 为奇. 用左半向量 $w=a q$, 两个秩一压缩因此为

$$
KpEe=c_e ww^T,\quad c_e=\frac{4\Delta}{ab^2}>0;\qquad
KpEo=c_o(Ew)(Ew)^T,\quad
c_o=-\frac{4(a^2+b^2)}{ab^2\Delta}<0. \tag{6.6}
$$

这恰是源码 c_e、c_o 和原 Ee、Eo 的系数. 尤其 KpEo 来自被拆出的两个相邻模态, 不是 (5.12) 中已消失的归一化 $QQ^T$ 项.

### 6.3 逐项核对旧 H 块

记 $p=-1$ 为本次 $u_2(1-x)=p u_2(x)$ 的反射因子. 若左半 $i,j\in\{1,2\}$ 的符号相同, 则右反射后符号相反; 若原来相反则反过来. (6.3) 的镜像压缩是左左块加或减左右反射块. 具体令 $C_{ij}=2a u_i u_j/b$, 有

$$
(KpHe)_{ij}=C_{ij}
\begin{cases}A(x_i,x_j)-pB(x_i,1-x_j),&\varepsilon_i\varepsilon_j=1,\\
-B(x_i,x_j)+pA(x_i,1-x_j),&\varepsilon_i\varepsilon_j=-1,
\end{cases} \tag{6.7}
$$

$$
(KpHo)_{ij}=C_{ij}
\begin{cases}A(x_i,x_j)+pB(x_i,1-x_j),&\varepsilon_i\varepsilon_j=1,\\
-B(x_i,x_j)-pA(x_i,1-x_j),&\varepsilon_i\varepsilon_j=-1.
\end{cases} \tag{6.8}
$$

这逐项对应源码 pn=-1、pmask、fac=2a/b 及 He/Ho 的组装. 其因子没有再乘 2: 单位镜像基底的四项压缩恰化为左左加/减左右两项.

由 (6.5)--(6.8), 旧合成对象严格为

$$
\boxed{oldKe=\operatorname{diag}(d)+KpEe+KpHe=B_e^TK_pB_e,}
$$

$$
\boxed{oldKo=\operatorname{diag}(d)+KpEo+KpHo=B_o^TK_pB_o.} \tag{6.9}
$$

这些等式的无限和版本给出真实 $K_p$ 的块; 共同有限截断版本给出 $K_p$ 的相应谱截断近似块. 原名中的 raw K 解释不能由这些组装式支持.

### 6.4 原 K 的返回值与分量映射

由第 1 节, 原 K 的两个块必须按下表恢复:

| 原 K 对象 | 从显式 Kp 对象恢复 |
|---|---|
| $K_e$ | $E\,KpOdd\,E=E\,oldKo\,E$ |
| $K_o$ | $E\,KpEven\,E=E\,oldKe\,E$ |
| $H_e$ | $E\,KpHo\,E$ |
| $H_o$ | $E\,KpHe\,E$ |
| $E_e$, 加性分量名 | $E\,KpEo\,E=c_o ww^T$ |
| $E_o$, 加性分量名 | $E\,KpEe\,E=c_e(Ew)(Ew)^T$ |

这里 $E_e,E_o$ 的下标名称与合同矩阵 $E=\operatorname{diag}(1,-1)$ 是不同对象. 对角项在 $E$ 合同下不变, 所以原 K 仍有 $K_e=\operatorname{diag}(d)+H_e+E_e$、$K_o=\operatorname{diag}(d)+H_o+E_o$. 不能只改总块名称而把附加分量、主导项说明或 c_e/c_o 的解释仍附在原同名扇区上.

一致截断下, 块交换合同本身是精确有限维代数. 但数值驻点残差、谱标签、奇偶值误差和谱尾项使实际浮点输出仅是近似; 同一程序中两种组装吻合也不能独立确认这些误差已受控. 两块交换不改变行列式乘积或总惯性, 所以历史输出的这些量有可能保留数值意义, 但本文不逐项追认历史输出.

### 6.5 第三张卡中的负秩一判据

按协调器后续定位的直接传播, 定点读取 tools/band-selfconsistency-equivariance.md 的约 280--365 行, 可见其“镜像扇区分解”复制了 (6.6)--(6.8) 的组装, 却以原 $K_e,K_o$ 标识. 在本节的条件下, 其这组表达应分别标作 $KpEven,KpOdd$. 本文不据此否定该卡其它独立段落, 也不重做历史扫描.

特别地令 $\alpha=|c_o|>0$, $z=Ew$, $A_{p,o}=\operatorname{diag}(d)+KpHo$. 正确对象是

$$
KpOdd=A_{p,o}-\alpha zz^T. \tag{6.10}
$$

对任意实对称 $A$ 及 $\alpha>0$, 有精确等价

$$
\boxed{A-\alpha zz^T\succ0
\quad\Longleftrightarrow\quad
A\succ0\ \hbox{且}\ \alpha z^TA^{-1}z<1.} \tag{6.11}
$$

证明: 左边成立则 $A=(A-\alpha zz^T)+\alpha zz^T\succ0$. 在 $A\succ0$ 下作合同, 得 $I-\alpha vv^T$, $v=A^{-1/2}z$. 其在 $v^\perp$ 上的特征值是 1, 在 $v$ 方向为 $1-\alpha\|v\|^2$; $v=0$ 情形直接成立. 这也证明了等号时的退化, 无需只援引 Sherman--Morrison 名称.

因此该卡所写负秩一正定判据实际针对 $KpOdd$, 等价于原 $K_e$ 的正定判据. 原块形式为

$$
K_e=A_{r,e}-\alpha ww^T,\qquad
A_{r,e}=E A_{p,o}E=\operatorname{diag}(d)+H_e. \tag{6.12}
$$

相应二次型保持相同值: $z^TA_{p,o}^{-1}z=w^TA_{r,e}^{-1}w$. 它不能在不换对象的情况下称作原 $K_o$ 的负秩一判据. 原 $K_o$ 在这套分拆中是正秩一项 $c_e(Ew)(Ew)^T$.

INF 如需针对原 $K_o=A_{r,o}+\beta(Ew)(Ew)^T$ 判负定, 其中 $\beta=c_e>0$, 则对 $-K_o$ 使用 (6.11), 得

$$
K_o\prec0\ \Longleftrightarrow\
A_{r,o}\prec0\ \hbox{且}\
\beta(Ew)^T(-A_{r,o})^{-1}(Ew)<1. \tag{6.13}
$$

这里 $A_{r,o}=\operatorname{diag}(d)+H_o$. 这仍只是条件化矩阵判据, 没有证明其两个前提沿任何 INF 分支成立.

另有一个与同一段落直接相关的符号边界: 若 $E_o\preceq0$, 则
$\lambda_{\min}(H_o-E_o)+\min d>0$ 一般不足以保证
$\operatorname{diag}(d)+H_o+E_o\succ0$. 例如 $d=(1,1)$, $H_o=0$, $E_o=-2zz^T$, $z=(1,-1)^T/\sqrt2$, 前一余量等于 1, 后一矩阵却有特征值 $-1,1$. 这是普通实对称矩阵反例, 不声称在实际 SL 配置上实现. 对当前加法约定, 可用的 Weyl 充分条件应含 $\lambda_{\min}(H_o+E_o)+\min d>0$, 或直接使用 (6.11). 因而这段历史“充分不等式”需要单独核对符号, 不能只换扇区名称后继续当作一般矩阵定理.

### 6.6 协调器所报 R4SUP 单例的正确放置

协调器提供的真实 CLI 重算线索为

$$
oldKo\approx\begin{pmatrix}4.3925&3.1184\\3.1184&6.9328\end{pmatrix},\qquad
rawKo\approx\begin{pmatrix}5.55777&-1.94306\\-1.94306&4.77344\end{pmatrix}.
$$

第一矩阵应以有限截断 $KpOdd$ 的身份与 (5.12) 比较, 第二矩阵才应与 (5.14) 比较. 两者不应作为同一块的两种实现直接作误差解释. 协调器还说明首次半谱 CLI 失败日志已经保留.

这些数字和日志状态均为协调器跟进记录. 本作者未读取该 CLI 日志或重新计算这些数字, 不给它们追加有效位数、误差上界、成功状态或存在性证明. 输入附件中的另一组 65 位 R4 数字也未在本作者会话中重放. (6.9) 的对象身份由前面的解析推导承担, 不依赖这些单例.

## 7. 相位指标、去极点身份与浮点证据的边界

### 7.1 为什么均匀变号扫描不提供每阶身份

若一个扫描格包含两个简单根, 世俗函数端点可能同号; 对已找到的格再二分不能找回该格. 一个精确的自包含说明是取 $L=1/2$、常密度 100:

$$
\mu_j^D=\frac{j^2\pi^2}{25},\qquad
\mu_j^N=\frac{(j-1/2)^2\pi^2}{25}. \tag{7.1}
$$

在 D 情形, 选任何 $0<l<\mu_1^D<\mu_2^D<r<\mu_3^D$. 从初始斜率 1 的解
$y(L)=\sin(5\sqrt\mu)/(10\sqrt\mu)$ 看, 端点 $l,r$ 同号, 却中间含两个根. 这证明变号扫描原则上会漏掉偶数个根. 它不冒称复现某一版本 Python 浮点网格的精确端点或附件所报列表; 后者属于另行执行的证据.

第 2 节算法比较的是固定的相位目标, 不是端点世俗函数符号, 所以精确算法不会把“第三根”按发现顺序重标成“第一根”.

### 7.2 去极点应绑定数学对象

约化核的被删项必须由“相同密度及区间、相同边界类型、相同一基谱指标”标识. 对本任务, 是 D1 和 N2. 有限和需要保留完整的指标映射; 从某张错误列表取出的数值再到另一张列表删除同一个数组位置, 不保证删除同一模态.

一次取得同指标长谱表并以其前缀形成 $N,2N$ 截断, 可以避免重复枚举带来的错位, 但它本身不证明表的指标正确. 参数数值接近也不能替代相位身份. 若必须数值排极点, 至少应同时检查目标谱参数、边界类型、指标及同一输入版本; 不能用一个宽松的“小分母阈值”任意删除多个模式. 身份无法区分时应报告不可分辨.

### 7.3 为什么浮点相位仍不是严格证书

第 2 节证明的是精确函数和精确实数算法. 浮点执行还会遇到:

- 三角函数、$\pi$、平方根及接口比值的舍入误差, 相位提升的取整分支误差, 大转数下低位丢失.
- 几何上正的极窄块在机器坐标中变成同一点; 相邻根或目标相位也可能无法分辨.
- 在近极点处相减两个大数的消去误差, 以及有限谱截断的尾项. Richardson 组合没有自动给出经证明的余项界.

因此增加精度、二分次数、正性检查、根残差、表内递增或两个共用枚举器的结果吻合, 均不自动成为严格区间证书. 若要认证一个具体索引区间, 须对精确输入或其明确包络使用向外取整的区间运算, 包住 $\pi$、初等函数及各相位分支, 证明端点相位分别位于目标两侧, 并在误差包络中保持累计转数及几何合法性. 若要进一步认证 Green 值、驻点或矩阵符号, 还须相应谱尾界、极点身份及驻点/矩阵的不等式证书. 这些工作未在本文执行.

## 8. 结论的量词与未完成义务

本稿的 (1.2) 适用于任意 $n\ge1$ 和任意实或复矩阵, 不需要 $KP=PK$. 第 2 节适用于每个有限正分块密度、两种指定边界和每个 $j\ge1$. 第 3--6 节适用于每个固定有限 $R>1$、每个满足 (3.1)--(3.3) 的 $n=2$ 五层配置, INF 和 SUP 两图案均包括在内. 这是“每个满足条件的配置上公式成立”, 不是“对每个 $R$ 都已构造或认证一个配置”.

对 SUP 候选, 若完整 $K\succ0$, 则 (4.13) 给出五层开家族内的严格局部最大; 对 INF 候选, 若 $K\prec0$, 则得到严格局部最小. 局部极值的必要二阶条件只给半定性. 仅有 $d_i$ 的符号、一个扇区的符号、单点行列式或 R4 单例, 都不足以推出完整定性. 五层家族内的局部结论也不能直接升级为所有允许密度中的全局结论.

以下义务保留, 本稿没有证明:

1. 全部有限 $R>1$ 上的对称带自洽配置存在、唯一及连续分支, 或排除其它非对称驻点.
2. 任意 $R$ 下两个原 K 扇区同时定号、完整 G1'、全局最优性及历史有限点 Green 惯性等式.
3. $R\downarrow1$ 时含 $1/(R-1)$ 的 K 公式的缩放极限, 或 $R\to\infty$ 的一致估计.
4. 仓库数值实现对全部输入的正确性、所报 R4 数字的严格误差、驻点区间包络及 Green 截断尾界.
5. _prims_9 全部原函数的独立重算、历史扫描的逐项恢复、完整分析或程序的 Lean 形式化.

作者的局部符号自检仅用于暴露代数因子和映射失误. 它不替代上述无限维推导, 也不是另一个作者隔离会话给出的检验结论.
