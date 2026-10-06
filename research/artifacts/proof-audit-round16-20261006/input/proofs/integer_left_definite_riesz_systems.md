# 固定整数阶 Krein 左定空间中的 Hermite–Legendre Riesz 替代系

**第十六轮新增解析补证；未合并，未经过另一位审稿人的独立复核，未作 Lean 验证。**

基线为 `ec45bf99ae746b0a3699557e06700a3c00c5a831`。本稿推广的是当前 A10 在 s=2、4 的积分 Legendre 替代系，不改变原稀疏族的成员门槛或非基结论。以下 r 为固定正整数，c 为固定正实数；常数可以依赖二者。

## 1. 模型与整数域

内积对第一变量线性，空间取复数域。设 I=(-1,1)，

\[
K_cf=-f''+cf,\quad
D(K_c)=\{f\in H^2(I): f'(1)=f'(-1)=[f(1)-f(-1)]/2\},
\quad \mathcal H_c^r=D(K_c^{r/2}).
\]

记 \(\mathcal Bf=(f'(1)-\Delta f/2,f'(-1)-\Delta f/2)^T\)，\(\Delta f=f(1)-f(-1)\)。令 m=⌊r/2⌋。所用整数域为

\[
V_r=\{f\in H^r(I):\mathcal B(f^{(2j)})=0,
                 \ 0\le j<m\}.
\tag{1}
\]

当 r=1 时条件为空。对每个整数 r≥1，\(\mathcal H_c^r=V_r\)，且图标度范数与普通 H^r 范数等价。这里没有半整数临界边界条件。

下面给出这一既有输入在整数阶的直接证明和可取的常数，以免将一个空间等同关系藏在未核对的分数域引用中。

### 1.1 第一层型范数

Kc 的闭型为

\[
q_c(f,g)=\int f'\overline{g'}-\tfrac12\Delta f\overline{\Delta g}
                +c\int f\overline g,\quad D(q_c)=H^1(I).
\tag{2}
\]

令 a=Δf/2，h=f-ax。则 Δh=0，

\[
q_c(f,f)=\|h'\|_2^2+c\|f\|_2^2.
\tag{3}
\]

对任意 H1 函数 h，\(\|h-\bar h\|_2\le2\|h'\|_2\)；这可由与平均值比较并积分一阶导数得到。将 f=a x+\bar h+(h-\bar h) 投影到 span{x}，有

\[
\sqrt{2/3}|a|\le\|f\|_2+2\|h'\|_2.
\]

因此

\[
\|f'\|_2\le\sqrt3\|f\|_2+(1+2\sqrt3)\|h'\|_2
\le C_1(c)q_c(f,f)^{1/2},
\quad C_1(c)^2=3/c+(1+2\sqrt3)^2.
\tag{4}
\]

型范数与 H1 等价、q_c≥c||f||²，故型闭且严格正。分部积分和独立的两个端点值表明其关联算子的定义域正是 D(Kc)。由正自伴算子的闭型/平方根对应，\(D(K_c^{1/2})=H^1\)，且平方根范数平方为 q_c。该对应亦可由 Kc 的正交谱展开构造型的完备化得到；这是本模型已有的第一左定空间事实，不是新的谱定理。

### 1.2 任意整数层

偶数 r=2m 时，迭代条件 \(f,K_cf,\ldots,K_c^{m-1}f\in D(K_c)\)，结合 f''=cf-Kcf，给出 (1)。边界条件从 B(Kc^j f)=0 到 B(f^(2j))=0 是三角可逆变换，不需要增加或删除条件。

奇数 r=2m+1 时，谱展开给出

\[
D(K_c^{m+1/2})=\{f\in D(K_c^m):K_c^mf\in D(K_c^{1/2})\}.
\]

由 1.1，右侧的最后条件为 Kc^m f∈H1。对每次方程 -u''+cu=v 作一维正则性递推，即得 f∈H^(2m+1) 及同样 m 组边界条件。反向代入也成立。

可以给出完全显式但不追求最优的等价常数。写

\[
U_{2m,c}^2=\sum_{j=0}^m{m\choose j}^2c^{2(m-j)},\quad
U_{2m+1,c}^2=\max(1,c)\sum_{j=0}^m{m\choose j}^2c^{2(m-j)}.
\tag{5}
\]

二项式展开和 (2) 的负边界项给出 ||f||_(r,c)≤U_(r,c)||f||_H^r。

反向取 \(d=1/2+1/\sqrt2\)。偶数 r=2m 定义

\[
 b_{2j}=2^jc^{j-m}\ (0\le j\le m),\qquad
 b_{2j+1}=\sqrt3b_{2j}+d b_{2j+2}\ (0\le j<m).
\tag{6}
\]

由 f^(2j)=(c-Kc)^j f、Kc≥c 和普通一维不等式
\(\|u'\|_2\le\sqrt3\|u\|_2+d\|u''\|_2\)，有 ||f^(k)||₂≤b_k||f||_(r,c)。

奇数 r=2m+1 定义

\[
 b_{2j}=2^jc^{j-m-1/2},\qquad
 b_{2j+1}=C_1(c)2^jc^{j-m}\quad(0\le j\le m).
\tag{7}
\]

这里 f^(2j)=(c-Kc)^j f 属于第一左定空间；以谱嵌入控制其第一左定范数，再用 (4) 即得奇导数界。于是，令

\[
 V_{r,c}^2=\sum_{k=0}^r b_k^2,
\quad
\|f\|_{H^r}\le V_{r,c}\|f\|_{r,c}.
\tag{8}
\]

(6) 所用普通一维不等式可由 u=A+Bx+∫₀ˣ(x-t)u''(t)dt、两半区间 Cauchy–Schwarz 和 ||A+Bx||²=2|A|²+2|B|²/3 推出；当前 A1/A10 证明也已给出这一不等式。

## 2. 自由端点数据与唯一低阶 Hermite 提升

取自由指标

\[
\mathcal E_r=\{(2j,\pm1):0\le2j<r\},\qquad
 d_r=|\mathcal E_r|=2\lceil r/2\rceil.
\tag{9}
\]

给定 ξ=(ξ_(2j,±))∈C^(d_r)，规定所有偶阶端点导数为这些自由数据；对每个 2j+1<r，规定

\[
p^{(2j+1)}(1)=p^{(2j+1)}(-1)
                  =(\xi_{2j,+}-\xi_{2j,-})/2.
\tag{10}
\]

这样正好规定了两个端点从 0 到 r-1 阶的 2r 个 Hermite 数据。存在唯一次数至多 2r-1 的多项式 \(\mathscr L_r\xi\) 具有这些数据。唯一性可直接证明：若全部端点 jet 为零，则 (x²-1)^r 整除该多项式，和次数小于 2r 矛盾。由维数相等，唯一性同时给出存在性。

记 h_1,...,h_(d_r) 为自由数据标准单位向量的像。这些多项式系数为有理数且与 c 无关，并有

\[
L_r:=\operatorname{span}\{h_j\}
     =\Pi_{2r-1}\cap V_r,\qquad \dim L_r=d_r.
\tag{11}
\]

对 f∈V_r，取 ξ_f 为它的自由偶阶端点数据。由于 f 本身满足 (10)，

\[
g=f-\mathscr L_r\xi_f\in H_0^r(I)
 :=\{g\in H^r:g^{(k)}(\pm1)=0,\ 0\le k<r\}.
\tag{12}
\]

重要区别：偶数 r 时低提升数为 r；奇数 r 时为 r+1。不能把 s=2、4 的“低提升数等于阶数”原样套到奇数阶。

## 3. 积分 Legendre 高阶列

令 e_n=√((2n+1)/2)P_n 为 L2 正交归一 Legendre 系，P_n(1)=1。记

\[
J^kv(x)=\frac1{(k-1)!}\int_{-1}^x(x-t)^{k-1}v(t)dt\ (k\ge1),
\quad b_n^{(r)}=J^r e_n\quad(n\ge r).
\tag{13}
\]

所有 0≤j<r 阶左端迹为零。右端迹为 ∫(1-t)^(r-1-j)e_n(t)dt 的倍数，由 n≥r 和正交性也为零。且 (b_n^(r))^(r)=e_n。

对任意 g∈H0^r，分部积分 r 次表明 g^(r)⊥Π_(r-1)。因此

\[
g^{(r)}=\sum_{n\ge r}z_ne_n,
\quad g=\sum_{n\ge r}z_nb_n^{(r)}\quad\text{在 }H^r\text{ 中收敛}.
\tag{14}
\]

最后一式由有界的逐次积分和左端零数据推出。由于低提升的 r 阶导数次数≤r-1，

\[
z_n=\langle f^{(r)},e_n\rangle_2\quad(n\ge r).
\tag{15}
\]

这给出了可直接提取的系数；它不是在未证明基性质之前预设无穷展开。

## 4. 完整 Riesz 基及显式次数一致界

**定理。** 对每个固定 c>0 和每个整数 r≥1，

\[
\Phi_{r,c}=(h_1,\ldots,h_{d_r},b_r^{(r)},b_{r+1}^{(r)},\ldots)
\tag{16}
\]

是实际空间 \(\mathcal H_c^r\) 的 Riesz 基。对 N≥2r-1，其次数≤N 的上述有限列张成

\[
\Pi_N\cap\mathcal H_c^r,
\qquad \dim=N+1-2\lfloor r/2\rfloor.
\tag{17}
\]

存在不依赖 N 的正数 A_(r,c)、B_(r,c)，使全部有限系数满足

\[
A_{r,c}\|w\|_{\ell^2}^2
\le\|T_rw\|_{r,c}^2
\le B_{r,c}\|w\|_{\ell^2}^2.
\tag{18}
\]

**证明。** (12)–(15) 证明完整性、唯一性和系数的 ℓ² 性。令 C₀=1，并取 J^k 的 Hilbert–Schmidt 上界

\[
C_k=\frac{2^k}{(k-1)!\sqrt{(2k-1)(2k)}}\quad(k\ge1).
\]

记

\[
H_r^2=\sum_{j=1}^{d_r}\|h_j\|_{H^r}^2,
\qquad J_r^2=\sum_{k=0}^rC_k^2.
\]

低提升是一个固定有限矩阵，H_r 可由有理多项式积分精确计算。高部分的普通 H^r 范数不超过 J_r||z||₂，因此

\[
\|T_rw\|_{r,c}\le
 U_{r,c}\sqrt{H_r^2+J_r^2}\|w\|_2.
\]

反向使用端点不等式

\[
|u(\pm1)|\le2^{-1/2}\|u\|_2+\sqrt2\|u'\|_2.
\]

两个端点平方和≤5(||u||²+||u'||²)。自由数据只取偶阶导数，相应相邻导数对互不重复，故

\[
\|\xi_f\|_2^2\le5\|f\|_{H^r}^2,
\qquad\sum_{n\ge r}|z_n|^2\le\|f^{(r)}\|_2^2.
\]

所以 ||w||²≤6V_(r,c)²||f||_(r,c)²。可以取

\[
A_{r,c}=\frac1{6V_{r,c}^2},
\quad B_{r,c}=U_{r,c}^2(H_r^2+J_r^2).
\tag{19}
\]

这些估计扩展到 ℓ²，合成映射为有界双射且逆有界，证明 Riesz 基结论。

若 f 为次数≤N 的域内多项式，减去次数≤2r-1 的低提升后，g^(r) 是次数≤N-r 且正交于 Π_(r-1) 的多项式，只用 e_r,...,e_(N-r) 展开。因此有限列精确张成 (17)。低列从端点 jet 独立，高列从第 r 阶导数独立，列数即给出所列维数。证毕。

s=0 独立采用标准 L2 Legendre 正交基即可。这里没有宣称一套固定、未经重新赋权的 (16) 同时成为所有 r 或非整数 s 的 Riesz 基。

## 5. 稀疏 Gram 结构

恒等式 JP_k=(P_(k+1)-P_(k-1))/(2k+1) 在 k≥1 时具有正确的左端零值。对 n≥r 连用 r 次，在最后一次以前最小索引始终至少为 1，所以

\[
b_n^{(r)}\in\operatorname{span}\{P_{n-r},P_{n-r+2},\ldots,P_{n+r}\}.
\tag{20}
\]

偶数 r=2m 时，Kc^m b_n^(r) 仍具有 (20) 范围内的支撑。奇数 r=2m+1 时，用 q_c(Kc^m b_n,Kc^m b_l) 计算 Gram；高列的 Kc^m 像两端为零，边界项消失。其函数和一阶导数的 Legendre 支撑分别包含于 [n-r,n+r] 与 [n-r+1,n+r-1]。所以所有整数 r 都有

\[
\langle b_n^{(r)},b_l^{(r)}\rangle_{r,c}=0
\quad\text{若 }|n-l|>2r\text{ 或 }n-l\text{ 为奇数}.
\tag{21}
\]

低提升和它的 Kc^m 像次数至多 2r-1，故低–高耦合只可能发生在 n≤3r-1。对奇数阶，涉及低列的边界项也因高列端点为零而消失。这些结论来自精确正交性，不是把浮点小数截断为零。

## 6. 逼近误差与一个新增的三阶例子

在 (14) 中保留 n≤N-r 和全部低提升，可得

\[
\|f-f_N\|_{r,c}\le U_{r,c}J_r
\left(\sum_{n>N-r}|z_n|^2\right)^{1/2}.
\tag{22}
\]

若另有 \(M_t^2=\sum_{n\ge r}(n+1)^{2t}|z_n|^2<\infty\)，则

\[
\|f-f_N\|_{r,c}\le U_{r,c}J_r (N-r+2)^{-t} M_t.
\tag{23}
\]

(23) 的附加条件是明确的系数条件，不把任意“光滑”无条件解释为某个代数或指数收敛率。

r=3 时可把低提升作固定可逆线性变换，写成更容易检查的四列

\[
1,\quad x,\quad \frac{(1-x^2)^2}{8},
\quad \frac{x(1-x^2)^2}{8}.
\]

它们分别指定端点值和二阶端点值的奇偶分量，满足第一组 Krein 条件；再加 \(J^3e_n,n\ge3\)，即得到三阶的完整稳定多项式系。它并不使原稀疏族变成 Schauder 或 Riesz 基。

## 7. 适用边界与可关闭的义务

独立复核通过后，可将 A10 的“存在可构造、次数一致稳定的边界相容多项式替代系”从 s=2、4 扩展到所有非负整数 s；包括奇数阶的 r+1 个低提升。

仍未覆盖：非整数阶的统一稳定基构造、r→∞ 或 c↓0 的一致常数、原稀疏族的稳定坐标、任意新约束下未经调整的同一基、浮点超高次组装的精度认证、完整测度/无限约束问题，以及 ND/G1/M3/KP。

当前来源：
- `literature/absorption-20260923/approximation/notes/03_legendre_krein_construction.md`：仅 s=2、4 的构造、积分引理和带宽思想。
- `tools/krein-integrated-legendre-riesz.md`：活动范围与已有来源归属。
- `tools/krein-fractional-trace-dictionary.md`：整数域与非整数临界情况的区别。
- `docs/SL_fractional_left_definite.tex`：Kc 的实际定义域、正性、自伴性、普通一维估计。

本稿的贡献是一般整数 r 的明确 Hermite 提升、完整域上的 Riesz 证明、显式次数一致上下界及带宽/尾误差，不声称 Hilbert 空间正交展开、Hermite 插值或边界适配思想本身为新结果。有限脚本只核对 r=1,...,6 的有限代数及几个 Gram 恒等式，不替代上述全指标证明。

一般正左定标度的外部基础另对照 Fischbacher–Gesztesy–Hagelstein–Littlejohn, *Abstract Left-Definite Theory: A Model Operator Approach, Examples, Fractional Sobolev Spaces, and Interpolation Theory*, arXiv:2408.01514v1, Theorem 1.1（谱幂域构造）。仅核对这一基础输入，新的 Hermite–Legendre 适配由本稿独立推导，不声称是该论文已有定理。
