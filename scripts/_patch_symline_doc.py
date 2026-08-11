# -*- coding: utf-8 -*-
# 一次性补丁脚本: 2026-08-12 复核修复 docs/SL_gap_n1_symline_allR_proof.tex 的
# 证书错误 (F-302 系列): G''(0) 显示值, C1 分数/十进制链与 pi 界方向, C3 精化界,
# C5 常数, (d) 情形分离, 余量 remark, 附录 B 数值更新.
import io, sys

p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_symline_allR_proof.tex"
s = io.open(p, encoding="utf-8").read()
orig = s

def rep(old, new, must=True):
    global s
    if old not in s:
        print("NOT FOUND >>>", old[:110].replace("\n", " / "))
        if must:
            sys.exit(1)
        return
    s = s.replace(old, new, 1)
    print("OK >>>", old[:60].replace("\n", " / "))

# ---------- 1. 引理 gstar 证明的链 (修正 pi 界方向) ----------
old1 = r"""\begin{equation*}
	\tan0.961\le\frac{19\,039\,844\,677}{13\,301\,445\,497}<1.4315
	<1.4546<\frac{2(22/7-0.961)}{3},
\end{equation*}
\begin{equation*}
	\tan0.97\ge\frac{3\,960\,529\,433}{2\,714\,143\,082}>1.4591
	>1.4472>\frac{2(223/71-0.97)}{3}.
	\qedhere
\end{equation*}"""
new1 = r"""\begin{equation*}
	\tan0.961<1.4472<\frac{2(223/71-0.961)}{3},
	\qquad
	\tan0.97>1.4546>\frac{2(22/7-0.97)}{3}.
	\qedhere
\end{equation*}
(第一、三个不等式来自证书 C1: $\tan0.961\le R_1<1.4315$ 与
$\tan0.97\ge R_2>1.4591$; 第二、四个分别用 $\pi>223/71$ 与 $\pi<22/7$.)"""
rep(old1, new1)

# ---------- 2. 附录 C1 整段替换 ----------
i1 = s.index(r"\textbf{C1 ($\varphi(0.961)<0<\varphi(0.97)$).}")
i2 = s.index(r"\textbf{C2 (引理 \ref{lem:ys2} 的端点).}")
newC1 = r"""\textbf{C1 ($\varphi(0.961)<0<\varphi(0.97)$).}
$\varphi(\gamma)=\tan\gamma-\frac23(\pi-\gamma)$ 严格递增.
用 $\sin$ 的交替级数上下界 ($0<x<1$ 时项单调递减)
\begin{equation*}
	\sin x\le x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\frac{x^9}{9!}
	-\frac{x^{11}}{11!}+\frac{x^{13}}{13!},
	\qquad
	\cos x\ge1-\frac{x^2}{2!}+\frac{x^4}{4!}-\frac{x^6}{6!}+\frac{x^8}{8!},
\end{equation*}
以及 $\tan x=\sin x/\cos x$, 得 ($x=961/1000$)
\begin{equation*}
	\tan x\le\frac{\sin_{\text{up}}(x)}{\cos_{\text{lo}}(x)}=:R_1
	<1.4315<1.4472<\frac{2(223/71-0.961)}3,
\end{equation*}
(末步用 $\pi>223/71$) 故 $\varphi(0.961)<0$. 又 ($x=97/100$)
\begin{equation*}
	\tan x\ge\frac{\sin_{\text{lo}}(x)}{\cos_{\text{up}}(x)}=:R_2
	>1.4591>1.4546>\frac{2(22/7-0.97)}3,
\end{equation*}
(末步用 $\pi<22/7$) 故 $\varphi(0.97)>0$. 于是 $\gamma_0^*\in(0.961,0.97)$,
$y_0\in(\pi-0.97,\pi-0.961)\subset(2.1708,2.1819)$. 精确比值
\begin{equation*}
	R_1=\frac{5104691704723563842653351044859938032346287993281}
	{3566219119511749539487170630605640000000000000000}
	\approx1.4314015863,
	\qquad
	R_2=\frac{329267980378932303644934573247}
	{225649563795645795591390000000}\approx1.4592006066.
\end{equation*}

"""
s = s[:i1] + newC1 + s[i2:]
print("OK >>> C1 段替换")

# ---------- 3. G''(0) 显示值 ----------
old3 = r"""	\item[\textbf{(c)}] $G''(0)=3\pi>0$; 由引理 \ref{lem:gstar}"""
new3 = r"""	\item[\textbf{(c)}] $G''(0)=3\pi-\pi^3/4=\pi(3-\pi^2/4)>0$ (因
		$\pi^2<12$, 经 $\pi<22/7$); 由引理 \ref{lem:gstar}"""
rep(old3, new3)

# ---------- 4. (d) 情形分离 ----------
old4 = r"""		$y\ge\pi/2$ 给出 $\pi^2-18y^2\le-3.5\pi^2$; 又
		$4y(2y^2-9)\cos w\sin w\le4y_0(2y_0^2-9)/2$
		($4y(2y^2-9)$ 在 $y\ge\pi/2$ 递增), 故
		\begin{equation}
			G'''\le6-3.5\pi^2\cos2w+\frac{4y_0(2y_0^2-9)}2
			\le6-3.5\pi^2\cos2w_0+\frac{4y_0(2y_0^2-9)}2
			<-0.43<0
			\label{eq:Gpppb}
		\end{equation}
		(证书 C3)."""
new4 = r"""		$y\ge\pi/2$ 给出 $\pi^2-18y^2\le-3.5\pi^2$; 又
		$4y(2y^2-9)\cos w\sin w\le2y_0(2y_0^2-9)$: 若 $2y^2-9\le0$ 则左端
		$\le0\le2y_0(2y_0^2-9)$ ($y_0>2.17$ 给出 $2y_0^2-9>0$); 若
		$2y^2-9>0$ 则 $\cos w\sin w\le1/2$ 且 $4y(2y^2-9)$ 在
		$y\ge\pi/2$ 递增, 左端 $\le2y(2y^2-9)\le2y_0(2y_0^2-9)$. 故
		\begin{equation}
			G'''\le6-3.5\pi^2\cos2w+2y_0(2y_0^2-9)
			\le6-3.5\pi^2\cos2w_0+2y_0(2y_0^2-9)
			<-0.43<0
			\label{eq:Gpppb}
		\end{equation}
		(证书 C3)."""
rep(old4, new4)

# ---------- 5. C3 精化界 ----------
old5 = r"""\textbf{C3 ($G'''<-0.43$).} 由 \eqref{eq:Gpppb}: 用 $y_0<2.1819$,
$w_0<0.6115$,
\begin{equation*}
	G'''\le6-\frac{7}{2}\Bigl(\frac{223}{71}\Bigr)^2
	\Bigl(1-\frac{(2w_0)^2}{2}\Bigr)+2y_0(2y_0^2-9)
	<-\frac{56}{129}<0.
\end{equation*}"""
new5 = r"""\textbf{C3 ($G'''<-56/129$).} 由 \eqref{eq:Gpppb}: 用精化有理界
$y_0^{\max}:=\frac{15273}{7000}$ ($=22/7-0.961$) 与
$w_0^{\max}:=y_0^{\max}-\frac{223}{142}$ ($\pi/2>223/142$),
再由 $\cos2w_0\ge1-(2w_0)^2/2\ge1-2(w_0^{\max})^2$ 与
$\pi^2>(223/71)^2$:
\begin{equation*}
	G'''\le6-\frac{7}{2}\Bigl(\frac{223}{71}\Bigr)^2
	\Bigl(1-2(w_0^{\max})^2\Bigr)+2y_0^{\max}
	\bigl(2(y_0^{\max})^2-9\bigr)
	<-\frac{56}{129}<0.
\end{equation*}
(若用粗略界 $w_0<0.6115$, $y_0<2.1819$, 左端只能压到约 $-0.4303$, 不足以推出
$<-56/129$; 精化有理界是关键.)"""
rep(old5, new5)

# ---------- 6. C5 常数 ----------
old6 = r"""	>\frac{3\,817}{200}>19.
\end{equation*}"""
new6 = r"""	>19.
\end{equation*}
(该下界精确值约 $19.081$; 取 19 即可.)"""
rep(old6, new6)

# ---------- 7. 余量 remark ----------
old7 = r"""\begin{remark}
证书中出现的所有有理数均由精确分数计算 (Python \texttt{fractions.Fraction},
脚本 \texttt{scripts/\_symline\_allR\_certificates.py}); 此处列出的分数
即脚本输出. 上述界余量: C1 约 $1.6\%$/$0.8\%$, C2 约 $13\%$, C3 约 $2.9$,
C4 约 $13$, C5 约 $19$.
\end{remark}"""
new7 = r"""\begin{remark}
证书中出现的所有有理数均由精确分数计算 (Python \texttt{fractions.Fraction},
脚本 \texttt{scripts/\_symline\_allR\_certificates.py}, 全部断言 PASS);
此处列出的分数即脚本输出. 界余量 (绝对值): C1 中 $1.4472$ 距
$2(223/71-0.961)/3$ 约 $3.0\times10^{-5}$, $1.4546$ 距
$2(22/7-0.97)/3$ 约 $2.9\times10^{-5}$ (分数链余量约 $9.8\times10^{-5}$
与 $1.0\times10^{-4}$); C2 约 $8.7\times10^{-4}$; C3 约
$3.4\times10^{-3}$; C4 约 $0.42$; C5 约 $0.081$ (下界取 19).
\end{remark}"""
rep(old7, new7)

# ---------- 8. 附录 B ----------
old8 = r"""脚本: \texttt{scripts/\_explore\_a1\_allR6.py}, \texttt{\_symline\_allR\_check.py}
(本会话新增), 全部为 \EVID{}:

\begin{enumerate}
	\item 张力比链: 网格 $\tilde q\in[10^{-13},1)$, $\gamma\in[\gamma_0^*,\pi/2)$
		共 37500 点, $\rho\le\rho_0$ 零违例;
	\item $\rho_0<1$: 200000 点扫描, $\min(1-\rho_0)\to0$ 仅在 $\gamma\to\pi/2$;
	\item 等价性 $\widetilde F_e<0\iff\rho<1$: 20000 点零违例;
	\item 端点: $\widetilde F_e(0^+)=\pi^2/(4\tilde q)$, $\widetilde F_e(1/2)<0$,
		$\widetilde F_e(c_0(\tilde q))<0$ 对 $\tilde q\in\{0.001,\dots,0.9\}$;
	\item 角点渐近: $1-\rho\approx K(t)\tilde q$ ($\gamma=\pi/2-t\tilde q$),
		$K(t)\ge1.97$, $K(1)=2$;
	\item 引理 \ref{lem:ys2}: $y^2s_2^2-\pi^2/4\ge0$ 于 $[\gamma_0^*,\pi/2)$,
		等号仅 $\gamma=\pi/2$.
\end{enumerate}"""
new8 = r"""脚本: \texttt{scripts/\_symline\_allR\_check.py} (本会话, scipy 双精度网格
+ mpmath 50 位复核), \texttt{scripts/\_explore\_a1\_allR*.py} (探索过程),
全部为 \EVID{}:

\begin{enumerate}
	\item 张力比链: 网格 $\tilde q\in[10^{-13},1-10^{-13})$,
		$\gamma\in[\gamma_0^*,\pi/2-10^{-8})$ 共 37500 点,
		$\rho\le\rho_0$ 零违例 (双精度); 最小余量点在角点附近
		$(\tilde q=1.5\times10^{-13},\ \gamma=\pi/2-10^{-8})$,
		双精度余量为 $-1.1\times10^{-16}$ (噪声), mpmath 50 位复核该点
		余量 $+2.9\times10^{-18}>0$; 沿 $\gamma=\pi/2-\varepsilon$,
		$\tilde q=\varepsilon$ 的角点方向余量 $\approx1.215\,\varepsilon$
		(mpmath 复核 4 点);
	\item $\rho_0<1$: 200000 点扫描, $\min(1-\rho_0)=7.9\times10^{-13}$
		在 $\gamma=\pi/2-10^{-12}$, 即 $\to0$ 仅当 $\gamma\to\pi/2$
		(mpmath 复核 $7.86\times10^{-13}$);
	\item 等价性 $\widetilde F_e<0\iff\rho<1$: 19901 点 (Claim A 域)
		零违例;
	\item 端点: $\widetilde F_e(10^{-12})\approx\pi^2/(4\tilde q)$
		(7 个 $\tilde q$ 值到 6 位), $\widetilde F_e(1/2^-)<0$,
		$\widetilde F_e(c_0(\tilde q))<0$ 对
		$\tilde q\in\{0.001,0.01,0.1,0.3,0.5,0.7,0.9\}$ (mpmath 50 位);
	\item 角点渐近: $1-\rho\approx K(t)\tilde q$
		($\gamma=\pi/2-t\tilde q$, $\tilde q=10^{-10}$), 实测
		$K(0.25)=4.13$, $K(0.5)=2.60$, $K(1)=2.00$, $K(2)=2.21$,
		$K(5)=4.19$, $K(10)=7.98$, $K(20)=15.77$, 故 $K(t)\ge1.97$,
		$K(1)=2$;
	\item 引理 \ref{lem:ys2}: $y^2s_2^2-\pi^2/4\ge0$ 于 $[\gamma_0^*,\pi/2)$,
		50000 点扫描最小 $3.1\times10^{-12}$ (在 $\gamma\to\pi/2$),
		与 ``等号仅 $\gamma=\pi/2$'' 一致.
\end{enumerate}"""
rep(old8, new8)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("PATCHED:", len(orig), "->", len(s), "chars")
