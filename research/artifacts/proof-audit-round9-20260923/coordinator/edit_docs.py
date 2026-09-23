from pathlib import Path
import json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923')
B=json.loads((O/'baseline.json').read_text())
def read(n):
	P=R/n;Raw=P.read_bytes()
	if hashlib.sha256(Raw).hexdigest()!=B['tracked'][n]:raise RuntimeError('Source changed '+n)
	return Raw.decode().replace('\r\n','\n'), b'\r\n' if b'\r\n' in Raw else b'\n'
def one(s,old,new):
	if s.count(old)!=1:raise RuntimeError('Expected one anchor '+old[:90])
	return s.replace(old,new)
def region(s,a,b,new):
	Start=s.index(a);End=s.index(b,Start)
	return s[:Start]+new+s[End:]
def write(n,s,eol):(R/n).write_bytes(s.encode().replace(b'\n',eol))
N='docs/SL_fixed_n_supremum.tex';S,E=read(N)
S=one(S,r'\date{2026-08-05}',r'\date{2026-09-23 (第九轮归一化与候选极限修订)}')
S=region(S,r'\begin{abstract}',r'\tableofcontents',r'''\begin{abstract}
固定 $n\ge1$ 的全局相邻比值上确界仍是本项目的开放问题.
本文刻画规定平衡交替配置 $[1,R,1,\dots,1]$ 的候选谱, 其中
$s=\sqrt R>1$, 轻块宽 $st_n$, 重块宽 $t_n=1/((n+1)s+n)$.
物理世俗函数 $F_n$ 的正确关系为
$F_n(\pi-y)=yF_n(y)/(\pi-y)$; 归一化函数
$\widehat F_n=\omega F_n$ 才严格反射对称.
归一化矩阵与 Jacobi 表示证明 $(0,\pi)$ 中恰有 $2n$ 个简单根.
嵌套 Jacobi 矩阵进一步给出候选值 $c_n(R)$ 严格递减, 且
\[
 c_n(R)\downarrow\left(\frac{\pi-\varphi(R)}{\varphi(R)}\right)^2,
 \qquad\varphi(R)=\arccos\frac{\sqrt R-1}{\sqrt R+1}.
\]
这是规定候选序列的解析结论, 不证明 $c_n(R)=\Lambda_n^{\sup}(R)$.
全局最优性 O1/O2 仍开放; 后续极大子结构结果与早期数值实验分别标明来源.
\end{abstract}

\medskip
\noindent\textbf{证据范围.} 反射、根计数及本稿候选单调极限有解析证明;
第 4 节保留历史有限数值证据, 不构成全局极值性证明.
第九轮的精确审查版本、独立检验与局部 Lean 范围见
\path{reports/proof-audit-round9-20260923/REPORT.md}.

''')
S=one(S,r'末块 $[1]$ (宽度 $st$, 相位 $y$): $T_{\mathrm{end}}(y)$. 世俗函数',r'''末块 $[1]$ (宽度 $st$, 相位 $y$): $T_{\mathrm{end}}(y)$.
这里 $\omega=\omega(y)=y/(st)$ 随 $y$ 改变. 物理状态为 $(u,u')$,
世俗函数''')
S=region(S,r'\begin{theorem}[反射对称]',r'\section{平衡定理与闭式}',r'''定义 $P_\omega=\operatorname{diag}(1,\omega)$,
$N=P_\omega^{-1}TP_\omega$, 以及
$\widehat F_n(y)=\omega(y)F_n(y)=(N_{\rm end}N_{\rm cell}^n)_{01}$.
写 $C=\cos y,S=\sin y$, 则
\[
 N_{\rm cell}=\begin{pmatrix}
 C^2-S^2/s &(s+1)SC/s\\ -(s+1)SC&C^2-sS^2
 \end{pmatrix},\qquad
 N_{\rm end}=\begin{pmatrix}C&S\\-S&C\end{pmatrix}.
\]
\begin{theorem}[归一化反射与物理比例]\label{thm:sym}
 对一切整数 $n\ge1$, $s>1$, $0<y<\pi$,
 \[
  \widehat F_n(\pi-y)=\widehat F_n(y),\qquad
  F_n(\pi-y)=\frac{y}{\pi-y}F_n(y).
 \]
\end{theorem}
\begin{proof}
 令 $J=\operatorname{diag}(1,-1)$. 直接用反射后三角函数的符号得到
 $N_{\rm cell}(\pi-y)=J N_{\rm cell}(y)J$,
 $N_{\rm end}(\pi-y)=-J N_{\rm end}(y)J$.
 由 $J^2=I$, 任意次幂的乘积满足
 \[
 N_{\rm end}(\pi-y)N_{\rm cell}(\pi-y)^n
 =-J[N_{\rm end}(y)N_{\rm cell}(y)^n]J.
 \]
 其 $01$ 项不变, 得第一式. 再除以 $\omega(\pi-y)=(\pi-y)/(st)$
 得第二式. 不能在反射时冻结 $\omega$.
\end{proof}
\begin{remark}
 正比例因子保留内部根及其单重性. 旧物理函数值的对称等式为假:
 $n=1,R=4$ 时
 $F_1(\pi/3)=-21\sqrt3/(40\pi)$,
 $F_1(2\pi/3)=-21\sqrt3/(80\pi)$.
 归一化在 $y=0$ 引入的零点不属于 Dirichlet 正谱, 本文仅在 $0<y<\pi$ 计数.
\end{remark}

''')
S=region(S,r'\begin{proof}[证明结构与层级]',r'\begin{theorem}[显式闭式]',r'''\begin{proof}
 令 $A=(s+1)^2/s$, $B=s+1/s=A-2$, $\delta=1/s\in(0,1)$.
 归一化矩阵行列式为一, Cayley--Hamilton 与首项计算给出
 \[
 \widehat F_n(y)=\sin y\,P_n(\cos^2y),\quad
 P_0=1,\quad P_1=Ax-s,\quad
 P_n=(Ax-B)P_{n-1}-P_{n-2}.
 \]
 设 $z=Ax-B$, $J_n$ 是首对角为 $-\delta$、其余对角为零、
 两条次对角线为一的实对称矩阵.
 展开最后一行的行列式并核对初值 $1,z+\delta$ 得
 $P_n(x)=\det((Ax-B)I-J_n)$.
 对任意非零实向量 $v$, 有
 \begin{align*}
 v^T(J_n+2I)v&=\sum_{j=1}^{n-1}(v_j+v_{j+1})^2
 +(1-\delta)v_1^2+v_n^2>0,\\
 v^T(2I-J_n)v&=\sum_{j=1}^{n-1}(v_j-v_{j+1})^2
 +(1+\delta)v_1^2+v_n^2>0.
 \end{align*}
 $n=1$ 时求和为空, 两个端点项仍分别计入.
 因而谱在 $(-2,2)$. 本征向量由第一坐标及三对角递推唯一确定,
 第一坐标为零将使全向量为零; 配合对称矩阵可对角化, 得所有本征值简单.
 因 $B>2$, $A=B+2$, 对应 $x=(B+z)/A$ 恰有 $n$ 个简单根位于 $(0,1)$.
 每个产生两个互补相位, 变量变换导数在这些点非零, 故物理函数和归一化函数
 在 $(0,\pi)$ 都恰有 $2n$ 个简单根. 它们按频率排序就是前 $2n$ 个正特征值.
 反射配对给出相邻中心根和比值公式.
 后续历史证明入口为
 \path{runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md}
 Part B; 其 $G_n=\omega F_n$ 已正确归一化, 不受旧物理等式错误否定.
\end{proof}

''')
S=S.replace(r'\text{ 其中 } Q_3, Q_4 \text{ 为 } F_n \text{ 的显式多项式}.',r'\text{ 其中 } Q_j(C)=P_j(C^2),\ j=3,4.')
S=region(S,r'\begin{proof}'+'\n'+r'\t$n = 1$:',r'\end{proof}', '') if False else S
Start=S.index(r'\begin{proof}',S.index(r'\begin{theorem}[显式闭式]'))
End=S.index(r'\end{proof}',Start)+len(r'\end{proof}')
S=S[:Start]+r'''\begin{proof}
 $n=1$: $Q_1(C)=((s+1)^2/s)C^2-s$, 故正根 $C=s/(s+1)$.
 $n=2$: 递推给出精确因式分解
 \[
 s^2 Q_2(C)=\bigl((s+1)^2C^2+(s+1)C-s^2\bigr)
 \bigl((s+1)^2C^2-(s+1)C-s^2\bigr).
 \]
 最小的正 $C$ 对应最大的下半相位根, 即所列 $y_2$.
 $n\ge3$ 的一般定义为 $Q_n(C)=P_n(C^2)$; 取最小正根, 不需数值验证来保证根的存在或指标.
 表中小数仅是历史有限数值展示.
\end{proof}'''+S[End:]
Start=S.index(r'\section{开放缺口 (如实登记)}');End=S.index(r'\section{涉及到的数学知识}',Start)
S=S[:Start]+r'''\section{候选序列的严格单调与精确极限}
\begin{theorem}\label{thm:limit}
 固定 $R>1$, 规定平衡配置的候选值满足
 \[
 c_n(R)\downarrow c_\infty(R)
 =\left(\frac{\pi-\varphi(R)}{\varphi(R)}\right)^2,
 \qquad \varphi(R)=\arccos\frac{\sqrt R-1}{\sqrt R+1},
 \]
 且每一步都严格下降. 此结论不包含 $c_n=\Lambda_n^{\sup}$.
\end{theorem}
\begin{proof}
 设 $z_n$ 是上一节 $J_n$ 的最小特征值.
 $J_n$ 是 $J_{n+1}$ 的顺序主子矩阵, 极小极大原理给出 $z_{n+1}\le z_n$.
 若相等, 给 $J_n$ 的最小本征向量补一个末尾零, 便取得 $J_{n+1}$ 的最小
 Rayleigh 商, 因而是其本征向量. 最后一行强迫原末坐标为零, 递推使全向量为零, 矛盾.
 取单位向量 $v_j=(-1)^j/\sqrt n$, 则
 \[
 -2<z_n\le v^T J_n v=-2+\frac{2-\delta}{n}.
 \]
 故 $z_n\downarrow-2$. 最小 $x_n=(B+z_n)/A$ 对应第 $n$ 个相位根,
 \[
 y_n=\arccos\sqrt{(B+z_n)/A}\uparrow
 \arccos\sqrt{(B-2)/A}=\varphi(R).
 \]
 最后 $H(y)=(\pi/y-1)^2$ 在 $(0,\pi/2)$ 满足
 $H'(y)=-2\pi(\pi/y-1)/y^2<0$.
 因此 $c_n=H(y_n)$ 严格递减并收敛到声明的值.
\end{proof}

\section{开放缺口 (如实登记)}
\begin{description}
 \item[全局极值性 O1/O2] 后续研究已给出全局极大子的交替 $2n$ 开关结构;
  该结构结果并不确定块宽. 仍须证明平衡等宽配置在完整容许族中达到全局最大,
  才能得 $\Lambda_n^{\sup}(R)=c_n(R)$.
  本轮只修订归一化和候选谱, 不重新审计该极大子结构证明.
 \item[根计数] 上一节给出全部 $R>1,n\ge1$ 的解析根计数, 已不是仅有限样本的观察.
 \item[两种序列] $c_n(R)$ 的单调与极限由定理~\ref{thm:limit} 完成;
  $\Lambda_n^{\sup}(R)$ 的同类结论没有随之完成.
\end{description}

'''+S[End:]
S=S.replace(r'$T(\pi-y)$ 与 $T(y)$ 的关系',r'$N(\pi-y)$ 与 $N(y)$ 的关系')
write(N,S,E)
N='docs/SL_spectral_topics_summary.tex';S,E=read(N)
Start=S.index(r'\emph{固定 $n$ 上确界猜想}');End=S.index(r'\subsection{\texorpdfstring{进展: 相邻间距',Start)
S=S[:Start]+r'''\emph{固定 $n$ 上确界猜想} (第九轮范围修订, \texttt{SL\_fixed\_n\_supremum.pdf}):
规定平衡交替配置 $[1,R,1,\dots,1]$ 的物理世俗函数记为 $F_n$,
归一化函数为 $\widehat F_n=\omega F_n$, $y=\omega\sqrt R\,t_n$.
准确关系是 $\widehat F_n(\pi-y)=\widehat F_n(y)$ 与
$F_n(\pi-y)=yF_n(y)/(\pi-y)$, $0<y<\pi$.
归一化 Chebyshev/Jacobi 表示证明恰有 $2n$ 个简单根并反射配对,
所以规定配置的比值为 $c_n(R)=((\pi-y_n)/y_n)^2$.
嵌套 Jacobi 矩阵的最小特征值严格下降到 $-2$, 给出
\[
 c_n(R)\downarrow\left(\frac{\pi-\varphi}{\varphi}\right)^2,
 \qquad \varphi=\arccos\frac{\sqrt R-1}{\sqrt R+1}.
\]
这是候选序列的解析定理, 不证明其等于全局上确界 $\Lambda_n^{\sup}(R)$.
后续极大子的交替 $2n$ 开关结构不确定最优块宽; O1/O2 的全局最优性仍开放.
本轮仅修订本段归一化与候选状态, 完整审查范围见第九轮报告.

'''+S[End:]
S=one(S,r'固定 $n$ 上确界仅反射对称结构严格, 全局极值性为数值支持的猜想 (会话 12, 见下).',r'固定 $n$ 的规定平衡候选已有归一化反射、根计数和单调极限证明, 全局最优性仍开放 (见下).')
Old=r'''\item \textbf{固定 $n$ 上确界猜想的收尾} (会话 12): 全局极值性
		(Keller 型归约到交替 bang-bang), $2n$-根计数, 以及
		$\Lambda_n^{\sup}(R)\downarrow c_\infty(R)$ 的单调收敛.'''
S=one(S,Old,r'''\item \textbf{固定 $n$ 上确界猜想的收尾}: 仍须证明平衡候选的全局最优性 O1/O2,
		以及整个 $\Lambda_n^{\sup}(R)$ 序列的单调极限.
		规定候选 $c_n(R)$ 的根计数与单调极限已有解析证明, 不再列为同一缺口.''')
write(N,S,E)
N='scripts/_gapn2_k_global_rank2.py';S,E=read(N)
S=one(S,'''applied to bump-regularized bang-bang dr does NOT converge to Q_true: the
width path rho(x; w + e dw) has d^2 rho = sum_i s_i dw_i^2 delta'(x - x_i),
a boundary-layer term of leading order (NEGATIVE result, R-206).''','''is the Hessian for a LINEAR density path. A moving-interface path also has
d^2 rho = sum_i s_i dx_i^2 delta'(x - x_i), contributing
-sum_i s_i dx_i^2 f'(x_i) to the FULL second derivative (one half to Q).
Unit-mass narrow pulses in this regular one-dimensional model have a finite
reduced-Green limit. The old R-206 divergence explanation and its universal
route-closure wording are withdrawn; no Hessian sign is proved by the old P3
samples. See research/artifacts/proof-audit-round9-20260923/analytic-repair.md
V3-V4. This clarification does not re-audit the global K identity above.''')
write(N,S,E)
for N,Text in [('docs/.gitattributes','\n# Ninth-round exact normalization source.\nSL_fixed_n_supremum.tex -text\n'),('tools/.gitattributes','\n# Ninth-round exact corrected tool versions.\nsecond-variation-weighted-eigenvalues.md -text\nsecular-chebyshev-jacobi-rootcount.md -text\nbloch-band.md -text\n')]:
	with (R/N).open('ab') as F:F.write(Text.encode())
print('Edited fixed-n proof, exact B3 summary passages, K-script explanation and scoped attributes.')
