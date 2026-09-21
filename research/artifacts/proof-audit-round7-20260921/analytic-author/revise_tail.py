"""Apply only the later-source local repairs explicitly requested by the user."""
from pathlib import Path
import hashlib

Root = Path(__file__).resolve().parent
Candidate = Root / 'SL_gap_nge2_symmetry_local_proof.tex'
Text = Candidate.read_text()

def replace_once(Old, New):
	global Text
	if Text.count(Old) != 1:
		raise RuntimeError(f'Expected one occurrence: {Old[:120]!r}')
	Text = Text.replace(Old, New, 1)

def replace_region(Start, End, New):
	global Text
	Left = Text.index(Start)
	Right = Text.index(End, Left)
	Text = Text[:Left] + New + Text[Right:]

replace_region(r'\begin{remark}[保留后段的审查边界与直接冲突]',
	r'\section{带自洽点处 Jacobian/Hessian 的闭式结构', r'''\begin{remark}[后段局部修正与未核验范围]\label{rem:retained-scope}
以下第~\ref{sec:aug}, \ref{sec:aug-ev}, \ref{sec:g2closed} 节是历史增补.
\textbf{本轮只作下列可核实的局部修正, 不认证其整体 Hessian 或 (G2) 闭合}:
\begin{enumerate}
\item 命题~\ref{prop:K} 保留行列式恒等式, 删除缺少惯性依据的定号等价推断.
$\det K>0$ 仅给出行列式条件, 定号需要额外惯性信息.
一般实对称矩阵 $\operatorname{diag}(1,1,-1,-1)$ 的行列式为正而不定,
这只说明一般线性代数推理不足. 本轮未证明它可实现为本 SL 模型的 $K$,
不将其称为本模型矩阵族等价结论的反例; 原推理仍需特殊谱结构或惯性依据.
\item 命题~\ref{prop:pf} 证明末行补上 $\lambda_{n+1}$.
这只是与其上一行公式对齐, 不代表本轮重审了正则化谱和及全部矩阵条目.
\item 第~\ref{sec:aug-ev} 节 SUP 历史记录中的行列式符号与 $K$ 全正在奇数 $n$
时冲突, 已标为待重新核算; 这里只登记联合断言的推理或标签问题,
不据此否定某一组历史计算, 也不替未重跑的数据选定一个数值符号.
同节关于主元符号的等价推断改为需要可用分解及惯性信息的充分条件.
\item 引理~\ref{lem:simplez} 改用 $W<0$ 直接计算 $f'$ 的短证,
删除跨不同特征方程使用 Cauchy 唯一性的错误步骤.
\item 定理~\ref{thm:g2} 的历史论证删去未证的定量盒谱隙下界,
仅使用固定正极限权的简单谱所给出的 $\lambda_{n+1}^*-\lambda_n^*>0$.
\end{enumerate}
后段关于 (G2) 已闭合和全局分类仅剩 (G1$'$) 的标题及结语均改为
\textbf{历史未重新认证}. 未整体核验退化极限的全部接口, 极限带匹配,
$\Sigma_\sigma$ 与带自洽集合的量词衔接, 正则化谱和收敛及 Hessian 全局惯性.
未读取后段所指旧 run addendum, 未重跑其历史数值. 本轮不扩大 INF 或全 $R$ 分类.
\end{remark}

''')
replace_once(r'\section{带自洽点处 Jacobian/Hessian 的闭式结构 (STRICT 增补, 2026-08-12)}',
	r'\section{带自洽点处 Jacobian/Hessian 的历史增补 (本轮仅局部修正)}')
replace_once("本节目的是把 (G1$'$) 归约为一个可检验的矩阵符号条件, 并给出",
	r'''\textbf{历史整体内容未重新认证.} 本轮只修正注~\ref{rem:retained-scope} 列明的错误.
原增补的目的是把 (G1$'$) 归约为可检验的矩阵条件, 并给出''')
replace_once(r'''故 (G1$'$) 等价于: 每个带自洽点处 $\det K>0$, 亦等价于
$\operatorname{Hess}(D_n)$ 处处定号 (SUP: 负定, INF: 正定).''', r'''因此在所考虑的带自洽点上, (G1$'$) 的行列式要求等价于 $\det K>0$.
单凭这一行列式恒等式不能推出 $K$ 或 $\operatorname{Hess}(D_n)$ 定号;
原等价推理缺少本 SL 矩阵族的特殊谱结构或惯性依据.
若另有惯性信息证明 SUP 的 $K$ 正定或 INF 的 $K$ 负定, 则分别得到
Hessian 负定或正定, 并蕴含该点的行列式条件.
逆向推断在本模型中能否另行证明, 不由这一行列式计算决定.''')
replace_once(r"f'(x_j)/s_j=\sigma\cdot 2c|W(x_j)|/(R-1)",
	r"f'(x_j)/s_j=\sigma\cdot 2\lambda_{n+1}c|W(x_j)|/(R-1)")
replace_once(r'\section{2026-08-12 审计增补: 符号审计与余量表 (EVIDENCE)}',
	r'\section{2026-08-12 历史数值增补: 符号与余量表 (EVIDENCE, 未重跑)}')
replace_once('以下全部为数值证据, 不构成证明; 其支撑的严格部分见\n第~\\ref{sec:aug} 节.',
	r'''以下均为本轮未重跑的历史数值记录, 不构成证明.
对应解析公式见第~\ref{sec:aug} 节, 其整体范围未重新认证.''')
replace_once(r'''	\item (G1$'$) 数值余量表 (对称分支, FD 权威):
	SUP $n=2..4$, $R\in[1.05,100]$: $\operatorname{sgn}\det J=(+1)^n$ 恒成立,
	$K$ 的特征值全正 (Hess 负定), 最小 $|\mathrm{ev}K|$ 在 $R=100$ 处为
	$0.0156/0.0185/0.0214$ ($n=2/3/4$);''', r'''	\item (G1$'$) 历史数值余量表 (对称分支, 待重新核算):
	SUP $n=2..4$, $R\in[1.05,100]$ 的原记录同时写
	$\operatorname{sgn}\det J=(+1)^n$ 与 $K$ 的特征值全正 (Hess 负定).
	\textbf{这两项在奇数 $n$ 时与 \eqref{eq:detK} 不相容, 待重新核算}.
	这里只登记联合记录的推理或标签冲突, 不据此否定其中某一组历史计算.
	本轮未重跑原程序, 不在两个冲突的历史断言中选定一个作为数值结论.
	原最小 $|\mathrm{ev}K|$ 在 $R=100$ 处的记录
	$0.0156/0.0185/0.0214$ ($n=2/3/4$) 也仅作历史数据保留;''')
replace_once(r'''	\item Sylvester 主元 (新证据): 沿对称分支 $K$ 的无换主元符号恒定
	(SUP 全正, INF 全负; $n=2,3$, $R\in\{1.2,2,4,10\}$), 与 $\det K>0$ 一致;
	由惯性律, 主元符号恒定等价于 (G1$'$). 符号模式''', r'''	\item Sylvester 主元 (历史数值, 本轮未重跑): 原记录称对称分支 $K$ 的无换主元
	符号为 SUP 全正, INF 全负 ($n=2,3$, $R\in\{1.2,2,4,10\}$).
	若无换主元的 $LDL^{\mathsf T}$ 分解存在且对角主元具有上述符号,
	惯性律给出相应定号, 从而是该点行列式条件的充分条件.
	$\det K>0$ 不能反推出各主元符号或保证消元每步可行;
	有限对称样本也不覆盖 (G1$'$) 的全部量词. 历史符号模式''')
replace_once(r'\section{2026-08-13 STRICT 增补: (G2) 闭合}',
	r'\section{2026-08-13 (G2) 闭合历史登记 (未重新认证)}')
replace_once(r'''本节登记 (G2) 的严格闭合, 并取代第~\ref{sec:global} 节 remark 中 "(G2) 开放"
的登记 (该 remark 反映 2026-08-12 的状态). 所有断言均为 STRICT; 完整论证见
run addendum''', r'''\textbf{本节历史整体闭合未重新认证, 不取代第~\ref{sec:global} 节的条件化范围.}
本轮仅修正内部零点短证和固定极限权的谱隙表述, 不提供全 (G2) 新证明.
原文曾将完整论证指向以下旧 run addendum, 本轮未读取该材料:
''')
replace_region(r'\begin{lemma}[内部零点简单性, STRICT]',
	r'\begin{proposition}[块能量与零点计数', r'''\begin{lemma}[内部零点简单性, 局部证明修正]\label{lem:simplez}
对本文的正分块密度及其正分块极限, 取按 $u_k'(0)>0$ 定号的相邻特征函数,
则 $f=\lambda_nu_n^2-\lambda_{n+1}u_{n+1}^2$ 在 $(0,1)$ 内无 $f=f'=0$ 点.
因此若一列此类密度对应的切换函数在 $C^1$ 中收敛到正分块极限权的切换函数,
两个不同内零点不能合并到同一内部点.
\end{lemma}
\begin{proof}
若 $f(a)=0$ 且 $u_n(a)=0$, 则 $u_{n+1}(a)=0$, 与相邻特征函数严格交错矛盾.
故 $u_{n+1}(a)=\epsilon c\,u_n(a)$, 其中 $\epsilon\in\{1,-1\}$,
$c=\sqrt{\lambda_n/\lambda_{n+1}}$. 直接求导得
\begin{equation*}
f'(a)=-2\lambda_{n+1}\epsilon c\,
\bigl(u_{n+1}'(a)u_n(a)-u_{n+1}(a)u_n'(a)\bigr)
=-2\lambda_{n+1}\epsilon c W(a)\ne0,
\end{equation*}
最后一步使用引理~\ref{lem:W} 的 $W(a)<0$. 在接口处 $u_k,u_k'$ 连续,
故该计算同样有效. 若两个零点趋于同一内部点, Rolle 定理在二者之间给出
导数零点; $C^1$ 收敛将产生极限函数的 $f=f'=0$ 点, 与上式矛盾.
\end{proof}

''')
replace_once(r'\begin{proposition}[块能量与零点计数 (STRICT 前提, 定理 6(e) 与文献 [1])]',
	r'\begin{proposition}[块能量与零点计数 (历史前提登记, 未整体复核)]')
replace_once(r'\begin{theorem}[(G2) 闭合, STRICT]',
	r'\begin{theorem}[历史 (G2) 闭合声明, 未重新认证]')
replace_once('\\begin{proof}\n反设存在带自洽解列',
	'\\begin{proof}[历史论证, 本轮仅局部修正]\n反设存在带自洽解列')
replace_once(r'''$[0,1]$ 上加权弦, 特征对 $(\lambda_n^*,\lambda_{n+1}^*)$ 收敛且
$\lambda_{n+1}^*-\lambda_n^*\ge(2n+1)\pi^2/R_1>0$, 归一化特征函数 $C^1$ 收敛,''', r'''$[0,1]$ 上的正分块加权弦. 对这一固定极限权, Dirichlet 谱简单, 因而
$D^*=\lambda_{n+1}^*-\lambda_n^*>0$. 这里只使用该固定极限谱隙的正性,
不声称存在由盒界直接给出的 $(2n+1)\pi^2/R_1$ 定量下界.
沿此序列特征对收敛, 归一化特征函数 $C^1$ 收敛,''')
replace_once(r'''定理 B).  (ii) 由定理~\ref{thm:framework}, 全局分类猜想现仅依赖 (G1$'$):
若 (G1$'$) 成立, 则对一切 $R>1$ 解唯一且反射对称.  (iii) 数值交叉''', r'''定理 B, 该旧材料本轮未读取).
(ii) \textbf{历史条件化结语, 未重新认证}: 只有本节 (G2) 声明及其与
$\Sigma_\sigma$ 的量词衔接获得验证后, 才能结合定理~\ref{thm:framework}
把全局分类归约为 (G1$'$). 本轮不宣布这些前提已完成.
(iii) 历史数值交叉 (本轮未重跑)''')
Candidate.write_text(Text)
print('Applied authorized local tail repairs:', Candidate)
print('SHA256',hashlib.sha256(Candidate.read_bytes()).hexdigest())
