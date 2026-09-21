from pathlib import Path
import hashlib

Out = Path('/mnt/f/tools/math-audit-round8-20260922')
Original = Out/'sources/docs/SL_gap_n1_inf_limit_proof.tex'
Text = Original.read_text()

def replace_once(Old, New):
	global Text
	if Text.count(Old) != 1:
		raise RuntimeError('Expected exactly one source anchor: '+Old[:90])
	Text=Text.replace(Old,New,1)

def replace_section(Start, End, New):
	global Text
	if Text.count(Start)!=1 or Text.count(End)!=1:
		raise RuntimeError('Ambiguous section anchors')
	A=Text.index(Start);B=Text.index(End,A)
	Text=Text[:A]+New+Text[B:]

replace_once('\\title{SL 相邻特征间距的 $R\\to\\infty$ 极限: 严格证明 (定理 A)}','\\title{SL 相邻特征间距的 $R\\to\\infty$ 极限: 第八轮修订证明}')
replace_once('\\date{2026-08-07}','\\date{2026-09-22 修订; 原稿 2026-08-07}')
Text=Text.replace('0.3299225081196866','0.32992250812006654959')
replace_section('\\subsection{相位与 secular 方程}','\\subsection{相位括号 (引理 2.1)}',(Out/'phase-repair.tex').read_text())
replace_once('由余切展开 $\\cot z=1/z-\\sum_{k\\ge1}c_kz^{2k+1}$ ($c_k>0$) 知 $R(z)/z=\\sum c_kz^{2k}$\n在 $(0,\\pi)$ 上递增, 故对 $z\\in[0,\\pi/8]$:',r'''由 NIST DLMF 4.22.3 的余切部分分式公式,
\[
 \frac{R(z)}z=2\sum_{j=1}^{\infty}\frac1{j^2\pi^2-z^2},\qquad 0<z<\pi.
\]
该级数在 $(-\pi,\pi)$ 的每个紧子区间上一致收敛, 每项在 $z>0$ 时严格递增.
因此 $R(z)/z$ 在 $(0,\pi)$ 上严格递增.
对应的 Laurent 展开为 $\cot z=1/z-\sum_{k\ge1}c_kz^{2k-1}$,
$c_k=2^{2k}|B_{2k}|/(2k)!>0$, 首项为 $z/3$.
把 $R(0)$ 连续定义为零, 则对 $z\in[0,\pi/8]$:''')
Start='对 $t\\le3/\\sqrt2$: $B(t)'
End='又 $1/(1-\\delta/(1+v(v+1)/(t\\theta)))'
A=Text.index(Start);B=Text.index(End,A)
Text=Text[:A]+(Out/'scalar-repair.tex').read_text()+Text[B:]
Text=Text.replace('=1.5601\\ldots$', '>1.56$').replace('3\\pi\\cdot1.5601\\cdot0.99996','3(333/106)\\cdot1.56\\cdot0.99996')
replace_once('这三个常数由\n脚本 19 以区间方向舍入认证 (见 §3.4). 证明本身是解析的.', '这三个常数由第八轮精确有理证书和上述连续区间的解析估计共同支撑\n(见 §\\ref{sec:cac}). 旧脚本 19 的浮点区间扩展不能作为当前认证依据.')
replace_section('\\begin{proof}[证明 (区间算术)]','\\subsection{T1: 极限与近极小化子收敛}',(Out/'t3-repair.tex').read_text()+(Out/'coefficient-repair.tex').read_text())
replace_section("\\subsection{引理 A\\texorpdfstring{$''$}{} (下界)}\\label{sec:lemAdp}", '\\subsection{T2: \\texorpdfstring', (Out/'large-w-repair.tex').read_text()+(Out/'sliver-repair.tex').read_text())
replace_section('\\subsection{T1: 极限与近极小化子收敛}', '\\begin{corollary}[定理 A]', (Out/'t1-repair.tex').read_text())
Text=Text.replace('其证明是初等的 (相位括号 + 差量下界 + 差量上界), 无需区间算术;\n深 sliver ($w\\le 2$) 由分段下界保证 $R\\cdot D_R(u)\\ge 25>\\bar D(u^*)$.',
 '其初等修订给出更强正余量 $G-\\bar D>\\ell/(Ru^3)$.\n薄层区域 ($w\\le2$) 用连续相位速度的统一下界覆盖, 得 $G>15\\pi^2/4>3\\pi^2$.\nT1 因而不依赖旧二维网格或 T3 的高精度数值; T3 由新的精确有理证书支撑.')
Text=Text.replace('(见 §2.7)', '(见 §\\ref{sec:T1})').replace('(见 §2.5)', '(见 §\\ref{sec:T2})').replace('(见 §2.6)', '(见 §\\ref{sec:T3})')
A=Text.index('先列证明大纲.');B=Text.index('\\subsection{全域匹配方程',A)
Text=Text[:A]+r'''证明先确定正确的模式分支. 大 $w$ 区域用初等差量界 $d_1>4\alpha$, $d_2<3\alpha$;
薄层区域用连续展开相位的速度上界, 统一得到 $G>15\pi^2/4$.
T1 只需这些连续估计和 T2 的解析单调结构; T3 的精确数值包含单独证明.

'''+Text[B:]
Old='又 $\\bar D(u)\\to+\\infty$ (当 $u\\to0^+$),\n$\\bar D(u)\\to3\\pi^2$ (当 $u\\to1/2^-$). \\qed'
New=r'''为核对端点, 当 $u\downarrow0$ 时写 $a=\pi/2+d$.
根方程等价于 $a\tan d=u/\ell$, 因而 $d/u\to4/\pi$,
$u\bar D(u)=(a+\pi/2)d/u\to4$. 故 $\bar D(u)\to+\infty$.
当 $u\uparrow1/2$ 时 $a\to\pi$, 直接代入得 $\bar D(u)\to3\pi^2$.
严格递增的右支还给出 $\bar D(u^*)<3\pi^2$. \qed'''
replace_once(Old,New)
replace_section('\\begin{remark}[数值定位]', '\\subsection{T3:', r'''\begin{remark}[解析唯一性与数值定位]
T2 的唯一性来自上述符号链. T3 只负责以精确包络定位已经确定唯一的根及其函数值.
\end{remark}

''')
replace_section('\\section{计算机辅助认证 (常数)}', '\\section{数值证据 (非证明)}',r'''\section{精确证书、连续覆盖与历史程序}\label{sec:cac}

当前标量证书位于第八轮工件目录中的 \texttt{certificate/certificate.py};
以 Python 标准库 Fraction 作证明算术, 以 Decimal 的定向舍入作十进制显示.
输入有理数、Machin 的交错余项、Taylor 的全局 Lagrange 余项及每次除法的非零分母均明确检查.
实现与独立执行证据见
\href{../reports/proof-audit-round8-20260922/REPORT.md}{第八轮修订报告}.

T3 使用根的异号端点和 T2 的唯一性, 经正确方向的单调像传播得到包含.
新的引理 A$''$ 主链已经解析证明 $B(t)\le8$ 及 $d_2/d_1<3/4$.
旧链所需的 $C_z<0.337$, $B(t)\le9$ 与比例 $<0.8256$ 也由新证书独立支持,
作为可复用标量工具保留; 这些细常数不再是 T1 的必要依赖.
薄层区域的连续覆盖以 §\ref{sec:sliver} 的新证明为准, 不再调用旧矩形网格.

历史 run \texttt{R-20260806T200000Z-inflimit-5B2C7D} 的源文件和输出保持原字节:
\begin{itemize}
 \item 脚本 05 把根的下界误作右端像上界, 且有普通浮点中间运算. 新证书替代其 T3 作用.
 \item 脚本 16 的普通超越函数值加一次 \texttt{nextafter} 不保证包含;
 B/D 曲边区域的矩形内缩、$w\downarrow0$ 和大 $R$ 尾部亦未完整覆盖.
 加密原网格不能消除这种方向错误.
 \item 脚本 19 同样存在余切漏包, 并把未包络的 $v$ 值当区间端点,
 以小于真实 $\pi$ 的浮点数结束网格. 标量结论现由精确有理证书及解析覆盖支撑.
 \item 脚本 17、18 及旧点抽样保留为历史记录, 本轮没有给它们重新授予区间认证或全域证明地位.
\end{itemize}
局部 Lean 的编译、实际声明和公理依赖另有独立证据; 它不等同于把本篇所有谱理论、
隐函数和连续区域估计全部形式化. 各证据的精确边界与失败记录均列于第八轮报告.

\subsection{余切细常数的正确来源}
对于 $0<z<\pi$, NIST DLMF4.22.3 给出
\[
 \frac{1/z-\cot z}{z}=2\sum_{j=1}^{\infty}\frac1{j^2\pi^2-z^2}.
\]
级数在 $(-\pi,\pi)$ 的每个紧子区间上一致收敛, 每项在正半轴严格递增.
故 $(1/z-\cot z)/z$ 严格递增, 并对 $0<z\le\pi/8$ 有
\[
 1/z-\cot z\le C_z z,\qquad
 C_z=\frac{8/\pi-(1+\sqrt2)}{\pi/8}<\frac{337}{1000}.
\]
Laurent 展开中的正确幂次为
$\cot z=1/z-\sum_{k\ge1}c_kz^{2k-1}$,
$c_k=2^{2k}|B_{2k}|/(2k)!>0$, 从 $z/3$ 开始.
不能把紧子区间上的一致收敛说成在整个 $(0,\pi)$ 上一致收敛.
证书用精确 $\pi$, $\sqrt2$ 有理包络核对细常数; 十进制打印值不作为零宽区间输入.

''')
replace_section('\\section{数值证据 (非证明)}','\\section{涉及到的数学知识}',r'''\section{数值证据与收敛阶的范围}\label{sec:numeric}

历史浮点扫描和拟合保存在原 run 中, 本轮不以它们证明连续区域的下界.
第八轮精确证书重新支持 T3 的显示区间; 附带高精度数值只用于检验解析式的行为.

命题 \ref{prop:fixed-u} 已解析证明固定内部 $u$ 的 $R^{-1}$ 展开.
在 $u^*$ 处, 非零系数约为 $15.5807908501$, 因而
$R(G(R,u^*)-\bar D(u^*))$ 趋于这一常数,
而 $\sqrt R(G(R,u^*)-\bar D(u^*))\to0$.
原文由数值误差声称非零 $R^{-1/2}$ 首项, 已撤回.
本节不推断极小化参数或任意近极小化子序列的收敛速度.

''')
Text=Text.replace('\\item \\textbf{区间算术}: mpmath.iv, 方向舍入, 计算机辅助认证.', '\\item \\textbf{精确包络}: 有理区间四则运算, Machin 恒等式, Taylor 余项及方向正确的像传播.')
Text=Text.replace('\\item \\textbf{Weyl 渐近}: $u\\to1/2$ 时 $\\rho\\to R$ 退化, $\\bar D\\to3\\pi^2$;', '\\item \\textbf{极限系统端点}: 由 $a(u)$ 的极限方程, $u\\to1/2$ 时 $\\bar D\\to3\\pi^2$;')
replace_once('\\item 本项目内部 run (见 \\texttt{runs/rigorous-open-math-research/}):', '\\item NIST Digital Library of Mathematical Functions, \\href{https://dlmf.nist.gov/4.22.E3}{公式 4.22.3},\n版本 1.2.8 (2026-09-15), 本轮实际读取该公式及极点排除条件.\n\\item 本项目内部 run (见 \\texttt{runs/rigorous-open-math-research/}):')
Candidate=Out/'candidates/docs/SL_gap_n1_inf_limit_proof.tex'
Candidate.parent.mkdir(parents=True,exist_ok=True)
Candidate.write_text(Text)
print('Complete analytic candidate written; fresh independent review pending.',len(Text),hashlib.sha256(Candidate.read_bytes()).hexdigest())
