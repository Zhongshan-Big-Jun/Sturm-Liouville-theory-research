# 第二左定空间中余有限稀疏子族的精确闭包

日期：2026-09-21。审查基线：`c0b36b90004cffb0552c9fa9f229e1f7cec8a706`。

本文是第五轮审计给出的替代证明，不是原仓库已有定理的转录。未写回仓库，未作 Lean 形式化，未声称整个 O1′LD 已解决。以下结论由解析论证承担，随附程序仅核对代数恒等式与有限实例。

## 1. 设定与需要纠正的命题

固定实数 c>0，在 L²(-1,1) 中考虑

\[
K_cf=-f''+cf,\qquad
\mathcal H_c^2=D(K_c)
=\{f\in H^2_{\rm Sob}(-1,1):f'(1)=f'(-1)=[f(1)-f(-1)]/2\}.
\]

使用左定范数 \(\|f\|_{\mathcal H_c^2}=\|K_cf\|_2\)。内积取第一变量线性。所有函数和线性空间均允许为复数。

令
\[
D=\{0,1\}\cup\{4,5,6,\ldots\},\quad p_0=1,\quad p_1=x,
\]
\[
p_{2m}=x^{2m}-\frac m{m-1}x^{2m-2},\qquad
p_{2m+1}=x^{2m+1}-\frac m{m-1}x^{2m-1},\quad m\ge2.
\]
定义 \(q_n=K_cp_n\)。与原仓库的 H² 定义和多项式族一致，不使用失效的高阶推广。

被替代的命题在以下当前被工具卡引用的证明包中：

`runs/rigorous-open-math-research/R-20260823T030000Z-leftdef-o1pld/candidate_proof.md`

其中 Claim 4、Theorem 5、Corollary 6 均标为 NOT-YET-STRICT。本轮证明它们按原陈述为假，而不是把它们误称为已验收定理。

## 2. 一个显式非零 L² 障碍

置 a=√c，定义
\[
g_{0,c}(x)=\frac{\cosh(a(1-|x|))}{2a\sinh a}.
\]

这是连续、非零、严格为正的 L² 函数。在 (-1,0) 与 (0,1) 上分别有
\[
-g_{0,c}''+cg_{0,c}=0.
\]
并有
\[
g_{0,c}'(-1)=g_{0,c}'(1)=0,\quad
g_{0,c}(1)=g_{0,c}(-1),\quad
g_{0,c}'(0-)={1\over2},\quad g_{0,c}'(0+)=-{1\over2}.
\]

对任意 f∈D(K_c)，在两个半区间分别分部积分。端点项因 Krein 条件抵消，零点处由导数跳跃留下 f(0)，得到
\[
\boxed{\langle K_cf,g_{0,c}\rangle_{L^2}=f(0).}
\]

这是对所有 f 的解析恒等式，不是采样结果。因此
\[
\langle q_0,g_{0,c}\rangle=1,\qquad
\langle q_n,g_{0,c}\rangle=0\quad(n\in D\setminus\{0\}).
\]

令 N=D\{0}。它是余有限集，而其 q_n 的闭线性包包含于非平凡闭超平面 \(g_{0,c}^\perp\)，不可能等于 L²。

另令
\[
V=\{f\in\mathcal H_c^2:f(0)=0\}.
\]
零点求值在 H²Sob 中连续，且 H²Sob 与左定范数在 D(K_c) 上等价，故 V 是真闭子空间。它恰好排除 p_0 而保留所有其余 p_n。于是“真闭子空间必排除无穷多个 p_n”的原推论也被否定。

### 尾部矩刚性也被同一个函数否定

取 \(M_k=\langle g_{0,c},x^k\rangle_2\)。因为 g 为实函数，上述正交关系也给出 \(\langle g_{0,c},q_n\rangle=0\)。故对所有 m≥2：
\[
cM_{2m}=\left[2m(2m-1)+\frac{cm}{m-1}\right]M_{2m-2}
-2m(2m-3)M_{2m-4}.
\]
所有奇矩为零，奇侧递推同样成立。然而
\[
\boxed{M_0=\int_{-1}^1g_{0,c}(x)\,dx=\frac1c\ne0.}
\]

因此原 Claim 4 不仅不能排除“特殊衰减解”，这种 L² 可实现的非零矩序列实际上明确存在。原低阶完备性证明需要 q_0、q_1 的正交条件来固定初始矩，本反例没有满足对 q_0 的正交性，不与该主定理冲突。

## 3. 真正正确的余有限分类

### 定理

对任意 N⊆D，若 D\N 有限，则
\[
\boxed{
\overline{\operatorname{span}\{p_n:n\in N\}}^{\mathcal H_c^2}
=
\{f\in\mathcal H_c^2:
0\notin N\Rightarrow f(0)=0,
\quad 1\notin N\Rightarrow f'(0)=0\}.
}
\]
因此
\[
\boxed{
\overline{\operatorname{span}\{q_n:n\in N\}}^{L^2}=L^2
\quad\Longleftrightarrow\quad 0,1\in N.
}
\]
这是 s=2 的结论。没有将其外推到 s=3 或其他阶数。

### 证明准备：范数与迹

K_c≥cI 给出 \(\|f\|_2\le c^{-1}\|K_cf\|_2\)。又
\[
\|f''\|_2\le c\|f\|_2+\|K_cf\|_2\le2\|K_cf\|_2.
\]
区间上的基本 Sobolev 估计 \(\|f'\|_2\le C(\|f''\|_2+\|f\|_2)\) 于是给出一侧范数控制，反向由三角不等式直接得到。故左定范数与 H²Sob 范数等价。值迹、导数迹在 H²Sob 中连续。

记
\[
V_*:=\{f\in\mathcal H_c^2:f(0)=f'(0)=0\}.
\]

### 引理 A：任意充分高的完整尾部都在 V_* 中稠密

固定 m₀≥2，令 L=2m₀−2（正偶数），并令
\[
\mathcal T_{m_0}=\operatorname{span}\{p_{2m},p_{2m+1}:m\ge m_0\}.
\]
先证明代数等式
\[
\mathcal T_{m_0}=\mathbb C[x]\cap D(K_c)\cap x^L\mathbb C[x].
\]
左侧每个成员都满足边界条件且被 x^L 整除。反向对右侧多项式作首项消去：只要最高次数 n≥L+2，就减去相应首项系数乘 p_n，保留域条件与整除条件。最后余式只能是 αx^L+βx^(L+1)。定义边界残差
\[
B(f)=\begin{pmatrix}f'(1)-[f(1)-f(-1)]/2\\
f'(-1)-[f(1)-f(-1)]/2\end{pmatrix}.
\]
因为
\[
B(x^L)=\binom{L}{-L},\qquad B(x^{L+1})=\binom{L}{L},
\]
两列的行列式为 2L²≠0，余式只能为零。代数等式成立。

现在取任意 f∈V_*。选光滑截断 η_δ：在 |x|≤δ 为零，在 |x|≥2δ 为一，\(|\eta_\delta^{(k)}|\le C\delta^{-k}\)（k≤2），且 δ<1/4。置 f_δ=η_δ f。零点的两个迹为零意味着
\[
f'(x)=\int_0^x f''(t)dt,\qquad
f(x)=\int_0^x(x-t)f''(t)dt.
\]
在 |x|<2δ 上可得
\[
\|f'\|_2\le C\delta\|f''\|_2,
\qquad\|f\|_2\le C\delta^2\|f''\|_2,
\]
此处左右范数均限制在该小邻域。对 η_δ f−f 求导两次，利用这些估计得到
\[
\|f_\delta-f\|_{H^2_{\rm Sob}}
\le C\|f''\|_{L^2(|x|<2\delta)}+o(1)\longrightarrow0.
\]
截断在两个端点附近恒为一，故 f_δ 仍满足 Krein 边界条件。

f_δ 在零点邻域恒为零，因此 h_δ=f_δ/x^L（在零点附近延为零）属于 H²Sob。取多项式 r_j→h_δ 于 H²Sob，则 b_j=x^Lr_j→f_δ 于 H²Sob。

这里多项式的 H²Sob 稠密性可直接证明：先在 L² 中用多项式逼近 h_δ''，再积分两次并匹配 h_δ(-1)、h_δ'(-1)。无需把不相容的单项式放入算子域。

b_j 还可能有端点残差。由于 B 连续且 B(f_δ)=0，B(b_j)→0。用固定的两维矩阵
\[
\begin{pmatrix}L&L\\-L&L\end{pmatrix}
\binom{\alpha_j}{\beta_j}=B(b_j)
\]
定义 α_j、β_j，则两者趋于零。令
\[
\widetilde b_j=b_j-\alpha_jx^L-\beta_jx^{L+1}.
\]
它满足 B(\widetilde b_j)=0，仍被 x^L 整除，且在 H²Sob 中趋于 f_δ。根据代数等式，\(\widetilde b_j\in\mathcal T_{m_0}\)。先取小 δ 再取大 j，证明 \(\overline{\mathcal T_{m_0}}=V_*\)。反向包含由两个连续迹和全部尾部多项式的零迹直接成立。

### 完成定理

N 余有限，所以包含某个完整尾部，故其闭线性包包含 V_*。每个 n≥4 的 p_n 都在 V_* 中；只有 p_0、p_1 提供迹方向
\[
\Gamma(p_0)=(1,0),\qquad\Gamma(p_1)=(0,1),\quad
\Gamma(f)=(f(0),f'(0)).
\]
因此该闭线性包恰为 V_* 加上 N 中保留的两个低阶方向。等价地就是定理右侧的迹条件空间。K_c 的等距满射把此结论传到 L²，得到所述充要条件。证毕。

## 4. L² 中的完整障碍表示

导数迹对应的另一个 L² 函数为
\[
g_{1,c}(x)=\frac{\operatorname{sgn}(x)\,[a\cosh(a(1-|x|))-\sinh(a(1-|x|))]}
{2(a\cosh a-\sinh a)},\qquad a=\sqrt c.
\]
零点的值任取。分母严格为正：函数 a cosh a−sinh a 在 a=0 为零，导数 a sinh a>0。

它是奇函数，在零点具有单位跳跃，导数在零点两侧相等，且在端点满足 \(g'_{1,c}(1)=g_{1,c}(1)\)。分别分部积分可得
\[
\langle K_cf,g_{1,c}\rangle=f'(0).
\]
注意 g₁ 本身有跳跃，只需属于 L²；不将它误当成 D(K_c) 成员。

对余有限 N，有精确障碍空间
\[
\boxed{
\bigl(\overline{\operatorname{span}\{q_n:n\in N\}}\bigr)^\perp
=\operatorname{span}\bigl(\{g_{0,c}:0\notin N\}\cup\{g_{1,c}:1\notin N\}\bigr).
}
\]

## 5. 对实际受约束子空间的含义

若 V⊆\(\mathcal H_c^2\) 是闭子空间，实际保留集
\(N_V=\{n\in D:p_n\in V\}\) 余有限，那么引理 A 强迫 V 包含 V_*。特别地，V 必保留所有 n≥4 的 p_n，真正能被排除的只剩 p_0、p_1。

不过，“只排除有限项”不保证保留族在 V 中稠密。取
\[
V=\{f:f(0)=f'(0)\}.
\]
它包含 V_* 和非零方向 1+x，却不包含 1 或 x。实际保留集是 D\{0,1}，其闭线性包仅为 V_*，严格小于 V。

因此这个余有限子类可以归结为二维迹空间中的线性代数，而不是“所有真闭子空间都排除无穷多项”。一般非余有限子族的 O1′LD 不由此自动解决。

## 6. 同一证明包中 Lemma 1 的局部修复

原奇部换元 f_o(x)=x h_o(x²) 写成
\[
\int_{-1}^1|f_o(x)|^2dx=\frac12\int_0^1|h_o(y)|^2y^{1/2}dy.
\]
右端不应有 1/2。取 f_o=x 即得到原式 2/3=1/3 的反例。

“从全部单项式中删去有限项仍在 L² 稠密”这个结论本身正确，而且有更短证明：若 f 正交于所有保留单项式，取 M 大于所有被删次数，则对任意多项式 p 有
\[
\langle x^M f,p\rangle=0.
\]
x^M f∈L²，全体多项式在 L² 中稠密，故 x^M f=0；而 x^M≠0 几乎处处，故 f=0。这个证明不需要奇偶换元或额外的 Müntz–Szász 定理。

必须区分：该结论适用于单项式 \(x^k\)，不适用于已经变成 \(q_n=K_cp_n\) 的像族。
