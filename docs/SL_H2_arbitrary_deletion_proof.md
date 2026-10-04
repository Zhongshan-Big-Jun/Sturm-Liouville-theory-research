# 第二左定空间中任意保留指标集的稠密性判据

**活动版本: 第十四轮解析补证. 独立审查及确切版本身份另见本轮报告; 未宣称 Lean 或 canonical 接收.**

核对版本：`a815803a6492951cbed010624b42805fb1b49bd8`。
当前来源 `literature/absorption-20260923/approximation/notes/04_infinite_deletions.md` 只闭合了完整等差数列子类与倒数可求和子类；其最后一节明确保留一般发散、非等差情形。本补证在固定 c>0、真实第二左定空间中填补该稠密性判定缺口。

## 1. 精确对象与定理

使用复 L²(−1,1)，内积第一变量线性。令

\[
K_cf=-f''+cf,\quad
D(K_c)=\{f\in H^2(-1,1):f'(1)=f'(-1)=(f(1)-f(-1))/2\},\quad c>0.
\]

记 \(\mathcal H_c^2=D(K_c)\)，范数 \(\|f\|_{\mathcal H_c^2}=\|K_cf\|_2\)。Kc 是严格正自伴算子，作为 \(\mathcal H_c^2\to L^2\) 的映射是等距同构。所有以下 p 均属于此真实定义域：

\[
p_0=1,\quad p_1=x,\quad
p_{2m}=x^{2m}-\frac m{m-1}x^{2m-2},\quad
p_{2m+1}=x^{2m+1}-\frac m{m-1}x^{2m-1},\qquad m\ge2.
\]

任取 J⊂{0,1}、Sₑ,Sₒ⊂{2,3,…}，保留指标

\[
N=J\cup\{2m:m\in S_e\}\cup\{2m+1:m\in S_o\},\qquad
Y_N=\overline{\operatorname{span}_{\mathbb C}\{p_n:n\in N\}}^{\mathcal H_c^2}.
\]

没有余有限、等差数列、正自然密度等额外假设。定义级数允许有限集合；有限集合的和当然有限。

**定理 A。**

\[
Y_N=\mathcal H_c^2
\iff
J=\{0,1\},\quad
\sum_{m\in S_e}\frac1m=\infty,\quad
\sum_{m\in S_o}\frac1m=\infty.\tag{A}
\]

更具体地，若两级数均发散，则

\[
Y_N=\{f\in\mathcal H_c^2:
0\notin J\Rightarrow f(0)=0,\quad
1\notin J\Rightarrow f'(0)=0\}.\tag{B}
\]

若至少一级数收敛，则 YN 的余维为无穷。

(B) 给出了发散情形的完整闭包；收敛情形只给出不稠密与无限余维，**不宣称已写出其全部空间元素的精确描述**。本定理也不处理其他左定阶数、一般非对角 Hilbert 空间或由任意连续约束产生的筛选族。

## 2. 既有的完整高阶尾部输入

当前仓库已证明

\[
\overline{\operatorname{span}\{p_{2m},p_{2m+1}:m\ge2\}}^{\mathcal H_c^2}
=V_*:=\{f:f(0)=f'(0)=0\}.\tag{T}
\]

这是第二左定空间的两迹结果，也是 `tools/krein-cofinite-closure-all-orders.md` 在 s=2、删除 p₀,p₁ 的特例。Kc 反射不变，两个奇偶子空间正交且在 Kc 下保持；对 (T) 作连续奇偶投影，可分别得到完整偶尾、奇尾的闭包。

本补证只使用这个已证的 s=2 输入，既不依赖全部分数阶结果，也不把“扩大后的单项式空间稠密”当作原差分族稠密。

## 3. 有界解析函数的零点引理

**引理。** 若 H 在右半平面 Re z>0 解析且有界，且 H(tⱼ)=0，其中 tⱼ 为互异、趋于正无穷的正实数，满足 \(\sum_j1/t_j=\infty\)，则 H 恒等于零。

证明：令 ζ=(z−1)/(z+1)，把 H 变为单位圆盘的有界解析函数。对充分大的 tⱼ，像点 ζⱼ∈(0,1)，且

\[
1-|\zeta_j|=\frac2{t_j+1}.
\]

非零有界圆盘解析函数的零点满足 Blaschke 条件 Σ(1−|ζⱼ|)<∞。为完整起见，这由 Jensen 公式直接得到：写圆盘函数 F(ζ)=H((1+ζ)/(1−ζ))=ζ^k G(ζ), 其中 G(0)≠0 且 G 有界. 先除去原点的有限阶零点；对不穿过零点的半径 r，有

\[
\sum_{|a_j|<r}\log\frac r{|a_j|}
\le\log\|G\|_\infty-\log|G(0)|.
\]

令 r↑1，再用 −log t≥1−t 即得 Blaschke 条件，与所给级数矛盾。除去原点有限阶零点不影响有界性：外环用 |ζ| 远离零控制，内圆盘用可去奇点后的连续性控制。证毕。

该经典引理及同一半平面映射可对照 Lukas Liehr, *Translation-based completeness on compact intervals*, Journal of Approximation Theory 305 (2025), 106104, §2 Lemma 2.1，DOI `10.1016/j.jat.2024.106104`。这里没有使用其 Gaussian 平移定理，只使用经典零点引理；下面的 Krein 适配另行证明。

## 4. 真实 L² 障碍产生的 Mellin 函数

先处理偶支。设 g∈Hc² 与所选偶支全部正交，取它的偶部并令 w=Kc g∈L² 为实际向量。限制到 (0,1)，记 h=w|_(0,1)。由于区间有限，h∈L¹∩L²。

定义

\[
M(z)=\int_0^1h(t)t^z\,dt.
\]

M 在 Re z>−1/2 解析；在 Re z≥0 上有 |M(z)|≤∥h∥₁，并在 z=0 从右连续。解析性可在每个更小闭半平面上用 Cauchy–Schwarz 控制 t^z(log t)^k 后对积分求导；这里只需 Re z>0 的部分。

通过 Kc 等距性，原正交条件是 ∫w Kc p=0，而不是任意指定的一串形式矩。偶函数在 (−1,1) 上积分恰为其半区间积分的两倍；该非零常数不影响正交条件。

由真实二阶微分作用，偶支有

\[
K_cp_{2m}=ct^{2m}-\left(2m(2m-1)+\frac{cm}{m-1}\right)t^{2m-2}
+2m(2m-3)t^{2m-4}.
\]

令 z=2m−4，定义

\[
H_e(z)=c(z+2)M(z+4)
-(z+4)[(z+2)(z+3)+c]M(z+2)
+(z+2)(z+4)(z+1)M(z).\tag{E}
\]

逐项代入可知

\[
H_e(2m-4)=(2m-2)\int_0^1h(t)K_cp_{2m}(t)\,dt.\tag{E1}
\]

这是恒等式，不在被删除的指标上假设递推成立。

每个系数都是次数至多 3 的多项式，所以

\[
\Phi_e(z)=\frac{H_e(z)}{(z+1)^3}
\]

在 Re z>0 解析且有界。理由是该半平面 |z+1|≥1，且每个固定 a≥0 的 |z+a|/|z+1| 有统一上界，M 的所有非负平移也有同一 L¹ 界。

若 Σ_(m∈Sₑ)1/m=∞，舍去可能的 m=2 不改变发散，Φₑ 在正实数 2m−4 上有一列违反 Blaschke 条件的零点。由第 3 节引理，Hₑ≡0。于是 (E1) 对所有 m≥3 给出正交性；m=2 由 z↓0 的连续性得到。因此，任一消去所选偶支的真实向量，也消去全部偶尾。

**关键区别：**我们没有把离散递推穿过缺口硬补出来；是先从实际 L² 向量构造有界解析函数，再用零点唯一性证明那些额外等式。

## 5. 奇支与发散侧闭包

取实际奇向量 w，仍直接限制到 (0,1) 定义 M；不作 t=x² 换元，因而没有遗漏权重或 Jacobian。

定义

\[
H_o(z)=c(z+2)M(z+5)
-(z+4)[(z+2)(z+5)+c]M(z+3)
+(z+2)(z+4)(z+3)M(z+1).\tag{O}
\]

由

\[
K_cp_{2m+1}=ct^{2m+1}-\left(2m(2m+1)+\frac{cm}{m-1}\right)t^{2m-1}
+2m(2m-1)t^{2m-3}
\]

可得与 (E1) 相同的恒等式：Hₒ(2m−4)=(2m−2)∫h Kc p₂ₘ₊₁。Hₒ/(z+1)³ 同样有界解析。奇支倒数和发散遂强迫全部奇尾正交。

因此，在两级数均发散时，所选高次族与完整高次族具有相同的正交补，闭包都等于 V*。又 p₀、p₁ 的中心迹分别为 (1,0)、(0,1)，高次族的两迹全零；V* 闭，添加有限维空间保持闭性，故得到 (B)。两个迹在 Hc² 中连续，缺失的仿射方向不能由高次尾恢复。因此发散情况下 (A) 成立。

## 6. 收敛侧：先扩大为单项式空间，再构造真实障碍

偶支定义去重指数集

\[
E_e=\{0\}\cup\bigcup_{m\in S_e}\{2m,2m-2,2m-4\};
\]

奇支定义

\[
E_o=\{1\}\cup\bigcup_{m\in S_o}\{2m+1,2m-1,2m-3\}.
\]

这些都是非负整数。包括仿射指数，即使相应仿射列没有保留，也只会扩大比较空间。若对应 Σ1/m 收敛，则 Σ_(α∈E)1/(α+1)<∞。

以下给出不依赖黑箱 Full Müntz 的 L² 证明。对有限互异实指数 αⱼ≥0、q>−1/2 且 q 不等于任一 αⱼ，Cauchy Gram 矩阵的 Schur 行列式公式给出

\[
\operatorname{dist}^2\left(t^q,\operatorname{span}\{t^{\alpha_1},\ldots,t^{\alpha_M}\}\right)
=\frac1{2q+1}\prod_{j=1}^M
\left(\frac{q-\alpha_j}{q+\alpha_j+1}\right)^2.\tag{C}
\]

证明细节：Gram 元素为 ∫t^(αᵢ+αⱼ)=1/(αᵢ+αⱼ+1)，追加 t^q 后的 Gram 行列式与原行列式之比就是距离平方。对两矩阵分别使用 Cauchy 行列式公式，原指数之间的差和因子消去，留下 (C)。Gram 正定来自不同指数函数的线性无关性。

取 q=1/2，则 q 不在整数集 E 中。对充分大的 α，绝对乘积因子为

\[
\frac{\alpha-q}{\alpha+q+1}=1-\frac{2q+1}{\alpha+q+1}.
\]

由于这些缺量的和有限，无限乘积严格为正；有限前缀因 q∉E 也无零因子。令有限指数集穷尽 E，距离单调趋于到闭线性包的距离，故

\[
W_E=\overline{\operatorname{span}\{t^\alpha:\alpha\in E\}}^{L^2(0,1)}
\ne L^2(0,1).
\]

这与 Erdélyi–Johnson 的 Full Müntz 定理在本非负离散指数子类的必要性一致；一般定理没有被用于原差分族的反向推论。

选非零 h∈W_E^⊥。偶支作偶延拓 w(x)=h(|x|)/√2；奇支作奇延拓 w(x)=sgn(x)h(|x|)/√2。对应的 Kc p 列都由 E 中的单项式组成，故 w 与相应全部所选 Kc p 正交；另一奇偶支自动正交。取真实 g=Kc^(-1)w，得到 g∈Hc² 非零，且与全部保留列正交。于是 (A) 的必要性得证。

## 7. 为什么收敛侧的余维是无穷

若 W_E 余维有限，由所有整数单项式在 L²(0,1) 中稠密，它们在有限维商空间中的像线性张满该商。故存在有限个额外单项式使 W_E 加上其线性包等于整个 L²。可是给 E 添加有限个非负整数不改变倒数和收敛，而 (C) 仍说明扩大的闭包不是整个 L²，矛盾。因此 W_E^⊥ 无限维。

第 6 节的延拓和 Kc^(-1) 都是单射，遂将这个无限维障碍空间送入 YN 的正交补。故 codim YN=∞。有限 S 的结论可直接由有限维多项式空间得到，也被同一论证覆盖。

## 8. 对仓库状态的准确改变

本结果若通过独立复审，可将 A11 拆分为：

- **任意保留集在 Hc² 中的稠密性判定：已证充要条件 (A)。**
- **两支发散时的精确闭包：已证两迹式 (B)。**
- **至少一支收敛：已证无限余维，但一般稀疏闭包的全部元素尚未作具体描述。**

不能将一般 A3/A4 的非对角矩可表示性、其他阶数、稳定基、误差速度或完整形式化连带标成已解。这里从一开始使用真实 L² 障碍，不需要声称任意满足离散递推的形式矩都可表示。

本轮脚本用 SymPy 核对了 (E1)/(O) 的系数恒等式，并在三个有限指数集上核对 (C)。这些有限检查只是防止代数抄写错误；全指标和无穷维结论由上述解析论证承担。

## 来源

1. 当前仓库 `literature/absorption-20260923/approximation/notes/04_infinite_deletions.md`：原问题、真实 Kc 传输、两子类及尚缺的反向桥梁。
2. 当前仓库 `tools/krein-cofinite-closure-all-orders.md`：只使用 s=2 的完整高尾两迹闭包。
3. Lukas Liehr, *Translation-based completeness on compact intervals*, J. Approx. Theory 305 (2025), 106104, §2 Lemma 2.1；DOI `10.1016/j.jat.2024.106104`。仅引用经典 Blaschke 零点条件。
4. T. Erdélyi, W. B. Johnson, *The “Full Müntz Theorem” in Lp[0,1] for 0<p<∞*, J. Analyse Math. 84 (2001), 145–172；作者稿 `https://people.tamu.edu/~terdelyi/papers-online/bill.pdf`。仅作单项式必要性的对照；本稿另给 Cauchy Gram 距离证明。

外部经典引理定点核对: [Liehr 作者预印本 v1, §2 Lemma 2.1](https://arxiv.org/html/2409.17563v1), [Erdelyi-Johnson 作者稿, Theorem 1.3](https://people.tamu.edu/~terdelyi/papers-online/bill.pdf). 本文的 Krein 适配和 Cauchy 距离乘积由正文独立推导, 不调用 Gaussian 平移定理.
