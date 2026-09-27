# 原稀疏多项式族的完整非负阶范围：补齐 3 < s < 7/2

日期：2026-09-21。
核对的仓库提交：`92d46e99e36cc0a74e8f7bb13430749c222ee54f`。

**性质：本轮新增解析推导。** 尚未写入仓库，未作 Lean 形式化，也没有另一独立审稿人的验收。本附录给出全指标证明；随附程序的有限检查不是稠密性或级数敛散性的替代证明。

## 1. 对象与结论

令
\[
K_cf=-f''+cf,\qquad c>0,
\]
\[
D(K_c)=\{f\in H^2_{\rm Sob}(-1,1):
f'(1)=f'(-1)=(f(1)-f(-1))/2\},
\]
并令
\[
\mathcal H_c^s=D(K_c^{s/2}),\qquad
\|f\|_s=\|K_c^{s/2}f\|_2,\quad s\ge0.
\]
算子是严格正的自伴算子，且 \(K_c\ge cI\)。本附录只使用非负阶，不讨论负阶完备化的额外表述。

原族的指标集为 \(\mathcal D=\{0,1\}\cup\{4,5,\ldots\}\)，其中
\[
p_0=1,\quad p_1=x,
\]
\[
p_{2m}=x^{2m}-\frac{m}{m-1}x^{2m-2},\quad
p_{2m+1}=x^{2m+1}-\frac{m}{m-1}x^{2m-1},\qquad m\ge2.
\]

### 定理

对每个固定 \(c>0\)：

1. 对每个 \(n\in\mathcal D\setminus\{0,1\}\)，有精确成员阈值
   \[
   p_n\in\mathcal H_c^s\quad\Longleftrightarrow\quad 0\le s<7/2.
   \]
   \(p_0,p_1\) 则属于全部非负幂域。
2. 对所有 \(0\le s<7/2\)，
   \[
   \boxed{\overline{\operatorname{span}\{p_n:n\in\mathcal D\}}^{\mathcal H_c^s}
   =\mathcal H_c^s.}
   \]
3. 对 \(s\ge7/2\)，整个原族不是目标空间的子集。若只保留单个已经属于空间的命名成员，剩下的只有 \(1,x\)，其线性包不是无限维空间 \(\mathcal H_c^s\) 中的稠密子空间。

第三项不排除非相容原成员经线性组合后得到高阶相容多项式，也不否定高阶多项式图核心。

## 2. 所用谱系及其归一化

Krein 模型的完整正交谱系为
\[
1,\quad x,\quad \cos(k\pi x),\quad \sin(\mu_kx),\qquad k\ge1,
\]
其特征值依次为 \(c,c,(k\pi)^2+c,\mu_k^2+c\)，其中
\[
k\pi<\mu_k<(k+1/2)\pi,\qquad \tan\mu_k=\mu_k.
\]
对应的 \(L^2\) 范数平方为
\[
2,\quad 2/3,\quad 1,\quad \frac{\mu_k^2}{1+\mu_k^2}.
\]
最后一个范数有统一正下界，并趋于一。将该谱系归一化为 \(e_j\)，则
\[
\|f\|_s^2=\sum_j\lambda_j^s|\langle f,e_j\rangle_2|^2,
\]
右边有限当且仅当 \(f\in\mathcal H_c^s\)。这组输入也见当前 `docs/SL_fractional_left_definite.tex` 的“对象与可用输入”。

## 3. 成员性：先证明所有原成员都在窗口中

### 引理 1：任意多项式的高频谱系数为 O(k^{-2})

对任意固定多项式 \(g\)，令 \(\omega=k\pi\)。分部积分两次得
\[
\int_{-1}^1g(x)\cos(\omega x)\,dx
=\frac{(-1)^k(g'(1)-g'(-1))}{\omega^2}
-\frac1{\omega^2}\int_{-1}^1g''(x)\cos(\omega x)\,dx.
\]
因此这个系数为 \(O_g(\omega^{-2})\)。

对 \(\mu=\mu_k\)，同样有
\[
\begin{aligned}
\int_{-1}^1g(x)\sin(\mu x)\,dx
={}&-\frac{\Delta g\cos\mu}{\mu}
+\frac{(g'(1)+g'(-1))\sin\mu}{\mu^2}\\
&-\frac1{\mu^2}\int_{-1}^1g''(x)\sin(\mu x)\,dx.
\end{aligned}
\]
利用 \(\cos\mu=\sin\mu/\mu\)，它化为
\[
\frac{\sin\mu}{\mu^2}
\bigl(g'(1)+g'(-1)-\Delta g\bigr)
-\frac1{\mu^2}\int_{-1}^1g''(x)\sin(\mu x)\,dx.
\]
因此也为 \(O_g(\mu^{-2})\)。常数依赖多项式，但不依赖谱指标。

### 引理 2：满足第一层边界条件的多项式的谱系数为 O(k^{-4})

若 \(p\in\mathbb C[x]\cap D(K_c)\)，则 \(K_cp\) 是多项式。对任一高频本征函数 \(\phi\)，自伴性给出
\[
\langle p,\phi\rangle_2
=\frac{\langle K_cp,\phi\rangle_2}{\lambda}.
\]
由引理 1 和 \(\lambda\asymp k^2\)，得到
\[
|\langle p,\phi\rangle_2|=O_p(k^{-4}).
\]
归一化正弦不会改变这个阶数。因此
\[
\sum_j\lambda_j^s|\langle p,e_j\rangle|^2
\quad\text{受常数乘 }\sum_{k\ge1}k^{2s-8}\text{ 控制}.
\]
这在 \(s<7/2\) 时收敛。所有原始 \(p_n\) 满足第一层边界条件，故都属于该窗口。

此处没有把原族的成员性由 \(p_4\) 单个例子外推，也没有在不属于空间的单项式上使用高阶内积。

### 引理 3：每个非仿射原成员的阈值都确实是 7/2

对偶成员，直接求导得
\[
p_{2m}'''(1)=4m(4m-5)>0,\qquad m\ge2.
\]
对奇成员，有
\[
p_{2m+1}'''(1)-p_{2m+1}''(1)=4m(4m-3)>0.
\]
这两个公式可由各单项式的连续下降阶乘展开直接化简，均对全部 \(m\ge2\) 成立。

再次对引理 1 中的剩余多项式积分应用同一估计，可得到
\[
\langle p_{2m},\cos(k\pi x)\rangle_2
=-\frac{8m(4m-5)(-1)^k}{(k\pi)^4}+O_m(k^{-6}),
\]
\[
\langle p_{2m+1},\sin(\mu_kx)\rangle_2
=-\frac{8m(4m-3)\sin\mu_k}{\mu_k^4}+O_m(\mu_k^{-6}).
\]
第一项的常数不为零；\(|\sin\mu_k|=\mu_k/\sqrt{1+\mu_k^2}\to1\)。故归一化谱系数的绝对值在充分大指标上被正的常数乘 \(k^{-4}\) 从下控制。

相应正项级数在 \(2s-8\ge-1\)，即 \(s\ge7/2\)，必然发散。这证明每个非仿射原成员的精确阈值。

例如两个最低例子是精确恒等式：
\[
\langle p_4,\cos(k\pi x)\rangle=-48(-1)^k/(k\pi)^4,
\]
\[
\langle p_5,\sin(\mu_kx)\rangle=-80\sin\mu_k/\mu_k^4.
\]
仿射函数满足 \(K_c(a+bx)=c(a+bx)\)，所以属于全部幂域。

## 4. 原族的代数包与四阶相容多项式

记
\[
\mathcal P_K=\operatorname{span}\{p_n:n\in\mathcal D\}.
\]
有精确代数等式
\[
\mathcal P_K=\mathbb C[x]\cap D(K_c).
\]
一侧来自边界条件。反向按次数减去首项系数乘相应的 \(p_n\)。最后可能留下 \(1,x,x^2,x^3\)；边界残差在 \(x^2,x^3\) 上分别为 \((2,-2),(2,2)\)，故剩余二、三次项必须消失。

特别地
\[
\mathcal C_4:=\mathbb C[x]\cap D(K_c^2)\subset\mathcal P_K.
\]
\(\mathcal C_4\) 不是仅由各个已经进入四阶域的命名 \(p_n\) 张成，而是允许它们的线性组合消去边界残差。例如
\[
p_6-\tfrac72p_4=x^6-5x^4+7x^2\in D(K_c^2).
\]

## 5. 四阶多项式图核心：单独补足一个短证明

仓库 A7 已有更一般的整数阶图核心证明。这里只证明本附录需要的四阶情形，避免依赖整套高阶结果。

记
\[
\mathcal Bf=(f'(1)-\Delta f/2,\ f'(-1)-\Delta f/2).
\]
首先
\[
D(K_c^2)=\{f\in H^4_{\rm Sob}(-1,1):\mathcal Bf=0,\ \mathcal B(f'')=0\}.
\]
事实上 \(f\in D(K_c^2)\) 时，\(f,K_cf\in H^2\)，从 \(f''=cf-K_cf\) 得 \(f\in H^4\)，并由
\(\mathcal B(K_cf)=c\mathcal Bf-\mathcal B(f'')\) 得条件；反向直接成立。

令
\[
T:H^4_{\rm Sob}\to\mathbb C^4,\quad Tf=(\mathcal Bf,\mathcal Bf'').
\]
四个迹均连续。它在 \(x^2,x^3,x^4,x^5\) 上的矩阵是
\[
B=\begin{pmatrix}
2&2&4&4\\
-2&2&-4&4\\
0&0&24&40\\
0&0&-24&40
\end{pmatrix},\qquad \det B=15360\ne0.
\]
因此存在取值于 \(\operatorname{span}\{x^2,x^3,x^4,x^5\}\) 的线性右逆 \(R\)，满足 \(TR=I\)。它是有限维连续映射。

给定 \(f\in D(K_c^2)\)，先取普通多项式 \(r_j\to f\) 于 \(H^4_{\rm Sob}\)。这一逼近可由多项式在 \(L^2\) 中逼近 \(f^{(4)}\)，再四次积分并匹配 \(-1\) 处的四个低阶迹得到。

令
\[
q_j=r_j-RT r_j.
\]
因 \(Tf=0\)，有 \(Tq_j=0\)，故 \(q_j\in\mathcal C_4\)，并且
\[
\|q_j-f\|_{H^4_{\rm Sob}}
\le(1+\|R\|\|T\|)\|r_j-f\|_{H^4_{\rm Sob}}\longrightarrow0.
\]
在算子域上
\[
K_c^2f=f^{(4)}-2cf''+c^2f,
\]
因此普通 \(H^4\) 收敛蕴含 \(\|K_c^2(q_j-f)\|_2\to0\)。这证明
\[
\boxed{\overline{\mathcal C_4}^{\mathcal H_c^4}=\mathcal H_c^4.}
\]

## 6. 用更强空间里的合法逼近闭合分数窗口

固定 \(0\le s<7/2\) 和 \(f\in\mathcal H_c^s\)。先作谱截断
\[
f_N=\sum_{j\le N}\langle f,e_j\rangle e_j.
\]
\(f_N\in\mathcal H_c^4\)，而 \(\|f-f_N\|_s\to0\)。

对任何 \(u\in\mathcal H_c^4\)，\(\lambda_j\ge c\) 给出
\[
\|u\|_s\le c^{(s-4)/2}\|u\|_4.
\]
给定 \(\varepsilon>0\)，先使 \(\|f-f_N\|_s<\varepsilon/2\)，再由上一节的图核心选
\(q\in\mathcal C_4\) 使
\[
\|f_N-q\|_4<\frac{\varepsilon}{2c^{(s-4)/2}}.
\]
由于 \(\mathcal C_4\subset\mathcal P_K\)，得到
\[
\|f-q\|_s<\varepsilon.
\]
第三节已证明原族的每个成员在这个 \(s\) 下都是合法空间元素，所以这确实是原族作为 \(\mathcal H_c^s\) 内部函数族的稠密性，而不仅是形式线性组合的域交。

这条论证没有从三阶稠密性向上推出强范数稠密性。它是先在四阶域中构造相容多项式逼近，再向下传递；因此不与先前撤回的错误全阶论证混同。

## 7. 建议的仓库接入范围

当前 `docs/SL_fractional_left_definite.tex` 和 `research_map.md` 仍把 \(3<s<7/2\) 标为未判定。经独立核对本附录后，可将 A1 的范围改为 \(0\le s<7/2\)，并加入全体非仿射命名成员的精确阈值。

应保留 \(s\ge7/2\) 的成员障碍、高阶相容多项式图核心、真正算子逆与代数逆的区别。此补证不处理任意受约束子空间、任意非余有限指标集、稳定展开或所有高阶分数幂域的完整边界刻画。

## 来源定位

- `docs/SL_fractional_left_definite.tex`：谱系、谱范数、当前窗口及 p4 阈值。
- `docs/SL_denseness_criteria.tex`：\(\mathcal P_K=\Pi\cap D(K_c)\) 的正确代数解释。
- `runs/three-arm-pilot-v2/pilot-v6-hs-domain/arms/c-qed/output/proof.md` STEP8：已有整数高阶图核心。
- Jones–Littlejohn–Quintero Roba, *Krein–Sobolev Orthogonal Polynomials II*, Axioms 14 (2025), 115：原模型与左定谱背景。本附录不作首创性断言。
