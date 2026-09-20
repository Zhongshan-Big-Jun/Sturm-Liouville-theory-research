# 第四轮审计的建设性补证

对象：`Zhongshan-Big-Jun/Sturm-Liouville-theory-research`，固定提交
`2e9bf3d66fa21a41e16bf779782739ddd9505233`。

本文是在本次审计中另行推导的修复方案，不是仓库已经接收的结果，也没有通过 Lean 形式化或另一个审稿人的独立验收。所用递推系数与该提交的 `docs/SL_third_order_recurrence_theory.tex`、`scripts/d4_third_order_theory.py` 对齐。代数、有限和及数值交叉检查见 `check_round4.py` 与 `round4_results.json`；下面的全指标论证与极限证明并不依赖有限扫描。

## A. 退化极限：区分函数代表与商空间中的元素

沿用 `docs/SL_krein_c0_limit.tex` 的定义：

\[
S_n=P_n-P_{n-2}\quad(n\ge2),\qquad
K_n^{(c)}=a_n(c)S_n+K_{n-2}^{(c)},
\]

\[
a_0=a_1=a_2=a_3=1,\qquad
 a_{n+2}=\left(1+\frac{4n^2-1}{c}\right)a_n
 +\frac{2n+1}{2n-3}(a_n-a_{n-2}),\quad n\ge2.
\]

### A1. 零参数 Gram 矩阵是显式对角的

Legendre 恒等式
\[
(P_n-P_{n-2})'=(2n-1)P_{n-1}
\]
及 \(S_n(1)=S_n(-1)=0\) 给出
\[
(S_n,S_m)_{1,0}=2(2n-1)\delta_{nm}.
\]
因此从 \(S_2,S_3,\ldots\) 作标准 Gram–Schmidt，取正首项系数，得到的多项式代表就是
\[
Q_n=\frac{S_n}{\sqrt{2(2n-1)}}.
\]
这个恒等式可以直接由 Legendre 三项递推及其导数恒等式推出，不需要数值判断 Gram 矩阵可逆。对每个固定阶数的极限，也不需要关于维数 \(N\) 的一致非退化估计。

### A2. 正确的普通 Sobolev H1 极限

原始归一化满足
\[
K_2^{(c)}=P_2,\quad \|K_2^{(c)}\|_{1,c}^2=6+2c/5,
\]
\[
K_3^{(c)}=P_3,\quad \|K_3^{(c)}\|_{1,c}^2=10+2c/7.
\]
所以
\[
\widehat u_2^{(c)}\longrightarrow P_2/\sqrt6=Q_2+1/\sqrt6,
\qquad
\widehat u_3^{(c)}\longrightarrow P_3/\sqrt{10}=Q_3+x/\sqrt{10}.
\]
这是系数收敛，因此也是普通 Sobolev H1 收敛，但不是收敛到标准 Gram–Schmidt 的 \(Q_2,Q_3\)。

对每个固定 \(n\ge4\)，系数递推给出
\[
a_n=C_n c^{-r_n}(1+O(c)),\quad C_n>0,
\]
其中偶数 \(r_n=(n-2)/2\)，奇数 \(r_n=(n-3)/2\)。证明是按奇偶递推：主项为
\((4n^2-1)a_n/c\)，其余项为 \(O(a_n)\)，低两阶系数的阶数少一。
特别地，不能把余项写成 \(O(1)\)；例如
\[
a_6-(63/c)a_4=1+42/c.
\]

递推还给出 \(K_{n-2}^{(c)}/a_n\to0\) 的多项式系数收敛；归一化公式给出
\[
\frac{\|K_n^{(c)}\|_{1,c}^2}{a_n^2}
 =\frac{2c}{2n+1}\frac{a_{n+2}}{a_n}
 \longrightarrow 2(2n-1).
\]
故
\[
\widehat u_n^{(c)}\longrightarrow Q_n
\quad\text{in ordinary }H^1,\qquad n\ge4.
\]

### A3. 对全部 n>=2 都正确的商空间版本

在 \(W=\operatorname{span}\{1,x\}\) 的商空间中，低阶差异消失。因此
\[
[\widehat u_n^{(c)}]\longrightarrow [Q_n]
\quad\text{in }(H^1/W,\|\cdot\|_{1,0}),\qquad n\ge2.
\]
仓库本次已经修复的商空间完备性证明可继续使用。需要更改的是函数代表层面的极限陈述，而不是撤回商空间完备性。

## B. 明确奇偶三阶递推的统一因式分解

设 \(c>0\)，\(\epsilon\in\{0,1\}\) 分别表示偶、奇侧，考虑 \(j\ge3\) 的递推
\[
c^2\mu_j=P_j\mu_{j-1}-Q_j\mu_{j-2}+R_j\mu_{j-3},
\]
其中
\[
P_j=4cj(2j+2\epsilon-1)+c^2\frac{j}{j-1},
\]
\[
Q_j=4j(j-1)(2j+2\epsilon-1)(2j+2\epsilon-3)
 +4cj(2j+2\epsilon-3),
\]
\[
R_j=4j(j-2)(2j+2\epsilon-3)(2j+2\epsilon-5).
\]
这些系数正是该提交程序中 `even_coeffs`、`odd_coeffs` 的两组系数。

定义
\[
v_j=\frac{c^j\mu_j}{(2j+\epsilon)!},\qquad
\theta_j=\frac{c}{2(j-1)(2j+2\epsilon-1)}.
\]
逐项约去阶乘可得
\[
v_j=(2+\theta_j)v_{j-1}-(1+2\theta_j)v_{j-2}
 +\theta_jv_{j-3}.
\]
例如第一项的系数由
\[
\frac{P_j}{c(2j+\epsilon)(2j+\epsilon-1)}=2+\theta_j
\]
给出；另外两项分别为 \(1+2\theta_j\) 和 \(\theta_j\)。
令
\[
d_j=v_j-2v_{j-1}+v_{j-2},
\]
便有
\[
\boxed{d_j=\theta_jd_{j-1}.}
\]
若
\[
a_j=\frac{j c^j}{(2j+\epsilon)!},\qquad j\ge1,
\]
则 \(a_j/a_{j-1}=\theta_j\)（\(j\ge2\)）。所以全部二阶差分为
\[
d_j=C a_j\qquad(j\ge2).
\]
这一步对每个 \(c>0\) 和两种奇偶性都是精确恒等式，不是渐近近似。

## C. 正项级数、向后迭代与最小解

定义
\[
\Phi_j=\sum_{r=j+2}^{\infty}(r-j-1)\frac{r c^r}{(2r+\epsilon)!}.
\]
所有项非负，级数绝对收敛。尾项相减给出
\[
\Phi_j-2\Phi_{j-1}+\Phi_{j-2}=a_j\quad(j\ge2).
\]
于是全部解可写为
\[
\boxed{v_j=A+Bj+C\Phi_j.}
\]
因为 \(\Phi_j\to0\)，满足 \(v_j\to0\) 的解空间是一维的。其余任一不与该支成比例的解具有非零仿射部分，故此支与该解之比趋于零，符合最小解的相对渐近定义。

\(\Phi_0>0\)，且 \(0!=1!=1\)。因此归一化 \(\mu_0=1\) 的唯一最小解为
\[
\boxed{\mu_j^*=\frac{(2j+\epsilon)!}{c^j}\frac{\Phi_j}{\Phi_0}.}
\]
仓库的 z 标度为
\[
z_j=\frac{\mu_j}{(j!)^2(4/c)^j},
\]
故 \(z_0=\mu_0\)，这里的归一化与仓库一致。

### C1. 明确证明向后迭代收敛

采用源文的终端形状 \(z_N\ne0,z_{N+1}=z_{N+2}=0\)；整体倍乘不改变按第零项归一化后的解，因此可取 \(\mu_N=1,\mu_{N+1}=\mu_{N+2}=0\)。

设
\[
\Phi_j^{(N)}=\sum_{r=j+2}^{N+2}(r-j-1)a_r.
\]
从 \(d_{N+2}=v_N\) 反推差分再求和，得到
\[
\frac{\mu_j^{(N)}}{\mu_0^{(N)}}
=\frac{(2j+\epsilon)!}{c^j}
\frac{\Phi_j^{(N)}}{\Phi_0^{(N)}}\quad(0\le j\le N).
\]
分母严格为正。对固定 \(j\)，分子、分母的正项有限和分别趋于 \(\Phi_j,\Phi_0\)，所以按固定指标归一化的向后极限确实存在，且等于上述最小解。这不需要将极限根为 \(0,1,1\) 的数值稳定性当成收敛定理。

## D. 一般 c>0 的常数闭式及严格尾项估计

源文的常数定义等价于
\[
K_\epsilon(c)=\lim_{j\to\infty}j^3\mu_j^*
 =\lim_{j\to\infty}z_j^*(j!)^2(4/c)^j j^3.
\]
正项级数中 \(r=j+2\) 的第一项为
\[
T_{j,1}=\frac{c^2(j+2)}{\Phi_0}
\frac{(2j+\epsilon)!}{(2j+4+\epsilon)!}.
\]
因此 \(j^3T_{j,1}\to c^2/(16\Phi_0)\)。

把其余项写成 \(r=j+\ell+1\), \(\ell\ge2\)。以第一项为单位，其比值不超过
\[
\ell^2 q_j^{\ell-1},\qquad
q_j=\frac{c}{(2j+5+\epsilon)^2}.
\]
这里使用 \((j+\ell+1)/(j+2)\le\ell\)，以及新增阶乘因子都至少为 \(2j+5+\epsilon\)。对充分大的 \(j\)，\(q_j<1\)，且
\[
\sum_{\ell=2}^{\infty}\ell^2q_j^{\ell-1}
=\frac{1+q_j}{(1-q_j)^3}-1=O(j^{-2}).
\]
所以尾部相对第一项为 \(O(j^{-2})\)，严格得到
\[
\boxed{K_\epsilon(c)=\frac{c^2}{16\Phi_0}.}
\]

令 \(D=c\,d/dc\)。对整函数级数逐项求导，
\[
\Phi_{0,0}=D(D-1)\cosh\sqrt c
=\frac{c\cosh\sqrt c-\sqrt c\sinh\sqrt c}{4},
\]
\[
\Phi_{0,1}=D(D-1)\frac{\sinh\sqrt c}{\sqrt c}
=\frac{(c+3)\sinh\sqrt c-3\sqrt c\cosh\sqrt c}{4\sqrt c}.
\]
由于二者也是严格正的级数，所有分母均为正。于是
\[
\boxed{K_{\rm even}(c)=
\frac{c^2}{4(c\cosh\sqrt c-\sqrt c\sinh\sqrt c)}},\qquad c>0,
\]
\[
\boxed{K_{\rm odd}(c)=
\frac{c^{5/2}}{4((c+3)\sinh\sqrt c-3\sqrt c\cosh\sqrt c)}},\qquad c>0.
\]
检查：\(K_{\rm even}(1)=e/4\)，\(K_{\rm even}(c)\to3/4\)、\(K_{\rm odd}(c)\to15/4\) 当 \(c\downarrow0\)。

这是对本文明确的两组系数、按 \(\mu_0=z_0=1\) 归一化得到的闭式；不涵盖任意变系数三阶递推，也不处理仓库的非齐次源项控制。

## E. 一个不设有理次数上限的分类补证

仓库 2026-08-22 的补充证明已经处理 root-1 的高次有理排除。本节给出另一种推导，同时处理明确递推的最小解分支。这里“有理比值”指一个有理函数在充分大的整数指标上等于解的相邻比值；所取指标上的分母必须非零。

写
\[
z_j=H_jv_j,\qquad
H_j=\frac{(2j+\epsilon)!}{4^j(j!)^2},\qquad
\frac{H_j}{H_{j-1}}=1+\frac{2\epsilon-1}{2j}.
\]
故 \(z_j/z_{j-1}\) 有理当且仅当 \(q(j)=v_j/v_{j-1}\) 有理。

反设通解 \(v_j=A+Bj+C\Phi_j\) 中 \(C\ne0\)，且 \(q\) 为有理函数。因为
\[
\Delta^2v_j=C a_j,
\]
除以 \(v_j\) 后得到
\[
\frac{C a_j}{v_j}
=1-\frac2{q(j)}+\frac1{q(j)q(j-1)}.
\]
右端不是零有理函数，因此存在非零有理函数 \(R\)，使
\[
v_j=C a_jR(j).
\]
定义多项式
\[
D_j=\frac{a_{j-1}}{a_j}
=\frac{2(j-1)(2j+2\epsilon-1)}{c}.
\]
代回二阶差分，得到有理函数恒等式
\[
\boxed{R(j)-2D_jR(j-1)+D_jD_{j-1}R(j-2)=1.}
\]
其成立于充分大的整数就意味着它作为有理函数恒等成立。

如果 \(R\) 有有限复极点，选取实部最小的一个 \(p\)。在 \(j=p\) 处，\(R(j)\) 有极点，而 \(R(j-1)\)、\(R(j-2)\) 若有极点，就要求 \(R\) 在 \(p-1\) 或 \(p-2\) 有极点，与最小性矛盾。多项式系数不会引入新极点。因此该极点不能抵消，矛盾。

故 \(R\) 无有限极点，是多项式。若其次数为 \(d\ge0\)，恒等式左边最后一项的次数为 \(d+4\)，前两项分别至多为 \(d\)、\(d+2\)；最高次项系数非零，不能得到常数 \(1\)。再次矛盾。

于是 \(C=0\)。全部有理比值解恰为
\[
v_j=A+Bj,\qquad
\boxed{e_j=\left(1+\frac{2\epsilon-1}{2j}\right)
\frac{A+Bj}{A+B(j-1)}}.
\]
反向直接代入 \(\Delta^2v=0\) 即成立。
这覆盖全部有理次数，并排除了最小解具有有理相邻比值的可能。

若进一步要求 \(z_0=1\)，则 \(A=1\)。\(B=0\) 为刚性解；\(B\ne0\) 时令 \(B=1/(\tau+1)\)，得到源文的 \(E^{(\tau)}\) 族。若要求比值从第 1 项开始处处有定义，还必须排除导致 \(A+B(j-1)=0\) 的参数，不能只看 \(\tau\ne-1\)。允许最终定义的轨迹则可在零点之后使用同一有理式。

这份补证未写回仓库，不能据此声称其研究状态或 canonical 图已经升级。

## F. 原降阶定理的最小修复

在需要使用的指标范围明确假设 \(E_j\ne0\)，或直接限定 \(E\) 为正的 \(E^+\)、\(E^-\)。令 \(r_j=z_j/E_j\)、\(s_j=r_j-r_{j-1}\)，正确收集项得到
\[
0=E_js_j+(a_2E_{j-2}+a_3E_{j-3})s_{j-1}
+a_3E_{j-3}s_{j-2}.
\]
于是源文最终的二阶递推式正确。
反向构造可用 \(r_0,s_1,s_2\) 初始化，先得到 \(r_1,r_2\)，再由二阶递推求其余 \(s_j\)，并令 \(r_j=r_0+\sum_{k=1}^j s_k\)、\(z_j=E_jr_j\)。不应省去零下标的构造。
