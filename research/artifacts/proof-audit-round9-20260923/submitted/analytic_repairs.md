# 第九轮补充推导：二阶变分、正确切空间与平衡候选的指标极限

日期：2026-09-23。审查基线：`2a81b608d53e3decee04c46716a8d8f8c2d9b1b4`。

本文是本轮独立推导，不是已经写回仓库、已经发表或已经通过 Lean 认证的结果。数值与符号检查分别见 `checks.py`；以下普遍命题由解析论证承担。

## 1. 真正的密度切向条件

在 $-u''=\lambda\rho u$ 的 Dirichlet 问题中固定基点 $\rho$，按 $\int\rho u_k^2=1$ 归一化。令

$$D_n=\lambda_{n+1}-\lambda_n,\qquad f=\lambda_nu_n^2-\lambda_{n+1}u_{n+1}^2.$$

对有界密度方向 $h$，一阶变分为 $D_n'[h]=\int_0^1fh$。将区间分成 $I_i$，宽度 $L_i>0$，取 $h=\sum b_i\mathbf1_{I_i}$。记

$$A_i=\int_{I_i}f(x)\,dx,\qquad g_i=A_i/L_i.$$

则准确的切向条件是 $b\cdot A=0$，不是 $b\cdot g=0$。各块等宽时二者等价；一般不等宽时不等价。

若采用系数空间的普通欧氏投影，应写

$$b=b^{(0)}-\frac{b^{(0)}\cdot A}{A\cdot A}A\quad(A\ne0).$$

若采用代表真实 $L^2$ 范数的内积 $\sum L_i b_i c_i$，则相应投影为

$$b=b^{(0)}-\frac{\sum L_i b_i^{(0)}g_i}{\sum L_i g_i^2}g.$$

这两种投影都能产生正确切向量，但所得向量通常不同。必须明确使用哪一个系数度量。$A=0$ 时所有分块方向都切向，不应除以零。诊断应另行直接积分 $fh$，并用足够准确、与实际端点对齐的积分规则验证，而不能仅打印构造时已经强制为零的错误内积。

### 一个严格的 SL 反例

取 $\rho=1$、$n=1$，则

$$f=2\pi^2\sin^2(\pi x)-8\pi^2\sin^2(2\pi x).$$

在宽度 $(1/4,3/4)$ 的两个块上，

$$A=\left(-\frac{3\pi^2}4-\frac\pi2,\ -\frac{9\pi^2}4+\frac\pi2\right),$$
$$g=\left(-3\pi^2-2\pi,\ -3\pi^2+\frac{2\pi}3\right).$$

选取有界方向

$$b=\left(-\frac{9\pi-2}{3(3\pi+2)},1\right).$$

直接得到 $b\cdot g=0$，但

$$D_1'[h]=b\cdot A=-\frac32\pi^2+\frac\pi3\ne0.$$

它反驳的是投影步骤的普遍正确性，不依赖有限差分精度或极值点的数值定位。

### 仓库实际参数的独立复算

采用 `scripts/op03_gap_table.json` 的 `n2_SUP` 十进制端点，视这些输入为精确十进制有理数；密度为 $[1,4,1,4,1]$。独立分块传递、求根与解析积分给出

- $\lambda_2\approx22.5004420511521483741113655391$；
- $\lambda_3\approx85.5936408854062481059637833054$；
- 从 $b^{(0)}=(1,0,0,0,0)$ 按旧平均值规则投影，$b\cdot g$ 的计算残差约 $9.1\times10^{-80}$；
- 同一方向的真实一阶变分为 $b\cdot A\approx-1.2468476907831298074897551717$。

这是高精度数值交叉检查，不声称这些四舍五入端点就是精确驻点。它也不是复跑原程序的固定随机样本；采用的是相同投影映射的一个确定输入。

## 2. 归一化导数的核分量

设 $\rho_t=\rho+t h$，$a=\int h u_k^2$，$v=u_k'(t)|_{t=0}$。归一化给出

$$\int\rho u_kv=-a/2.$$

在加权正交基下，正确展开为

$$v=-\frac a2u_k+\lambda_k\sum_{l\ne k}\frac{\int h u_k u_l}{\lambda_l-\lambda_k}u_l.$$

其中离模态部分来自一阶方程的投影，沿 $u_k$ 的部分来自归一化。

若 $R^\perp$ 特指 $L=A-\lambda_k B$ 在**普通** $L^2(dx)$ 中对核 $\operatorname{span}\{u_k\}$ 的约化逆，先定义

$$v_0=\lambda_k R^\perp[(h-a\rho)u_k],$$

则应恢复为

$$v=v_0-\left(\frac a2+\int\rho u_kv_0\right)u_k.$$

因此源文所写 $v=\lambda_k R^\perp[(h-a\rho)u_k]$ 不能无条件按真正归一化导数的等式读取，只能说明一个模核的特解。

最短检查是 $h=\rho$：$\lambda_k(t)=\lambda_k/(1+t)$、$u_k(t)=u_k/\sqrt{1+t}$。此时约化逆的右端为零，但 $v=-u_k/2\ne0$。

这不破坏源文的主要二阶特征值公式。因为核分量不进入 $\langle v,(A-\lambda B)v\rangle$，或者从正确展开直接计算，仍得到

$$\lambda_k''=2\lambda_k a^2-2\lambda_k^2\sum_{l\ne k}\frac{(\int h u_k u_l)^2}{\lambda_l-\lambda_k}.$$

本节取实密度、实特征函数与实方向；复参数需另写相应的半双线性约定。

## 3. 正常质量缩放的窄脉冲不导致该一维 Green 二次型发散

### 3.1 明确反例与极限

取 $\rho=1$，$u_k=\sqrt2\sin(k\pi x)$，$\lambda_k=k^2\pi^2$，以及单位总质量矩形脉冲

$$h_\eta(x)=\frac1{2\eta}\mathbf1_{|x-1/2|<\eta},\qquad0<\eta<1/2.$$

每个固定 $\eta$ 都是 $L^\infty$ 方向；先在密度参数零处求导，再令 $\eta\downarrow0$，不把一个共同的扰动半径当作已知。

记 $B_{kl}(\eta)=\int h_\eta u_k u_l$，则

$$B_{kl}(\eta)=\cos((k-l)\pi/2)\operatorname{sinc}((k-l)\pi\eta)
-\cos((k+l)\pi/2)\operatorname{sinc}((k+l)\pi\eta),$$

其中 $\operatorname{sinc}(z)=\sin z/z$，在零点取值一。对每个 $k,l$，$B_{kl}\to u_k(1/2)u_l(1/2)$，且 $|B_{kl}|\le2$。

固定 $k$ 时 $\sum_{l\ne k}|l^2-k^2|^{-1}<\infty$，因此可以对二阶变分的谱和用控制收敛。对 $k=1$，

$$\sum_{l\ne1}\frac{u_l(1/2)^2}{\lambda_l-\lambda_1}
=\frac2{\pi^2}\sum_{m=1}^\infty\frac1{(2m+1)^2-1}
=\frac1{2\pi^2},$$

其中 $\sum_{m\ge1}1/[4m(m+1)]=1/4$。由于 $u_1(1/2)^2=2$，得到

$$\lim_{\eta\downarrow0}\lambda_1''[h_\eta,h_\eta]
=2\pi^2\cdot4-2\pi^4\cdot\frac1{\pi^2}=6\pi^2.$$

对 $k=2$，$u_2(1/2)=0$，同一控制收敛给出 $\lambda_2''\to0$。故

$$\boxed{\lim_{\eta\downarrow0}\tfrac12D_1''[h_\eta,h_\eta]=-3\pi^2.}$$

这是真正谱隙二阶变分的有限极限，不只是某个截断矩阵有界。

### 3.2 为什么密度的有限跳点也不会自动造成这种发散

对固定正的有界密度，Dirichlet 基本解在空间变量中连续且一阶连续，对谱参数解析。Green 核在特征值外可由左右基本解和其 Wronskian 表达。由于特征值单重，其极点是简单极点；减去

$$\frac{u_k(x)u_k(y)}{\lambda_k-z}$$

后，在 $z=\lambda_k$ 取有限部，得到在闭正方形上连续、有界的核 $\widetilde G_k(x,y)$。这可直接从基本解的解析展开、Wronskian 的简单零点及连续参数依赖验证；密度跳跃影响二阶导数，不使函数值的 Green 核产生对角无穷大。

对应谱和的二次型可写为

$$\iint h_\eta(x)h_\eta(y)u_k(x)u_k(y)\widetilde G_k(x,y)\,dx\,dy.$$

对集中到一个固定点、总变差一致有界的脉冲，核的连续性保证该表达式趋于有限点值。有限个脉冲的线性组合也一样。

所以，“一维正则问题中单位质量脉冲的宽度趋零极限必因 Green 对角发散而失效”不成立。若换成无界总质量的缩放、高维奇异核或核的导数，必须另作判断，不能与这里的核混同。

### 3.3 真正需要补的是路径加速度

移动接口 $a(t)=a+t d$，密度跳量 $s=\rho_R-\rho_L$ 时，分布意义下

$$\dot\rho=-s d\,\delta_a,\qquad \ddot\rho=s d^2\delta'_a.$$

因此对一阶切换函数 $f$，密度路径的二阶链式法则包含

$$D_n'[\ddot\rho]=-s d^2 f'(a).$$

一般多个接口则对各接口求和。它是有限的、通常非零的主阶项；驻点的 $f(a)=0$ 不使 $f'(a)$ 自动为零。线性密度二阶变分不能直接等于移动接口 Hessian，但正确原因是漏掉这个有限项，而不是必然发生 Green 对角发散。

本段不替代对任意分布路径的可微性证明，也不声称已解决 (G1') 的定号。它识别了必须保留的链式法则项，并纠正了否定路线的错误理由。

## 4. 未归一化世俗函数的正确反射关系

平衡交替配置取 $s=\sqrt R$、$t_n=1/((n+1)s+n)$、$y=\omega s t_n$。物理状态为 $(u,u')$，令

$$F_n(y)=(T_{\rm end}(y)T_{\rm cell}(y)^n)_{01},\qquad \omega(y)=y/(s t_n).$$

在反射 $y\mapsto\pi-y$ 时，$\omega$ 也改变，不能保持它不变。

以 $P_\omega=\operatorname{diag}(1,\omega)$ 变换状态，归一化矩阵为

$$N_{\rm cell}=\begin{pmatrix}
C^2-S^2/s &(s+1)SC/s\\
-(s+1)SC&C^2-sS^2
\end{pmatrix},\qquad
N_{\rm end}=\begin{pmatrix}C&S\\-S&C\end{pmatrix},$$

其中 $C=\cos y,S=\sin y$。对 $J=\operatorname{diag}(1,-1)$，

$$N_{\rm cell}(\pi-y)=J N_{\rm cell}(y)J,\qquad
N_{\rm end}(\pi-y)=-J N_{\rm end}(y)J.$$

因此归一化的 $\widehat F_n=\omega F_n$ 满足准确对称性，原函数则满足

$$\boxed{F_n(\pi-y)=\frac{y}{\pi-y}F_n(y),\qquad0<y<\pi.}$$

$n=1,R=4,t_1=1/5$ 时，

$$F_1(\pi/3)=-\frac{21\sqrt3}{40\pi},\qquad
F_1(2\pi/3)=-\frac{21\sqrt3}{80\pi}.$$

所以原文的函数值等式为假。正因子不改变内部零点及其单重性，故零点反射、后续以 $\omega F_n$ 推导的 Chebyshev 根计数仍然可以保留。

## 5. 建设性补证：平衡候选值的严格递减和精确极限

本节只研究规定平衡配置的候选比值 $c_n(R)$，**不声称它已经等于所有密度上的 $\Lambda_n^{\sup}(R)$**。

固定 $s>1$，令

$$A=(s+1)^2/s,\qquad B=s+1/s=A-2,\qquad\delta=1/s\in(0,1).$$

由归一化转移矩阵的 Cayley–Hamilton 递推，

$$\widehat F_n(y)=\sin y\,P_n(\cos^2y),$$
$$P_0=1,\quad P_1=Ax-s,\quad P_n=(Ax-B)P_{n-1}-P_{n-2}.$$

令 $z=Ax-B$。这个多项式为对称三对角矩阵 $J_n$ 的特征多项式，其中主对角是 $(-\delta,0,\ldots,0)$，两条副对角全为一。它与仓库采用的“最后对角为 $-\delta$”矩阵经坐标倒序酉相似。

设 $z_n$ 是 $J_n$ 的最小特征值。对任意向量 $v$，

$$\langle(J_n+2I)v,v\rangle
=\sum_{j=1}^{n-1}|v_j+v_{j+1}|^2+(1-\delta)|v_1|^2+|v_n|^2>0\quad(v\ne0),$$

故 $z_n>-2$。类似的减号平方和证明全部特征值小于二。

$J_n$ 是 $J_{n+1}$ 的顺序主子矩阵。极小极大原理给出 $z_{n+1}\le z_n$。若等号成立，将 $J_n$ 的最小特征向量补一个末尾零，就取得 $J_{n+1}$ 的最小 Rayleigh 值，因而是其特征向量。最后一行强迫原向量最后坐标为零，递推再迫使所有坐标为零，矛盾。因此

$$z_{n+1}<z_n.$$

取交替符号的单位向量 $v_j=(-1)^j/\sqrt n$，得到

$$-2<z_n\le-2+\frac{2-\delta}{n},$$

所以 $z_n\downarrow-2$。三对角矩阵的每个特征向量由第一个坐标唯一确定，故特征值简单；这也保证对应的相位根都是简单的。

$P_n$ 的最小根是 $x_n=(B+z_n)/A\in(0,1)$；它对应 $(0,\pi/2)$ 中最大的、也就是第 $n$ 个相位根

$$y_n=\arccos\sqrt{(B+z_n)/A}.$$

于是 $y_n$ 严格增加，且

$$y_n\uparrow\varphi(R)=\arccos\frac{\sqrt R-1}{\sqrt R+1}.$$

从物理相位和特征值的比例关系，以及相邻中心根的反射配对，

$$c_n(R)=\left(\frac{\pi-y_n}{y_n}\right)^2.$$

右边随 $y_n\in(0,\pi/2)$ 严格递减，因此

$$\boxed{c_n(R)\downarrow\left(\frac{\pi-\varphi(R)}{\varphi(R)}\right)^2.}$$

例如 $R=4$ 时极限约为 $2.4091685548064623$。这可把 `tools/bloch-band.md` 中关于**平衡候选序列本身**的数值观察升级为解析结论，但不能将未解决的全局最优性、等宽极值性或完整 $\Lambda_n^{\sup}$ 分类一并升级。
