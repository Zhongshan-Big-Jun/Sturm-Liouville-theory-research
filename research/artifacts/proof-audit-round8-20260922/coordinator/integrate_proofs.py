from pathlib import Path
import hashlib,json,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A=R/'research/artifacts/proof-audit-round8-20260922'
B=json.loads((O/'baseline.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def original(n):
	p=R/n
	if sha(p)!=B['tracked'][n]: raise RuntimeError('Concurrent source change '+n)
	d=A/'before'/n;d.parent.mkdir(parents=True,exist_ok=True)
	if not d.exists(): shutil.copyfile(p,d)
	return p.read_bytes()
names=['docs/SL_gap_n1_inf_limit_proof.tex','docs/SL_gap_n1_proof.tex','docs/SL_spectral_topics_summary.tex']
for n in names: original(n)
shutil.copyfile(O/'candidates'/names[0],R/names[0])
text=(R/names[1]).read_text()
a=text.index('本节记录相邻间距在 INF 侧');b=text.index('\\begin{remark}[与 O3a/C1',a)
new=r'''本节采用 2026-09-22 第八轮修订证明, 完整论证见
\texttt{SL\_gap\_n1\_inf\_limit\_proof.pdf}; 原 05/16/19 浮点证书仅留作历史记录.

\begin{theorem}[对称阱族的 INF 极限]
设 $m_R=\inf_{0<u<1/2}D_R(u)$, 限于对称阱族 $[R,1,R]$. 则
\[
 \lim_{R\to\infty}Rm_R=M=\bar D(u^*),\qquad
 0\le Rm_R-M=O(R^{-1}).
\]
其中 $u^*$ 是 $S(u)=0$ 的唯一根. 精确包络为
\begin{align*}
 u^*&\in[0.32992250812006654958,\ 0.32992250812006654960],\\
 M&\in[24.9438661384324768968,\ 24.9438661384324769084].
\end{align*}
若 $R_j\to\infty$, $\eta_j\ge0$, $R_j\eta_j\to0$,
$D_{R_j}(u_j)\le m_{R_j}+\eta_j$, 则 $u_j\to u^*$.
\end{theorem}

\begin{itemize}
 \item T2 由解析符号链给出唯一极小点和 $M<3\pi^2$; 高精度数值不是这一步的前提.
 \item 对 $R\ge1500$, $w=u\sqrt R\ge2$, 初等修订的引理 A$''$ 给
 $G(R,u)>\bar D(u)+\ell/(Ru^3)$, 使用 $d_1>4\alpha$, $d_2<3\alpha$.
 \item 对整个 $0<w\le2$, 连续相位速度给
 $G\ge\pi^2/[2\varepsilon(w+\ell)(w+\varepsilon\ell)]>15\pi^2/4>3\pi^2$.
 它覆盖任意小 $w$、原曲边遗漏区和无穷 $R$ 尾部, 取代旧矩形网格.
 \item T1 结合上述全域下界及固定 $u^*$ 的上界, 不依赖 T3 数值.
 T3 另由 Machin/Taylor 精确有理包络和正确方向的根像传播支持.
 \item 固定内部 $u$ 时 $G=\bar D+C(u)/R+O_u(R^{-2})$,
 $C(u^*)=\pi^2(1/2-u^*)/[3(u^*)^3]>0$. 旧非零 $R^{-1/2}$ 首项已撤回;
 这里不推断最优值的精确首项系数或极小化参数收敛率.
\end{itemize}
全域先用无极点匹配方程识别模态; $\theta_2>\pi/2$ 仅在所证参数域使用.
局部 Lean 和精确数值证据的范围见第八轮报告, 不等同于整篇谱理论已形式化.

'''
(R/names[1]).write_text(text[:a]+new+text[b:])
raw=(R/names[2]).read_bytes();text=raw.decode('utf-8');newline='\r\n' if b'\r\n' in raw else '\n';norm=text.replace('\r\n','\n')
a=norm.index('\\emph{会话 30 进展}');b=norm.index('\\subsection{已解决:',a)
new=r'''\emph{INF 极限, 2026-09-22 修订}: 对称阱族 $[R,1,R]$ 有
$Rm_R\to M=\bar D(u^*)$, 且 $0\le Rm_R-M=O(R^{-1})$.
T2 的解析单调结构给唯一 $u^*$ 和 $M<3\pi^2$; T3 的新精确有理证书给
$u^*\in[0.32992250812006654958,0.32992250812006654960]$,
$M\in[24.9438661384324768968,24.9438661384324769084]$.
T1 以 $R\ge1500$ 下两块连续估计闭合: $w\ge2$ 时
$G>\bar D+\ell/(Ru^3)$; 整个 $0<w\le2$ 时连续相位速度给
$G>15\pi^2/4>3\pi^2$. 因而不再使用旧矩形网格或 T3 高精度值作为收敛前提.
误差 $\eta_R\ge0$, $R\eta_R\to0$ 的近极小化子均收敛到 $u^*$.
固定内部 $u$ 的首项为 $C(u)/R$, 余项 $O_u(R^{-2})$;
$C(u^*)=\pi^2(1/2-u^*)/[3(u^*)^3]>0$, 非零 $R^{-1/2}$ 首项撤回.
全域无极点匹配和有条件的奇相位分支已分开; 历史 05/16/19 的认证作用已被替代.
完整证明见 \path{SL_gap_n1_inf_limit_proof.pdf}; 本段只重审所述对称阱族,
不由此重新认证其它全盒类结论. 第八轮报告区分解析证明、精确证书与局部 Lean 范围.

'''
(R/names[2]).write_bytes((norm[:a]+new+norm[b:]).replace('\n',newline).encode())
for n in [x.replace('.tex','.pdf') for x in names]: original(n)
result={n:sha(R/n) for n in names}
(O/'integrated-proof-sources.json').write_text(json.dumps(result,indent=2)+'\n')
print(result,flush=True)
