from pathlib import Path
import hashlib

Root = Path('/mnt/f/tools/math-audit-round7-20260921/analytic-author')
Source = Path('/mnt/f/LaTeX/BVE research/docs/SL_gap_nge2_symmetry_local_proof.tex')
Original = Source.read_bytes()
Expected = '151c7ec65a67789a043b01a46f6c87c40e6827e9994be9fb4be88a45da0c0aaa'
if hashlib.sha256(Original).hexdigest() != Expected:
	raise RuntimeError('Source changed; author must rebase deliberately.')
Text = Original.decode('utf-8')

def replace_once(Old, New):
	global Text
	if Text.count(Old) != 1:
		raise RuntimeError(f'Expected one occurrence: {Old[:100]!r}')
	Text = Text.replace(Old, New, 1)

def replace_region(Start, End, New):
	global Text
	Left = Text.index(Start)
	Right = Text.index(End, Left)
	Text = Text[:Left] + New + Text[Right:]

replace_once('% 日期: 2026-08-12', '% 日期: 2026-09-21, 第七轮范围修订; 验收见版本绑定报告.')
replace_once(r'\date{2026 年 8 月 12 日}', r'\date{2026 年 9 月 21 日\\第七轮范围修订; 验收见版本绑定报告}')
replace_once('严格区分.\n\\end{abstract}', r'''严格区分. 本轮另从 minmax 原理证明, 对所有 $n\ge1$, 可测盒类及不限制
块数的有限分块类的谱隙上确界均满足
$\lim_{R\to\infty}S_n(R)=(n+1)^2\pi^2$. 此结论不预设全 $R$ 自洽分支存在.
后段 Hessian 与 (G2) 历史增补仅作列明的局部修正, 其整体闭合未重新认证;
实际修正和未核验范围见注~\ref{rem:retained-scope}.
第七轮范围修订; 验收见版本绑定报告.
\end{abstract}''')
replace_once('$u_k$ 为 $\\int_0^1\\rho u_k^2\\,dx=1$ 归一化特征函数. 记',
             '$u_k$ 为 $\\int_0^1\\rho u_k^2\\,dx=1$ 归一化特征函数, 统一选择符号使\n$u_k\'(0)>0$. 记')
replace_once(r'\item[(d)] $f(0+)<0$, $f(1-)<0$;',
             r'\item[(d)] $f(0)=f(1)=0$, 且 $f$ 在两个端点的某个单侧邻域内严格负;')
replace_once("$W(x)<W(w_i)=-u_{n+1}(w_i)u_n'(w_i)<0$",
             "$W(x)<W(w_i)=-u_{n+1}(w_i)u_n'(w_i)\\le0$")
replace_once('(符号依 $i$ 的奇偶性检查, 结点导数与函数值符号交替). 故 $W<0$ 于 $(0,1)$.',
             '(内结点处严格小于 $0$, 而 $w_n=1$ 处等于 $0$; 结点导数与函数值符号交替).\n故 $W<0$ 于 $(0,1)$.')
replace_once('(正特征函数斜率为正)', '(由已固定的特征函数符号约定)')
replace_once('同理 $f(1-)<0$ (用 $q_1^2>1>c^2$). 证 (d).',
             '同理 $f<0$ 于 $1$ 的某个左邻域 (用 $q_1^2>1>c^2$).\n端点值本身均为 $0$. 证 (d).')
replace_once(r'$\rho=R$ 块恰为 $(x_{2i-1},x_{2i})=\bigcup_i(r_i^-,r_i^+)$; 对 INF,',
             r'$\rho=R$ 的开块之并恰为 $\bigcup_i(x_{2i-1},x_{2i})=\bigcup_i(r_i^-,r_i^+)$; 对 INF,')
replace_once(r'''Wronskian: $W=u_{n+1}'u_n-u_{n+1}u_n'=-2(n+1)\pi\sin(\pi x)<0$ 于 $(0,1)$
(直接代入 $u_k=\sqrt2\sin(k\pi x)$). 商 $Q=u_{n+1}/u_n$: 在每个胞腔上
$Q'=W/u_n^2<0$; 在 $(w_{i-1},z_i)$ 上 $Q$ 与 $u_n$ 同号、在 $(z_i,w_i)$ 上异号,''', r'''令 $\theta=\pi x$. 由积化和差及有限和恒等式
$\sin((2n+1)\theta)=\sin\theta(1+2\sum_{j=1}^n\cos(2j\theta))$, 得
\begin{equation}\label{eq:Wconstant}
\begin{aligned}
W&=2\pi\bigl((n+1)\sin(n\theta)\cos((n+1)\theta)
-n\sin((n+1)\theta)\cos(n\theta)\bigr)\\
&=\pi\bigl(\sin((2n+1)\theta)-(2n+1)\sin\theta\bigr)
=-4\pi\sin\theta\sum_{j=1}^n\sin^2(j\theta)<0.
\end{aligned}
\end{equation}
最后一步用 $0<\theta<\pi$ 且和中的 $j=1$ 项严格正. 例如 $n=2,x=1/2$ 时
$W=-4\pi$. 商 $Q=u_{n+1}/u_n$: 在每个胞腔上 $Q'=W/u_n^2<0$;
在 $(w_{i-1},z_i)$ 上 $Q>0$, 在 $(z_i,w_i)$ 上 $Q<0$,''')
replace_once(r'''对称性: $u_k(1-x)=\sqrt2\sin(k\pi x-k\pi\cdot0)$ 中
$\sin(k\pi-k\pi x)=\pm\sin(k\pi x)$, 故 $f_1(1-x)=f_1(x)$: 零点集反射不变,''',
             r'''对称性: $u_k(1-x)=\sqrt2\sin(k\pi-k\pi x)=(-1)^{k+1}u_k(x)$,
故 $f_1(1-x)=f_1(x)$: 零点集反射不变,''')
replace_once(r'$f_1(x)=2\pi^2(n^4-(n+1)^4)x^2+O(x^4)<0$',
             r'$f_1(x)=2\pi^4(n^4-(n+1)^4)x^2+O_n(x^4)<0$')

replace_region(r'\begin{corollary}[$n=2$ 闭式]', r'\section{\texorpdfstring{$R\to1$}', r'''\begin{corollary}[$n=2$ 闭式与精确非退化性]\label{cor:r1n2}
$n=2$ 时, 令 $t_\pm=(11\pm2\sqrt{10})/36$,
$\theta_1=\arccos\sqrt{t_+}$, $\theta_2=\arccos\sqrt{t_-}$. 则
\begin{equation*}
x^*=\bigl(\theta_1,\theta_2,\pi-\theta_2,\pi-\theta_1\bigr)/\pi
\approx(0.25597364,0.38264716,0.61735284,0.74402636).
\end{equation*}
这里小数仅为位置说明. 严格地, $f_1'(x_j^*)$ 的符号为 $(+,-,+,-)$, 且
\begin{equation}\label{eq:n2det-exact}
\det D_xF(1,x^*)=\frac{\prod_{j=1}^4 f_1'(x_j^*)}{(9\pi^2)^4}
=\frac{7030400000}{4782969}\pi^4>0.
\end{equation}
\end{corollary}
\begin{proof}
令 $\theta=\pi x$, $t=\cos^2\theta$, $P(t)=144t^2-88t+9$. 三角恒等式给出
\begin{equation*}
f_1(x)=2\pi^2\sin^2\theta\bigl(16t-9(4t-1)^2\bigr)
=-2\pi^2(1-t)P(t).
\end{equation*}
$0<x<1$ 时 $1-t>0$, 故内零点恰由 $P(t)=0$ 给出.
$P$ 的两个根为上述 $t_\pm$, 且 $0<t_-<t_+<1$. 每根产生两个互为反射的
$x$, 因而升序正是所列四点. 在根上
\begin{equation*}
f_1'(x)=4\pi^3\cos\theta\sin\theta(1-t)P'(t),\qquad
P'(t_\pm)=\pm16\sqrt{10}\ne0.
\end{equation*}
因 $0<t_\pm<1$, 其余因子亦非零. 这直接给出简单性与符号 $(+,-,+,-)$,
不需用小数排除零. 进一步,
\begin{equation*}
f_1'(x)^2=40960\pi^6 t(1-t)^3,\qquad
t_+t_-=\frac1{16},\quad (1-t_+)(1-t_-)=\frac{65}{144}.
\end{equation*}
每个反射对的导数乘积为负的平方, 两对相乘得
\begin{equation*}
\det D_xF(1,x^*)=
\frac{40960^2}{9^4}\,\frac1{16}\left(\frac{65}{144}\right)^3\pi^4
=\frac{7030400000}{4782969}\pi^4.
\end{equation*}
\end{proof}

''')

replace_region(r'\begin{lemma}[零点一致远离端点]', r'\begin{theorem}[局部存在唯一与对称性]', r'''\begin{lemma}[可测盒密度的统一端点估计与连续依赖]\label{lem:away}
固定 $n\ge2$. 存在仅依赖 $n$ 的 $\varepsilon_0>0$, $\delta_1>0$, $C_n<\infty$
使下述结论对每个可测密度 $1\le\rho\le1+\varepsilon$ a.e.,
$0\le\varepsilon\le\varepsilon_0$, 同时成立. 取权归一化且 $u_{k,\rho}'(0)>0$ 的
特征函数, $k=n,n+1$, 则
\begin{equation}\label{eq:uniform-c1}
|\lambda_k(\rho)-(k\pi)^2|+
\|u_{k,\rho}-\sqrt2\sin(k\pi\,\cdot)\|_{C^1([0,1])}\le C_n\varepsilon.
\end{equation}
写 $\gamma_n=2\pi^4((n+1)^4-n^4)>0$, 则
\begin{equation}\label{eq:uniform-endpoint}
f_\rho(x)\le-\frac{\gamma_n}{4}x^2\quad(0<x<\delta_1),\qquad
f_\rho(x)\le-\frac{\gamma_n}{4}(1-x)^2\quad(1-\delta_1<x<1).
\end{equation}
并有 $\|f_\rho-f_1\|_{C^1}\le C_n\varepsilon$, 必要时增大 $C_n$.
特别地, 全部内零点一致远离端点. 结论包含闭单纯形 $\overline U$ 中的
所有分块配置, 不要求任何块宽下界.
\end{lemma}
\begin{proof}
\textbf{谱夹逼.} 在 $H=H_0^1(0,1)$ 上记
$a(v,v)=\int|v'|^2$, $b_\rho(v,v)=\int\rho v^2$.
由 minmax 原理及 $b_1\le b_\rho\le(1+\varepsilon)b_1$,
\begin{equation}\label{eq:spectral-squeeze}
\frac{(k\pi)^2}{1+\varepsilon}\le\lambda_k(\rho)\le(k\pi)^2.
\end{equation}
这里可测有界正权的变分谱确实对应射击谱: $H$ 上由
$a(T_\rho v,w)=b_\rho(v,w)$ 定义的正自伴算子是紧算子
(一维 $H_0^1\hookrightarrow C[0,1]$ 的紧嵌入), 其正特征值的倒数给出
minmax 值; 弱特征方程给出 $u\in W^{2,\infty}$ 及 $-u''=\lambda\rho u$ a.e.
一维初值唯一性使每个 Dirichlet 特征空间一维. 本证明使用的正则性是
$u\in C^1$, $u'$ 绝对连续, 不要求跨密度跳点的 $C^2$ 或 $C^3$.

\textbf{全区间 Volterra 估计.} 可先限 $\varepsilon\le1$,
置 $\Lambda=(n+1)^2\pi^2$, $M=2\Lambda$, $C=e^{1+M}$.
对 $k=n,n+1$, 取初值为 $y(0)=0,y'(0)=1$ 的射击解
\begin{equation}\label{eq:volterra}
y(x)=x-\lambda_k(\rho)\int_0^x(x-t)\rho(t)y(t)\,dt,\qquad
y'(x)=1-\lambda_k(\rho)\int_0^x\rho(t)y(t)\,dt.
\end{equation}
有界可测核的逐次迭代给出唯一解, 导数为绝对连续函数.
由于 $|\lambda_k\rho|\le M$, 一阶积分系统的 Gronwall 估计给出
$|y(x)|+|y'(x)|\le C$, 并由 $y(0)=0$ 得 $|y(x)|\le Cx$.
再次代回 \eqref{eq:volterra}, 对所有 $0<x\le1$ 有
\begin{equation}\label{eq:volterra-remainder}
\left|\frac{y(x)}x-1\right|\le\frac{MC}{6}x^2,\qquad
|y'(x)-1|\le\frac{MC}{2}x^2.
\end{equation}
这些是全区间积分估计, 可直接跨过任意多个跳点.

\textbf{射击解的 $C^1$ 连续依赖与权归一化.}
令 $y_{k,0}(x)=\sin(k\pi x)/(k\pi)$.
由 \eqref{eq:spectral-squeeze},
$\|\lambda_k(\rho)\rho-(k\pi)^2\|_\infty\le2\Lambda\varepsilon$.
将两个一阶积分系统相减, 零初值差满足
\begin{equation*}
|y(x)-y_{k,0}(x)|+|y'(x)-y_{k,0}'(x)|
\le(1+M)\int_0^x\bigl(|y-y_{k,0}|+|y'-y_{k,0}'|\bigr)\,dt
+2\Lambda C\varepsilon.
\end{equation*}
再用 Gronwall, 左侧一致不超过 $2\Lambda C^2\varepsilon$.
设
\begin{equation*}
N_{k,\rho}=\left(\int_0^1\rho y^2\,dx\right)^{1/2},\qquad
N_{k,0}=\frac1{\sqrt2 k\pi},\qquad u_{k,\rho}=\frac{y}{N_{k,\rho}}.
\end{equation*}
利用上述一致界,
$|N_{k,\rho}^2-N_{k,0}^2|\le C_n\varepsilon$.
缩小 $\varepsilon_0$ 后 $N_{k,\rho}\ge N_{k,0}/2>0$, 因而
$|N_{k,\rho}^{-1}-N_{k,0}^{-1}|\le C_n\varepsilon$.
这证明 \eqref{eq:uniform-c1}, 特别是端点斜率
$a_{k,\rho}:=u_{k,\rho}'(0)=N_{k,\rho}^{-1}\to\sqrt2 k\pi$ 一致.
乘积求导立即给出 $f_\rho\to f_1$ 的一致 $C^1$ 界.

\textbf{不依赖首块的端点符号.} 置
$B_\rho=\lambda_n a_{n,\rho}^2-\lambda_{n+1}a_{n+1,\rho}^2$.
由刚证的估计, $|B_\rho+\gamma_n|\le C_n\varepsilon$.
选 $\varepsilon_0$ 使 $B_\rho\le-\gamma_n/2$.
另一方面 \eqref{eq:volterra-remainder} 与斜率的一致有界性给出
\begin{equation*}
\left|\frac{f_\rho(x)}{x^2}-B_\rho\right|\le C_n x^2\qquad(0<x\le1).
\end{equation*}
取 $\delta_1<1/2$ 且 $C_n\delta_1^2\le\gamma_n/4$, 即得左端的
\eqref{eq:uniform-endpoint}. 对反射密度 $\widehat\rho(t)=\rho(1-t)$ 应用同一估计.
反射保持谱及权归一化, 而平方消去特征函数的符号选择, 故
$f_{\widehat\rho}(t)=f_\rho(1-t)$, 得右端估计. 全程没有将接口与零点等同,
没有使用首个结点或首块宽的下界, 也没有假设带自洽性.
\end{proof}

\begin{lemma}[全部内零点的一致隔离]\label{lem:isol}
可选互不相交的闭区间 $I_j$ ($j=1,\dots,2n$), 每个 $x_j^*$ 位于 $I_j$ 的
内部, 并缩小 $\varepsilon_0$, 使所有可测 $1\le\rho\le1+\varepsilon_0$ 的
$f_\rho$ 在每个 $I_j$ 中恰有一个简单零点, 在其余 $(0,1)$ 中无零点.
所有这些零点随 $\varepsilon\to0$ 一致趋于对应的 $x_j^*$.
\end{lemma}
\begin{proof}
先缩小引理~\ref{lem:away} 的 $\delta_1$, 使 $x_j^*$ 全部位于
$(\delta_1,1-\delta_1)$. 由 $f_1'(x_j^*)\ne0$, 可取其中互不相交的闭区间
$I_j=[\alpha_j,\beta_j]$, 使 $f_1'$ 在每个 $I_j$ 上定号且绝对值有正下界,
并有 $f_1(\alpha_j)f_1(\beta_j)<0$.
一致 $C^1$ 收敛保证 $f_\rho'$ 保持该符号和正下界, 两端函数值亦保号,
故每个 $I_j$ 中恰有一个简单零点.
在紧集
$[\delta_1,1-\delta_1]\setminus\bigcup_j(\alpha_j,\beta_j)$ 上
$|f_1|$ 有正下界, 一致 $C^0$ 收敛排除额外零点.
两端开区间由 \eqref{eq:uniform-endpoint} 排除零点, 覆盖全部 $(0,1)$.
最后, 若有零点不趋于对应 $x_j^*$, 取子列及极限, 一致收敛将产生
$I_j$ 内另一个 $f_1$ 零点, 矛盾. 这也排除了两个不同零点合并到同一 $x_j^*$.
\end{proof}

''')

replace_once(r'''\textbf{解析性与非退化性.} 转移矩阵 $M(s;R,x)$ (逐块正弦/余弦传播) 对
$(R,x)$ 解析; 谱简单且 $\lambda_n,\lambda_{n+1}$ 在 $(1,x^*)$ 的紧邻域上分离
($\lambda_k\to(k\pi)^2$), 故 $(\lambda_k,u_k)$ 与 $F$ 在该邻域上解析
(简单谱的解析扰动理论).''', r'''\textbf{解析性与非退化性.} 每块长度为 $\ell$, 密度为 $r$ 时, 射击转移矩阵为
\begin{equation*}
\begin{pmatrix}
\cos(\sqrt{\lambda r}\ell)&\sin(\sqrt{\lambda r}\ell)/\sqrt{\lambda r}\\
-\sqrt{\lambda r}\sin(\sqrt{\lambda r}\ell)&\cos(\sqrt{\lambda r}\ell)
\end{pmatrix}.
\end{equation*}
在 $(1,x^*)$ 邻域, 有限个矩阵的乘积及各接口射击值均对 $(\lambda,R,x)$ 解析.
在 Dirichlet 根处, 对射击方程按 $\lambda$ 微分并积分 Wronskian 恒等式给出
$y'(1)\partial_\lambda y(1)=\int_0^1\rho y^2>0$.
因 $y'(1)\ne0$, 根简单, 故 $\lambda_n,\lambda_{n+1}$ 解析依赖 $(R,x)$;
其编号由 \eqref{eq:spectral-squeeze} 在该邻域固定. 权范数由有限个块积分组成,
亦为正的解析函数. 因此权归一化后的接口值与 $F$ 解析.
这里不声称移动跳点时整个特征函数在高阶函数空间中解析.''')
replace_once(r'''\textbf{带自洽.} (i) 由构造成立. (ii) 在 $R=1$ 极限处, 由
定理~\ref{thm:r1}(iii): $f_1$ 在 $2n+1$ 个区间上的符号为 $(-,+,-,\dots,-)$.
对 SUP 图案, $\rho=1$ 块恰为奇数号区间 ($f_1<0$), $\rho=R$ 块恰为偶数号区间
($f_1>0$); 对 INF 图案恰好互换. 分支块中点收敛到极限块中点 ($x_j(R)\to x_j^*$),
且 $f_R\to f_1$ 一致 (在 $[0,1]$ 上), 故对 $R-1$ 充分小, 符号图案保持:
SUP 下 $f<0$ 于 $\rho=1$ 块、$f>0$ 于 $\rho=R$ 块 (INF 反之). 证毕.''', r'''\textbf{整块带自洽性.} (i) 由构造成立. 引理~\ref{lem:isol} 给出 $f_R$ 在
$(0,1)$ 中恰有 $2n$ 个简单零点. 方程 $F=0$ 的 $2n$ 个互异接口已占满这些零点,
所以每个开块内部没有其他零点, $f_R$ 在整块上严格定号.
由引理~\ref{lem:away}, 第一块的符号为负; 每经过一个简单零点符号翻转,
故全部 $2n+1$ 个开块的符号严格为 $(-,+,-,\dots,-)$.
对 SUP, 奇数块密度为 $1$, 偶数块为 $R$; 对 INF 密度互换, 正好分别满足
定义~\ref{def:bc}(ii). 这是整块符号隔离, 不仅是块中点符号检验;
所用两个引理均未预设接口是切换函数的全部零点. 证毕.''')

replace_once(r'''\section{全局分类框架与开放条件 (STRICT 陈述)}\label{sec:global}

记''', r'''\section{全局分类框架与开放条件 (条件化陈述)}\label{sec:global}

本节分类框架仍以 (G1$'$)(G2) 为前提. 对后文历史 ``(G2) 闭合'' 登记,
本轮仅修正已列明的局部问题, 不予整体新增认证, 见注~\ref{rem:retained-scope}.
由分类框架推出盒类极值子的最后一步还使用文献 [1] 的外部约化结果,
本轮未读取或重新证明该依赖; 以下新增上确界极限定理不使用该依赖.

记''')
replace_once(r'''\begin{remark}[开放条件的现状 (诚实登记)]
\begin{itemize}''', r'''\begin{remark}[开放条件与历史数值登记]
以下数值沿用源文, 本轮未重跑其原程序; 不能作为当前审查通过的依据.
\begin{itemize}''')
replace_once(r'''	\item 对称分支的 $R\to\infty$ 行为: SUP 分支 $R$ 块宽 $\to0$ (中心质量
	钉扎, $D\to4\pi^2$), INF 分支 $D\to0$; 这与 (G2) 不矛盾 (G2 只要求有限
	$R$).''', r'''	\item 原先的 $4\pi^2$ 极限只能限于 $n=1$ 的 SUP 上确界.
	对一般 $n\ge1$, 下述定理~\ref{thm:sup-limit} 证明盒类上确界极限为
	$(n+1)^2\pi^2$, 不将此上确界与未经证明存在于全 $R$ 的自洽分支等同.
	INF 的大 $R$ 行为保留为原数值记录, 本轮不扩大其严格结论.
	有限 $R$ 上的 (G2) 也不由一个 $R\to\infty$ 构造得到.''')

GlobalAddition = r'''\begin{remark}[自洽 SUP 分支上的单调性]\label{rem:sup-branch}
若在某个 $R$ 区间内已有以 $R$ 为参数的可微带自洽 SUP 分支 $x(R)$,
记 $s_j=\rho(x_j+)-\rho(x_j-)$. 由一阶变分与移动接口公式,
\begin{equation*}
\frac{dD_n}{dR}=\int_{\{\rho=R\}}f\,dx-
\sum_{j=1}^{2n}s_j f(x_j)x_j'(R)=\int_{\{\rho=R\}}f\,dx>0.
\end{equation*}
所以从 $R=1$ 的局部分支继续得到的此类分支, 在其成立区间上从
$(2n+1)\pi^2$ 严格增加; $n\ge2$ 时不可能降到 $4\pi^2$.
此计算不排除折点, 不证明全 $R$ 延拓或唯一性, 亦不预设分支就是全局极值子.
\end{remark}

\begin{theorem}[一般指标的 SUP 上确界极限]\label{thm:sup-limit}
对整数 $n\ge1$ 及 $R>1$, 定义
\begin{align*}
\mathcal A_R&=\{\rho:(0,1)\to\mathbb R\text{ 可测}:1\le\rho\le R\text{ a.e.}\},\\
\mathcal P_R&=\{\rho\in\mathcal A_R:\rho\text{ 在某个有限区间分割上逐块常值}\},\\
S_n^{\mathcal A}(R)&=\sup_{\rho\in\mathcal A_R}(\lambda_{n+1}(\rho)-\lambda_n(\rho)),\qquad
S_n^{\mathcal P}(R)=\sup_{\rho\in\mathcal P_R}(\lambda_{n+1}(\rho)-\lambda_n(\rho)).
\end{align*}
$\mathcal P_R$ 不预设块数上限. 则
\begin{equation}\label{eq:sup-limit}
\lim_{R\to\infty}S_n^{\mathcal A}(R)
=\lim_{R\to\infty}S_n^{\mathcal P}(R)=(n+1)^2\pi^2.
\end{equation}
更具体地, 令 $h=1/(n+1)$, $\delta=\min\{h/12,R^{-2/3}\}$,
$a_j=jh$ ($j=1,\dots,n$),
\begin{equation}\label{eq:thin-density}
I_j=(a_j-\delta,a_j+\delta),\qquad
\rho_R=1+(R-1)\mathbf1_{\bigcup_{j=1}^n I_j}.
\end{equation}
这里 $\delta$ 是每个薄层的\textbf{半宽}, 全宽是 $2\delta$.
此对称 bang--bang 密度有 $2n+1$ 个块, 且满足
\begin{equation}\label{eq:thin-bounds}
\lambda_n(\rho_R)\le\frac{12}{5hR\delta}\le\frac6{hR\delta},\qquad
\lambda_{n+1}(\rho_R)\ge
\left(\frac{h^2}{\pi^2}+\frac{(R-1)\delta^2}{2}\right)^{-1}.
\end{equation}
\end{theorem}
\begin{proof}
对任意盒密度使用 Rayleigh 商
$\mathcal R_\rho(v)=\int_0^1|v'|^2/\int_0^1\rho|v|^2$, $0\ne v\in H_0^1(0,1)$,
以及
$\lambda_k(\rho)=\min_{\dim V=k}\max_{0\ne v\in V}\mathcal R_\rho(v)$.
其可测权谱的依据已在引理~\ref{lem:away} 中说明, 与 $n\ge2$ 的限制无关.
由于 $\rho\ge1$, 比较 minmax 分母得
\begin{equation}\label{eq:sup-universal-upper}
D_n(\rho)\le\lambda_{n+1}(\rho)\le(n+1)^2\pi^2.
\end{equation}
常密度 $\rho=1$ 又给出两个上确界均不小于 $(2n+1)\pi^2$.

\textbf{$n$ 维平台试探空间.} 对 $c=(c_1,\dots,c_n)\in\mathbb R^n$, 取
$v_c\equiv c_j$ 于 $I_j$, 在相邻平台之间线性连接, 并在线性首尾段连接到
$v_c(0)=v_c(1)=0$. 这些函数构成 $n$ 维子空间 $V$.
首尾线性段的长度各为 $h-\delta$, 内部连接段的长度为 $h-2\delta$.
令 $c_0=c_{n+1}=0$, 即使 $n=1$, 下述计算仍包含首尾两段:
\begin{align*}
\int_0^1|v_c'|^2
&=\frac{c_1^2+c_n^2}{h-\delta}
+\sum_{j=1}^{n-1}\frac{(c_{j+1}-c_j)^2}{h-2\delta}\\
&\le\frac1{h-2\delta}\sum_{j=0}^{n}(c_{j+1}-c_j)^2
\le\frac4{h-2\delta}\sum_{j=1}^n c_j^2,\\
\int_0^1\rho_R v_c^2&\ge2R\delta\sum_{j=1}^n c_j^2.
\end{align*}
用 $(a-b)^2\le2a^2+2b^2$ 得上述因子 $4$, 用 $\delta\le h/12$ 得
$h-2\delta\ge5h/6$. 因此
$\max_{v\in V\setminus\{0\}}\mathcal R_{\rho_R}(v)
\le2/[R\delta(h-2\delta)]\le12/(5hR\delta)$,
minmax 给出第一个界, 并立即蕴含报告形式的较松常数 $6$.

\textbf{中心取零的余维 $n$ 约束.} 定义闭子空间
$Z=\{v\in H_0^1(0,1):v(a_j)=0,\ j=1,\dots,n\}$.
一维点值连续, 而上述平台函数可取任意中心值, 故 $Z$ 的余维恰为 $n$.
把 $a_0=0,a_{n+1}=1$ 加入分割, $v\in Z$ 在每个长度为 $h$ 的区间两端为零,
由 Dirichlet Poincar\'e 不等式,
\begin{equation*}
\int_0^1v^2\le\frac{h^2}{\pi^2}\int_0^1|v'|^2.
\end{equation*}
该常数可由区间上的正弦展开得到; 亦可先对光滑紧支撑函数用恒等式
$\int(|v'|^2-(\pi/h)^2v^2)
=\int\sin^2(\pi t/h)|(v/\sin(\pi t/h))'|^2\ge0$, 再以 $H_0^1$ 稠密性延拓.
在每个薄层的右半段, $v(a_j)=0$ 与 Cauchy--Schwarz 给出
\begin{align*}
\int_0^\delta|v(a_j+t)|^2\,dt
&\le\int_0^\delta t\int_0^t|v'(a_j+s)|^2\,ds\,dt\\
&=\frac12\int_0^\delta(\delta^2-s^2)|v'(a_j+s)|^2\,ds
\le\frac{\delta^2}{2}\int_0^\delta|v'(a_j+s)|^2\,ds.
\end{align*}
左半段同理. $I_j$ 彼此不交, 因而
\begin{equation*}
\int_0^1\rho_Rv^2
\le\left(\frac{h^2}{\pi^2}+\frac{(R-1)\delta^2}{2}\right)\int_0^1|v'|^2
\qquad(v\in Z).
\end{equation*}
取前 $n+1$ 个权正交特征函数张成的空间 $E$.
因 $\dim E=n+1$ 而 $Z$ 仅有 $n$ 个线性约束, 存在 $0\ne v\in E\cap Z$.
在 $E$ 上 $\mathcal R_{\rho_R}(v)\le\lambda_{n+1}(\rho_R)$,
在 $Z$ 上该商至少为上式括号的倒数. 这给出 \eqref{eq:thin-bounds} 的第二个界.

\textbf{极限夹逼.} 固定 $n$ 后, 最终 $\delta=R^{-2/3}$,
故 $R\delta\to\infty$, $(R-1)\delta^2\to0$.
由 \eqref{eq:thin-bounds} 与 \eqref{eq:sup-universal-upper},
$\lambda_n(\rho_R)\to0$, $\lambda_{n+1}(\rho_R)\to\pi^2/h^2$,
于是 $D_n(\rho_R)\to(n+1)^2\pi^2$.
构造的 $\rho_R$ 属于 $\mathcal P_R\subset\mathcal A_R$, 所以
\begin{equation*}
D_n(\rho_R)\le S_n^{\mathcal P}(R)\le S_n^{\mathcal A}(R)\le(n+1)^2\pi^2,
\end{equation*}
夹逼即得结论. 不需要有限 $R$ 上上确界已被取到, 不需要最优接口或带自洽性.
\end{proof}

\begin{remark}
本定理在 $n=1$ 时给出 $4\pi^2$, 在 $n=2$ 时给出 $9\pi^2$.
它只回答上述两种盒类的上确界极限. 构造密度虽具有对称 SUP 图案,
并未证明满足 $F=0$, 故不推出 (G1$'$), (G2), 全 $R$ 分支分类或 INF 结论.
\end{remark}

'''
replace_once(r'\section{数值交叉检验 (EVIDENCE, 不构成证明)}',
             GlobalAddition + r'\section{数值交叉检验 (EVIDENCE, 不构成证明)}')
replace_once('以下全部为数值证据, 不进入定理', '以下历史数值沿用源文, 本轮未重跑原数值程序; 全部仅为数值证据, 不进入定理')
replace_once('''	\\item $R=1$ 零点结构 (一般 $n$): 对 $n=2,\\dots,8$, 数值求根
	$f_1(x)=2\\pi^2(n^2\\sin^2(n\\pi x)-(n+1)^2\\sin^2((n+1)\\pi x))=0$:
''', '')

TailMarker = r'\section{带自洽点处 Jacobian/Hessian 的闭式结构 (STRICT 增补, 2026-08-12)}'
ScopeNotice = r'''\begin{remark}[保留后段的审查边界与直接冲突]\label{rem:retained-scope}
以下第~\ref{sec:aug}, \ref{sec:aug-ev}, \ref{sec:g2closed} 节保留原有文字及历史
``STRICT'' 标签, \textbf{不属于本轮已核实结论}, 不能据其旧标签认定 (G2) 已闭合.
在通读指定全文时已看到以下直接冲突, 此处明确登记, 不补写完整后段审查:
\begin{enumerate}
\item 命题~\ref{prop:K} 中 $\det K>0$ 不等价于 $K$ 或 Hessian 定号.
例如 $n=2$ 时 $K=\operatorname{diag}(1,1,-1,-1)$ 的行列式为正而不定.
因而后段把特定主元符号模式与 (G1$'$) 等价也需要额外连通性和惯性论证.
\item 命题~\ref{prop:pf} 证明末行由其上一行恒等式实际应得
$f'(x_j)/s_j=\sigma\,2\lambda_{n+1}c|W(x_j)|/(R-1)$;
原末行漏掉 $\lambda_{n+1}$. 在 $K_{jj}$ 中除以 $\lambda_{n+1}$ 后的首项
与这个修正相容, 此处不据此认证其余谱和计算.
\item 第~\ref{sec:aug-ev} 节 SUP 数值行写 $\operatorname{sgn}\det J=(+1)^n$,
却同时称 $K$ 全正, 与 \eqref{eq:detK} 在奇数 $n$ 时直接冲突.
原数据未重跑, 不能据此选择哪个数值记录正确.
\item 引理~\ref{lem:simplez} 的 Cauchy 唯一性步骤把不同特征值的两个方程混同.
两个函数在一点有成比例的 Cauchy 数据, 不推出它们在不同方程下处处成比例.
例如 $\sin x$ 与 $\tfrac12\sin(2x)$ 在 $0$ 处的函数值和导数相同,
但分别满足特征参数 $1$ 与 $4$ 的方程. 此例否定该推理规则, 不否定零点引理本身.
已知 $W<0$ 可以用于另行修补局部零点论证, 但本轮不据此宣布整个 (G2) 证明通过.
\item 定理~\ref{thm:g2} 使用的
$\lambda_{n+1}^*-\lambda_n^*\ge(2n+1)\pi^2/R_1$ 不是两条盒谱夹逼之差的结论:
夹逼最多直接给出 $(n+1)^2\pi^2/R_1-n^2\pi^2$, 可能非正.
简单谱可给固定极限权的正间隙, 但原定量下界仍需独立证明, 本轮未确认.
\end{enumerate}
后段关于全局分类仅剩 (G1$'$) 的旧结语也保留在未经本轮审查范围.
本轮严格推导仅按前文各命题实际证明及明确前提使用, 不扩大 INF 或全 $R$ 分类.
\end{remark}

'''
replace_once(TailMarker, ScopeNotice + TailMarker)
if Text[Text.index(TailMarker):] != Original.decode('utf-8')[Original.decode('utf-8').index(TailMarker):]:
	raise RuntimeError('Retained tail changed.')
Candidate = Root / Source.name
Candidate.write_text(Text, encoding='utf-8')
print('Wrote', Candidate)
print('Lines', len(Text.splitlines()))
print('SHA256', hashlib.sha256(Candidate.read_bytes()).hexdigest())
print('Retained tail unchanged')
