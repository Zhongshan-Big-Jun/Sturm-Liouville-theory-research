# 投影稠密性与有限矩准则：反例和最小修复

日期：2026-09-21。版本：`92d46e99e36cc0a74e8f7bb13430749c222ee54f`。
本附录是本轮独立推导，不是原仓库既有验收记录。尚未写回仓库，未作 Lean 形式化。

## 1. 目标与证据状态

`runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`
的 Theorem 1 正确声称 \(P_V\Pi\) 在闭子空间 \(V\) 中稠密，但又称“特别地”
\(\operatorname{span}\{P_Vp_n\}\) 稠密，并以 \(\operatorname{span}\{p_n\}=\Pi\) 为依据。
后一个代数等式不成立。该 run 的 `audit_report.md` 仍对 Theorem 1 记录 PASS，
当前 `research_map.md` 仍将该结构结果作为 A4 上游。

错误不在连续投影保持全体多项式的稠密性，而在被投影的输入族被替换了。

## 2. 有限余维、非零约束下的显式反例

令 \(H_2\) 为复多项式在
\[
\langle x^j,x^k\rangle=\delta_{jk}(k+1)^4
\]
下的完备化。下标 2 在这里是对角权重参数 \(\beta=2\)，**不是第二左定空间**。

每个元素的系数满足 \(\sum|a_k|^2(k+1)^4<\infty\)，由 Cauchy–Schwarz 有
\(\sum|a_k|<\infty\)，故可实现为 \([-1,1]\) 上连续函数，且在开区间内为幂级数。
所有多项式属于空间并稠密，符合原定理设置。

取
\[
V=\ker M_0=\{f:\langle f,1\rangle=0\}.
\]
它是闭余维一子空间，约束表示元是有限多项式 1。正交投影仅删除常数系数：
\[
P_Vp_0=0,\qquad P_Vp_n=p_n\quad(n\ne0).
\]
其实际保留集为 \(N=\mathcal D\setminus\{0\}\)。

构造
\[
w=\sum_{m=1}^{\infty}\frac{m}{(2m+1)^4}x^{2m}.
\]
有
\[
0<\|w\|^2=\sum_{m\ge1}\frac{m^2}{(2m+1)^4}
\le\frac1{16}\sum_{m\ge1}\frac1{m^2}<\infty.
\]
其矩为
\[
M_0=M_1=0,\qquad M_{2m}=m,\qquad M_{2m+1}=0.
\]
因此 \(w\in V\setminus\{0\}\)，并且对所有 \(m\ge2\)，
\[
\langle w,p_{2m}\rangle
=m-\frac{m}{m-1}(m-1)=0.
\]
奇项由奇偶矩为零，\(p_1=x\) 也为零。因此
\[
\langle w,P_Vp_n\rangle=0\quad\forall n\in\mathcal D.
\]
但 \(\langle w,x^2\rangle=1\)，且 \(x^2\in V\)。投影后的稀疏族不能在 \(V\) 中稠密。

该反例不使用无限多个约束，不使用无法实现的形式矩，也不需要非对角内积。
在原定理声称覆盖的对角子类中已经失败。

## 3. Corollary 1.1 的充要判据也失效

原推论说，筛选族 \(\mathcal Q_V=\{p_n:p_n\in V\}\) 在 \(V\) 中稠密，
当且仅当每个被排除成员的投影 \(P_Vp_n\) 都属于筛选族闭包。

在上述反例中，只有 \(p_0\) 被排除，而 \(P_Vp_0=0\) 显然在闭包里。
故推论右侧成立，左侧却不成立。它不只是丢失一种证明方法，而是错误的充要判据。

## 4. 投影结论的准确修复

令
\[
M=\overline{\operatorname{span}\{p_n\}}^{H}.
\]
对任意闭 \(V\subset H\)，精确等价条件为
\[
\boxed{\overline{\operatorname{span}\{P_Vp_n\}}=V
\iff V\cap M^\perp=\{0\}.}
\]
证明：对 \(w\in V\)，有 \(\langle w,P_Vp_n\rangle=\langle w,p_n\rangle\)。
故投影族在 \(V\) 内的正交补就是 \(V\cap M^\perp\)。

三种最小改法如下，按所需用途选择：

- 保留无条件的 \(\overline{P_V\Pi}=V\)，删除稀疏族的“特别地”。
- 明确增加 \(\overline{\operatorname{span}\{p_n\}}=H\) 这一充分假设。
- 不增加假设，但补回 \(x^2,x^3\)：
  \[
  \boxed{\overline{\operatorname{span}\bigl(\{P_Vp_n\}\cup\{P_Vx^2,P_Vx^3\}\bigr)}=V.}
  \]
  这是因为 \(\Pi=\operatorname{span}(\{p_n\}\cup\{x^2,x^3\})\)。

原 Corollary 1.1 的正确无条件版本应是：筛选族稠密，当且仅当全部被排除的
\(P_Vp_n\) **以及** \(P_Vx^2,P_Vx^3\) 都属于筛选族闭包。
若已另外证明原稀疏族在整个 \(H\) 中稠密，则原先简化的判据才可以保留。

这不影响已经有全族稠密性输入的具体 Krein 低阶投影定理。也不自动推翻后续独立通过矩可表示性证明的对角或带状子类判据；应按真实依赖分别核对。

## 5. 上游 Theorem F：附加假设相互矛盾

目标：
`runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md`
第 5 节 Theorem F。

该定理要求：

1. \(V\) 包含从某处起的全部偶、奇 \(p_n\)。
2. 不存在非零 \(w\in V\)，同时正交于有限个低阶保留成员并满足 \(M_2=M_3=0\)。

第一项使 \(V\) 包含无限多个次数不同、线性无关的多项式，所以 \(V\) 无限维。
第二项却要求有限个线性泛函在 \(V\) 上共同具有零核。

若有限个低阶测试共有 \(r\) 个，定义
\[
F:V\to\mathbb C^{r+2},\qquad
w\mapsto(\langle w,p_{n_1}\rangle,\ldots,\langle w,p_{n_r}\rangle,M_2,M_3).
\]
在 \(V\) 内任选 \(r+3\) 个独立尾部多项式，它们张成的子空间上，\(F\) 必有非零核。
故两个假设不能同时成立。

**分类：这不是一个“假设成立而结论失败”的反例；它是一个没有适用实例的空洞条件定理。**
当前工具卡仍将 F/G 概括为可复用的 STRICT 充分准则，因而需要修正文稿与复用入口。
Theorem G 对“如 F 的低阶钉住条件”的交叉引用也必须重新明确，而不能借 F 视为已完成。

## 6. 一个有适用实例的正确尾部准则

设 \(H\) 含全部多项式并以其为稠密子空间，且
\[
\|x^k\|_H\le C(k+1)^\beta,\qquad \beta<1.
\]
给定 \(m_0\ge2\)，令 \(L=2m_0-2\)，并定义
\[
Z_L=\{w\in H:M_k(w)=0\text{ 对所有 }k\ge L\}.
\]

### 引理

原稀疏族从 \(m_0\) 起的完整尾部的正交补恰为 \(Z_L\)。而且 \(\dim Z_L\le L\)。

证明：正交于尾部时，两侧递推给出
\[
M_{2m}=\frac{m}{m_0-1}M_{2m_0-2},\qquad
M_{2m+1}=\frac{m}{m_0-1}M_{2m_0-1},\qquad m\ge m_0.
\]
\(\beta<1\) 的矩界迫使两个尾部初值为零，故全部 \(k\ge L\) 的矩为零。
反向由每个尾部 \(p_n\) 只含这些高阶单项式立即得到。

在 \(Z_L\) 上，\(w\mapsto(M_0,\ldots,M_{L-1})\) 是单射；否则全部矩为零，
多项式稠密性推出 \(w=0\)。所以维数至多为 \(L\)。证毕。

若闭 \(V\) 包含该尾部，令 \(J\) 为低于 \(2m_0\) 的实际保留指标集，则
\[
\boxed{\overline{\operatorname{span}\{p_n:p_n\in V\}}=V
\iff (V\cap Z_L)\cap\bigcap_{n\in J}\ker\langle\,\cdot\,,p_n\rangle=\{0\}.}
\]

正确的有限低阶测试应作用于 **尾部测试之后剩余的有限维障碍空间** \(V\cap Z_L\)，
而不是要求它们杀死整个无限维 \(V\)。
例如 \(m_0=2,V=H_0\) 时，\(Z_2=\operatorname{span}\{1,x\}\)，低阶测试 \(p_0,p_1\)
确实消掉该障碍，给出一个有内容的充分性实例。

## 7. Theorem H 的解释性等价还需更正

同一原稿称约束表示元对 \(x^2,x^3\) “非零检测”与它们属于 \(V^\perp\) 等价。
这不成立。

取对角 \(H_0\)，约束表示元 \(v=x^2+x^3\)。则
\[
\langle v,x^2\rangle=\langle v,x^3\rangle=1,
\]
但
\[
w=x^2-x^3\in V=v^\perp,
\qquad M_2(w)=1,\quad M_3(w)=-1.
\]
约束并未分别钉零两个矩。正确要求是
\[
\boxed{\operatorname{span}\{x^2,x^3\}\subset
V^\perp=\operatorname{span}\{v_1,\ldots,v_r\}.}
\]
这是一处错误解释，不否定主判据 \(V\cap Q^\perp=\{0\}\)。

## 8. 冻结证据与修订方式

旧候选和审计应作为历史保留，另建勘误并在当前工具卡与研究图中明确区分：
投影全体多项式的正确结论、投影原稀疏族的条件结论、F 的新有效障碍空间，以及 H 的准确表示元条件。
不能继续只用旧的 PASS 标签引用被反例否定的“特别地”或充要判据。
